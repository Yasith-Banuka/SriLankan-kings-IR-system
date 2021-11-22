from flask import Flask
from flask import render_template, request
import json

from Search import search, autocomplete

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        results = search(request.form['query'])
        return render_template('index.html', results = results)
    return render_template('index.html', results = '')

@app.route('/autocomplete', methods=["GET", "POST"])
def auto():
    data = request.form.get("data")
    response = autocomplete(str(data))
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True)