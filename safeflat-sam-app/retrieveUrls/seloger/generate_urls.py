def generate_url(postal_code):
    base_url = "https://www.seloger.com/list.htm?projects=1&types=2,1&places=[{%22postalCodes%22:[%22"
    end_url = "%22]}]&mandatorycommodities=0&privateseller=1&enterprise=0&qsVersion=1.0&m=search_refine-redirection-search_results"
    complete_url = f"{base_url}{postal_code}{end_url}"
    return complete_url