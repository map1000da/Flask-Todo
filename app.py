from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

import datetime

app = Flask(__name__)

#環境変数の設定
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#データベースの作成とMigrateの準備
db = SQLAlchemy(app)
Migrate(app, db)

#Taskテーブル
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100)) #タイトル
    status = db.Column(db.String(20))
    created_date = db.Column(db.Date)

    def __init__(self, title, status, created_date):
        self.title = title
        self.status = status
        self.created_date = created_date

    #Task クラスのインスタンスが表示される際に以下の形式で表示されるようにする
    def __repr__(self):
        return f'<Task {self.id}>'

@app.route("/")
def index():
    tasks = Task.query.all() #データベースからタスク一覧を取得
    return render_template("index.html", tasks = tasks)

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST": #POSTメソッドではフォームから送信されたタスクの情報をDBに追加する．
        title = request.form["title"]
        status = request.form["status"]
        creted_date = datetime.date.today()
        new_task = Task(title, status, creted_date)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("index"))
    
    return render_template("add_task.html") #GETメソッドではadd_task.htmlを表示する．

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        if request.method == "POST":
            task.title = request.form["title"]
            task.status = request.form["status"]
            db.session.commit()
            return redirect(url_for("index"))
        return render_template("edit_task.html", task=task)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)