def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")

# FIX: The stub raised NotImplementedError. I asked the AI to implement check_guess
# so the starter tests would pass. The AI ported the comparison logic from app.py
# and simplified it to return just the outcome string (no message tuple), matching
# what the existing tests assert.
def check_guess(guess, secret):
    """
    Compare guess to secret and return outcome string.

    outcome: "Win", "Too High", or "Too Low"
    """
    try:
        if guess == secret:
            return "Win"
        if guess > secret:
            return "Too High"
        return "Too Low"
    except TypeError:
        if guess == int(secret):
            return "Win"
        if guess > int(secret):
            return "Too High"
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    raise NotImplementedError("Refactor this function from app.py into logic_utils.py")
