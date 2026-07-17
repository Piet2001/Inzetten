import json
from calendar import monthrange
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent.parent
COMPLETE_FILE = ROOT / "complete.json"
MISSION_DATES_FILE = ROOT / "Overige" / "mission_dates.json"
ARCHIVE_FILE = ROOT / "Overige" / "archive.json"
DUTCH_TIMEZONE = ZoneInfo("Europe/Amsterdam")


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def parse_ddmmyyyy(value: str) -> Optional[date]:
    try:
        return datetime.strptime(value, "%d-%m-%Y").date()
    except (TypeError, ValueError):
        return None


def subtract_months(source: date, months: int) -> date:
    year = source.year
    month = source.month - months
    while month <= 0:
        month += 12
        year -= 1

    last_day = monthrange(year, month)[1]
    day = min(source.day, last_day)
    return date(year, month, day)


def main() -> None:
    complete_data = load_json(COMPLETE_FILE)
    mission_dates = load_json(MISSION_DATES_FILE)
    archive_data = load_json(ARCHIVE_FILE) if ARCHIVE_FILE.exists() else []

    if not isinstance(complete_data, list):
        raise ValueError(f"{COMPLETE_FILE} must contain a JSON list.")
    if not isinstance(mission_dates, list):
        raise ValueError(f"{MISSION_DATES_FILE} must contain a JSON list.")
    if not isinstance(archive_data, list):
        raise ValueError(f"{ARCHIVE_FILE} must contain a JSON list.")

    today_nl = datetime.now(DUTCH_TIMEZONE).date()
    cutoff_date = subtract_months(today_nl, 3)
    dates_by_id: dict[str, date] = {}
    for item in mission_dates:
        if not isinstance(item, dict) or "id" not in item:
            continue

        mission_id = str(item["id"])
        parsed_date = parse_ddmmyyyy(item.get("date"))
        if parsed_date is not None:
            dates_by_id[mission_id] = parsed_date

    keep_missions = []
    removed_missions = []
    for mission in complete_data:
        if not isinstance(mission, dict) or "id" not in mission:
            keep_missions.append(mission)
            continue

        mission_id = str(mission["id"])
        mission_date = dates_by_id.get(mission_id)
        if mission_date is not None and mission_date < cutoff_date:
            removed_missions.append(mission)
        else:
            keep_missions.append(mission)

    keep_ids = {
        str(mission["id"])
        for mission in keep_missions
        if isinstance(mission, dict) and "id" in mission
    }

    archive_by_id = {
        str(item.get("id")): item
        for item in archive_data
        if isinstance(item, dict) and "id" in item and str(item.get("id")) not in keep_ids
    }
    for mission in removed_missions:
        archive_by_id[str(mission["id"])] = mission

    updated_archive = list(archive_by_id.values())

    with COMPLETE_FILE.open("w", encoding="utf-8") as file:
        json.dump(keep_missions, file, indent=2, ensure_ascii=False)

    with ARCHIVE_FILE.open("w", encoding="utf-8") as file:
        json.dump(updated_archive, file, indent=2, ensure_ascii=False)

    print(f"Cutoff date (older than 3 months): {cutoff_date.strftime('%d-%m-%Y')}")
    print(f"Removed from complete: {len(removed_missions)}")
    print(f"Remaining in complete: {len(keep_missions)}")
    print(f"Total in archive: {len(updated_archive)}")


if __name__ == "__main__":
    main()