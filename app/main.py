import re

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('text_to_hand.html')


@app.route("/api/")
def text_to_sign():
    word = request.args.get("word")
    # word = "hello"

    result = requests.post('http://spreadthesign.com/includes/search.inc.php', data={'search': word, 'lang': 13})
    match = re.search('a href="\/us\/(\d+)\/{}-american-english"'.format(word), result.content.decode("utf-8"))

    if match:
        return 'https://media.spreadthesign.com/video/mp4/13/{}.mp4'.format(match.group(1))
    else:
        return ''


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(debug=True, port=5000)