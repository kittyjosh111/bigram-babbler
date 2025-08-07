### bigram-babbler

Simple text generator using the concept of bigrams to choose the next related word. How it works is that you first generate all bigrams for a tokenized piece of text, then you supply a starting word and how many words after that to generate.

For each word generated, all bigrams whose first word matches the selected word are chosen. They are then grouped by the second word in the bigram, and their proportions calculated. A random number is then generated, which determines what the next word in the text sequence will be.

#### installation

Dependencies are in ```requirements.txt```. I suggest setting up a virtual environment to use, then running ```pip install -r requirements.txt```.

If you want to use the flask app, you'll also need to install flask. There is an additional ```requirements.txt``` inside the flask-app folder, just in case.

For any use-case, you'll also need a txt file for the script to read and generate bigrams from. Place it somewhere the script can read.

#### python script usage

A sample usage is to do the following:

- ```b = find_bigrams(tokenize("1984.txt"), debug=True)```: selects the local file "1984.txt" to tokenize and generate bigrams for.

- ```generate("brother", b, 50, debug=True)```: generate 50 words, starting from the word "brother". First argument is the beginning word, second argument is how many times to run the generator.

The generator function has caching included, so it should kind of help the program run faster.

If you don't want to have debug messages, don't supply the debug argument as shown above. It defaults to False, so debug messages won't be printed unless you specifically set the argument to True.

#### flask app usage

1. COPY bigram_babbler.py into the flask-app folder.

2. Find a source of text and replace the empty ```source.txt``` already inside the flask-app folder. Make sure that the replacement txt file is also named ```source.txt```.

3. Run ```app.py``` in a terminal, or however you choose to start flask apps.

---

Inspired by lab 10 / app 2 for STAT 133, and using DATA 8's datascience package as well as CS61A's lectures on recursion.

![Flowchart of the processes](https://raw.githubusercontent.com/kittyjosh111/bigram-babbler/refs/heads/main/screenshot/diagram.png)
