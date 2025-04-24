from .parse_response import DiscordEmbedData

def parse_collection(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'COLLECTION' type
    print(f"Parsing COLLECTION data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Collection event processed"]}
