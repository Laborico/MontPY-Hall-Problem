from click import option
import jyserver.Flask as jsf
from random import randint
from flask import Flask, render_template

app = Flask(__name__)

door_amount = 3
state = 'PICK'
doors = []
@jsf.use(app) # Connect Flask object to JyServer
class App:
    def pickdoor(self, id):
        self.js.document.getElementById(id).classList.add("picked")
        self.reveal(id)
    
    def reveal(self, id):
        options = []
        for i, value in enumerate(doors):
            if i!= id and value != '🚂':
                options.append(i)
        
        #player selected correct door
        if len(options) == door_amount -1:
            options.pop(randint(0, len(options)- 1))
        
        print("---------")
        print(options)
        print("---------")
        for revealdoor in options:
            tag = '[prize="'+str(revealdoor)+'"]'
            self.js.document.getElementById(revealdoor).classList.add("revealed")
            self.js.document.querySelector(tag).innerHTML = doors[revealdoor]
        
    def reset(self):
        global state
        global doors
        doors = ['🐐' for i in range(door_amount)]
        winner = randint(0, door_amount-1)
        doors[winner] = '🚂'
        for i in range(door_amount):
            self.js.document.getElementById(id).classList.remove("revealed")
            self.js.document.getElementById(id).classList.remove("picked")
            self.js.document.getElementById(id).classList.remove("won")
        state = 'PICK'

            
        

@app.route("/")
def home():
    return App.render(render_template("index.html", door_amount = door_amount))
    
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)