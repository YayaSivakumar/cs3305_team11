from flask import render_template
from server.run import app


@app.route('/')
def home():
    return render_template('index.html')

