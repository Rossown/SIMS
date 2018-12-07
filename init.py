import os
from flask import Flask, render_template, session, request, redirect
from pprint import pprint

import database

def create_app(test_config=None): #initialize program
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'fish'

    #ensure we have the correct file pathings
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #index page
    @app.route('/')
    def index():
        #check if user has logged in
        if 'name' not in session.keys() or 'password' not in session.keys() or 'name'=='':
            return redirect("/login")
        #check if items list has been initialized
        if 'items' not in session.keys() or session['items'] == None:
            print("reset items")
            session['items'] = []
        session.modified = True
        #display page
        return render_template('index.html', item_list = session['items'], name = session['name'])

    #login page
    @app.route("/login", methods = ['GET', 'POST'])
    def login():
        #taking in a login request
        if request.method == 'POST':
            #verify request from database
            if(request.form['name'] != '' and database.checkLogin(request.form['name'], request.form['password'])):
                session['name'] = request.form['name']
                session['password'] = request.form['password']
                data = database.load(session['name'], session['password'])
                #verify loading of data
                if(data != False):
                    session['items'] = database.load(session['name'], session['password'])
                    session.modified = True
                    return redirect('/')
            return redirect('/login')
        #reset name in session
        if 'name' in session.keys():
            del session['name']
        #reset password in session
        if 'password' in session.keys():
            del session['password']
        #display page
        return render_template('Login.html')

    #add item page
    @app.route("/add", methods = ['GET', 'POST'])
    def add():
        #verify logged in
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        #take in item additions
        if request.method == 'POST':
            #get highest id to prevent repetition
            maxId = 0
            for item in session['items']:
                maxId = max(item['id'], maxId)
            #create item dictionary for local save
            dic = {
                "id":maxId+1,
                "name":request.form["name"],
                "price":request.form["price"],
                "weight":request.form["weight"],
                "color":request.form["color"],
                "quantity":request.form["quantity"],
            }
            #save item to session
            session['items'].append(dic)
            session.modified = True
            return redirect('/')
        #display input form
        return render_template('Form.html')

    #delete item page
    @app.route("/delete/<id>")
    def delete(id):
        #verify logged in
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        #check for correct id, and delete first if exists
        for i in range(len(session['items'])):
            if(str(session['items'][i]['id']) == id):
                del session['items'][i]
                break
        #return to index
        session.modified = True
        return redirect('/')

    #print page
    @app.route('/print')
    def printReport():  
        #display printable page      
        return render_template('Report.html', item_list = session['items'])
    
    #modify page
    @app.route("/modify/<id>", methods = ['GET', 'POST'])
    def details(id):
        #verify login
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        #take inputs
        if request.method == 'POST':
            #search for correct item by id
            for i in range(len(session['items'])):
                if(str(session['items'][i]['id']) == id):
                    #replace item with new dictionary with new information
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
            #modify and return to index
            session.modified = True
            return redirect('/')
        #search for correct item by id, display item's information on modify page
        for i in range(len(session['items'])):
            if(str(session['items'][i]['id']) == id):
                return render_template('DetailsPage.html', item = session['items'][i])
        #return to index (should never happen)
        return redirect('/')
    
    #save page
    @app.route("/save")
    def save():
        #verify login
        if 'name' not in session.keys() or 'password' not in session.keys():
            return redirect("/login")
        #call database save function
        database.save(session['name'], session['items'], session['password'])
        #return to index
        return redirect("/")

    #send application with functions to client
    return app

#create application in main method
if __name__ == '__main__':
    app = create_app()
    app.run()