from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def ex():
    return render_template("layout.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/organization")
def organization():
    return render_template("organization.html")

if __name__ == "__main__":
    app.run(debug = True)
    