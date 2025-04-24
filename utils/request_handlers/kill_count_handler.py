from .parse_response import DiscordEmbedData

def parse_kill_count(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'KILL_COUNT' type
    print(f"Parsing KILL_COUNT data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Kill count event processed"]}
