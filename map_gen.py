import folium

CITY_COORDS = {
    "Paris": [48.8566, 2.3522],
    "Rome": [41.9028, 12.4964],
    "London": [51.5074, -0.1278],
    "Delhi": [28.6139, 77.2090],
    "Tokyo": [35.6762, 139.6503]
}

def generate_map_html(cities: list[str]) -> str:
    if not cities:
        return ""
    center = CITY_COORDS.get(cities[0], [20.0, 0.0])
    m = folium.Map(location=center, zoom_start=4)
    for c in cities:
        folium.Marker(CITY_COORDS.get(c, center), popup=c).add_to(m)
    return m._repr_html_()
