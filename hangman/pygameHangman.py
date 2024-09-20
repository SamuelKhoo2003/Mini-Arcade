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

def play(word):
    pygame.init()
    width, height = 800, 600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hangman")

    hang_man_images = [pygame.image.load(f"hangman\hangman_img\{i}.jpg") for i in range(11)]

    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 11
    guessed_correctly = set()

    font = pygame.font.SysFont('arial', 36)

    def draw():
        win.fill((255, 255, 255))
        win.blit(hang_man_images[11-tries], (150, 100))
        display_word = " ".join([char if char in guessed_correctly else "_" for char in word])
        text = font.render(display_word, True, (0, 0, 0))
        win.blit(text, (400, 200))

        guessed_text = font.render("Guessed Letters: " + " ".join(guessed_letters), True, (0, 0, 0))
        win.blit(guessed_text, (150, 500))

        pygame.display.update()

    run = True
    while not guessed and tries > 0 and run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                guess = pygame.key.name(event.key).upper()

                # Handle letter guesses
                if len(guess) == 1 and guess.isalpha():
                    if guess in guessed_letters:
                        print(f"You already guessed the letter {guess}")
                    elif guess not in word:
                        guessed_letters.append(guess)
                        tries -= 1
                        print(f"{guess} is not in the word.")
                    else:
                        guessed_letters.append(guess)
                        guessed_correctly.add(guess)
                        print(f"{guess} is in the word!")
                        if all([char in guessed_correctly for char in word]):
                            guessed = True

                # Handle full word guess
                elif len(guess) == len(word) and guess.isalpha():
                    if guess in guessed_words:
                        print(f"You have already guessed the word {guess}")
                    elif guess != word:
                        guessed_words.append(guess)
                        tries -= 1
                        print(f"{guess} is not the word.")
                    else:
                        guessed = True
                        word_completion = word

        # Check if player won or lost
        if guessed:
            print(f"Congrats! You've guessed the word: {word}")
        elif tries == 0:
            print(f"Sorry, you lost! The word was {word}.")

    pygame.quit()

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