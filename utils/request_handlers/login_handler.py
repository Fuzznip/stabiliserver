def parse_login(data) -> dict[str, list[str]]:
    # Implement logic for handling 'LOGIN' type
    print(f"Parsing LOGIN data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Login event processed"]}
