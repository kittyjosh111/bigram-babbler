### bigram-babbler

Simple text generator using the concept of bigrams to choose the next related word. How it works is that you first generate all bigrams for a tokenized piece of text, then you supply a starting word and how many words after that to generate.

For each word generated, all bigrams whose first word matches the selected word are chosen. They are then grouped by the second word in the bigram, and their proportions calculated. A random number is then generated, which determines what the next word in the text sequence will be.

A sample usage is to do the following:

- ```global_debug = True```: turns debug messages on.

- ```b = find_bigrams(tokenize("1984.txt"))```: selects the local file "1984.txt" to tokenize and generate bigrams for.

- ```generate("brother", b, 50)```: generate 50 words, starting from the word "brother". First argument is the beginning word, second argument is how many times to run the generator.

The generator function has caching included, so it should kind of help the program run faster.

Inspired by lab 10 / app 2 for STAT 133, and using DATA 8's datascience package as well as CS61A's lectures on recursion.

![Flowchart of the processes](/screenshots/diagram.png)
