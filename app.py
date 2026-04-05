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
    if not roles.query.filter_by(role="student").first():
        db.session.add(roles(role="student"))

    if not roles.query.filter_by(role="company").first():
        db.session.add(roles(role="company"))

    if not roles.query.filter_by(role="admin").first():
        db.session.add(roles(role="admin"))


    admin_user= admin.query.filter_by(email='admin@gmail.com').first()

    if not admin_user:
        admin_user= admin(
            name="Admin",
            email="admin1@gmail.com",
            password="admin12345",
            role_id=3
        )
        db.session.add(admin_user)


    db.session.commit()


@app.route("/")
def home():
    return render_template("home.html")



@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):
    if request.method == "POST":
        # username = request.form.get("username")
        # password = request.form.get("password")
        if role=="student":
            email=request.form.get('email')
            password=request.form.get('password')

            user=students.query.filter_by(email=email,password=password).first()

            if user:
                session['user_id']=user.id
                session['role']=user.role_id
               
                flash("Login succesful")
                return redirect(url_for("student_dashboard",role=role))
            elif user is None:
                flash("Signup first")
                return redirect(url_for('signup', role=role))
            else:
                flash("Invalid email or password")
                return render_template("login.html",role=role)
            
        elif role=="company":

            email=request.form.get('email')
            password=request.form.get('password')

            user=company.query.filter_by(email=email,password=password).first()

            if user:
                session['user_id']=user.id
                session['role']=user.role_id
               
                flash("Login succesful")
                return redirect(url_for("company_dashboard",role=role))
            elif user is None:
                flash("Signup first")
                return redirect(url_for('signup', role=role))
            else:
                flash("Invalid email or password")
                return render_template("login.html",role=role)
            
            return render_template("company/dashboard.html",role=role)
        elif role=="admin":
            


            email=request.form.get('email')
            password=request.form.get('password')

 
            user=admin.query.filter_by(email="admin1@gmail.com").first()
            if user:
                if user.password==password and user.email==email:
                    session['user_id']=user.id
                    session['role']=user.role_id
                    flash('Welcome to the admin dashboard')
                    return render_template("admin/dashboard.html",role=role)
                else :
                    flash('Invalid email or password')


    return render_template("login.html", role=role)





@app.route("/signup/<role>",  methods=["POST","GET"])
def signup(role):
    if request.method=="POST":
        if role=='student':
            name=request.form.get('name')
            email=request.form.get('email')
            password=request.form.get('password')
            phone=request.form.get('phone')


            user=students.query.filter_by(name=name,email=email).first()
            if user is None:
                new_student=students(
                    name=name,
                    email=email,
                    password=password,
                    phone=phone,
                    role_id=1
                )
                db.session.add(new_student)
                db.session.commit()
                # flash('Now you can login')
                return redirect(url_for("login",role=role))

            if user:
                flash('You have already an account')
                return redirect(url_for("login",role=role))
            


    #signup for company
        if role=='company':
            company_name=request.form.get('name')
            email=request.form.get('email')
            password=request.form.get('password')
            hr_contact=request.form.get('phone')
            website=request.form.get('website')


            user=company.query.filter_by(company_name=company_name,email=email).first()
            if user is None:
                new_company=company(
                    company_name=company_name,
                    email=email,
                    password=password,
                    hr_contact=hr_contact,
                    role_id=2,
                    website=website
                )
                db.session.add(new_company)
                db.session.commit()
                # flash('Now you can login')
                return redirect(url_for("login",role=role))

            if user:
                flash('You have already an account')
                return redirect(url_for("login",role=role))
        




    return render_template("signup.html",role=role)

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