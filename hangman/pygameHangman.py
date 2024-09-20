import pygame
import random
import requests

def get_word(difficulty):
    response = requests.get('https://random-word-api.herokuapp.com/word?number=10')
    if response.status_code == 200:
        words = response.json()
        if difficulty == "EASY":
            word_list = [word for word in words if len(word) < 6]
        elif difficulty == "MEDIUM":
            word_list = [word for word in words if 6 <= len(word) < 9]
        elif difficulty == "HARD":
            word_list = [word for word in words if len(word) >= 9]
        if word_list:
            return random.choice(word_list).upper()
    else:
        print("API request failed. Using default word.")
    return "PYTHON"

def choose_difficulty():
    while True:
        choose_difficulty = input("Choose difficulty (easy, medium, hard): ").upper()
        if choose_difficulty in ["EASY", "MEDIUM", "HARD"]:
            return choose_difficulty
        else:
            print("Invalid difficulty. Please enter easy, medium, or hard.")

def run_game():
    difficulty = choose_difficulty()
    word = get_word(difficulty)
    play(word)

def main():
    run_game()
    while input("Play Again? (Y/N) ").upper() == "Y":
        run_game()
    print("Thanks for playing!")

if __name__ == "__main__":
    main()