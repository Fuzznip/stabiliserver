from .parse_response import DiscordEmbedData

def parse_trade(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'TRADE' type
    print(f"Parsing TRADE data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Trade event processed"]}
