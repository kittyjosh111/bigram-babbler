# First tokenize, then generate bigrams, then count / get proportions per start word
from datascience import *
import re
import numpy as np
import random

## Sample usage:
## b = find_bigrams(tokenize("1984.txt"))
## generate("brother", b, 50)

def tokenize(filename):
  """funtion to tokenize text from a given file named FILENAME.
  for our cases, tokenize = split by word basically.
  Returns an array of tokens."""
  with open(filename) as read:
    not_tokenized = read.read()
  not_tokenized = not_tokenized.lower().replace("\n", ' ') #make all lowercase, remove newlines
  not_tokenized = re.sub(r'[^a-zA-Z0-9. \-]+', '', not_tokenized) #remove symbols
  tokens = not_tokenized.split() #split by word
  return np.array(tokens) #store them all into an array

def find_bigrams(token_array, debug=False):
  """Function to find / make bigrams given an array of tokens TOKEN_ARRAY.
  Returns a table with cols 'Word 1' and 'Word 2'"""
  word1_list = [] #bigrams are goupings of two words. So we want a word 1...
  word2_list = [] #...and a word 2
  for i in range(len(token_array) - 2):
    word1 = token_array[i] #this goes one by one through all the words to generate bigrams
    word2 = token_array[i+1]
    word1_list.append(word1) #and here to store
    word2_list.append(word2)
  bigram_table = Table().with_columns(
    "Word 1", np.array(word1_list),
    "Word 2", np.array(word2_list) #tables are easier to work with
  )
  if debug:
    print(f"[DEBUG]: find_bigrams output:\n{bigram_table}")
  return bigram_table

def bigram_count(search_word, bigram_table):
  """Function to find the bigrams that start with SEARCH_WORD, then sorts by appearance count
  Returns a table with the Word 2, rng_min, rng_max columns. Use the rng cols to determine which Word 2 to choose"""
  filtered_table = bigram_table.where("Word 1", search_word) #first we filter by first word
  grouped_table = filtered_table.group("Word 2").sort("count", descending=True) #since word 1 is the same, group by word 2
  rng_max_array = make_array() #i cant just append list/arrays with np.append. cringe
  rng_min_array = make_array()
  count_counter = 1 #start from 1, end on the sum of all counts
  for i in range(grouped_table.num_rows):
    new_max = grouped_table.column("count")[i] #our new maximum
    rng_max_array = np.append(rng_max_array, count_counter + new_max - 1)
    rng_min_array = np.append(rng_min_array, count_counter) #and our old minimum
    count_counter += new_max
  grouped_table = grouped_table.with_columns("rng_min", rng_min_array, "rng_max", rng_max_array)
  return grouped_table

def make_sentences(word_list):
  """Function to make sentences out of words in a list. Assumes there are words with periods attached to them."""
  capitalize_next = True #first word should be capital
  sentence_out = "" #begin building our sentences to return
  for this_word in word_list:
    if this_word.endswith('.'): #marks the end of a sentence...
      capitalize_next = True #...so next word has to be capital
    else:
      if capitalize_next == True:
        this_word = this_word.capitalize() #like so
        capitalize_next = False #then reset the toggle
    sentence_out += f"{this_word} " #add spaces
  sentence_out = sentence_out[:-1] + "." #remove last space, replace with period
  return sentence_out

def generate(word, found_bigram_table, n, word_list=False, cache=False, debug=False):
  """Function that takes in a word, then looks at a table of sorted bigrams, and generates a next word.
  Continues N times recursively"""
  word = word.lower() #since our bigram stuff used all lowercase, do the same
  if word_list == False:
    word_list = [] #should be false by default
  if cache == False:
    cache = {} #and you too
  if n <= 0:
    return make_sentences(word_list) #based cased
  else: #take the recursive leap of faith!
    word_list.append(word) #so we can print it all in the end
    if word in cache: #check if we saved the computation
      if debug:
        print(f"[DEBUG]: cache for '{word}' found in generate(). Skipping bigram_count call...")
      bigram_table = cache[word]
    else:
      bigram_table = bigram_count(word, found_bigram_table)
      cache[word] = bigram_table #and then just save it to cache
    total_counts = sum(bigram_table.column("count"))
    if total_counts <= 0:
      print(f"[ERROR]: bigrams could not be generated for the word: {word}")
      return word_list
    rng_int = random.randint(1, total_counts)
    for i_row in range(bigram_table.num_rows):  #ok i bet theres a better algo for this, but whatev
      rng_min = int(bigram_table.row(i_row)[2])
      rng_max = int(bigram_table.row(i_row)[3])
      if rng_int >= rng_min and rng_int <= rng_max:
        if debug:
          print(f"[DEBUG]: generate output. Word 1 is {word}. (runs remaining: {n}):\n{bigram_table}\nRNG number is {rng_int}.\n\n")
        new_word = bigram_table.row(i_row)[0] #get the word corresponding to the rng
        return generate(new_word, found_bigram_table, n-1, word_list, cache, debug)
