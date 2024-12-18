from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "wordle_secret_key"

# List of 5-letter words
WORDS = ["apple", "grape", "peach", "melon", "mango", "berry", "lemon"]

def generate_feedback(secret_word, guess):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback.append("green")  # Correct letter and position
        elif guess[i] in secret_word:
            feedback.append("yellow")  # Correct letter, wrong position
        else:
            feedback.append("gray")  # Incorrect letter
    return feedback

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        guess = request.form["guess"].lower()

        if "secret_word" not in session:
            return redirect(url_for("reset"))

        secret_word = session["secret_word"]
        attempts = session.get("attempts", [])
        
        if len(guess) != 5 or not guess.isalpha():
            error = "Please enter a valid 5-letter word."
            return render_template("index.html", attempts=session.get("attempts", []), error=error)
        
        feedback = generate_feedback(secret_word, guess)
        attempts.append({"guess": guess, "feedback": feedback})
        session["attempts"] = attempts

        if guess == secret_word:
            return render_template("index.html", attempts=prepare_attempts(attempts), success=True, secret_word=secret_word)
        elif len(attempts) == 6:
            return render_template("index.html", attempts=prepare_attempts(attempts), failure=True, secret_word=secret_word)
        
        return redirect(url_for("index"))

    if "secret_word" not in session:
        return redirect(url_for("reset"))

    return render_template("index.html", attempts=prepare_attempts(session.get("attempts", [])))

@app.route("/reset")
def reset():
    session["secret_word"] = random.choice(WORDS)
    session["attempts"] = []
    return redirect(url_for("index"))

def prepare_attempts(attempts):
    return [zip(attempt["guess"], attempt["feedback"]) for attempt in attempts]

if __name__ == "__main__":
    app.run(debug=True)
