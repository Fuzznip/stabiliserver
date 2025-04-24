from .parse_response import DiscordEmbedData

def parse_speedrun(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'SPEEDRUN' type
    print(f"Parsing SPEEDRUN data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Speedrun event processed"]}
