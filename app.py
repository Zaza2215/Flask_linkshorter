from flask import Flask, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from forms import UrlForm

from config import SECRET_KEY, HOST

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url.db"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


# >>>from app import app, db
# >>>app.app_context().push()
# >>>db.create_all()

class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False, unique=True)
    url_short = db.Column(db.Integer, nullable=False, unique=True)

    def __repr__(self):
        return f"<Url {self.id}>"


def get_url_short():
    url = Url.query.order_by(desc(Url.url_short)).first()
    if url:
        url = url.url_short + 1
    else:
        url = 0

    return url


@app.route("/", methods=["POST", "GET"])
def index():
    form = UrlForm()

    if form.validate_on_submit():
        url_main = form.url.data

        if Url.query.filter_by(url=url_main).first():
            print("Url is already exist!")
            url = Url.query.filter_by(url=url_main).first()
            # flash("Url is already exist!")
        else:
            url_short = get_url_short()
            url = Url(url=url_main, url_short=url_short)
            db.session.add(url)
            db.session.commit()

        return render_template("index.html", url=url, form=form, host=HOST)
    elif request.method == "POST":
        flash("Invalid url")

    return render_template("index.html", form=form)


@app.route("/<int:short_url>")
def short_url_route(short_url):
    shorter_url = Url.query.filter_by(url_short=short_url).first()
    if not shorter_url:
        flash("There isn't such url")
    # return render_template("short_url.html", shorter_url=shorter_url)
    return redirect(shorter_url.url, code=301)


if __name__ == "__main__":
    app.run(debug=True)
