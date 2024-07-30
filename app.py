from flask import Flask, request, render_template, redirect, url_for
from turbo_flask import Turbo
import os

app = Flask(__name__)
turbo = Turbo(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/upload')
def upload_file():
    if 'file' not in request.files:
        return turbo.stream(turbo.append(render_template('error.html', message="No file part"), target='error'))
    file = request.files['file']
    if file.filename == '':
        return turbo.stream(turbo.append(render_template('error.html', message="No selected file"), target='error'))
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        insights = process_resume(filepath)
        return turbo.stream(turbo.append(render_template('insights.html', insights=insights), target='insights'))


def process_resume(filepath):
    insights = {"name": "John Doe", "skills": ["Python", "Flask", "AI"]}
    return insights


if __name__ == '__main__':
    app.run(debug=True)
