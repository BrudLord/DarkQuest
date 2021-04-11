from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/countdown')
def main_menu():
    return '''<!DOCTYPE html>
    <head>
    <style>
    body {background-color: #2B2517; background-size: cover;}
    </style>
    </head>
    <body background="https://steamuserimages-a.akamaihd.net/ugc/253716559962314766/4C9C8BAA47DD8DBFE20E5A6243D1E7B41104BB87/" width="100%" height="100%">
    <input type="button" value=" Нажми меня нежно ">
    </body>
    </html>
    '''







if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
