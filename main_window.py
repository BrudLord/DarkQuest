from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
@app.route('/countdown')
def main_window():
    return render_template('main_window.html')
@app.route('/help')
def help():
    return render_template('help.html')







if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
