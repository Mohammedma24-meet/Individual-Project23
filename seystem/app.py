from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


config = {
  "apiKey": "AIzaSyBPXC-YUNjgHx3CbP1kXdwNFY7pEXX5dOc",
  "authDomain": "tha-good-chef-fa8b1.firebaseapp.com",
  "projectId": "tha-good-chef-fa8b1",
  "storageBucket": "tha-good-chef-fa8b1.appspot.com",
  "messagingSenderId": "699692664128",
  "appId": "1:699692664128:web:7dfe59a7f3362e39fee6a5",
  "measurementId": "G-1BRZV2PF0K",
  "databaseURL": "https://tha-good-chef-fa8b1-default-rtdb.europe-west1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

    


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        username = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "username": username,
            "bio": bio,
            }
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")


@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/post_home')
def post_home():
    return render_template("post_home.html")





@app.route('/post_food', methods=['GET', 'POST'])
def post_food():
    if request.method == 'POST':
        Title = request.form['Title']
        Text = request.form['Text']
        image = request.form['image']
        UID = login_session['user']['localId']

        try:
            tweet = {"Title": Title,
                      "Text": Text, 
                      "image": image,
                      "UID" : UID}
            db.child("Tweets").push(tweet)
            return redirect(url_for('food'))
        except:
            print("Couldn't add tweet")
   


    return render_template("post_food.html")




@app.route('/post_fast_food', methods=['GET', 'POST'])
def post_fast_food():
    if request.method == 'POST':
        Title2 = request.form['Title2']
        Text2 = request.form['Text2']
        image2 = request.form['image2']
        UID = login_session['user']['localId']

        try:
            tweet2 = {"Title2": Title2,
                      "Text2": Text2, 
                      "image2": image2,
                      "UID" : UID}
            db.child("fast").push(tweet2)
            return redirect(url_for('fast_food'))
        except:
            print("Couldn't add tweet")
   


    return render_template("post_fast_food.html")

@app.route('/post_cakes', methods=['GET', 'POST'])
def post_cakes():
    if request.method == 'POST':
        Title4 = request.form['Title4']
        Text4 = request.form['Text4']
        image4 = request.form['image4']
        UID = login_session['user']['localId']

        try:
            tweet3 = {"Title4": Title4,
                      "Text4": Text4, 
                      "image4": image4,
                      "UID" : UID}
            db.child("cakes").push(tweet3)
            return redirect(url_for('cakes'))
        except:
            print("Couldn't add tweet")
   


    return render_template("post_cakes.html")
    
    

@app.route('/food')
def food():
    tweet1=db.child("Tweets").get().val()
    return render_template("food.html", tweet1=tweet1)


@app.route('/fast_food')
def fast_food():
    tweet11=db.child("fast").get().val()
    return render_template("fast_food.html", tweet11=tweet11)


@app.route('/cakes')
def cakes():
    tweet12=db.child("cakes").get().val()
    return render_template("cakes.html", tweet12=tweet12)




if __name__ == '__main__':
    app.run(debug=True)


