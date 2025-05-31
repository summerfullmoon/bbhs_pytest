# app.py
import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your-secret-key"  # 세션을 위한 키 설정

quiz_list = [
    {
        "id": 0,
        "code": "print(3 * '배방고\\n')",
        "answer": "배방고\n배방고\n배방고\n"
    },
    {
        "id": 1,
        "code": "a = 5\nb = 3\nprint(a + b)",
        "answer": "8"
    },
    {
        "id": 2,
        "code": "for i in range(2):\n    print('Hello')",
        "answer": "Hello\nHello"
    },
    {
        "id": 3,
        "code": "print('3' * 3)",
        "answer": "333"
    },
    {
        "id": 4,
        "code": "print(len('파이썬'))",
        "answer": "3"
    }
]

def normalize_output(output: str) -> str:
    return output.strip().replace('\r\n', '\n').replace('\r', '\n')


@app.route('/')
def index():
    selected_quiz = random.choice(quiz_list)

    # 점수 세션 초기화
    if 'score' not in session:
        session['score'] = 0
        session['total'] = 0
        session['retry'] = None

    return render_template(
        "index.html",
        question_code=selected_quiz["code"],
        quiz_id=selected_quiz["id"],
        score=session['score'],
        total=session['total'],
        retry=False
    )


@app.route('/submit', methods=['POST'])
def submit():
    user_output = request.form['user_output']
    quiz_id = int(request.form['quiz_id'])
    selected_quiz = next((q for q in quiz_list if q["id"] == quiz_id), None)

    if not selected_quiz:
        return "문제를 찾을 수 없습니다.", 400

    user_normalized = normalize_output(user_output)
    correct_normalized = normalize_output(selected_quiz["answer"])
    is_correct = (user_normalized == correct_normalized)

    # 점수 누적
    session['total'] = session.get('total', 0) + 1
    if is_correct:
        session['score'] = session.get('score', 0) + 1
        session['retry'] = None
    else:
        session['retry'] = quiz_id  # 틀렸을 경우 다시 풀 문제 기억

    return render_template(
        "index.html",
        question_code=selected_quiz["code"],
        user_output=user_output,
        correct_output=selected_quiz["answer"],
        is_correct=is_correct,
        result=True,
        quiz_id=quiz_id,
        score=session['score'],
        total=session['total'],
        retry=True if not is_correct else False
    )


@app.route('/retry')
def retry():
    retry_id = session.get('retry')
    if retry_id is None:
        return redirect(url_for('index'))

    quiz = next((q for q in quiz_list if q["id"] == retry_id), None)
    return render_template(
        "index.html",
        question_code=quiz["code"],
        quiz_id=quiz["id"],
        score=session['score'],
        total=session['total'],
        retry=False
    )


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
