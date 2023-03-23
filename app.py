from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///url.db"
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


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
