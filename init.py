import os
from flask import Flask, render_template, session, request, redirect
from pprint import pprint

from item import item
from database import database

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = '🍏'

    # app.config.from_mapping(SECRET_KEY='dev', DATABASE="")

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.congif.from_pyfile('config.py',silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    
    # # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        if 'items' not in session.keys() or session['items'] == None:
            print("reset items")
            session['items'] = [
                {"name":"Item A", "price":2.0, "weight":32.5, "color":"red", "quantity":345},
                {"name":"Item B", "price":6.0, "weight":2.5, "color":"blue", "quantity":525},
                {"name":"Item C", "price":5.60, "weight":24.5, "color":"green", "quantity":63},
            
            ]
        session.modified = True
        return render_template('index.html', item_list = session['items'])

    @app.route("/add", methods = ['GET', 'POST'])
    def add():
        if request.method == 'POST':
            dic = {
                "name":request.form["name"],
                "price":request.form["price"],
                "weight":request.form["weight"],
                "color":request.form["color"],
                "quantity":request.form["quantity"],
            }
            session['items'].append(dic)
            pprint(session['items'])
            session.modified = True
            return redirect('/')
        return render_template('Form.html')

    @app.route("/delete/<itemname>")
    def delete(itemname):
        for i in range(len(session['items'])):
            if(session['items'][i]['name'] == itemname):
                del session['items'][i]
                break
        session.modified = True
        return redirect('/')

    @app.route('/print')
    def print():        
        return render_template('Report.html', item_list = session['items'])
    
    return app
   


if __name__ == '__main__':
    app = create_app()
    app.run()