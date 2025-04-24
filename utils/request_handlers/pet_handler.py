from .parse_response import DiscordEmbedData

def parse_pet(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'PET' type
    print(f"Parsing PET data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Pet event processed"]}
