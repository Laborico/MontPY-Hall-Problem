import enum
import jyserver.Flask as jsf
from random import randint
from flask import Flask, render_template

app = Flask(__name__)

door_amount = 30
state = 'PICK'
options = []
winner_index = 0
@jsf.use(app) # Connect Flask object to JyServer
class App:
    
    def start(self):
        global state
        global winner_index
        winner_index = randint(1, door_amount-1)
        
        state = 'PICK'
        
        self.js.document.getElementById("choices").classList.add("hidden")
        self.js.document.getElementById("play-again").classList.add("hidden")
        
    def reset(self):
        self.start()
        for i in range(1, door_amount + 1):
            self.js.document.getElementById(i).classList.remove("revealed")
            self.js.document.getElementById(i).classList.remove("picked")
            self.js.document.getElementById(i).classList.remove("won")
        
        self.js.document.querySelector("#instruction > p").innerHTML = "Pick a Door!"
        

    def pickdoor(self, id):
        self.js.document.getElementById(id).classList.add("picked")
        self.reveal(id)
    
    def reveal(self, id):
        global options
        options = []
        for i in range(1, door_amount + 1):
            if i!= id and i!= winner_index:
                options.append(i )
        
        #player selected correct door
        if len(options) == door_amount -1:
            options.pop(randint(0, len(options)- 1))
            
        
        for revealdoor in options:
            tag = '[prize="'+str(revealdoor)+'"]'
            self.js.document.getElementById(revealdoor).classList.add("revealed")
            self.js.document.querySelector(tag).innerHTML = '🐐'
            
        
        last_door = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
        message = "Do you want to switch to door #"+str(last_door)+"?"
        self.js.document.querySelector("#instruction > p").innerHTML = message
        
        self.js.document.getElementById("choices").classList.remove("hidden")
    
    def choose_door(self, switched):
        self.js.document.getElementById("choices").classList.add("hidden")
        
        if switched:
            """
                jyserver does not save the results of each query to a varible
                once a new query is done, all the varibles that had a query asign 
                get overriden, that's why I had to do the same query twice
            """
            new_door = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id        
            self.js.document.getElementById(new_door).classList.add("new")
            new_door = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
            self.js.document.getElementById(new_door).classList.add("picked")
            
            last_door = self.js.document.querySelector(".door-container:not(.revealed):not(.new)").id
            self.js.document.getElementById(last_door).classList.remove("picked")
            
        self.check_win()
        
    def check_win(self):
        door1 = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
        if door1 == str(winner_index):
            door1 = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
            
            tag = '[prize="'+str(door1)+'"]'
            
            door1 = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
            self.js.document.getElementById(door1).classList.add("revealed")
            
            #sets emoji to winner door
            self.js.document.querySelector(tag).innerHTML = '🚂'
            
            #sets emoji to loser door
            door2 = self.js.document.querySelector(".door-container:not(.revealed):is(.picked)").id
            
            tag = '[prize="'+str(door2)+'"]'
            
            door2 = self.js.document.querySelector(".door-container:not(.revealed):is(.picked)").id
            self.js.document.getElementById(door2).classList.add("revealed")
            
            self.js.document.querySelector(tag).innerHTML = '🐐'
        else:
            door1 = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
            
            tag = '[prize="'+str(door1)+'"]'
            
            door1 = self.js.document.querySelector(".door-container:not(.revealed):not(.picked)").id
            self.js.document.getElementById(door1).classList.add("revealed")
            
            #sets emoji to loser door
            self.js.document.querySelector(tag).innerHTML = '🐐'
            
            #sets emoji to winner door
            door2 = self.js.document.querySelector(".door-container:not(.revealed):is(.picked)").id
            
            tag = '[prize="'+str(door2)+'"]'
            
            door2 = self.js.document.querySelector(".door-container:not(.revealed):is(.picked)").id
            self.js.document.getElementById(door2).classList.add("revealed")
            
            self.js.document.querySelector(tag).innerHTML = '🚂'

        
        current_door = self.js.document.querySelector(".door-container.picked > .content").innerHTML
        
        if current_door == '🚂':
            self.js.document.querySelector("#instruction > p").innerHTML = "You Win:D!"
        else:
            self.js.document.querySelector("#instruction > p").innerHTML = "You Lose:C!"
            
        self.js.document.getElementById("play-again").classList.remove("hidden")
        
        self.js.document.getElementById("play-again").classList.remove("hidden")
        

        

@app.route("/")
def home():
    return App.render(render_template("index.html", door_amount = door_amount))
    
if __name__ == "__main__":
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)