from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

from forms import UrlForm

from config import SECRET_KEY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url.db"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


# >>>from app import app, db
# >>>app.app_context().push()
# >>>db.create_all()

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    url_short = db.Column(db.String(32))

    def __repr__(self):
        return f"<Url {self.id}>"


@app.route("/", methods=["POST", "GET"])
def index():
    form = UrlForm()

    if form.validate_on_submit():
        url = form.url.data
        return render_template("index.html", url=url, form=form)
    flash("Invalid url")
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
