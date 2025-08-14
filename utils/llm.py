import os
from typing import List, Dict, Any

USE_BEDROCK = os.getenv("USE_BEDROCK", "true").lower() in {"1", "true", "yes"}

def _fallback_compose(**kwargs) -> str:
    cities = kwargs.get("cities", [])
    hops = kwargs.get("hops", [])
    rag = kwargs.get("rag_tips", "")
    lines = ["# Draft Itinerary (Fallback)\n"]
    for idx, city in enumerate(cities, start=1):
        lines.append(f"Day {idx}: Explore {city}")
    if rag:
        lines.append("\n# Tips from Blogs\n" + rag[:1000])
    return "\n".join(lines)

def compose_itinerary_llm(
    cities: List[str],
    hops: List[Dict[str, Any]],
    interests: str,
    budget: int,
    flights: Any,
    hotels: Any,
    rag_tips: str,
) -> str:
    prompt = f"""
You are a travel planner. Build a concise day-by-day itinerary.

Cities: {cities}
Hops: {hops}
Budget (USD): {budget}
Interests: {interests}

Flight offers (may be empty): {flights}
Hotel offers (may be empty): {hotels}

Incorporate these crowd tips (if any):
{rag_tips}

Return a readable plan with days, activities, brief reasons, and where useful, tie to flights/hotels.
"""
    if USE_BEDROCK:
        try:
            from langchain_aws.chat_models import ChatBedrock
            llm = ChatBedrock(model_id=os.getenv("BEDROCK_MODEL_ID", "mistral.mistral-large-2407"))
            return llm.invoke(prompt).content
        except Exception as e:
            return _fallback_compose(cities=cities, hops=hops, rag_tips=rag_tips)
    else:
        return _fallback_compose(cities=cities, hops=hops, rag_tips=rag_tips)
