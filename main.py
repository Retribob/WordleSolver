from collections import Counter

import string

STARTING_WORD = "SALET"


#read all valid wordle words
with open("valid_word_choices.txt") as f:
    word_choices = [line.strip().upper() for line in f if len(line.strip()) == 5]
print(len(word_choices), "words choices loaded")

with open("valid_word_answers.txt") as f:
    word_answers = [line.strip().upper() for line in f if len(line.strip()) == 5]
print(len(word_answers), "word answers loaded")

def play():

    #candidates is a list containing all remaining words after filtering from 
    #previous feedback
    candidates = word_answers
    choices = word_choices

    print(f"Your starting word is {STARTING_WORD}.\n")
    word = STARTING_WORD

    #input/output loop
    # give user input (feedback)
    # filter candidates based on feedback
    # provide next word guess
    while True:
        #the feedback list records the most recent results from the previous guess
        feedback = []

        result = input("The result of the word is: ")
        result = result.upper()
        if result == 'EXIT':
            break
        if result == 'GGGGG':
            print("You win!")
            break

        print(f"Your input is {result}")

        for i in range(len(word)):
            feedback.append((word[i], result[i]))

        candidates = filter_candidates(candidates, feedback)
        if not candidates:
            print("No candidates match that feedback — check your input and try again.")
            break

        word = guess_word(candidates, choices, feedback)
        print(f"Your next word is {word}")

def filter_candidates(candidates, feedback):
    filtered_candidates = []
    for word in candidates:
        valid_candidate = True
        letter_count = Counter(word)
        for i, (letter, status) in enumerate(feedback):
            if status == 'G':
                if word[i] != letter:
                    valid_candidate = False
                    break
                letter_count[letter] -= 1

        if not valid_candidate: continue

        for i, (letter, status) in enumerate(feedback):
            if status == 'Y':
                if word[i] == letter or letter_count[letter] <= 0:
                    valid_candidate = False
                    break
                letter_count[letter] -= 1

        if not valid_candidate: continue

        for i, (letter, status) in enumerate(feedback):
            if status == 'U' and letter_count[letter] > 0:
                valid_candidate = False
                break

        if not valid_candidate: continue

        if valid_candidate:
            filtered_candidates.append(word)

    print(len(filtered_candidates))
    return filtered_candidates


def guess_word(candidates, choices, feedback):
    if (len(candidates) == 1): return candidates[0]

    frequency = count_letters(candidates)
    word_score = {}

    for (letter, status) in feedback:
        if status == 'G' or status == 'Y':
            frequency[letter] -= len(candidates)

    for word in choices:
        score = 0
        letter_count = Counter(word)
        for letter in letter_count:
            score += frequency[letter]
        word_score[word] = score

    sorted_word_score = dict(sorted(word_score.items(), key=lambda item: item[1], reverse=True))
    return next(iter(sorted_word_score))            


def count_letters(candidates):
    frequency = {letter: 0 for letter in string.ascii_uppercase}
    
    for word in candidates:
        for letter in word:
            frequency[letter] += 1

    return frequency

if __name__ == "__main__":
    play()