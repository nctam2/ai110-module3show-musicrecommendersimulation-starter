# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

JustVibes 1.0

---

## 2. Intended Use

JustVibes 1.0 takes a small catalog of songs and a user taste profile and returns the top 5 tracks that best match that taste. The profile is a mix of liked genres, liked moods, and numeric feature targets like energy and tempo. The system assumes the user has at least some sense of what they like, and that a simple content-based match is good enough.

**This is for classroom exploration, not real users.** Treat it as a way to learn how scoring, weighting, and ranking work in a toy system.

**Not intended for:**

- Powering a real music app or playlist feature.
- Making decisions that affect anyone outside of this project.
- Comparing artists, labels, or anything involving money or exposure.
- Any setting where the 24-song catalog would be mistaken for a real library.

---

## 3. How the Model Works

Each song in the catalog comes tagged with a genre, a mood, and five numbers between 0 and 1 for energy, valence (how positive it feels), danceability, acousticness, and tempo (converted into a 0 to 1 range).

The user is described in the same language: a set of liked genres, a set of liked moods, and target values for each of those same five numbers. The numeric targets come from averaging the feature values of songs the user already likes.

To score a song, the system asks a few questions. Does this song's genre sit inside the user's liked genres? Does its mood sit inside the user's liked moods? How close is each of the numeric features to what the user wants? Closeness is just 1 minus the distance between the two values, so a perfect match is 1 and being on opposite ends is 0.

All of those answers get blended into one score using fixed weights. Genre and mood each count for 20 percent. Energy and valence each count for 15 percent. Danceability, acousticness, and tempo each count for 10 percent. The system does this for every song, throws out anything the user has already heard, sorts by score, and returns the top 5 along with a short "because" explanation listing the strongest reasons each song ranked where it did.

---

## 4. Data

The catalog is `data/songs.csv`, which has 24 songs. Each row has an id, title, artist, genre, mood, and five numeric features: energy, tempo_bpm, valence, danceability, and acousticness. All numeric values are on a 0 to 1 scale except tempo_bpm, which gets normalized at scoring time.

I used the starter dataset as-is. Nothing was added or removed.

**Genre spread (24 songs total):**

- 3 each: pop, lofi, indie folk, ambient
- 2 each: hip hop, edm, classical
- 1 each: rock, techno, synthwave, jazz, indie pop, drum and bass

**Mood spread:**

- 6 intense, 5 chill, 4 happy, 3 sad, 3 moody, 2 relaxed, 1 focused

The catalog is small and intentionally tilted toward electronic and indie styles. Big parts of real musical taste are just missing. There is no country, no metal, no r&b, no latin, no funk, no gospel, no k-pop, no reggae, and no spoken-word or genre-blending tracks. On the mood side, things like "romantic," "nostalgic," or "angry" are also absent. Whose taste does this reflect? Broadly speaking, a young, English-speaking, mostly-Western listener with a preference for chill electronic and indie music. The recommender should not be treated as neutral.

---

## 5. Strengths

Users with a clear, consistent taste profile get confident, intuitive rankings. The chill-lofi profile is the best example: Midnight Coding scored 0.97 and the rest of the top 5 were all low-energy acoustic tracks. If I was a lofi listener and opened the app, that list would feel correct on the first look.

Every recommendation comes with a plain-language "because" line naming the strongest reasons that song scored where it did. That transparency makes it easy to understand why a pick landed in the list, and it also makes it easy to spot when the scoring is doing something weird.

The system degrades gracefully when the user's favorite genre is thin in the catalog. The deep-intense-rock profile has only one rock song available, and that song was already heard. Instead of returning nothing, the recommender pulled from nearby genres like techno, edm, and synthwave that shared the intense or moody mood. The ranking still felt directionally correct.

Finally, the math is fast and easy to debug. Closeness and weighted sums are simple enough that I can hand-verify a score if something looks off, which made the whole evaluation phase possible.

---

## 6. Limitations and Bias

The catalog has 24 songs, which is the biggest limitation on its own. Any recommender is only as good as the pool it picks from, and with this small a pool the system can run out of real matches fast. A concrete example: the `focused` mood only shows up on one song (Focus Flow), so a user whose taste leans toward focus music gets exactly one genuine mood match and four numeric-proximity songs dressed up to look similar. Rock is in the same spot with just one track in the catalog.

The closeness scoring has no diversity push built in. Once the system finds a song that nails a user's profile, the next best results tend to be near-duplicates of the first one, so the top 5 feels like variations on a theme instead of a range of options. Genre and mood together hold 0.40 of the total weight, which acts as a soft cap on how much a numerically-perfect song from another genre can climb. That came out clearly in the adversarial-conflicting profile, where a sad-tagged indie folk track got beaten by edm intense tracks that had both the genre match and the strong energy numbers in their favor.

