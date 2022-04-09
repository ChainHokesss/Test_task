from crypt import methods
from flask import Flask, render_template, request, flash, jsonify, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import json


DEBUG = True
SECRET_KEY = "qwerty1234"
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:06082003@localhost:5432/test_pr"
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)


class MainModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    value = db.Column(JSONB)

    def __repr__(self):
        return f"{self.id} {self.value}"

    def toJSON(self):
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'value':  self.value
        })


@app.route("/", methods=['POST', 'GET'])
def homeView():
    if request.method == "POST":
        print(len(request.form))
        for name in request.form:
            print(name + " " + request.form[name])
            try:
                if len(request.form[name]) > 2:
                    value = MainModel(value = request.form[name], name = name)
                    db.session.add(value)
                    db.session.commit()
                else:
                    flash("FORM ERROR")
            except:
                db.session.rollback()
                print("FORM ERROR")

    return render_template("home_page.html")


@app.route("/output")
def jsonView():
    query = MainModel.query.all()

    jsonQuery = list(map(lambda x : x.toJSON(), query))
    return jsonify(jsonQuery)

@app.errorhandler(404)
def error404(error):
    return render_template("page404.html"), 404


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])