from flask import Flask,render_template,url_for,redirect,session


app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/student/dashboard")
def student_dashboard():
    return render_template("student/dashboard.html")

@app.route("/student/internship")
def internship():
    return render_template("student/internship.html")

@app.route("/student/myapplication")
def student_application():
    return render_template("student/myapplication.html")

@app.route("/student/profile")
def student_profile():
    return render_template("student/profile.html")



if __name__ =="__main__":
    app.run(debug=True)