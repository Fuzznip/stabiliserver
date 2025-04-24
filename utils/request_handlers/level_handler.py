from .parse_response import DiscordEmbedData

def parse_level(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'LEVEL' type
    print(f"Parsing LEVEL data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Level event processed"]}
