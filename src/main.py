"""
Command line runner for the Music Recommender Simulation.

Usage: python -m src.main <profile>

Available profiles:
  chill-lofi, high-energy-pop, deep-intense-rock,
  adversarial-conflicting, adversarial-empty-taste
"""

import sys

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "chill-lofi": {
        "favorite_genres": {"lofi"},
        "favorite_moods": {"chill", "focused"},
        "target_energy": 0.375,
        "target_valence": 0.595,
        "target_danceability": 0.59,
        "target_acousticness": 0.82,
        "target_tempo_bpm": 76,
        "target_tempo_normalized": 0.225,
        "liked_song_ids": [4, 9],
        "already_heard_ids": [4, 9],
    },
    "high-energy-pop": {
        "favorite_genres": {"pop", "edm"},
        "favorite_moods": {"happy"},
        "target_energy": 0.85,
        "target_valence": 0.85,
        "target_danceability": 0.80,
        "target_acousticness": 0.15,
        "target_tempo_bpm": 128,
        "target_tempo_normalized": 0.55,
        "liked_song_ids": [1, 10, 18],
        "already_heard_ids": [1, 10, 18],
    },
    "deep-intense-rock": {
        "favorite_genres": {"rock"},
        "favorite_moods": {"intense", "moody"},
        "target_energy": 0.90,
        "target_valence": 0.30,
        "target_danceability": 0.70,
        "target_acousticness": 0.15,
        "target_tempo_bpm": 150,
        "target_tempo_normalized": 0.6875,
        "liked_song_ids": [3, 8, 19],
        "already_heard_ids": [3, 8, 19],
    },
    "adversarial-conflicting": {
        "favorite_genres": {"edm"},
        "favorite_moods": {"sad"},
        "target_energy": 0.90,
        "target_valence": 0.20,
        "target_danceability": 0.85,
        "target_acousticness": 0.10,
        "target_tempo_bpm": 160,
        "target_tempo_normalized": 0.75,
        "liked_song_ids": [],
        "already_heard_ids": [],
    },
    "adversarial-empty-taste": {
        "favorite_genres": set(),
        "favorite_moods": set(),
        "target_energy": 0.5,
        "target_valence": 0.5,
        "target_danceability": 0.5,
        "target_acousticness": 0.5,
        "target_tempo_bpm": 120,
        "target_tempo_normalized": 0.5,
        "liked_song_ids": [],
        "already_heard_ids": [],
    },
}


def main() -> None:
    profile_name = sys.argv[1] if len(sys.argv) > 1 else "chill-lofi"
    if profile_name not in PROFILES:
        print(f"Unknown profile: {profile_name}")
        print(f"Available: {', '.join(PROFILES)}")
        sys.exit(1)

    user_prefs = PROFILES[profile_name]
    songs = load_songs("data/songs.csv")
    print(f"Profile: {profile_name}")
    print(f"Loaded songs: {len(songs)}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
