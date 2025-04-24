from .parse_response import DiscordEmbedData

def parse_login(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'LOGIN' type
    print(f"Parsing LOGIN data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Login event processed"]}
