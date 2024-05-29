def handler(event, context):
    print(event["website"])
    sublist = event["sublist"]  # The event itself is the sublist
    print("urls received: ", sublist)
    return "no error so far"
