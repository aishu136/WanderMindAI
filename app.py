import streamlit as st
import json
from app_core import get_planner

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")

st.title("✈️ AI Travel Itinerary Designer")
st.caption("LangGraph + Bedrock + Live Data + RAG + MCP + A2A")

col1, col2 = st.columns(2)
with col1:
    destinations = st.text_input("Destinations (use '->' between cities)", "Paris -> Rome")
    dates = st.text_input("Dates (comma-separated YYYY-MM-DD, aligns with hops)", "2025-09-10,2025-09-14")
with col2:
    budget = st.number_input("Total Budget (USD)", min_value=300, max_value=20000, value=2000)
    interests = st.text_input("Interests (comma-separated)", "history, art, food")

run_live = st.checkbox("Use Live Flights/Hotels (Amadeus)", value=False)
run_rag = st.checkbox("Use RAG from blogs", value=False)

if st.button("Generate Itinerary"):
    with st.spinner("Planning with agents..."):
        planner = get_planner(use_live=run_live, use_rag=run_rag)
        state_in = {
            "inputs": {
                "destinations": destinations,
                "dates": dates,
                "budget": int(budget),
                "interests": interests
            }
        }

        # Ensure invoke returns a dict
        result = planner.invoke(state_in)
        if not isinstance(result, dict):
            try:
                result = json.loads(result)
            except Exception:
                st.error("Planner did not return valid itinerary data.")
                st.stop()

    st.success("Itinerary ready!")

    # -------- Summary --------
    st.subheader("Summary")
    summary_data = result.get("summary", {})
    if isinstance(summary_data, dict):
        summary_text = (
            f"Cities: {', '.join(summary_data.get('cities', []))}\n"
            f"Budget: {summary_data.get('budget', 'N/A')}\n"
            f"Interests: {summary_data.get('interests', 'N/A')}"
        )
        st.text(summary_text)
    else:
        st.text(str(summary_data))

    # -------- Flights / Hotels --------
    cols = st.columns(2)
    with cols[0]:
        st.subheader("Flights")
        flights_data = result.get("flights", [])

        # Flatten if nested list-of-lists
        if flights_data and isinstance(flights_data[0], list):
            flights_data = [f for sublist in flights_data for f in sublist]

        if flights_data:
            flight_texts = []
            for flight in flights_data:
                if not isinstance(flight, dict):
                    continue  # skip invalid entries
                price = f"{flight.get('price', 'N/A')} {flight.get('currency', '')}"
                for itin in flight.get("itineraries", []):
                    for seg in itin.get("segments", []):
                        dep = seg.get("departure", {})
                        arr = seg.get("arrival", {})
                        dep_time = dep.get("at", "")
                        arr_time = arr.get("at", "")
                        dep_code = dep.get("iataCode", "")
                        arr_code = arr.get("iataCode", "")
                        carrier = seg.get("carrierCode", "")
                        number = seg.get("number", "")
                        duration = seg.get("duration", "")
                        flight_texts.append(
                            f"Flight {flight.get('id')}: {dep_code} ({dep_time}) → {arr_code} ({arr_time}) "
                            f"| {carrier}{number} | Duration: {duration} | Price: {price}"
                        )
            st.text("\n".join(flight_texts))
        else:
            st.info("No flights data available.")

    with cols[1]:
        st.subheader("Hotels")
        hotels = result.get("hotels", [])
        if hotels and not (len(hotels) == 1 and "error" in hotels[0]):
            st.json(hotels)
        else:
            st.info("No hotels found.")

   

    # -------- RAG Tips --------
    if result.get("rag_tips"):
        st.subheader("RAG Tips")
        st.write(result["rag_tips"])

    # -------- Final Itinerary --------
    st.subheader("Final Itinerary (LLM composed)")
    itinerary_text = result.get("itinerary_text", "No itinerary available.")
    st.text(itinerary_text)

    # -------- Map --------
    if result.get("map_html"):
        st.subheader("Map")
        st.components.v1.html(result["map_html"], height=600, scrolling=True)

    # -------- Download Button --------
    st.download_button(
        "Download Itinerary (.txt)",
        data=itinerary_text.encode("utf-8"),
        file_name="itinerary.txt",
        mime="text/plain",
    )
