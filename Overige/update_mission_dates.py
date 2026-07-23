import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
MISSION_DATES_FILE = ROOT / "Overige" / "mission_dates.json"
INZETTEN_FILE = ROOT / "inzetten.json"
DUTCH_TIMEZONE = ZoneInfo("Europe/Amsterdam")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def sort_key(value: str):
    head = ""
    tail = value
    for i, ch in enumerate(value):
        if not ch.isdigit():
            head = value[:i]
            tail = value[i:]
            break
    else:
        head = value
        tail = ""

    if head.isdigit():
        return (0, int(head), tail)
    return (1, value, "")


def main() -> None:
    today_nl = datetime.now(DUTCH_TIMEZONE).strftime("%d-%m-%Y")

    inzetten_data = load_json(INZETTEN_FILE)
    mission_dates_data = load_json(MISSION_DATES_FILE) if MISSION_DATES_FILE.exists() else []

    if not isinstance(inzetten_data, list):
        raise ValueError(f"{INZETTEN_FILE} must contain a JSON list.")
    if not isinstance(mission_dates_data, list):
        raise ValueError(f"{MISSION_DATES_FILE} must contain a JSON list.")

    ids_from_inzetten: List[str] = []
    seen_ids = set()
    for mission in inzetten_data:
        if not isinstance(mission, dict) or "id" not in mission:
            continue

        mission_id = str(mission["id"])
        if mission_id not in seen_ids:
            seen_ids.add(mission_id)
            ids_from_inzetten.append(mission_id)

    by_id: Dict[str, dict] = {}
    for item in mission_dates_data:
        if not isinstance(item, dict) or "id" not in item:
            continue

        mission_id = str(item["id"])
        existing_date = item.get("date")
        by_id[mission_id] = {
            "id": mission_id,
            "date": existing_date if isinstance(existing_date, str) else today_nl,
        }

    updated = 0
    added = 0
    for mission_id in ids_from_inzetten:
        if mission_id in by_id:
            if by_id[mission_id]["date"] != today_nl:
                by_id[mission_id]["date"] = today_nl
                updated += 1
        else:
            by_id[mission_id] = {"id": mission_id, "date": today_nl}
            added += 1

    result = sorted(by_id.values(), key=lambda x: sort_key(x["id"]))

    with MISSION_DATES_FILE.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print(f"Updated file: {MISSION_DATES_FILE}")
    print(f"Missions in output: {len(result)}")
    print(f"Updated date on existing missions: {updated}")
    print(f"Added missing missions: {added}")
    print(f"Date set to: {today_nl}")


if __name__ == "__main__":
    main()
