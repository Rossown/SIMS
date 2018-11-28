import os
from flask import Flask, render_template, session, request, redirect
from pprint import pprint

import database

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'fish'

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
            session['items'] = []
        session.modified = True
        return render_template('index.html', item_list = session['items'], name = session['name'])

    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        if request.method == 'POST':
            if(database.checkLogin(request.form['name'], request.form['password'])):
                session['name'] = request.form['name']
                session['password'] = request.form['password']
                data = database.load(session['name'], session['password'])
                if(data != False):
                    session['items'] = database.load(session['name'], session['password'])
                    session.modified = True
                    return redirect('/')
            return redirect('/login')
        if 'name' in session.keys():
            del session['name']
        if 'password' in session.keys():
            del session['password']
        return render_template('Login.html')

    @app.route("/add", methods = ['GET', 'POST'])
    def add():
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        if request.method == 'POST':
            maxId = 0
            for item in session['items']:
                maxId = max(item['id'], maxId)
            dic = {
                "id":maxId+1,
                "name":request.form["name"],
                "price":request.form["price"],
                "weight":request.form["weight"],
                "color":request.form["color"],
                "quantity":request.form["quantity"],
            }
            session['items'].append(dic)
            session.modified = True
            return redirect('/')
        return render_template('Form.html')

    @app.route("/delete/<id>")
    def delete(id):
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        for i in range(len(session['items'])):
            if(str(session['items'][i]['id']) == id):
                del session['items'][i]
                break
        session.modified = True
        return redirect('/')

    @app.route('/print')
    def printReport():        
        return render_template('Report.html', item_list = session['items'])
    
    @app.route("/modify/<id>", methods = ['GET', 'POST'])
    def details(id):
        if request.method == 'POST':
            for i in range(len(session['items'])):
                if(str(session['items'][i]['id']) == id):
                    dic = {
                        "id":id,
                        "name":request.form["name"],
                        "price":request.form["price"],
                        "weight":request.form["weight"],
                        "color":request.form["color"],
                        "quantity":request.form["quantity"]
                    }
                    session['items'][i] = dic
                    break
            session.modified = True
            return redirect('/')
        for i in range(len(session['items'])):
            if(str(session['items'][i]['id']) == id):
                return render_template('DetailsPage.html', item = session['items'][i])
        return redirect('/')
    
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