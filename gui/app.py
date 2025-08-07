from flask import Flask, render_template, request, jsonify
from bigram_babbler import *

app = Flask(__name__)
global_debug = True

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/bigram_babble', methods=['POST'])
def generate_text():
  data = request.json
  word = data.get("word", "")
  length = data.get("length", 100)
  try:
    b = find_bigrams(tokenize("source.txt"), debug=global_debug)
    result = generate(word, b, int(length), debug=global_debug)
  except:
    result = "Invalid inputs."
  return jsonify({"result": result})

if __name__ == '__main__':
  app.run(debug=global_debug)
