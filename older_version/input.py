# this file is to handle user input for the next weight compute
def get_user_input():
    # we will handle two kinds of input: 
    # 1. user input from command line 
    # 2. user input fro a file 
    # if python main.py --file input.txt , we will read from input.txt
    # else we will read from command line
    import argparse
    parser = argparse.ArgumentParser(description='Process some input.')
    parser.add_argument('--file', type=str, help='Input file path')
    arg = parser.parse_args()
    if arg.file:
        with open(arg.file, 'r') as f:
            text = f.read()
    else:
        text = input("Please enter the input:\n")
        # multi-line input until EOF
        while True:
            try:
                line = input()
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            text += '\n' + line
    return text


def find(user_input):
    # find all the word in the user input
    # first convert to downcase
    user_input = user_input.lower()
    import re
    # pattern = r"[\u4e00-\u9fff]+|[a-zA-Z]+(?:['-][a-zA-Z]+)*"
    # at fisrt we just handle simple words (just english letters)
    # pattern = r"\b\w+\b"
    # if we want to handle can't or it's , we can use this pattern
    pattern = r"\b\w+(?:'\w+)?\b"
    words = re.findall(pattern, user_input)

    return words

def remove(words, to_remove):
    # remove the words in to_remove from words
    filtered_words = [word for word in words if word not in to_remove]
    return filtered_words

def compute_weights(words):
    # compute the weights of each word
    counter = {}
    total = len(words)
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1
    # sort the counter by value
    sorted_counter = dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))
    return sorted_counter, total