Finally, the user profile is built by averaging the features of a user's liked songs. Anyone with eclectic taste, say both high-energy workout music and low-energy study music, gets flattened into a mushy middle that does not match either cluster they actually like. The system treats every user as if their preferences live in one spot, which is not how taste actually works. Something that would definitely need to be approached differently for future iterations.

---

## 7. Evaluation

I evaluated the recommender two ways: a pytest suite that covers the scoring math and edge cases (19 tests in `tests/test_recommender.py`), and a set of five named user profiles in `src/main.py` that exercise the system end to end. Each profile run is saved in `docs/runs/`.

**Profiles tested and what each was probing for:**

- **chill-lofi:** clean baseline with low energy, high acousticness, lofi plus focused and chill moods. Checking that a straightforward profile produces a confident, on-target top pick.
- **high-energy-pop:** pop and edm with a happy mood at energy 0.85. Checking whether the ranking stays pop-forward when several non-pop songs also hit the energy target.
- **deep-intense-rock:** high energy rock with intense and moody moods. The catalog only has one rock song and it is already heard, so I wanted to see whether the fallback logic finds nearby genres.
- **adversarial-conflicting:** edm genre with a sad mood and energy 0.90. Mood and genre are pulling in opposite directions on purpose.
- **adversarial-empty-taste:** no favorite genres or moods, every numeric target at 0.5. A "user with no preferences" stress test.

**What surprised me:**

- chill-lofi: how dominant Midnight Coding was. It scored 0.97 while the next song scored 0.74. A perfect multi-axis match basically runs away with the ranking.
- high-energy-pop: Block Party (hip hop, not pop or edm) tied with Gym Hero at 0.76. Strong mood plus energy alignment closed the gap on the genre bonus.
- deep-intense-rock: with the only rock song filtered out as already heard, the system quietly fell back to techno, edm, and synthwave tracks that shared the intense mood. That graceful degradation was a nice surprise.
- adversarial-conflicting: the system leaned toward genre plus energy over the mood tag. Bass Drop Overdrive and Pulse Reactor (edm, intense) beat Empty Rooms (indie folk, sad) even though only the indie folk track matched the user's stated mood.
- adversarial-empty-taste: every score clustered around 0.50 and the top pick (Midnight Coding) is basically the song closest to the middle of every numeric axis. Without any categorical hooks, the ranking becomes a bland middle.

Beyond the profile runs, I did a weight experiment where I doubled energy to 0.30 and halved genre to 0.10. The top 5 orderings stayed the same for chill-lofi and high-energy-pop, but Block Party's lead over Gym Hero widened noticeably. That confirmed weights matter most when two songs are close, not when there is a runaway winner.

---

## 8. Future Work

If I kept developing this, three changes would matter most:

1. **Add a diversity push to the top 5.** Right now the ranker just picks the five best-scoring songs, which often means five near-duplicates of the same winner. A small tweak that penalizes songs too similar to ones already in the list would give the user more range without throwing out the closeness idea entirely.
2. **Let a user profile hold more than one taste cluster.** The current average-based profile flattens eclectic taste into a mushy middle. Storing two or three clusters per user (gym music, study music, late-night music) and scoring against each separately would fix that without making the model hard to explain.
3. **Grow the catalog and balance it.** 24 songs is enough to demo the math but not enough to surface real recommendations. Pulling from a public dataset and ensuring at least a handful of songs per genre and mood would make the evaluation much more meaningful. It would also make the focused and rock edge cases stop being edge cases.

---

## 9. Personal Reflection

The thing that stuck with me most is how much the "smart" behavior of a recommender is really just weighted math over features someone decided to include. There is no hidden intelligence here. If a genre is missing from the catalog, no user can ever be recommended it. If a weight is set too high, one dimension crowds out all the others. Every design choice shows up in the output, and the output looks confident even when the underlying data is thin. It makes me wonder how these systems are tested in productions. Do they roll out to sample users? How much data do they test off of? Would be interesting to hear from someone with experience working on these systems.

The unexpected part was watching the adversarial-conflicting profile. I thought asking for sad edm at high energy would break the system or produce chaos, but instead it just quietly prioritized the edm intense tracks and pushed the one sad indie folk match to position 3. The system was not confused. It was doing exactly what the weights told it to do, and the result just did not match the user's stated mood. That felt like a small version of what goes wrong in real recommenders: the math is fine, the scoreboard is fine, and the user still ends up with something they did not want.

It also changed how I think about the apps I use. Spotify's Discover Weekly and Apple Music's recommendations are doing something far more sophisticated than this, but the same underlying question applies. What features did someone pick, what weights did they tune, whose taste is overrepresented in the training pool, and which users are being quietly served a narrower version of the catalog. Human judgment matters in all of those choices, and I do not think that goes away just because the model gets bigger. But I do have a lot more respect for the time the engineers put into the more sophisticated models, into a small feature that I definitely take for granted every day when listening on Spotify.
