import redis
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
list = ['p1.png',
        'legi2.jpeg', 'p4.png']
i = 0
hostname = 'redis-16515.c330.asia-south1-1.gce.redns.redis-cloud.com'
port = 16515
password = 'h3aWFel7EUUxQI0xp9y0aqSrBjU6tCtX'
r = redis.StrictRedis(
    host=hostname,
    port=port,
    password=password,
    decode_responses=True  # Ensures responses are decoded as strings, not bytes
)
username = ""


dict = {}
l = []


@app.route('/')
def home():

    # Initialize session variable for index if it doesn't exist
    if 'index' not in session:
        session['index'] = 0
    return render_template('login.html')


@app.route('/Question', methods=['POST'])
def questions():
    user = request.form.get('username')
    global username
    if (user):
        username = user
    global i
    if i >= len(list):
        # Loop back to the start if all images are shown

        return render_template('success.html')
    image_name = list[i]
    i += 1
    return render_template('round_1.html', image_name=image_name)


@app.route('/1', methods=['POST'])
def process_submission():

    # Use .get() to avoid errors if the keys are missing
    answer = request.form.get('Answer')  # Safely get 'Answer'
    reason = request.form.get('reason')  # Safely get 'reason'
    print(f"Answer received: {answer}")
    print(f"Reason received: {reason}")
    '''answer = str(i)+" "+answer
    reason = str(i)+" "+reason'''
    r.hset(username, f"answer_{i}", answer)
    r.hset(username, f"reason{i}", reason)

    if not answer:
        return "Error: No answer provided", 400

    return questions()


if __name__ == "__main__":
    app.run()
