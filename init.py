import os
from flask import Flask, render_template, session, request, redirect
from pprint import pprint

import database

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'key'

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
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        if 'items' not in session.keys() or session['items'] == None:
            print("reset items")
            session['items'] = [
                {"name":"ItemA", "price":2.0, "weight":32.5, "color":"red", "quantity":345},
                {"name":"ItemB", "price":6.0, "weight":2.5, "color":"blue", "quantity":525},
                {"name":"ItemC", "price":5.60, "weight":24.5, "color":"green", "quantity":63},
            
            ]
        session.modified = True
        return render_template('index.html', item_list = session['items'])

    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['name'] = request.form['name']
            session['password'] = request.form['password']
            session.modified = True
            return redirect('/')
        return render_template('Login.html')

    @app.route("/add", methods = ['GET', 'POST'])
    def add():
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
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
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        for i in range(len(session['items'])):
            if(session['items'][i]['name'] == itemname):
                del session['items'][i]
                break
        session.modified = True
        return redirect('/')

    @app.route('/print')
    def print():        
        return render_template('Report.html', item_list = session['items'])
    
    @app.route("/modify/<itemname>", methods = ['GET', 'POST'])
    def details(itemname):
        if request.method == 'POST':
            for i in range(len(session['items'])):
                if(session['items'][i]['name'] == itemname):
                    dic = {
                        "name":request.form["name"],
                        "price":request.form["price"],
                        "weight":request.form["weight"],
                        "color":request.form["color"],
                        "quantity":request.form["quantity"]
                    }
                    session['items'][i] = dic
                    break;
            session.modified = True
            return redirect('/')
        for i in range(len(session['items'])):
            if(session['items'][i]['name'] == itemname):
                return render_template('DetailsPage.html', item = session['items'][i])
        return rediret('/')
    
    @app.route("/save")
    def save():
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        database.save(session['name'], session['items'], session['password'])
        return redirect("/")

    return app
   


if __name__ == '__main__':
    app = create_app()
    app.run()