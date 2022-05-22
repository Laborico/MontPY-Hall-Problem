from flask import Flask, render_template

app = Flask(__name__)

from js_server import App
from js_server import door_amount

@app.route("/")
def home():
    return App.render(render_template("index.html", door_amount = door_amount))
    
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)