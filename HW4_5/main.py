from flask import Flask, render_template, url_for, abort
from jinja2 import TemplateNotFound
import os
import random

BASE_DIR = os.path.dirname(__file__)
app = Flask(__name__,
            static_folder=os.path.join(BASE_DIR, 'static') , 
            template_folder=os.path.join(BASE_DIR, 'templates'))

@app.route("/")
def index():
    return render_template('base.html')

@app.route('/task<int:task_number>/')
def show_task(task_number):
    template_name = f'task{task_number}.html'
    try:
        if task_number == 10:
            random_task = random.randint(1,12)
            return render_template('task10.html', random_task=random_task)
        return render_template(template_name)
    except TemplateNotFound:
        abort(404, description="Задание не найдено")

if __name__ == '__main__':
    app.run(debug=True)