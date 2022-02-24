import random
import math

BLACK = "⬛"
GREEN = "🟩"
YELLOW = "🟨"

WORDLE_WORDS = set(open("wordle_words.txt", "r").read().split())
VALID_WORDS = set(open("valid_words.txt", "r").read().split())

class Wordle_Game:
    def __init__(self, word):
        self.word = word
        #        self.valid_words = valid_words
    def guess(self, guess):
        #if not guess in self.valid_words:
        #    return "Not a valid words"
        answer = [BLACK] * 5
        letter_dict = {}
        for i in range(5):
            try:
                if guess[i] == self.word[i]:
                    answer[i] = GREEN
                else:
                    letter_dict[self.word[i]] = letter_dict.get(self.word[i], 0) + 1
            except IndexError:
                print(i, guess, self.word)

        for i in range(5):
            if answer[i] == GREEN: continue
            guess_letter = guess[i]
            if letter_dict.get(guess_letter, 0) > 0:
                answer[i] = YELLOW
                letter_dict[guess_letter] = letter_dict.get(guess_letter, 0) - 1
        return answer

possible_results = []
options = [GREEN, YELLOW, BLACK]
for i in range(3):
    for j in range(3):
        for k in range(3):
            for l in range(3):
                for m in range(3):
                    possible_results.append([options[i], options[j], options[k], options[l], options[m]])


def get_words_matching(guess_word, guess_result, probability_space):
    new_probability_space = set()
    for word in probability_space:
        broke = False
        for i in range(5):
            letter = guess_word[i]
            if guess_result[i] == GREEN and word[i] != guess_word[i]:
                broke = True
                break
            if guess_result[i] == YELLOW:
                # find number of yellow flags for current letter
                yellow_flags = 0
                for letter_index in range(len(guess_word)):
                    if guess_word[letter_index] == letter and guess_result[i] == YELLOW:
                        yellow_flags += 1
                if word.count(letter) > yellow_flags:
                    broke = True
                if word[i] == guess_word[i]:
                    broke = True
            if guess_result[i] == BLACK and word.count(letter) >= guess_word.count(letter):
                broke = True
                break
        if not broke:
            new_probability_space.add(word)
    return new_probability_space

def get_entropy_of_word(word, probability_space):
    entropy = 0
    for possible_result in possible_results:
        num_word_matching = len(get_words_matching(word, possible_result, probability_space))
        if num_word_matching != 0:
            probability = num_word_matching / len(probability_space)
            entropy += probability * math.log2(1/probability) 

    return entropy

def simulate(starting_word):
    probability_space = WORDLE_WORDS
    game = Wordle_Game(starting_word)
    next_word = "tares"
    i = 1
    while len(probability_space) > 1:
        result = game.guess(next_word)
        """
        for result_index in range(len(result)):
            result[result_index] = {
                "G": GREEN,
                "Y": YELLOW,
                "B": BLACK,
            }[result[result_index]]
        """
        if result == [GREEN] * 5:
            return i
            #print("Solved in", i+1, "move(s)")
        probability_space = get_words_matching(next_word, result, probability_space)

        max_entropy = 0
        max_entropy_word = ""
        for word in probability_space:
            entropy = get_entropy_of_word(word, probability_space)
            if entropy > max_entropy:
                max_entropy = entropy
                max_entropy_word = word
        next_word = max_entropy_word
        i += 1
    return i

"""
total = 0
iterations = 1000
successful = 0
WORDLE_WORDS_LIST = list(WORDLE_WORDS)
for i in range(iterations):
    choice = random.choice(WORDLE_WORDS_LIST)
    score = simulate(choice)
    if score > 0:
        successful += 1
        total += score 
    else:
        print(choice)
    print("Simulating #" + str(i+1))
print("Score", total/successful)
print("Success Rate:", successful, "out of", iterations)
"""
