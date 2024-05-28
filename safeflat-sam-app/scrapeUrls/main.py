def handler(event, context):
    sublist = event  # The event itself is the sublist
    total = sum(sublist)
    print(f"Sublist: {sublist}, Total: {total}")
    return {"sublist": sublist, "total": total}
