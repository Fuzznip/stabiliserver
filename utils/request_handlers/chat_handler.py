from .parse_response import DiscordEmbedData

def parse_chat(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'CHAT' type
    print(f"Parsing CHAT data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Chat event processed"]}
