import streamlit as st
from langgraph.graph import StateGraph, START, END
from langchain_aws.chat_models import ChatBedrock
import os
from dotenv import load_dotenv
from typing import TypedDict

# Load AWS credentials from .env
load_dotenv()
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
os.environ["AWS_REGION"] = os.getenv("AWS_REGION", "ap-south-1")

# --- Define State Schema ---
class TripState(TypedDict):
    trip_details: str

# --- Simple Agent Class ---
class SimpleAgent:
    def __init__(self, name, llm, system_prompt):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt

    def __call__(self, state: TripState) -> TripState:
        user_input = state.get("trip_details", "")
        prompt = f"{self.system_prompt}\n\nUser request: {user_input}"
        result = self.llm.invoke(prompt).content
        return {"trip_details": result}

# --- Bedrock Models ---
destination_llm = ChatBedrock(model_id="amazon.titan-text-express-v1")
budget_llm = ChatBedrock(model_id="mistral.mistral-large-2402-v1:0")
itinerary_llm = ChatBedrock(model_id="meta.llama3-70b-instruct-v1:0")

# --- Agents ---
destination_agent = SimpleAgent(
    name="DestinationResearchAgent",
    llm=destination_llm,
    system_prompt="You are a travel expert. Suggest 5 attractions and activities for each city."
)

budget_agent = SimpleAgent(
    name="BudgetOptimizationAgent",
    llm=budget_llm,
    system_prompt="Optimize the itinerary based on the given budget, without removing all fun."
)

itinerary_agent = SimpleAgent(
    name="ItineraryComposerAgent",
    llm=itinerary_llm,
    system_prompt="Combine all inputs into a day-by-day travel itinerary with short descriptions."
)

# --- Graph Setup ---
graph = StateGraph(TripState)  # Pass schema here
graph.add_node("destination", destination_agent)
graph.add_node("budget", budget_agent)
graph.add_node("itinerary", itinerary_agent)

graph.add_edge(START, "destination")
graph.add_edge("destination", "budget")
graph.add_edge("budget", "itinerary")
graph.add_edge("itinerary", END)

app = graph.compile()

# --- Streamlit UI ---
st.set_page_config(page_title="Travel Itinerary Designer", page_icon="✈️")

st.title("✈️ AI Travel Itinerary Designer")
st.markdown("Powered by **LangGraph Workflow** + **AWS Bedrock**")

destination = st.text_input("Enter destinations (comma-separated):", "Paris, Rome")
travel_dates = st.text_input("Enter travel dates:", "2025-09-10 to 2025-09-17")
budget = st.number_input("Enter your budget (USD):", min_value=500, max_value=20000, value=2000)
interests = st.text_area("Your interests (e.g., museums, hiking, food, shopping):", "history, art, food")

if st.button("Generate Itinerary"):
    with st.spinner("AI agents are planning your trip..."):
        user_input = {
            "trip_details": f"{travel_dates}, budget ${budget}, destinations: {destination}, interests: {interests}"
        }
        result_state = app.invoke(user_input)
        result = result_state.get("trip_details", "")

    st.success("Itinerary Ready!")
    st.subheader("📅 Your Travel Plan:")
    st.write(result)

    st.download_button(
        label="Download Itinerary as Text",
        data=result.encode("utf-8"),
        file_name="travel_itinerary.txt",
        mime="text/plain"
    )
