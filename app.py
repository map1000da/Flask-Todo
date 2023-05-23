from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from datetime import datetime

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

if __name__ == "__main__":
    app.run(debug=True)