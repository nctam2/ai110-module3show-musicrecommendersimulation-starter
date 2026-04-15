# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real world music recommenders like Spotify or Apple Music work by mixing a few different strategies at once. Collaborative filtering looks at what other listeners with similar taste have enjoyed, while content based filtering looks at the actual attributes of each song such as tempo, mood, and energy. On top of that, platforms pull in signals like skips, likes, playlist adds, session context, and even text from blogs and reviews to figure out what fits a listener's vibe. My version keeps things simple and focuses purely on the content based side. It treats each user as an average of the songs they already like, then scores every candidate song by how close its features are to that preference rather than just picking songs with the highest values. The priority is transparency and using a closeness idea of similarity, so a user who likes mellow lofi gets more mellow lofi back instead of whatever happens to have the biggest numbers.

### Algorithm Recipe

This is the current algorithm my system follows:

1. Load all the songs from `data/songs.csv` into a list.
2. Build the user profile by averaging the numeric features (energy, valence, danceability, acousticness, normalized tempo) across their liked songs, and collecting their liked genres and moods into sets.
3. For every song in the catalog:
   1. If its id is in the already heard list, skip it.
   2. Compute a closeness score for each numeric feature, which is just 1 minus the absolute difference between the song value and the user target. Closer to 1 means more similar.
   3. Check if the song's genre is in the user's liked genres. If yes, that piece of the score is 1, otherwise 0. Same idea for mood.
   4. Combine all of those into one weighted sum using the weights in `WEIGHTS`: genre and mood are worth 0.20 each, energy and valence 0.15 each, and danceability, acousticness, and tempo 0.10 each.
   5. Collect a few human readable reasons for why the song scored where it did (matched genre, close energy, etc.).
4. Sort all the scored songs from highest to lowest.
5. Return the top k (default 5) as the final ranking with their explanations.

### Potential Biases

A few things I expect could go sideways with this setup:

- Genre and mood together take up 0.40 of the total weight, so the system probably over prioritizes exact genre matches and might skip over a song that nails the user's vibe numerically but happens to be tagged under a different genre. A lofi listener might never see a chill jazz track even if the energy and acousticness line up perfectly.
- Because the user profile is built from averages, anyone with eclectic taste gets flattened into a mushy middle. If you like both super chill study music and high energy workout songs, the average lands somewhere in between and you end up with mid tempo stuff you probably do not actually want.
- The score rewards closeness, which means it keeps recommending more of the same. There is no diversity push, so you get stuck in a loop instead of discovering something new.
- The catalog itself is tiny and hand picked, so whatever genres happen to be overrepresented in the CSV will dominate results no matter what the user asks for.

**Song features used in the simulation:**

- `genre` (categorical, for example lofi, pop, rock)
- `mood` (categorical, for example chill, happy, intense)
- `energy` (numeric, 0 to 1)
- `valence` (numeric, 0 to 1, how positive the song feels)
- `danceability` (numeric, 0 to 1)
- `acousticness` (numeric, 0 to 1)
- `tempo_bpm` (numeric, normalized to 0 to 1 for scoring)

**UserProfile features used in the simulation:**

- Average `energy` across liked songs
- Average `valence` across liked songs
- Average `danceability` across liked songs
- Average `acousticness` across liked songs
- Average normalized `tempo` across liked songs
- Set of liked `genre` tags
- Set of liked `mood` tags
- List of already heard song ids (so the ranker can filter them out)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

