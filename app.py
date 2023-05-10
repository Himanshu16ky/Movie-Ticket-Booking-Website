from flask import Flask,url_for
from flask import render_template
from flask import request,flash
from flask_sqlalchemy import SQLAlchemy
from flask import redirect
import time
import urllib
import json
import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt


movies = []
lst = []


app = Flask(__name__)
app.secret_key = "invalid credantials."

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'admin.sqlite3'))
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Admin(db.Model):
    __tablename__ = 'admin'
    username = db.Column(db.String, nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String, nullable = False)

class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String, nullable = False, unique = True, primary_key = True)
    password = db.Column(db.String, nullable = False)
    towatch = db.Column(db.String)

class Movies(db.Model):
    __tablename__ = "movies"
    serial = db.Column(db.Integer)
    id = db.Column(db.String ,primary_key = True )
    title = db.Column(db.String )
    poster = db.Column(db.String )
    release_date = db.Column(db.String )
    plot = db.Column(db.String )
    rating = db.Column(db.String )
    runtime = db.Column(db.String )
    genre = db.Column(db.String )
    venue_name = db.Column(db.String,primary_key = True )
    place = db.Column(db.String ,primary_key = True )
    location = db.Column(db.String ,primary_key = True )
    capacity = db.Column(db.Integer )
    show_name = db.Column(db.String )
    rating = db.Column(db.String )
    timing = db.Column(db.String ,primary_key = True )
    price = db.Column(db.Integer)

class Venues(db.Model):
    __tablename__ = "venues"
    venue_name = db.Column(db.String, nullable = False, primary_key = True)
    place = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    capacity = db.Column(db.Integer, nullable = True)

class Shows(db.Model):
    __tablename__ = "shows"
    serial = db.Column(db.Integer,primary_key = True)
    venue_name = db.Column(db.String)
    showname = db.Column(db.String)
    rating = db.Column(db.String)
    timing = db.Column(db.String)
    tags = db.Column(db.String)
    price = db.Column(db.Integer)
    location = db.Column(db.String)
    place = db.Column(db.String)
    capacity = db.Column(db.Integer )
    newrate = db.Column(db.String)

class Userdash(db.Model):
    __tablename__ = "userdash"
    id = db.Column(db.String,primary_key = True)
    title = db.Column(db.String)
    rating = db.Column(db.String)
    rated = db.Column(db.String)
    genere = db.Column(db.String)
    poster = db.Column(db.String)
    plot = db.Column(db.Integer)
    language = db.Column(db.String)
    newrate = db.Column(db.Integer)


@app.route('/',methods = ['Post','GET'])
def index():
    return render_template("index.html")

@app.route('/adminlogin',methods=['POST','GET'])
def admin():
    print("admin")
    adminfound = False
    if(request.method =='POST'):
        print("posted")
        u = request.form['username']
        p = request.form['password']
        Admin_input = Admin(username = u, password = p)
        s = Admin.query.all()
        for e in s:
            if(e.username==u and e.password==p):
                print("adminfound")
                adminfound = True
                break
            else:adminfound = False
        if(adminfound == False):
            flash("!! Invalid username or password. Retry")
            return render_template("adminlogin.html",s = Admin.query.all())
        else:
            return redirect("http://127.0.0.1:5000/admindashboard",code = 302)
    else:
        return render_template("adminlogin.html")


@app.route('/admindashboard',methods = ['POST','GET','DELETE'])
def userdashboard():
    print("admindashboard")
    
    if request.method == 'POST':  
        print("post")     
        try:
            print("tried")
            button = request.form['button']
        except:
            print("excepted")
            button = request.form['delete']
            print(button)
            print("deleting........")
                
            table = Movies.query.all()
            print(button)
            lst.remove(button)
            print(lst)
            ventable = Venues.query.all()
            for e in ventable:
                if e.venue_name == button:
                    db.session.delete(e)
                    db.session.commit()
            for e in table:
                if e.venue_name == button:
                    db.session.delete(e)
                    db.session.commit()
                    return render_template("admindashboard.html",table = Movies.query.all() )

        if button == 'editvenue':
            print("editvenue")
            return redirect("http://127.0.0.1:5000/editvenue")

        if button == 'addvenue':
            print("button 1")
            return render_template('venueadder.html')

        if button == 'save venue':
            print("button 2")
            v = request.form['venuename']
            
            if(v in lst):
                flash("venue already exists !!")
                return render_template("venueadder.html")
            p = request.form['palce']
            l = request.form['location']
            c = request.form['capacity']
            

            lst.append(v)
            table2 = Venues(venue_name = v,place = "p",location = l,capacity = c)
            db.session.add(table2)
            db.session.commit()
            table = Movies(venue_name = v, place = p, location = l, capacity = c,
            id = "1",title = ".",poster = ".",release_date = ".",plot = ".",timing = ".")
            db.session.add(table)
            db.session.commit()
            print("here")
            return redirect('/admindashboard')

        if button == 'all show':
            print("all show")

            return render_template("shows.html",table = Movies.query.all())

    else:
        print("else")
        return  render_template("admindashboard.html",table = Movies.query.all())

