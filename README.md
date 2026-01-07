# word-cloud
## implement a wordcloud generation as a vci project

## You should know although python has a wordcloud library, no one has lanuched a wordcloud generation from scratch with python in github, heihei.

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

### current status
```
1. rewrite the data structure of the board to speed up the placement of words.
   now, we use a list of integers to represent each row of the board and word sprite.
   And we use bitwise operations to check the placement of words.
2. add a mask to let word cloud into a specific shape.
3. use the Impact font to make the word cloud more stylish.
4. adjust the size range of words from smooth distribution to layered distribution to make the word cloud more visually.
5. adjust the angle selection use layered distribution with random selection.
6. adjust the color selection with fixed color scheme.
7. don't forget we solve the problem of bbox and anchor in PIL draw.text function.

to do list:
1. maybe can use the mask corrsponding to the text topic. such as heart shape for love text. basically done,but just for testing now.
2. not only use the frequency of words to determine the size, maybe can add sentiment analysis to determine the size.already done something(frequency,length,emothion weights), but the emotion list is not good enough and the percent of three weights need further adjustment.
3. maybe can add a line except a word. already done, notice to use Arial Unicode font, the Impact font doesn't support Chinese characters.
4. besides download some files, can also get them from internet.
5. maybe a ui ? （streamlit?）
And 1-4 is related to the input text, so let's start.
By the way,I added a --max_num argument to limit the number of words in the word cloud.
```