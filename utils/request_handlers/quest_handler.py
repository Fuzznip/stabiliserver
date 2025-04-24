from .parse_response import DiscordEmbedData

def parse_quest(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'QUEST' type
    print(f"Parsing QUEST data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Quest event processed"]}