@app.route('/editvenue/<venuename>', methods = ['POST','GET','UPDATE'])
def editvenue(venuename):
    
    if request.method == 'POST':
        print(venuename)
        print("venue editor post")
        but = request.form['button']
        v = request.form['venuename']
        p = request.form['palce']
        l = request.form['location']
        c = request.form['capacity']
        
        record = Venues.query.filter_by(venue_name = venuename).all()
        for i in record:
            i.venue_name=v
            i.place=p
            i.location=l
            i.capacity=c
            try:
                lst.append(v)
                db.session.commit()
            except:
                flash("Venue already exists")
                return render_template("venueeditor.html",venuename = venuename)
        record = Movies.query.filter_by(venue_name = venuename).all()
        for i in record:
            i.venue_name=v
            i.place=p
            i.location=l
            i.capacity=c
            db.session.commit()
        lst.append(v)

        return redirect("/admindashboard")
    else:
        print("venue editor else")
        return render_template("venueeditor.html",venuename = venuename)


timing = [[]]
tags = [[]]
price = [[]]

@app.route('/shows/<venue_name>/<i>',methods = ['POST',"GET"])
def shows(venue_name,i):
    print("in shows function................")
    table = Shows.query.all()
    length = len(table)
    if request.method =='POST':
        print("post in shows ............")
        button = request.form['button']
        if button == 'add show':
            print("adding shows.........")
            return render_template("showadder.html",venue_name = venue_name,i=i)
            
        if button == "edit":
            print("edit show")
            return redirect(f"http://127.0.0.1:5000/editshows/{i}",code = 302)

        if button == "delete":
            print("delete shows")
            table = Shows.query.all()
            print(i)
            for e in table:
                if(e.serial == int(i)):
                    print("hehe")
                    db.session.delete(e)
                    db.session.commit()
            l = len(table)
            table = Shows.query.all()
            return redirect(f"/shows/{venue_name}/{i}")
        if button == "save show":
            table = Movies.query.all()
            print("saving show.......")
            n = (request.form['showname'])
            r = request.form['rating']
            t = request.form['timing']
            g = request.form['tags']
            p = request.form['price']
            forcap = Venues.query.filter_by(venue_name = venue_name).all()
            for e in forcap:
                if e.venue_name == venue_name:
                    c = e.capacity

            title = n.replace(" ","%20")
            url1 = f"https://www.omdbapi.com/?apikey=add_your_api_key={title}"
            response = urllib.request.urlopen(url1)
            data = response.read()
            jsonData = json.loads(data)

            
            try:
                table = Shows(venue_name = venue_name,showname = jsonData['Title'],rating = r,timing = t,tags = g,price = p,capacity = c)
                db.session.add(table)
                db.session.commit()
                table = Shows.query.all()
            except: return "No Movie With This Name Check Spelling Or Try Another One"


            timing = t
            price = p
            x = False

            print(movies)
            print(jsonData["Title"])
            if jsonData["Title"] not in movies:
                try:
                    print("in try")
                    api = Userdash(id = jsonData['imdbID'], title = jsonData['Title'], 
                    rating = jsonData["imdbRating"], rated = jsonData['Rated'], genere = jsonData['Genre'], 
                    poster = jsonData['Poster'], plot = jsonData['Plot'])
                    db.session.add(api)
                    x = True
                    movies.append(jsonData["Title"])
                    print("why try ..............")
                    db.session.commit()
                    
                except:
                    print("not")
                    flash("movie not found. please check the spelling")

        l = len(table)
        print(l)
        try:
            return render_template("shows.html",venue_name = venue_name,i = i,table = table,l=  length)
        except:
            return render_template("rough.html",venue_name = venue_name)
        return redirect(f"http://127.0.0.1:5000/shows/{venue_name}",code = 302)
    else:
        print("else of shows")
        return render_template("shows.html",venue_name = venue_name,i=i, table = table,l = length)

