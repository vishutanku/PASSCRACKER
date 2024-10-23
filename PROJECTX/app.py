from flask import Flask, request, jsonify, send_from_directory
import hashlib
import os

app = Flask(__name__)

# Helper function to generate MD5 and SHA1 hashes
def generate_hashes(text):
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    sha1_hash = hashlib.sha1(text.encode()).hexdigest()
    return md5_hash, sha1_hash

# Simple hash cracking using a wordlist
def crack_hash(input_hash, hash_type):
    with open('wordlist.txt', 'r') as file:
        for word in file:
            word = word.strip()
            if hash_type == 'md5':
                if hashlib.md5(word.encode()).hexdigest() == input_hash:
                    return word
            elif hash_type == 'sha1':
                if hashlib.sha1(word.encode()).hexdigest() == input_hash:
                    return word
    return None

# Route to serve the main HTML page
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Route to serve the CSS file
@app.route('/styles.css')
def css():
    return send_from_directory('.', 'styles.css')

# Route to handle hash generation
@app.route('/generate', methods=['POST'])
def generate():
    input_text = request.form['inputText']
    md5_hash, sha1_hash = generate_hashes(input_text)
    return jsonify({'md5': md5_hash, 'sha1': sha1_hash})

# Route to handle hash cracking
@app.route('/crack', methods=['POST'])
def crack():
    input_hash = request.form['inputHash']
    if len(input_hash) == 32:  # Assuming MD5
        cracked_text = crack_hash(input_hash, 'md5')
    elif len(input_hash) == 40:  # Assuming SHA1
        cracked_text = crack_hash(input_hash, 'sha1')
    else:
        cracked_text = "Invalid Hash Length"

    return jsonify({'crackedText': cracked_text if cracked_text else 'Not Found'})

if __name__ == '__main__':
    app.run(debug=True)
