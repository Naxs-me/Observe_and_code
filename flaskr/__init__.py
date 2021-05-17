import os
import sys
import ast
from zipfile import ZipFile
import pickle

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask, send_from_directory
)
from flaskr.db import get_db
import flaskr.ast_code as ast_code


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def base():
        return redirect(url_for('home'))

    @app.route('/home', methods=('GET', 'POST'))
    def home():
        db = get_db()
        if request.method == 'POST':
            question = request.form['questions']
            pyCommand = request.form['pyCommand']
            data = db.execute(
                'SELECT * FROM question WHERE id = ?',(question,)
            ).fetchone()
            temp = data[2].split('\n')
            code = []
            for k in temp:
                code.append(' '*4+k)
            s = '\n'
            s = s.join(code)
            s = "def fun():\n" + s + "\n" + " "*4 + "return 0\nfun()\n"
            # print(s)
            code = ast.parse(s)
            visitor = ast_code.MyVisitor(nb = [], lineNo = [])
            visitor.visit(code)
            print()
            visitor.get_Notebook()

            f = open("flaskr/combine.py", "r")
            combine = f.readlines()
            # print(combine)
            combine[combine.index("# <__code__insertion__>\n")] = s.replace('\r\n','\n')
            # print("combine",combine)
            f.close()

            f = open("flaskr/combine2.py", "r")
            combine2 = f.readlines()
            # print(combine)
            combine2[combine2.index("# <__code__insertion__>\n")] = s.replace('\r\n','\n')
            # print("combine",combine)
            f.close()


            combine = ''.join(combine)
            combine2 = ''.join(combine2)
            
            f = open("flaskr/combine_modified.py","w")
            f.write(combine)
            f.close()

            f = open("flaskr/combine_modified2.py","w")
            f.write(combine2)
            f.close()

            testcases = data[3].split("\r\n\r\n")
            visited = []
            with open("visited.txt", "wb") as fp:
                pickle.dump(visited, fp)
            # for k in range(len(testcases)):
            print("testcase",testcases[0])
            f = open("flaskr/input.txt","w")
            f.writelines(testcases[0].split("\n"))
            f.close()
            # if k == 0:
            os.system(str(pyCommand) + ' flaskr/combine_modified.py < flaskr/input.txt')
            # else:
            #     os.system(str(pyCommand) + ' flaskr/combine_modified2.py < flaskr/input.txt')
            with ZipFile('cospex.zip','w') as zip:
                zip.write("result.ipynb", os.path.basename("result.ipynb"))
                zip.write("stack.txt", os.path.basename("stack.txt"))
                zip.write("flaskr/execute.py", os.path.basename("flaskr/execute.py"))
            return redirect(url_for('download'))

            # f = open("flaskr/example.py", "w")
            # f.writelines(data[2].split('\n'))
            # f.close()
            # visitor = ast_code.MyVisitor


            # with open("flaskr/ast_code.py", "r+") as file1:
            #     ast_code = file1.read()
            # exec(ast_code)

        data = db.execute(
            'SELECT id,q_text FROM question'
        ).fetchall()
        return render_template('home.html',data = data)

    @app.route('/download', methods=('GET', 'POST'))
    def download():
        return send_from_directory(os.getcwd(),"cospex.zip",as_attachment=True)
        # return send_file("D:\\document readability\\FlaskUI\\astIPYNB.ipynb", attachment_filename='python.ipynb')

    from . import db
    db.init_app(app)

    from . import print_db
    app.register_blueprint(print_db.bp)

    return app