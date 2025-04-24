from .parse_response import DiscordEmbedData

def parse_group_storage(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'GROUP_STORAGE' type
    print(f"Parsing GROUP_STORAGE data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Group storage event processed"]}
