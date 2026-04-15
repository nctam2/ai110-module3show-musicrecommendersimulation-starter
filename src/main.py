"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Study-lofi profile, built from the averages of "Library Rain" (id 4)
    # and "Focus Flow" (id 9) — a user who wants calm, acoustic, focus music.
    user_prefs = {
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
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
