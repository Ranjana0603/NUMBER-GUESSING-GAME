from flask import Flask, render_template, request, session, jsonify 
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  

@app.route('/')
def home():
    return render_template('game.html')  

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    difficulty = data.get('difficulty')

    if difficulty == "easy":
        lower_bound, upper_bound = 1, 50
    elif difficulty == "medium":
        lower_bound, upper_bound = 1, 100
    else:
        lower_bound, upper_bound = 1, 200

    session['number_to_guess'] = random.randint(lower_bound, upper_bound)
    session['lower_bound'], session['upper_bound'] = lower_bound, upper_bound
    session['attempts'] = 0  

    return jsonify({
        'message': f"Game started! Guess a number between {lower_bound} and {upper_bound}.",
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    })

@app.route('/play', methods=['POST'])
def play():
    if 'number_to_guess' not in session:
        return jsonify({'message': "Start a new game first!"})

    data = request.json
    try:
        user_guess = int(data.get('guess'))
    except ValueError:
        return jsonify({'message': "Invalid input! Please enter a number."})

    lower_bound, upper_bound = session['lower_bound'], session['upper_bound']
    number_to_guess = session['number_to_guess']
    session['attempts'] += 1
    attempts_left = 10 - session['attempts']

    if session['attempts'] >= 10:
        session.pop('number_to_guess', None)
        return jsonify({'message': f"Game Over! The correct number was {number_to_guess}.", 'game_over': True})

    if user_guess < lower_bound or user_guess > upper_bound:
        return jsonify({'message': f"Enter a number between {lower_bound}-{upper_bound}!"})

    if user_guess < number_to_guess:
        return jsonify({'message': f"Too low! Attempts left: {attempts_left}"})
    elif user_guess > number_to_guess:
        return jsonify({'message': f"Too high! Attempts left: {attempts_left}"})
    else:
        session.pop('number_to_guess', None)
        return jsonify({'message': f"Correct! You guessed {number_to_guess} in {session['attempts']} attempts!", 'game_over': True})

if __name__ == "__main__":
    app.run(debug=True)

