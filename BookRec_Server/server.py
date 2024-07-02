from flask import Flask, request, jsonify
import recommender as rcmd
from did_you_mean import get_likely_titles
lower_titles = [rcmd.preprocess_text(x) for x in rcmd.titles_list]

app = Flask(__name__)

@app.route('/input', methods=['POST'])

def handle_input():
    data = request.json  # Assuming JSON data is sent in the request body
    book_title = data.get('text')  # Extract input data
    count = int(data.get('count')) + 1  # Extract input data

    result = []
    if str(book_title).lower() not in lower_titles:
        result.append(get_likely_titles(book_title, rcmd.titles_list))
        result.append(0) #Code for no titles found
    else:
        result.append(rcmd.recommend_books(book_title, n = count))
        result.append(1)
        
    # Return response as JSON
    return jsonify({'result': result}), 200

def process_input(input_text):
    # Placeholder for processing logic
    print(input_text)
    return f'Received input: {input_text}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
