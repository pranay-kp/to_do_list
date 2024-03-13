from flask import Flask, render_template, url_for, request,redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float



app = Flask(__name__)
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class Todo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Todo).order_by(Todo.title))
    all_todo = result.scalars()
    return render_template("index.html", lists= all_todo)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_todo = Todo(
            title=request.form["todo"],

        )
        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/delete")
def delete():
    todo_id = request.args.get('id')

    # DELETE A RECORD BY ID
    todo_to_delete = db.get_or_404(Todo, todo_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))













if __name__ == "__main__":
    app.run(debug=True)