@app.route('/editshows/<i>', methods = ['POST','GET'])
def editshow(i):
    print("in show editor function.......")
    if request.method == "POST":

        print("show editor post")
        n = request.form['showname']
        r = request.form['rating']
        t = request.form['timing']
        g = request.form['tags']
        p = request.form['price']

        table = Shows.query.all()
        for e in table:
            if(e.serial == int(i)):
                e.showname = n
                e.rating = r
                e.timing = t
                e.tags = g
                e.price = p
            
            v = e.venue_name
            db.session.commit()
        title = n.replace(" ","%20")
        url1 = f"https://www.omdbapi.com/?apikey=add_your_api_key={title}"
        response = urllib.request.urlopen(url1)
        data = response.read()
        jsonData = json.loads(data)
        print(jsonData['Title'])
        
        try:
            api = Userdash(id = jsonData['imdbID'], title = jsonData['Title'], 
            rating = jsonData["imdbRating"], rated = jsonData['Rated'], genere = jsonData['Genre'], 
            poster = jsonData['Poster'], plot = jsonData['Plot'])
            db.session.add(api)
            db.session.commit()

            print("well tried.........")
        except:
            db.session.rollback()
            print("didn't updated")

        l = len(table)
        print(v)
        return render_template("shows.html", venue_name = v, table = table, i=i, l= l)
    else:
        return render_template("editshows.html",i = i)

@app.route('/userlogin',methods=['POST','GET'])
def user():
    try:
        print("user1")
        userfound = False
        if(request.method == 'POST'):
            u = request.form['username']
            p = request.form['password']
            t = ""
            user_input = User(username = u, password = p)
            s = User.query.all()
            for e in s:
                if(e.username==u and e.password==p):
                    print("userfound")
                    userfound = True
                    break
                else:userfound = False
            if(userfound == False):
                flash("Invalid username or password.\n\n Register if you're new user")
                return render_template("userlogin.html",s = s)
            
            print("almost there")
            
            return redirect(f'http://127.0.0.1:5000/userdash/{u}', code=302)
        else:
            return render_template("userlogin.html")
    except:
        print("user2")
        return render_template("rough.html")


@app.route('/register',methods=['POST','GET'])
def register():
    userfound = False
    s = User.query.all()
    if(request.method == 'POST'):
        print("posted")
        u = request.form['username']
        p = request.form['password']
        p2 = request.form['password2']
        t = ""
        user_input = User(username = u, password = p,towatch = t)
        for e in s:
            if(e.username==u):
                print("userfound")
                userfound = True
                break
        if(userfound==True):
            print("flash")
            flash("user already exists.\n go back to login")
            return render_template("register.html",p=p,p2=p2,found = userfound)
        if(p!=p2):
            print("wrong password")
            flash("passwords don't match. Please enter the password again")
            return render_template("register.html")
        db.session.add(user_input)
        db.session.commit()
        print("this1")
        return redirect('http://127.0.0.1:5000/userlogin')
    else:
        print("this2")
        return render_template("register.html",s=s,p=0,p2=0)


