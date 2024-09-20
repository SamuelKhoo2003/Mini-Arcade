# for now we are using a wordList.py but could also use an API for a random word
import random
from wordList import word_list

def get_word():
    # Could implement using an API for V2
    word = random.choice(word_list)
    return word.upper()

def play(word):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    print("Let's play Hangman!")
    print(displayHangman(tries)) # this function is what displays the hang man
    print(word_completion)
    print("\n")
    while not guessed and tries > 0:
        guess = input("Please guess a letter or a word: ").upper()
        if len(guess) == 1 and guess.isalpha:
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                guessed_letters.append(guess)
                tries -= 1
                print(guess, "is not in the word.")
            else:
                guessed_letters.append(guess)
                print(guess, "is in the word!")
                word_as_list = list(word_completion)
                for i, char in enumerate(word):
                    if char == guess:
                        word_as_list[i] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True

        elif len(guess) == len(word) and guess.isalpha:
            if guess in guessed_words:
                print("You have already guessed the word", guess)
            elif guess != word:
                guessed_words.append(guess)
                tries -= 1
                print(guess, "is not the word.")
            else:
                guess = True
                word_completion = word
        else:
            print("Not a valid guess.")

        print(displayHangman(tries)) # this function is what displays the hang man
        print(word_completion)
        print("\n")

    if guessed:
        print("You guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")

def displayHangman(numTries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[numTries]

def main():
    word = get_word()
    play(word)
    while input("Play Again? (Y/N) ").upper() == "Y":
        word = get_word()
        play(word)
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
