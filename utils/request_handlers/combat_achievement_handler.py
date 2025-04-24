from .parse_response import DiscordEmbedData

def parse_combat_achievement(data) -> list[tuple[str, DiscordEmbedData]]:
    # Implement logic for handling 'COMBAT_ACHIEVEMENT' type
    print(f"Parsing COMBAT_ACHIEVEMENT data: {data}")
    return {"threads": ["example_thread_id"], "messages": ["Combat achievement event processed"]}
