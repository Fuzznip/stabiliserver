from .parse_response import DiscordEmbedData

def parse_death(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'DEATH' type
    print(f"Parsing DEATH data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Death event processed"]}
