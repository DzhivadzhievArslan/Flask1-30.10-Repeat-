from flask import Flask, jsonify, abort, request
from random import choice
from tools_db import create_connection, execute_query, execute_read_query, BASE_DIR
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'test.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },

]

db = SQLAlchemy(app)


class QuoteModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    quote = db.Column(db.String(255), unique=False)

    def __init__(self, author, quote):
        self.author = author
        self.quote = quote

    def __repr__(self):
        return f"Quote: {self.author}/ {self.quote[:10]}..."

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.quote,
        }


@app.route("/quotes")
def quotes_list():
    quotes = QuoteModel.query.all()
    new_quotes = []
    for quote in quotes:
        new_quotes.append(quote.to_dict())
    return jsonify(new_quotes)


@app.route("/quotes/<int:id>")
def get_quote(id):
    quote = QuoteModel.query.get(id)
    if quote is None:
        abort(404, description=f"Quote with id = {id} is not found.")
    return jsonify(quote.to_dict())


@app.route("/count_quotes")
def count_quotes():
    return {
        "count": len(quotes)
    }


@app.route("/quotes", methods=["POST"])
def create_quote():
    new_quote = request.json
    # quote = QuoteModel(new_quote["author"], new_quote["quote"])
    quote = QuoteModel(**new_quote)
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote.to_dict()), 201


@app.route("/quotes/<int:id>", methods=["PUT"])
def edit_quote(id):
    new_data = request.json
    for quote in quotes:
        if quote["id"] == id:
            if new_data.get("author"):
                quote["author"] = new_data["author"]
            if new_data.get("text"):
                quote["text"] = new_data["text"]
            return quote, 200
        new_data["id"] = quotes[-1]["id"] + 1
        quotes.append(new_data)
        return new_data, 201


@app.route("/quotes/<int:id>", methods=["DELETE"])
def delete(id):
    for quote in quotes:
        if quote["id"] == id:
            quotes.remove(quote)
            return f"Quote with id {id} was deleted.", 200
        abort(404, description=f"Quote with id = {id} is not found.")


@app.route("/random_quotes")
def random_quotes():
    return jsonify(choice(quotes))


if __name__ == "__main__":
    app.run(debug=True)
