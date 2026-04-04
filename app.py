from flask import Flask,render_template,url_for,redirect,session,request,flash
from controller.database import *


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/// database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key="Secretxyz21"
# db = SQLAlchemy(app)
db.init_app(app) 
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("home.html")


# @app.route('/signup', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         password = request.form.get('password')
#         registered = students.query.filter_by(name=name).first()
#         if not registered:
#             name= students(name=name, email=email, password=password)
#             db.session.add(name)
#             db.session.commit()
#         return redirect('/login')
#     return render_template('signup.html')





# @app.route("/login")
# def login():
#     return render_template("login.html")

@app.route("/signup",  methods=["POST","GET"])
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



# for company

@app.route("/company/dashboard")
def company_dashboard():
    return render_template("company/dashboard.html")

@app.route("/company/profile")
def company_profile():
    return render_template("company/profile.html")

@app.route("/company/internship")
def create_internship():
    return render_template("company/create_internship.html")




#for Admin

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")

@app.route("/admin/student")
def admin_student():
    return render_template("admin/students.html")

@app.route("/admin/company")
def admin_company():
    return render_template("admin/company.html")

@app.route("/admin/internship")
def admin_internship():
    return render_template("admin/admin_internship.html")

@app.route("/admin/application")
def admin_application():
    return render_template("admin/application.html")










if __name__ =="__main__":
    app.run(debug=True)