@app.route('/userdash/<username>',methods=['POST','GET'])
def userdash(username):
    lst = []
    lst2 = []
    s = Userdash.query.all()
    shows = Shows.query.all()
    count = 0

    if(request.method == "POST"):
        search=request.form['search_input']
        search_by=request.form['search_by']

        if search_by=='movie':
            q = Userdash.query.filter_by(title = search).all()
            return render_template("userdashboard.html", s = q,shows = shows,username = username)

        elif search_by=='venue':
            q = Shows.query.filter_by(venue_name = search).all()
            for e in q:
                lst.append(e.showname)
            lst = set(lst)
            for e in lst:
                lst2.append(Userdash.query.filter_by(title = e).first())
            
            return render_template("userdashboard.html", s = lst2,shows = shows,username = username)
        elif search_by=='tags':
            lst3 = []
            q = Userdash.query.all()
            for e in q:
                k = e.genere.split(",")
                print(k)
                for f in k:
                    if f == search:
                        lst3.append(Userdash.query.filter_by(title = e.title).first())
            print(lst3)
            return render_template("userdashboard.html", s = lst3,shows = shows,username = username)

        elif search_by=='rating':
            q = Userdash.query.filter_by(rating = search).all()
            return render_template("userdashboard.html", s = q,shows = shows,username = username)

    else:
        return render_template("userdashboard.html",s=s,shows = shows,username = username,count = 0)

@app.route('/booking/<i>/<username>',methods = ["POST","GET"])
def booking(i,username):
    
    data = Shows.query.filter_by(serial = i).first()
    x = data.capacity
    venue_name = data.venue_name
    timing = data.timing
    showname = data.showname
    price = data.price
    print(x,venue_name,timing,showname,price)

    if request.method == 'POST':
        print("post")
        y = int(x)-int(request.form['number'])
        if y<=-1:
            print("flash")
            x = x
            flash("Sorry!! No enough seats left.")
            return render_template("booking.html",data = data,x = x,showname = showname,venue_name = venue_name,timing = timing,price = price,i = i,username = username)
        else:
            left = Shows.query.filter_by(serial= i).all()
            for e in left:
                e.capacity = y
                db.session.commit()
        x = y

        li = User.query.filter_by(username = username).all()
        for e in li:
            e.towatch += str(i)+","
            db.session.commit()
        flash("seat booked")
        return render_template("booking.html",data = data,x = x,showname = showname,venue_name = venue_name,timing = timing,price = price,i = i,username = username)


    return render_template("booking.html",data = data,x = x,showname = showname,venue_name = venue_name,timing = timing,price = price,i = i,username = username)

@app.route('/booked/<username>',methods = ['POST','GET'])
def booked(username):

    moviename = []
    rate2 =""
    u = User.query.filter_by(username = username).first()
    print(u)
    cj = u.towatch
    c = cj.replace(" ", "")
    print(c)
    z = c.split(",")
    print(z)
    z.pop()
    print(z)
    a = set(z)
    print(type(a))
    print(a)
    s = Shows.query.all()
    for e in a:
        g = Shows.query.filter_by(serial = e).all()
        for f in g:
            print(f.showname)
            moviename.append(f.showname)
    print(moviename)

    if request.method == "POST":
        print("posted")
        showname = request.form["button"]
        rate = request.form[showname]

        addrate = Userdash.query.all()
        for e in addrate:
            if e.title == showname and e.newrate == None:
                e.newrate = "0"
        for e in addrate:
            if e.title == showname:
                e.newrate += rate
                db.session.commit()
        print(showname)
        print(rate)

        return render_template("rate.html",u = u,a = a,s=s,username = username)
    else:
        return render_template("rate.html",u = u,a = a,s=s,username = username)

@app.route('/test', methods = ['POST',"GET"])
def test():
    print("in test...............")
    if request.method == 'POST':
        print("in post")
        x = request.form['search_input']
        y = request.form['']
        print(x)
        return x
    return print("select ")


@app.route('/summary', methods=['POST','GET'])
def submit():
    print("in summary ....................")
    rate = []
    moviename = []
    movie = Userdash.query.all()
    for e in movie:
        name = e.title
        moviename.append(name)
        if e.newrate == None:
            data = "0"
        else:
            data = e.newrate
        l = len(data)
        sum = 0
        for f in data:
            sum += int(f)
        avg = int(sum/l)
        rate.append(avg)
        lst = [1,2,3,4,5,6,7,8,9,10]
        plt.figure().set_figheight(18)
        plt.xticks(rotation=90)
        plt.bar(moviename, rate, width = 0.8, color = ['purple', 'black'])
        
        plt.xlabel('x - axis')
        plt.ylabel('y - axis')
        plt.title('My bar chart!')
        plt.savefig(r'static\img.png')

        plt.close()

    return render_template("summary.html")

if __name__ == '__main__':
	app.run(debug = True)