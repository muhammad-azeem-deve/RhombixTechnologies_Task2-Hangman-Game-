from flask import Flask, render_template_string, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

WORDS = ["python", "flask", "developer", "hangman", "programming", "computer"]
MAX_ATTEMPTS = 6

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Hangman Game</title>
    <style>
        body { font-family: Arial; text-align: center; background: #1e1e2f; color: white; }
        .box { background: #2c2c3e; padding: 20px; margin: 50px auto; width: 400px; border-radius: 10px; }
        input { padding: 10px; width: 50px; text-align: center; }
        button { padding: 10px 20px; background: #4CAF50; color: white; border: none; }
        .word { font-size: 30px; letter-spacing: 10px; }
        .msg { margin-top: 10px; color: #FFD700; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🎯 Hangman Game</h1>
        <p class="word">{{ word_display }}</p>
        <p>Attempts Left: {{ attempts }}</p>
        <form method="POST">
            <input type="text" name="letter" maxlength="1" required>
            <button type="submit">Guess</button>
        </form>
        <p class="msg">{{ message }}</p>
        <form action="/reset">
            <button type="submit">Restart</button>
        </form>
    </div>
</body>
</html>
"""


def init_game():
    word = random.choice(WORDS)
    session['word'] = word
    session['guessed'] = []
    session['attempts'] = MAX_ATTEMPTS


def get_display_word():
    return " ".join([letter if letter in session['guessed'] else '_' for letter in session['word']])


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        init_game()

    message = ""

    if request.method == 'POST':
        letter = request.form['letter'].lower()

        if letter in session['guessed']:
            message = "Already guessed!"
        elif letter in session['word']:
            session['guessed'].append(letter)
            message = "Correct guess!"
        else:
            session['attempts'] -= 1
            session['guessed'].append(letter)
            message = "Wrong guess!"

    word_display = get_display_word()

    if '_' not in word_display:
        message = "🎉 You Won!"
    elif session['attempts'] <= 0:
        message = f"💀 You Lost! Word was: {session['word']}"

    return render_template_string(HTML,
                                  word_display=word_display,
                                  attempts=session['attempts'],
                                  message=message)


@app.route('/reset')
def reset():
    init_game()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
