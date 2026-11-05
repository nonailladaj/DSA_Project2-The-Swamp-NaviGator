import csv
import os
from datetime import datetime
from data.data_generator import GAME_DAY_DATES, generate_checkins
from src.models import CheckIn, Venue

DAY_NAMES = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

def load_venues(venues_csv_path: str) -> list[Venue]:
    venues: list[Venue] = []
    with open(venues_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            venues.append(
                Venue(
                    name=row["name"],
                    category=row["category"],
                    open_hour=int(row["open_hour"]),
                    close_hour=int(row["close_hour"]),
                    address=row["address"],
                    base_cover=float(row["base_cover"]),
                )
            )
    return venues

def load_checkins(venues_csv_path: str, checkins_csv_path: str) -> list[CheckIn]:
    if not os.path.exists(checkins_csv_path):
        generate_checkins(venues_csv_path, checkins_csv_path)
    checkins: list[CheckIn] = []
    date_cache: dict[str, tuple[str, bool]] = {}
    with open(checkins_csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = row["Timestamp"]
            date_part = ts[:10]
            hour_part = int(ts[11:13])

            if date_part not in date_cache:
                dt = datetime.strptime(date_part, "%Y-%m-%d")
                date_cache[date_part] = (DAY_NAMES[dt.weekday()], date_part in GAME_DAY_DATES)

            day_name, is_game = date_cache[date_part]
            checkins.append(
                CheckIn(
                    checkin_id=int(row["ID"]),
                    venue_name=row["Venue name"],
                    timestamp=ts,
                    day_of_week=day_name,
                    hour=hour_part,
                    is_game_day=is_game,
                    cover_price=float(row["Cover_price"]),
                    crowd_density=int(row["Crowd_density"]),
                )
            )
    return checkins