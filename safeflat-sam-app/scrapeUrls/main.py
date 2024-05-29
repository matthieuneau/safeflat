def handler(event, context):
    print(event["website"])
    sublist = event["sublist"]  # The event itself is the sublist
    total = sum(sublist)
    print(f"Sublist: {sublist}, Total: {total}")
    return {"sublist": sublist, "total": total}
