from flask import Flask, render_template, url_for, redirect, request, flash
import os

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static') , 
            template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/task1/")
def task1():
    return render_template('task1.html')

@app.route("/task2/")
def task2():
    return render_template('task2.html')

if __name__ == '__main__':
    app.run(debug=True)