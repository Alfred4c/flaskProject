from flask import Flask, abort, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE = "sqlite:///{}".format(os.path.join(BASE_DIR, "todo.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    done = db.Column(db.Integer, default=0)

    def __str__(self):
        return "id:{}".format(self.id)


@app.route("/add", methods=["POST"])
def add_Todo():
    text = request.form.get("text")
    if len(text) > 50:
        abort(404)
        return None
    todo = Todo(text=text)
    db.session.add(todo)
    db.session.commit()
    db.session.refresh(todo)
    return redirect("/", code=302)


def all_Todos():
    return db.session.query(Todo).all()


@app.route("/delete", methods=["POST"])
def delete_Todo():
    id = request.form.get("id")
    db.session.query(Todo).filter_by(id=id).delete()
    db.session.commit()
    return redirect("/", code=302)


@app.route("/finished", methods=["POST"])
def finished():
    id = request.form.get("id")
    text_info = db.session.query(Todo).filter_by(id=id).first()
    text_info.done = 1
    db.session.commit()
    return redirect("/", code=302)


@app.route("/")
def index():
    return render_template("index.html", todos=all_Todos())


if __name__ == "__main__":
    db.create_all()
    app.run(port=5000, debug=True)

