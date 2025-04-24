from .parse_response import DiscordEmbedData

def parse_leagues_relic(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'LEAGUES_RELIC' type
    print(f"Parsing LEAGUES_RELIC data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Leagues relic event processed"]}
