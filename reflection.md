# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked functional on the surface but had several clear bugs. The sidebar showed "Attempts allowed: 8" for Normal difficulty, but the actual number of attempts the player received was also 8 — the display was correct but the attempts counter started at 1 instead of 0, meaning the player effectively lost one attempt immediately without doing anything.

The hints were completely backwards. If the secret number was 68 and I guessed 50 (which is lower), the game told me to "Go LOWER" — the opposite of what it should say. Similarly, guessing 70 (which is higher than 68) showed "Go HIGHER" instead of "Go LOWER." This made the game unwinnable through normal play.

The game also had no input validation on the range. Even though the range was supposed to be 1–100, I could type numbers like 500 or -10 and the game would just respond with higher/lower feedback instead of rejecting the input. Finally, clicking "New Game" did not properly restart the game — the old secret number and state carried over, so a fresh game was not actually starting.

---

## 2. How did you use AI as a teammate?

I used **Claude Code (Anthropic)** as my primary AI assistant throughout this project.

**Correct suggestion — fixing the score deduction logic:**
I described the intended scoring rule to the AI: award 100 points for a first-attempt correct guess, and deduct `int(100 / attempt_limit)` for each wrong guess before winning. The AI correctly identified that the original `update_score` function was using a difficulty rank (Easy=1, Normal=2, Hard=3) as the divisor, which caused Normal mode to deduct 50 points per wrong guess instead of the correct 16. It rewrote the function using `ATTEMPT_LIMIT = {"Easy": 8, "Normal": 6, "Hard": 5}` as the divisor. I verified this by playing the game on Normal difficulty, guessing wrong once, then winning — the final score was 84 (100 − 16), which matched the expected result exactly.

**Incorrect/misleading suggestion — first attempt at the score divisor:**
In its first pass, the AI introduced `DIFFICULTY_LEVEL = {"Easy": 1, "Normal": 2, "Hard": 3}` and divided 100 by that rank. This produced a 50-point deduction per wrong guess on Normal, which was wrong. I caught this by playing the game: after one wrong guess on Normal, winning gave only 50 points instead of the expected 84. I reported the result back to the AI, explained the correct formula (`100 / attempt_limit`), and it corrected the divisor to use the actual attempt counts.

---

## 3. Debugging and testing your fixes

I decided a bug was truly fixed only after both a manual play-through and a passing pytest run confirmed the expected behavior.

**Manual test — score calculation:** I opened the app on Normal difficulty (attempt limit = 6), intentionally guessed wrong once, then guessed the correct number. Before the fix the final score showed 50; after the fix it showed 84 (`100 − 1 × 16`). I repeated this on Easy (expected 88) and Hard (expected 80) to confirm all three difficulty branches were correct.

**Automated test — `test_normal_second_attempt_deducts_16_not_50`:** This pytest case in `tests/test_game_logic.py` calls `_update_score(0, "Win", attempt_number=2, difficulty="Normal")` and asserts the result equals 84. Before the fix this test would have returned 50 and failed, directly pinpointing the broken line. After the fix all 12 tests passed (`pytest tests/test_game_logic.py -v`).

The AI helped design the regression suite by suggesting specific boundary cases: first-attempt baseline (100 pts), the exact broken scenario (second attempt on Normal), score floor at 0, and confirming that wrong guesses should not alter the score mid-game.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
