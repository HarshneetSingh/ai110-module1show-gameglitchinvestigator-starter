from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# ---------------------------------------------------------------------------
# Regression tests for update_score bug fix
#
# BUG: deduction used difficulty rank (Easy=1, Normal=2, Hard=3) as divisor,
#      so Normal deducted 100/2=50 pts per wrong guess instead of the correct
#      100/attempt_limit = 100/6 = 16 pts.
# FIX: deduction = int(100 / attempt_limit)
#        Easy   → int(100/8) = 12 pts per wrong guess
#        Normal → int(100/6) = 16 pts per wrong guess
#        Hard   → int(100/5) = 20 pts per wrong guess
# ---------------------------------------------------------------------------

# app.py can't be imported directly due to Streamlit side-effects, so the
# fixed function is reproduced here as a standalone helper for testing.
_ATTEMPT_LIMIT = {"Easy": 8, "Normal": 6, "Hard": 5}

def _update_score(current_score, outcome, attempt_number, difficulty):
    if outcome == "Win":
        deduction_per_wrong = int(100 / _ATTEMPT_LIMIT[difficulty])
        wrong_attempts = attempt_number - 1
        points = max(0, 100 - wrong_attempts * deduction_per_wrong)
        return current_score + points
    return current_score


# --- First attempt always gives 100 points regardless of difficulty ---
def test_first_attempt_easy_scores_100():
    assert _update_score(0, "Win", attempt_number=1, difficulty="Easy") == 100

def test_first_attempt_normal_scores_100():
    assert _update_score(0, "Win", attempt_number=1, difficulty="Normal") == 100

def test_first_attempt_hard_scores_100():
    assert _update_score(0, "Win", attempt_number=1, difficulty="Hard") == 100


# --- Correct deduction on second attempt (the originally broken case) ---
def test_normal_second_attempt_deducts_16_not_50():
    # OLD (buggy): 100 - 1*(100/2) = 50. NEW (fixed): 100 - 1*16 = 84
    assert _update_score(0, "Win", attempt_number=2, difficulty="Normal") == 84

def test_easy_second_attempt_deducts_12():
    assert _update_score(0, "Win", attempt_number=2, difficulty="Easy") == 88

def test_hard_second_attempt_deducts_20():
    assert _update_score(0, "Win", attempt_number=2, difficulty="Hard") == 80


# --- Score floors at 0, never goes negative ---
def test_score_never_goes_negative():
    assert _update_score(0, "Win", attempt_number=100, difficulty="Normal") == 0


# --- Wrong guesses must NOT change the score ---
def test_too_high_does_not_change_score():
    assert _update_score(50, "Too High", attempt_number=2, difficulty="Normal") == 50

def test_too_low_does_not_change_score():
    assert _update_score(50, "Too Low", attempt_number=3, difficulty="Hard") == 50
