import re

import requests
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/")
def text_to_sign():
    words = [request.args.get("word").lower(), request.args.get("word").lower().replace("ing", "")]
    language = request.args.get("language")

    for word in words:
        result = requests.post('http://spreadthesign.com/includes/search.inc.php', data={'search': word, 'lang': 13})
        matches = re.finditer('<a href=\"\/us\/(\d+)\/{}(?:-[^-]*)?-american-english(?:.*)\" .* data-video-language=\"(\d+)\" data-video-id=\"\d+\"'.format(word), result.content.decode("utf-8"))

        for match in matches:
            if 'title="{}"'.format(language) in match.group(0):
                return 'https://media.spreadthesign.com/video/mp4/{}/{}.mp4'.format(match.group(2), match.group(1))

    return ''


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(debug=True, port=5000)