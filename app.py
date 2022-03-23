from flask import Flask, jsonify, abort, request
from random import choice

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

about_me = {
    "name": "Евгений",
    "surname": "Юрченко",
    "email": "eyurchenko@specialist.ru"
}

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

@app.route("/quotes/<int:id>")
def get_quote(id):
    for quote in quotes:
        if quote["id"] == id:
            return jsonify(quote)
    abort(404, description=f"Quote with id = {id} is not found.")


@app.route("/count_quotes")
def count_quotes():
    return {
        "count": len(quotes)
    }

@app.route("/quotes")
def quotes_list():
    return jsonify(quotes)

@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    new_id = quotes[-1]["id"] + 1
    new_quote["id"] = new_id
    quotes.append(new_quote)
    return new_quote, 201 # Created

@app.route("/random_quotes")
def random_quotes():
    return jsonify(choice(quotes))

if __name__ == "__main__":
    app.run(debug=True)
