from models.submission import Submission
from models.notification_models import LootExtra

def parse_loot(data: Submission) -> dict[str, list[str]]:
    # Implement logic for handling 'LOOT' type
    print(f"Parsing LOOT data: { data }")
    return {"threads": ["example_thread_id"], "messages": ["Loot event processed"]}
