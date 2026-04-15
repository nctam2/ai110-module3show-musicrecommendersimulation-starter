# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias

The catalog has 24 songs, which is the biggest limitation on its own. Any recommender is only as good as the pool it picks from, and with this small a pool the system can run out of real matches fast. A concrete example: the `focused` mood only shows up on one song (Focus Flow), so a user whose taste leans toward focus music gets exactly one genuine mood match and four numeric-proximity songs dressed up to look similar. Rock is in the same spot with just one track in the catalog.

The closeness scoring has no diversity push built in. Once the system finds a song that nails a user's profile, the next best results tend to be near-duplicates of the first one, so the top 5 feels like variations on a theme instead of a range of options. Genre and mood together hold 0.40 of the total weight, which acts as a soft cap on how much a numerically-perfect song from another genre can climb. That came out clearly in the adversarial-conflicting profile, where a sad-tagged indie folk track got beaten by edm intense tracks that had both the genre match and the strong energy numbers in their favor.

Finally, the user profile is built by averaging the features of a user's liked songs. Anyone with eclectic taste, say both high-energy workout music and low-energy study music, gets flattened into a mushy middle that does not match either cluster they actually like. The system treats every user as if their preferences live in one spot, which is not how taste actually works.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
