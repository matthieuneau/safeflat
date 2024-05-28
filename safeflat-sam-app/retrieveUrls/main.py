def handler(event, context):
    print(event["website"])
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    return {"website": event["website"], "lists": data}
