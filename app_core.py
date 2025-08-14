import os
from typing import TypedDict, Dict, Any, List
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from utils.llm import compose_itinerary_llm
from integrations.amadeus_api import search_flights, search_hotels
from rag.rag_travel_blogs import build_retriever_if_needed, rag_query
from map_gen import generate_map_html

load_dotenv()

class TripState(TypedDict, total=False):
    inputs: Dict[str, Any]
    flights: List[dict]
    hotels: List[dict]
    rag_tips: str
    itinerary_text: str
    map_html: str
    summary: Dict[str, Any]

def _parse_inputs(state: TripState) -> TripState:
    i = state["inputs"]
    # normalize
    cities = [c.strip() for c in i.get("destinations", "").split("->") if c.strip()]
    date_parts = [d.strip() for d in i.get("dates", "").split(",") if d.strip()]
    summary = {
        "cities": cities,
        "hops": [{"from": cities[idx], "to": cities[idx+1], "date": date_parts[idx] if idx < len(date_parts) else None}
                 for idx in range(len(cities)-1)],
        "budget": i.get("budget"),
        "interests": i.get("interests")
    }
    state["summary"] = summary
    return state

def _live_data_node(use_live: bool):
    def node(state: TripState) -> TripState:
        if not use_live:
            state["flights"] = [{"note": "live search disabled"}]
            state["hotels"] = [{"note": "live search disabled"}]
            return state

        flights, hotels = [], []
        hops = state["summary"].get("hops", [])
        for hop in hops:
            origin = hop["from"][:3].upper() if len(hop["from"]) >= 3 else hop["from"].upper()
            dest = hop["to"][:3].upper() if len(hop["to"]) >= 3 else hop["to"].upper()
            date = hop["date"]
            fl = search_flights(origin, dest, date) if date else []
            flights.append(fl)
        # Use last city as stay location for hotel search
        if state["summary"]["cities"]:
            city_code = state["summary"]["cities"][-1][:3].upper()
            check_in = state["summary"]["hops"][-1]["date"] if state["summary"]["hops"] else None
            check_out = None
            hotels = search_hotels(city_code, check_in, check_out) if check_in else []

        state["flights"] = flights
        state["hotels"] = hotels
        return state
    return node

def _rag_node(use_rag: bool):
    def node(state: TripState) -> TripState:
        if not use_rag:
            state["rag_tips"] = ""
            return state
        build_retriever_if_needed()  # one-time build / persisted
        q = f"Pro tips for {', '.join(state['summary']['cities'])} for interests: {state['summary'].get('interests')}"
        state["rag_tips"] = rag_query(q)
        return state
    return node

def _compose_node(state: TripState) -> TripState:
    txt = compose_itinerary_llm(
        cities=state["summary"].get("cities", []),
        hops=state["summary"].get("hops", []),
        interests=state["summary"].get("interests", ""),
        budget=state["summary"].get("budget"),
        flights=state.get("flights", []),
        hotels=state.get("hotels", []),
        rag_tips=state.get("rag_tips", "")
    )
    state["itinerary_text"] = txt
    return state

def _map_node(state: TripState) -> TripState:
    state["map_html"] = generate_map_html(state["summary"].get("cities", []))
    return state

def get_planner(use_live: bool, use_rag: bool):
    graph = StateGraph(TripState)
    graph.add_node("parse_inputs", _parse_inputs)
    graph.add_node("live_data", _live_data_node(use_live))
    graph.add_node("rag", _rag_node(use_rag))
    graph.add_node("compose", _compose_node)
    graph.add_node("map", _map_node)

    graph.add_edge(START, "parse_inputs")
    graph.add_edge("parse_inputs", "live_data")
    graph.add_edge("live_data", "rag")
    graph.add_edge("rag", "compose")
    graph.add_edge("compose", "map")
    graph.add_edge("map", END)

    return graph.compile()
