# this file is to handle user input for the next weight compute
def get_user_input(arg):
    # we will handle two kinds of input: 
    # 1. user input from command line 
    # 2. user input fro a file 
    # if python main.py --file input.txt , we will read from input.txt
    # else we will read from command line

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


def find(user_input,line_mode=False):
    # find all the word in the user input
    # first convert to downcase
    user_input = user_input.lower()
    import re
    # pattern = r"[\u4e00-\u9fff]+|[a-zA-Z]+(?:['-][a-zA-Z]+)*"
    # at fisrt we just handle simple words (just english letters)
    # pattern = r"\b\w+\b"
    # if we want to handle can't or it's , we can use this pattern
    # now maybe we can get all line as a word
    if line_mode:
        pattern = r".+"
    else:
        pattern = r"\b\w+(?:'\w+)?\b"
    words = re.findall(pattern, user_input)
    # for word in words:
    #     print(word)
    return words

def remove(words, to_remove):
    # remove the words in to_remove from words
    filtered_words = [word for word in words if word not in to_remove]
    return filtered_words

def compute_counts(words,max_num):
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
    # limit the number of words to max_num
    if len(sorted_counter) > max_num:
        sorted_counter = dict(list(sorted_counter.items())[:max_num])
        # recompute total
        total = sum(sorted_counter.values())
    return sorted_counter, total

# in this function, we compute the weights of each word
# not only think about the frequency, but also the length of the word, the emotional weight, etc.
def count_positive_words(word):
    # a simple positive word list
    positive_words = ['good', 'great', 'excellent', 'happy', 'joy', 'love', 'wonderful', 'amazing', 'fantastic', 'positive']
    counts = 0
    for pw in positive_words:
        if pw in word:
            counts += 1
    return counts
def count_negative_words(word):
    # a simple negative word list
    negative_words = ['bad', '不如','terrible', 'awful', 'sad', 'hate', 'horrible', 'negative', 'worst', 'angry', 'disappointing']
    counts = 0
    for nw in negative_words:
        if nw in word:
            counts += 10
    return counts

def compute_weights(counts,total):
    weights = {}
    for word, count in counts.items():
        length_weight = len(word) / 100
        sentiment_weight = (count_positive_words(word) - count_negative_words(word)) / 10
        frequency_weight = count / total
        weight = frequency_weight + 0.5*length_weight + 0.3*sentiment_weight
        weights[word] = max(weight, 0.001)  # ensure weight is positive
    return weights




