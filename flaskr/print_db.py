import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.db import get_db

bp = Blueprint('print_db', __name__, url_prefix='/print_db')

@bp.route('/insert_question', methods=('GET', 'POST'))
def insert_question():
    if request.method == 'POST':
        question = request.form['question']
        code = request.form['code']
        testcase = request.form['testcase']
        db = get_db()
        cur = db.cursor()
        error = None

        if not question:
            error = 'Question is required.'
        elif not code:
            error = 'Code is required.'
        elif not testcase:
            error = 'Testcases are required.'
        elif db.execute(
            'SELECT id FROM question WHERE q_text = ?', (question,)
        ).fetchone() is not None:
            error = 'Question {} is already registered.'.format(question)

        # a = cur.execute('SELECT * FROM question')
        # rows = a.fetchall()
        # for row in rows:
        #     print(row[1])

        if error is None:
            db.execute(
                'INSERT INTO question (q_text,code,testcase) VALUES (?,?,?)',(question,code, testcase)
            )
            # id = db.execute(
            #     'SELECT count(*) FROM question'
            # ).fetchone()
            # db.execute(
            #     'INSERT INTO testcases (q_id, body) VALUES (?,?)',(id,testcase)
            # )
            db.commit()
            # test = db.execute(
            #     'SELECT * FROM question'
            # ).fetchall()

            return redirect(url_for('print_db.question_inserted'))

        flash(error)

    return render_template('insert_question/insert_question.html')

@bp.route('/question_inserted', methods=('GET', 'POST'))
def question_inserted():

    return render_template('/question_inserted.html')