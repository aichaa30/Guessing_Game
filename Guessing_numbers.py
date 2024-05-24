import random
import json

HIGH_SCORES_FILE = 'high_scores.json'

def generate_secret_code(difficulty):
    """Generate a list of random numbers based on the selected difficulty level."""
    length = 3 if difficulty == 'easy' else 4 if difficulty == 'medium' else 5
    return [random.randint(1, 9) for i in range(length)]

def get_user_guesses(length):
    """Prompt the user to guess numbers based on the secret code length and return the guesses as a list."""
    while True:
        try:
            guesses = [int(input(f"Guess number {i + 1} (between 1 and 9): ")) for i in range(length)]
            if all(1 <= guess <= 9 for guess in guesses):
                return guesses
            else:
                print("All numbers must be between 1 and 9. Try again.")
        except ValueError:
            print("Invalid input. Please enter integers only. Try again.")

def compare_guesses(secret_code, user_guesses):
    """Compare user guesses with the secret code and return the number of correct guesses."""
    correct = sum(1 for secret_digit, user_digit in zip(secret_code, user_guesses) if secret_digit == user_digit)
    for i, (secret_digit, user_digit) in enumerate(zip(secret_code, user_guesses)):
        if secret_digit == user_digit:
            print(f"You got the {i + 1} number right!")
        else:
            print(f"You didn't get the {i + 1} number right.")
    return correct

def calculate_score(tries, difficulty):
    """Calculate score based on the number of tries and difficulty level."""
    base_score = 100
    difficulty_multiplier = {'easy': 1, 'medium': 1.5, 'hard': 2}
    return max(base_score - (tries * 10) * difficulty_multiplier[difficulty], 0)

def load_high_scores():
    """Load high scores from a file."""
    try:
        with open(HIGH_SCORES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_high_scores(high_scores):
    """Save high scores to a file."""
    with open(HIGH_SCORES_FILE, 'w') as file:
        json.dump(high_scores, file)

def display_high_scores(high_scores):
    """Display the high scores."""
    if not high_scores:
        print("No high scores yet!")
    else:
        print("High Scores:")
        for score in high_scores:
            print(f"{score['name']} - {score['score']} (Difficulty: {score['difficulty']}, Tries: {score['tries']})")

def play_game():
    """Main function to play the guessing game."""
    print("Hello, Welcome to the game of guesses!")
    player_name = input("What is your name? ")
    ask_player = input(f"Hi, {player_name}, would you like to play the guessing game? (Enter Yes/No) ").strip().lower()

    if ask_player != 'yes':
        print("Oh Okay, have a good one! :(")
        return

    difficulty = input("Choose difficulty level (easy/medium/hard): ").strip().lower()
    while difficulty not in ['easy', 'medium', 'hard']:
        print("Invalid choice. Please select 'easy', 'medium', or 'hard'.")
        difficulty = input("Choose difficulty level (easy/medium/hard): ").strip().lower()

    secret_code = generate_secret_code(difficulty)
    tries = 0
    correct = 0
    code_length = len(secret_code)

    while correct != code_length:
        user_guesses = get_user_guesses(code_length)
        correct = compare_guesses(secret_code, user_guesses)
        tries += 1
        print(f"Tries: {tries}")

    score = calculate_score(tries, difficulty)
    print(f"Congratulations, {player_name}! It took you {tries} tries to guess the secret code. Your score is {score}.")

    high_scores = load_high_scores()
    high_scores.append({'name': player_name, 'score': score, 'difficulty': difficulty, 'tries': tries})
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    save_high_scores(high_scores)

    display_high_scores(high_scores)

if __name__ == "__main__":
    play_game()
