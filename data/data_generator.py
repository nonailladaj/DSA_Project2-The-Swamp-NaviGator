import csv
import os
import random
from datetime import datetime, timedelta

RANDOM_SEED = 42
DEFAULT_NUM_RECORDS = 120_000

GAME_DAY_DATES = {
    "2026-09-05", "2026-09-12", "2026-09-19", "2026-10-10",
    "2026-10-24", "2026-10-31", "2026-11-14", "2026-11-28",
    "2027-01-16", "2027-02-13", "2027-03-17", "2027-04-03",
    "2027-04-10", "2027-04-21",
}

SCHOOL_BREAK_DATES = {
    "2026-11-22", "2026-11-23", "2026-11-24", "2026-11-25",
    "2026-11-26", "2026-11-27", "2026-12-12", "2026-12-13",
    "2026-12-14", "2026-12-15", "2026-12-16", "2027-01-18",
    "2027-03-06", "2027-03-07", "2027-03-08", "2027-03-09",
    "2027-03-10", "2027-03-11", "2027-03-12", "2027-03-13",
    "2027-03-14", "2027-05-01", "2027-05-02", "2027-05-03",
}


def is_venue_open(open_hour, close_hour, hour):
    if open_hour < close_hour:
        return open_hour <= hour < close_hour
    return hour >= open_hour or hour < close_hour


def generate_checkins(
    venues_csv_path,
    output_csv_path,
    num_records=DEFAULT_NUM_RECORDS,
    seed=RANDOM_SEED,
):
    rng = random.Random(seed)

    with open(venues_csv_path, mode="r", encoding="utf-8") as f:
        venues = [
            {
                "name": row["name"],
                "category": row["category"],
                "open_hour": int(row["open_hour"]),
                "close_hour": int(row["close_hour"]),
                "base_cover": float(row["base_cover"]),
            }
            for row in csv.DictReader(f)
        ]

    fall_dates = [datetime(2026, 8, 20) + timedelta(days=i) for i in range(119)]
    spring_dates = [datetime(2027, 1, 11) + timedelta(days=i) for i in range(113)]
    all_dates = fall_dates + spring_dates

    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Venue name", "Timestamp", "Cover_price", "Crowd_density"])

        for checkin_id in range(1, num_records + 1):
            venue = rng.choice(venues)
            chosen_date = rng.choice(all_dates)
            date_str = chosen_date.strftime("%Y-%m-%d")
            day_of_week = chosen_date.strftime("%A")
            is_game_day = date_str in GAME_DAY_DATES
            is_break = date_str in SCHOOL_BREAK_DATES
            is_weekend = day_of_week in ("Thursday", "Friday", "Saturday")

            open_h = venue["open_hour"]
            close_h = venue["close_hour"]
            valid_hours = [h for h in range(24) if is_venue_open(open_h, close_h, h)] or list(range(24))

            hour = rng.choice(valid_hours) if rng.random() < 0.97 else rng.randint(0, 23)
            minute = rng.randint(0, 59)
            timestamp_str = f"{date_str} {hour:02d}:{minute:02d}"

            cat = venue["category"]
            base_cover = venue["base_cover"]

            if not is_venue_open(open_h, close_h, hour):
                cover_price = 0.0
                crowd_density = rng.randint(1, 5)
            elif is_break:
                cover_price = 0.0
                crowd_density = rng.randint(5, 22)
            else:
                if cat in ("Midtown Bar", "Nightclub"):
                    if hour >= 21 or hour <= 2:
                        base_crowd = rng.randint(68, 95) if is_weekend else rng.randint(35, 65)
                        cover_price = base_cover + (5.0 if is_weekend else 0.0)
                    else:
                        base_crowd = rng.randint(25, 55)
                        cover_price = max(0.0, base_cover - 5.0)
                elif cat in ("Downtown Bar", "Lounge & Arcade Bar"):
                    if hour >= 21 or hour <= 2:
                        base_crowd = rng.randint(60, 88) if is_weekend else rng.randint(30, 60)
                        cover_price = (base_cover + 5.0) if (base_cover > 0 and is_weekend) else base_cover
                    else:
                        base_crowd = rng.randint(20, 50)
                        cover_price = 0.0
                else:
                    if hour >= 18 or hour <= 1 or hour in (12, 13):
                        base_crowd = rng.randint(60, 88) if is_weekend else rng.randint(40, 70)
                    else:
                        base_crowd = rng.randint(20, 50)
                    cover_price = base_cover

                if is_game_day:
                    base_crowd = min(100, base_crowd + rng.randint(18, 35))
                    if cat in ("Midtown Bar", "Nightclub"):
                        cover_price += rng.choice([10.0, 15.0, 20.0])
                    elif cat == "Sports Bar & Grill":
                        cover_price += rng.choice([5.0, 10.0])
                    elif base_cover > 0:
                        cover_price += rng.choice([5.0, 10.0])

                crowd_density = max(1, min(100, base_crowd + rng.randint(-5, 5)))
                if cover_price > 0:
                    cover_price = round(max(0.0, cover_price + rng.choice([0.0, 0.0, 2.0, -2.0])), 2)

            writer.writerow([checkin_id, venue["name"], timestamp_str, f"{cover_price:.2f}", crowd_density])

    return num_records


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    generate_checkins(
        os.path.join(base_dir, "venuedata.csv"),
        os.path.join(base_dir, "checkins.csv"),
    )