def handler(event, context):
    print(event["website"])
    sublist = event["sublist"]  # The event itself is the sublist
    return "no error so far"
