from .parse_response import DiscordEmbedData

def parse_grand_exchange(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'GRAND_EXCHANGE' type
    print(f"Parsing GRAND_EXCHANGE data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Grand exchange event processed"]}
