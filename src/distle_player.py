from edit_dist_utils import *
import random

class DistlePlayer:
    '''
    AI Distle Player! Contains all of the logic to automagically play
    the game of Distle with frightening accuracy (hopefully)
    '''
    
    def start_new_game(self, dictionary: set[str], max_guesses: int) -> None:
        '''
        Initializes and sets up the game for a new session.

        Parameters:
        - dictionary (set[str]): The set of valid words to use in the game.
        - max_guesses (int): The maximum number of guesses allowed in the game.

        This method:
        1. Stores a copy of the dictionary for gameplay, allowing modifications without altering the original dictionary.
        2. Calculates the most common word length within the dictionary.
        3. Identifies words that match this common length to focus the game on a typical word size.
        4. Counts the frequency of each letter within these words of the common length.
        5. Determines the most frequently occurring letters up to the common word length.
        6. Finds words of the common length that contain all these frequent letters.
        7. Selects a starting word for the game based on these criteria. If no words contain all frequent letters, a random word of the common length is chosen.

        Attributes Set:
        - dictionary (set[str]): The provided dictionary of words for the game.
        - new_dict (set[str]): A modifiable copy of the dictionary to be used in each game.
        - total_guesses (int): Tracks the current number of guesses made, initialized to 0.
        - first_match (str): The initial word guess, chosen based on common letter and length criteria.
        '''
        self.dictionary: set[str] = dictionary
        self.new_dict: set[str] = dictionary
        self.total_guesses: int = 0

        # Gets the lengths of every word
        length_counts: dict[int, int] = {}
        for word in self.dictionary:
            length = len(word)
            if length in length_counts:
                length_counts[length] += 1
            else:
                length_counts[length] = 1

        # Gets the most common length of the words
        most_common_length = 0
        highest_count = 0
        for length, count in length_counts.items():
            if count > highest_count:
                most_common_length = length
                highest_count = count

        matching_words = [word for word in self.dictionary if len(word) == most_common_length]

        # Gets the number of times every letter is used
        letter_counts: dict[str, int] = {}
        for word in matching_words:
            for letter in word:
                if letter in letter_counts:
                    letter_counts[letter] += 1
                else:
                    letter_counts[letter] = 1
                    
        # Finds the x most common letters, x being the most common number of letters of the words      
        sorted_letter_counts = sorted(letter_counts.items(), key=lambda item: item[1], reverse=True)
        common_letters = [letter for letter, _ in sorted_letter_counts[:most_common_length]]

        # Finds every word using the most common letters with the most common length
        best_words = [word for word in matching_words if all(letter in word for letter in common_letters)]

        self.first_match = random.choice(best_words) if best_words else random.choice(matching_words)

        
    
    def make_guess(self) -> str:
        '''
        Requests a new guess to be made by the agent in the current game of Distle.
        Uses only the DistlePlayer's attributes that had been originally initialized
        in the start_new_game method.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Returns:
            str:
                The next guessed word from this DistlePlayer
        '''
        # Gets best first word at the beginning, after chooses a random word from the updated list
        if self.total_guesses == 0:
            self.total_guesses += 1
            return self.first_match
        else:
            self.total_guesses += 1
            return random.choice(list(self.dictionary))
   

    def get_feedback(self, guess: str, edit_dist: int, transforms: list[str]) -> None:
        '''
        Called by the DistleGame after the DistlePlayer has made an incorrect guess.
        The feedback furnished is described in the parameters below. Your agent will
        use this feedback in an attempt to rule out as many remaining possible guess
        words as it can, through which it can then make better guesses in make_guess.
        
        [!] You will never call this method yourself, it will be called for you by
        the DistleGame that is running.
        
        Parameters:
            guess (str):
                The last, incorrect guess made by this DistlePlayer
            edit_distance (int):
                The numerical edit distance between the guess your agent made and the
                secret word
            transforms (list[str]):
                The list of top-down transforms needed to turn the guess word into the
                secret word, i.e., the transforms that would be returned by your
                get_transformation_list(guess, secret_word)
        '''
        # Removes all words that do not have same transformations from the initial guess
        self.dictionary = {word for word in self.dictionary if transforms == get_transformation_list(guess, word)}
        return