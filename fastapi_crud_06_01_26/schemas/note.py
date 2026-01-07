def noteEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "email":item["email"],
        "age":item["age"],
        "title":item["title"],
        "desc":item["desc"],
        "important":item["important"]
    }