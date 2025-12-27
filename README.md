# word-cloud
implement a wordcloud generation as a vci project

## How it works (learn these skills from the https://s3.amazonaws.com/static.mrfeinberg.com/bv_ch03.pdf)
### 1. Finding words
When users upload a text file, we use a regular expression to find all the words.
### 2. Determine the script 
we use the Unicode Script property to determine which script each word belongs to.
### 3. Guessing the language and removing stop words
How to create the stop lists for each language?
select the most common words from a large corpus of text in that language.
How to guess the language of a text?
we can get the most frequent words(50) in the text, and compare their nums which is in the stop lists of different languages, and the most matched language is the guessed language.
### 4. weighting the words
we use the count of each word as its weight.
### 5. Weighted words into shapes

### 6. The playing field
create a space to place the words

### 7. Placing the words by a spiral
we use an Archimedean spiral to place the words.


### current status
```
I have basically implemented all the steps mentioned above.
We can upload a text file and generate a word cloud image.
And the word cloud image have different color.
And with different direction of words.
Different size of words.

Next step:
1. improve the performance of the code. such as using better data structure to speed up the placement of words.
2. improve the visual effect of the word cloud. such as better color scheme, better font selection.
   Better direction selection .
3. add a mask to let word cloud into a specific shape.
4. maybe a line except a word.
```