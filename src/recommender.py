from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


WEIGHTS = {
    "energy": 0.15,
    "valence": 0.15,
    "danceability": 0.10,
    "acousticness": 0.10,
    "tempo": 0.10,
    "genre": 0.20,
    "mood": 0.20,
}

TEMPO_MIN = 40
TEMPO_MAX = 200


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def normalize_tempo(bpm: float) -> float:
    return max(0.0, min(1.0, (bpm - TEMPO_MIN) / (TEMPO_MAX - TEMPO_MIN)))


def closeness(song_value: float, user_value: float) -> float:
    return 1.0 - abs(song_value - user_value)


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        score = 0.0
        if song.genre == user.favorite_genre:
            score += 0.4
        if song.mood == user.favorite_mood:
            score += 0.3
        score += 0.2 * closeness(song.energy, user.target_energy)
        if user.likes_acoustic:
            score += 0.1 * song.acousticness
        else:
            score += 0.1 * (1.0 - song.acousticness)
        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        return sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        parts = []
        if song.genre == user.favorite_genre:
            parts.append(f"matches your favorite genre ({song.genre})")
        if song.mood == user.favorite_mood:
            parts.append(f"matches your favorite mood ({song.mood})")
        parts.append(f"energy closeness {closeness(song.energy, user.target_energy):.2f}")
        return "Recommended because it " + " and ".join(parts) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("id"):
                continue
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences using the weighted
    closeness formula. Returns (score, reasons).
    """
    c_energy = closeness(song["energy"], user_prefs["target_energy"])
    c_valence = closeness(song["valence"], user_prefs["target_valence"])
    c_dance = closeness(song["danceability"], user_prefs["target_danceability"])
    c_acoustic = closeness(song["acousticness"], user_prefs["target_acousticness"])
    c_tempo = closeness(
        normalize_tempo(song["tempo_bpm"]),
        user_prefs["target_tempo_normalized"],
    )

    genre_score = 1.0 if song["genre"] in user_prefs["favorite_genres"] else 0.0
    mood_score = 1.0 if song["mood"] in user_prefs["favorite_moods"] else 0.0

    score = (
        WEIGHTS["energy"] * c_energy
        + WEIGHTS["valence"] * c_valence
        + WEIGHTS["danceability"] * c_dance
        + WEIGHTS["acousticness"] * c_acoustic
        + WEIGHTS["tempo"] * c_tempo
        + WEIGHTS["genre"] * genre_score
        + WEIGHTS["mood"] * mood_score
    )

    reasons: List[str] = []
    if genre_score == 1.0:
        reasons.append(f"matches your {song['genre']} taste")
    if mood_score == 1.0:
        reasons.append(f"fits a {song['mood']} mood")
    if c_energy >= 0.9:
        reasons.append(f"energy {song['energy']:.2f} is close to your target")
    if c_acoustic >= 0.9:
        reasons.append(f"acousticness {song['acousticness']:.2f} feels right")
    if c_tempo >= 0.9:
        reasons.append(f"tempo {int(song['tempo_bpm'])} BPM is in your range")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, filters out already-heard tracks, sorts by score
    descending, and returns the top k as (song, score, explanation) tuples.
    """
    heard = set(user_prefs.get("already_heard_ids", []))
    scored: List[Tuple[Dict, float, str]] = []
    for song in songs:
        if song["id"] in heard:
            continue
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "numeric similarity only"
        scored.append((song, score, explanation))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
