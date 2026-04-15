from src.recommender import (
    Song,
    UserProfile,
    Recommender,
    closeness,
    normalize_tempo,
    load_songs,
    score_song,
    recommend_songs,
    TEMPO_MIN,
    TEMPO_MAX,
    WEIGHTS,
)


def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def make_song_dict(**overrides):
    base = {
        "id": 1,
        "title": "Test Song",
        "artist": "Tester",
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "tempo_bpm": 120.0,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }
    base.update(overrides)
    return base


def make_user_prefs(**overrides):
    base = {
        "favorite_genres": {"pop"},
        "favorite_moods": {"happy"},
        "target_energy": 0.8,
        "target_valence": 0.9,
        "target_danceability": 0.8,
        "target_acousticness": 0.2,
        "target_tempo_normalized": normalize_tempo(120),
        "already_heard_ids": [],
    }
    base.update(overrides)
    return base


# OOP API (Recommender class)

def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommend_respects_k_smaller_than_catalog():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    assert len(rec.recommend(user, k=1)) == 1


# Helpers

def test_closeness_identical_values_returns_one():
    assert closeness(0.5, 0.5) == 1.0


def test_closeness_max_distance_returns_zero():
    assert closeness(0.0, 1.0) == 0.0
    assert closeness(1.0, 0.0) == 0.0


def test_normalize_tempo_clamps_below_min():
    assert normalize_tempo(TEMPO_MIN - 50) == 0.0


def test_normalize_tempo_clamps_above_max():
    assert normalize_tempo(TEMPO_MAX + 50) == 1.0


def test_normalize_tempo_midpoint():
    midpoint = (TEMPO_MIN + TEMPO_MAX) / 2
    assert normalize_tempo(midpoint) == 0.5


# score_song (dict API used by main.py)

def test_score_song_returns_float_and_list():
    score, reasons = score_song(make_user_prefs(), make_song_dict())
    assert isinstance(score, float)
    assert isinstance(reasons, list)


def test_score_song_perfect_match_beats_opposite():
    user = make_user_prefs()
    perfect = make_song_dict()
    opposite = make_song_dict(
        id=2,
        genre="rock",
        mood="intense",
        energy=0.0,
        valence=0.0,
        danceability=0.0,
        acousticness=1.0,
        tempo_bpm=200,
    )
    perfect_score, _ = score_song(user, perfect)
    opposite_score, _ = score_song(user, opposite)
    assert perfect_score > opposite_score


def test_score_song_reasons_include_genre_and_mood_on_match():
    score, reasons = score_song(make_user_prefs(), make_song_dict())
    joined = " ".join(reasons)
    assert "pop" in joined
    assert "happy" in joined


def test_score_song_weights_sum_to_expected_max():
    score, _ = score_song(make_user_prefs(), make_song_dict())
    assert score == sum(WEIGHTS.values())


# recommend_songs (dict API used by main.py)

def test_recommend_songs_filters_already_heard():
    user = make_user_prefs(already_heard_ids=[1])
    songs = [make_song_dict(id=1), make_song_dict(id=2)]
    results = recommend_songs(user, songs, k=5)
    assert all(song["id"] != 1 for song, _, _ in results)
    assert len(results) == 1


def test_recommend_songs_sorts_descending():
    user = make_user_prefs()
    songs = [
        make_song_dict(id=1, genre="rock", mood="intense"),
        make_song_dict(id=2, genre="pop", mood="happy"),
        make_song_dict(id=3, genre="lofi", mood="chill"),
    ]
    results = recommend_songs(user, songs, k=3)
    scores = [score for _, score, _ in results]
    assert scores == sorted(scores, reverse=True)
    assert results[0][0]["id"] == 2


def test_recommend_songs_respects_k():
    user = make_user_prefs()
    songs = [make_song_dict(id=i) for i in range(1, 6)]
    assert len(recommend_songs(user, songs, k=2)) == 2


def test_recommend_songs_k_larger_than_catalog():
    user = make_user_prefs()
    songs = [make_song_dict(id=1), make_song_dict(id=2)]
    assert len(recommend_songs(user, songs, k=10)) == 2


def test_recommend_songs_empty_catalog():
    assert recommend_songs(make_user_prefs(), [], k=5) == []


def test_recommend_songs_returns_tuple_shape():
    results = recommend_songs(make_user_prefs(), [make_song_dict()], k=1)
    assert len(results) == 1
    song, score, explanation = results[0]
    assert isinstance(song, dict)
    assert isinstance(score, float)
    assert isinstance(explanation, str)


# load_songs

def test_load_songs_real_csv_has_expected_types():
    songs = load_songs("data/songs.csv")
    assert len(songs) > 0
    first = songs[0]
    assert isinstance(first["id"], int)
    assert isinstance(first["energy"], float)
    assert isinstance(first["tempo_bpm"], float)
    assert isinstance(first["title"], str)
