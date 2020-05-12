from flask import Flask, render_template,request
import sqlite3 as sql


app = Flask(__name__)


con = sql.connect("users.db")
cur = con.cursor()
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/newuser',methods = ['POST', 'GET'])
def newuser():
    if request.method == 'POST':

        firstname = request.form['fnm']
        lastname = request.form['lnm']
        username = request.form['unm']
        email = request.form['email']
        password = request.form['password']
        re_password = request.form['repassword']
        
        with sql.connect("users.db") as con:
            cur = con.cursor()
            if password == re_password:
                records = cur.execute("SELECT * from users").fetchall()
                
                id=1
                if id != 0:
                    id = len(records) + 1
                else:
                    id=1
                
                cur.execute("INSERT INTO users (id,username,First_name,Last_name,email,password) VALUES (?,?,?,?,?,?)",(id,username,firstname,lastname,email,password) )
                con.commit()
                
                msg = "user created"
                return render_template("login.html",msg = msg)
            else:
                msg = "Please provide same password in both fields"
                return render_template("404.html",msg = msg)
      
@app.route('/signin',methods = ['POST', 'GET'])
def signin():
    if request.method == 'POST':
        signin_username = request.form['lusername']
        signin_password = request.form['lpassword']
        
        with sql.connect("users.db") as con:
            cur = con.cursor()
            signin_data=cur.execute("SELECT username, password FROM users").fetchall()
            pro_signin_data = (signin_username,signin_password)
            if signin_data==pro_signin_data:
                msg = signin_username
                return render_template("dashboard.html",msg = msg)
            else:
                msg="Invalid credantials"
                return render_template("login.html",msg = msg)   

con.close()
     
if __name__ == "__main__":
    app.run(debug=True)