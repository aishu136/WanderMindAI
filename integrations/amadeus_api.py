import os
from amadeus import Client, ResponseError

def _client():
    cid = os.getenv("AMAD_CLIENT_ID")
    csec = os.getenv("AMAD_CLIENT_SECRET")
    if not cid or not csec:
        raise EnvironmentError("Set AMAD_CLIENT_ID and AMAD_CLIENT_SECRET in .env")
    return Client(client_id=cid, client_secret=csec)

def search_flights(origin: str, destination: str, depart_date: str, adults: int = 1, max_offers: int = 3):
    try:
        a = _client()
        res = a.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=depart_date,
            adults=adults,
            max=max_offers
        )
        out = []
        for o in res.data[:max_offers]:
            out.append({
                "id": o.get("id"),
                "price": o.get("price", {}).get("total"),
                "currency": o.get("price", {}).get("currency"),
                "itineraries": o.get("itineraries")
            })
        return out
    except ResponseError as e:
        return [{"error": str(e)}]

def search_hotels(city_code: str, check_in: str, check_out: str | None, radius_km: int = 5, size: int = 8):
    if not check_in:
        return []
    try:
        a = _client()
        hotels = a.reference_data.locations.hotels.by_city.get(cityCode="PAR")
        hotel_ids = [hotel["hotelId"] for hotel in hotels.data]

    # Take the first few hotel IDs
        ids_str = ",".join(hotel_ids[:3])
       
        res = a.shopping.hotel_offers_search.get(
         hotelIds="PARH001",
         adults=1,
         checkInDate=check_in,
         checkOutDate=check_out
        )
        out = []
        for h in res.data[:size]:
            out.append({
                "name": h.get("hotel", {}).get("name"),
                "rating": h.get("hotel", {}).get("rating"),
                "offers": h.get("offers", []),
            })
        return out
    except ResponseError as e:
        return [{"error": str(e)}]
