# python main.py or python main.py --file input.txt
from src.input import get_user_input,find,remove ,compute_weights
from utils.style import select_font_sizes,create_canvas
from src.layout import layout 


def main():
    # first get user input
    user_input = get_user_input()

    #print("User Input Received:")
    #print(user_input)

    # second process the input 
    processed_input = find(user_input)

    # print("Processed Input:")
    # for word in processed_input:
    #     print(word)

    # remove words like 'the', 'is', 'and' or self-defined to_remove list
    to_remove = ['the', 'is', 'and', 'a', 'an', 'in', 'on', 'at', 'of', 'for', 'to', 'with']
    filtered_words = remove(processed_input, to_remove)

    # next, compute the weights
    counts, total = compute_weights(filtered_words)
    weights = {word: count / total for word,count in counts.items()}
    # print("Word Weights:")
    # for word, count in counts.items():
    #     print(f"{word}: {count} ({count/total:.2%})")

    # next, judge the font size or color based on the weights

    font_sizes = select_font_sizes(weights, min_size=20, max_size=85)
    # print("Font Sizes:")
    # for word, size in font_sizes.items():
    #     print(f"{word}: {size}")

    # next, generate special canvas or area to draw the words (we can use the canvas we like)
    canvas = create_canvas(width=2000, height=1600, color=(255, 255, 255), file_path=None,threshold=50)
    #print("Canvas created.")
    # canvas.show()

    # next, place the words on the canvas based on the spiral pattern
    layout_words = {}  # word: (x, y, font_size)
    layout(canvas, layout_words, font_sizes,padding=7,min_size=20,max_size=85)

    # finally, output the result 
    canvas.show()
    # canvas.save("word_cloud_output.png")

if __name__ == "__main__":
    main()