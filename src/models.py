from dataclasses import dataclass

@dataclass(frozen=True)
class Venue:
    name: str
    category: str
    open_hour: int
    close_hour: int
    address: str
    base_cover: float
    def is_open_at(self, hour: int) -> bool:
        if self.open_hour < self.close_hour:
            return self.open_hour <= hour < self.close_hour
        return hour >= self.open_hour or hour < self.close_hour

@dataclass(frozen=True)
class CheckIn:
    checkin_id: int
    venue_name: str
    timestamp: str
    day_of_week: str
    hour: int
    is_game_day: bool
    cover_price: float
    crowd_density: int

@dataclass
class VenueAggregate:
    venue_name: str
    count: int = 0
    total_cover: float = 0.0
    total_crowd: float = 0.0
    def add_checkin(self, cover_price: float, crowd_density: int) -> None:
        self.count += 1
        self.total_cover += cover_price
        self.total_crowd += crowd_density
    def merge(self, other: "VenueAggregate") -> None:
        self.count += other.count
        self.total_cover += other.total_cover
        self.total_crowd += other.total_crowd
    @property
    def avg_cover(self) -> float:
        return self.total_cover / self.count if self.count > 0 else 0.0
    @property
    def avg_crowd(self) -> float:
        return self.total_crowd / self.count if self.count > 0 else 0.0

@dataclass(frozen=True)
class UserQuery:
    category: str
    day_of_week: str
    hour: int
    preferred_crowd: str
    max_budget: float
    is_game_day: bool

@dataclass(frozen=True)
class ScoredVenue:
    score: float
    venue_name: str
    category: str
    address: str
    expected_cover: float
    expected_crowd: float
    sample_count: int

    def __lt__(self, other: "ScoredVenue") -> bool:
        if self.score != other.score:
            return self.score < other.score
        if self.expected_cover != other.expected_cover:
            return self.expected_cover > other.expected_cover
        return self.venue_name > other.venue_name

    def __gt__(self, other: "ScoredVenue") -> bool:
        if self.score != other.score:
            return self.score > other.score
        if self.expected_cover != other.expected_cover:
            return self.expected_cover < other.expected_cover
        return self.venue_name < other.venue_name