import json
import base64
from datetime import datetime

def encode_cursor(section_offset, items_offset, version):
    # Create the JSON object
    cursor_dict = {
        "section_offset": section_offset,
        "items_offset": items_offset,
        "version": version
    }
    
    # Convert the JSON object to a string
    cursor_json = json.dumps(cursor_dict)
    
    # Encode the JSON string to bytes
    cursor_bytes = cursor_json.encode('utf-8')
    
    # Encode the bytes to base64
    cursor_base64 = base64.b64encode(cursor_bytes)
    
    # Convert the base64 bytes back to a string
    cursor_base64_str = cursor_base64.decode('utf-8')
    
    return cursor_base64_str

def generate_airbnb_url(postal_code, page_number, checkin_date, checkout_date):
    # Format dates to yyyy-mm-dd
    checkin_date_formatted = datetime.strptime(checkin_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    checkout_date_formatted = datetime.strptime(checkout_date, "%d/%m/%Y").strftime("%Y-%m-%d")
    
    # Generate cursor for the given page
    results_per_page = 18
    items_offset = results_per_page * (page_number - 1)
    cursor = encode_cursor(0, items_offset, 1)
    
    # Base URL
    base_url = "https://www.airbnb.fr/s/{postal_code}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes"
    base_url += "&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-06-01&monthly_length=3&monthly_end_date=2024-09-01"
    base_url += "&price_filter_input_type=0&channel=EXPLORE&date_picker_type=calendar"
    base_url += f"&checkin={checkin_date_formatted}&checkout={checkout_date_formatted}"
    base_url += "&source=structured_search_input_header&search_type=filter_change&price_filter_num_nights=1"
    base_url += "&zoom_level=15&room_types%5B%5D=Entire%20home%2Fapt&adults=1&flexible_date_search_filter_type=6"
    base_url += f"&query={postal_code}&search_mode=regular_search"
    
    # Add pagination parameters if page_number is greater than 1
    if page_number > 1:
        base_url += "&pagination_search=true&cursor=" + cursor
    
    return base_url



