from flask import Flask, render_template

app = Flask(__name__)

@app.route('./plantas')
def plantas():
    return render_template('plantas.py')


if __name__ == "__main__":
    app.run(debug=True)