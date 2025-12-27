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