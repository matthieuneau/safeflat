def generate_abritel_url(lat, lon, nb_chambres, nb_salles_de_bains, prix_min, prix_max, sort_order):
    base_url = "https://www.abritel.fr/search"
    
    # Define smaller map bounds
    map_bound_south = lat - 0.005
    map_bound_west = lon - 0.005
    map_bound_north = lat + 0.005
    map_bound_east = lon + 0.005
    
    # Sort order mapping
    sort_mapping = {
        'asc': 'PRICE_LOW_TO_HIGH',
        'desc': 'PRICE_HIGH_TO_LOW'
    }
    
    sort = sort_mapping.get(sort_order, 'PRICE_LOW_TO_HIGH')
    
    url = (
        f"{base_url}?adults=1&allowPreAppliedFilters=false"
        f"&bedroom_count_gt={nb_chambres}"
        f"&children="
        f"&latLong={lat}%2C{lon}"
        f"&mapBounds={map_bound_south}%2C{map_bound_west}"
        f"&mapBounds={map_bound_north}%2C{map_bound_east}"
        f"&multi_neighborhood_group="
        f"&neighborhood="
        f"&nightly_price={prix_min}%2C{prix_max}"
        f"&poi="
        f"&quick_filter_pricing_group="
        f"&quick_filter_rooms_spaces_group="
        f"&sort={sort}"
        f"&sortTriggerPill="
        f"&theme="
        f"&us_bathroom_count_gt={nb_salles_de_bains}"
        f"&userIntent="
    )
    
    return url

# Example usage:
lat = 43.178517
lon = 5.609222
nb_chambres = 1
nb_salles_de_bains = 1
prix_min = 0
prix_max = 2000
sort_order = 'asc'  # 'asc' for ascending, 'desc' for descending

#print(generate_abritel_url(lat, lon, nb_chambres, nb_salles_de_bains, prix_min, prix_max, sort_order))
