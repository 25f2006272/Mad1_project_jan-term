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
    # if not roles.query.filter_by(role="student").first():
    #     db.session.add(roles(role="student"))

    # if not roles.query.filter_by(role="company").first():
    #     db.session.add(roles(role="company"))

    # if not roles.query.filter_by(role="admin").first():
    #     db.session.add(roles(role="admin"))


    admin_user= admin.query.filter_by(email='admin@gmail.com').first()

    if not admin_user:
        admin_user= admin(
            name="Admin",
            email="admin1@gmail.com",
            password="admin12345",
        
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
                session['role']=role

                if user.status == "False":
                    flash("You are blacklisted!")
                    return redirect('/login')
                
                elif user.password!=password and user.email!=email:
                    flash("Invalid email or password")
                    return render_template("login.html",role=role)

            
                else:
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
                session['role']=role
                if user.is_approved==False:
                    flash('Your account is not approved')
                    return render_template("login.html",role=role)
                
                elif user.password!=password and user.email!=email:
                    flash("Invalid email or password")
                    return render_template("login.html",role=role)
                else:
                    flash("Login succesful")
                    return redirect(url_for("company_dashboard",role=role))

            elif user is None:
                flash("Signup first")
                return redirect(url_for('signup', role=role))
            else:
                flash("Invalid email or password")
                return render_template("login.html",role=role)
            

        elif role=="admin":
            


            email=request.form.get('email')
            password=request.form.get('password')

 
            user=admin.query.filter_by(email="admin1@gmail.com").first()
            if user:
                if user.password==password and user.email==email:
                    session['user_id']=user.id
                    session['role']=role
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
                 
                )
                db.session.add(new_student)
                db.session.commit()
                flash('Now you can login')
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
                    
                    website=website
                )
                db.session.add(new_company)
                db.session.commit()
                flash('Now you can login')
                return redirect(url_for("login",role=role))

            if user:
                flash('You have already an account')
                return redirect(url_for("login",role=role))
        




    return render_template("signup.html",role=role)

@app.route("/student/dashboard",methods=['GET','POST'])
def student_dashboard():
    student_id=session['user_id']
    studentdetail=students.query.get(student_id)

    total_drive=drive.query.count()
    applied=application.query.filter_by(studennt_id=student_id).count()
    selected=application.query.filter_by(studennt_id=student_id,status="Applied").count()

    drives=drive.query.all()

    return render_template("student/dashboard.html",studentdetail=studentdetail,total_drive=total_drive,applied=applied,selected=selected,drives=drives)

@app.route("/student/internship")
def internship():
    drives=drive.query.all()
    return render_template("student/internship.html",drives=drives)

@app.route("/student/myapplication")
def student_application():
    student_id=session['user_id']
    allapplication=application.query.filter_by(studennt_id=student_id).all()

    if allapplication :
        return render_template("student/myapplication.html")

    else:
        return render_template("student/myapplication.html")
    

@app.route("/student/profile",methods=['GET','POST'])
def student_profile():
    if request.method == 'POST':
        user_id = session['user_id']

        user =students.query.get(user_id)

        user.name = request.form.get('name')
        user.phone = request.form.get('phone')
        user.branch = request.form.get('branch')
        user.grad_year = request.form.get('graduation')
        user.skills = request.form.get('skill')
        file = request.files.get('resume')
        if file and file.filename != "":
            filename = file.filename
            file.save("static/resume/"+filename)
            user.resume = filename

        db.session.commit()

        flash("Profile Updated Successfully")
        return redirect(url_for('student_dashboard'))

    return render_template("student/profile.html")



# for company

@app.route("/company/dashboard",methods=['GET','POST'])
def company_dashboard():
    company_id=session['user_id']
    companydetail=company.query.get(company_id)

    total_drive=drive.query.count()
    total_application=application.query.count()
    stats=company.query.filter_by(id=company_id)



    all_drives = drive.query.filter_by(company_id=company_id).all()


    return render_template("company/dashboard.html",companydetail=companydetail,total_drive=total_drive,total_application=total_application,stats=stats,all_drives=all_drives)

@app.route("/company/profile",methods=['GET','POST'])
def company_profile():
    if request.method == 'POST':
        user_id = session['user_id']

        user =company.query.get(user_id)

        name = request.form.get('name')
        hr = request.form.get('hr_contact')
        website = request.form.get('website')
        description = request.form.get('description')
        address = request.form.get('address')

        user.company_name =name
        user.hr_contact =hr
        user.website =website
        user.description =description
        user.address =address
        db.session.commit()

        flash("Profile Updated Successfully")
        return redirect(url_for('company_dashboard'))
    return render_template("company/profile.html")

@app.route("/company/internship",methods=['GET','POST'])
def create_internship():
    if request.method == 'POST':
        user_id = session['user_id']

        job_title= request.form.get('job_title')
        job_description= request.form.get('job_description')
        criteria= request.form.get('criteria')
        salary_package= request.form.get('salary_package')
        location= request.form.get('location')
        application_deadline= request.form.get('application_deadline')

        deadline = datetime.strptime(request.form.get("application_deadline"), "%Y-%m-%d").date()
        new_drive=drive(
            company_id=user_id,
            job_title=job_title,
            job_description=job_description,
            criteria=criteria,
            salary_package=salary_package,
            location=location,
            application_deadline=deadline

        )
        
        db.session.add(new_drive)
        db.session.commit()

        flash("Drive Created Successfully")
        return redirect(url_for('company_dashboard'))
    return render_template("company/create_internship.html")




#for Admin

@app.route("/admin/dashboard")
def admin_dashboard():
    total_students=students.query.count()
    total_company=company.query.count()
    total_application=application.query.count()
    total_drives=drive.query.count()

    return render_template("admin/dashboard.html",total_students=total_students,total_company=total_company,total_application=total_application,total_drives=total_drives)

@app.route("/admin/student")
def admin_student():
    search=request.args.get('search')
    if search:
        student=students.query.filter(
            (students.name.contains(search))|
            (students.email.contains(search))|
            (students.phone.contains(search))
        ).all()

    else:
        student=students.query.all()


    return render_template("admin/students.html", student=student)


@app.route("/admin/student/block/<int:id>")
def block_student(id):
    student=students.query.get(id)
    student.status=False
    db.session.commit()
    return redirect('/admin/student')
@app.route("/admin/student/unblock/<int:id>")
def unblock_student(id):
    student=students.query.get(id)
    student.status=True
    db.session.commit()
    return redirect('/admin/student')


@app.route("/admin/company")
def admin_company():
    search=request.args.get('search')
    if search:
        companies=company.query.filter(
            (company.company_name.contains(search))|
            (company.email.contains(search))
            ).all()

    else:
        companies=company.query.all()
    return render_template("admin/company.html",companies=companies)


@app.route("/admin/company/block/<int:id>")
def block_company(id):
    companies=company.query.get(id)
    companies.status=False
    db.session.commit()
    return redirect("/admin/company")

@app.route("/admin/company/unblock/<int:id>")
def unblock_company(id):
    companies=company.query.get(id)
    companies.status=True
    db.session.commit()
    return redirect("/admin/company")

@app.route("/admin/company/approve/<int:id>")
def approve_company(id):
    companies = company.query.get(id)
    companies.is_approved = True
    db.session.commit()
    flash('Approved succesfully')
    return redirect("/admin/company")




@app.route("/admin/internship")
def admin_internship():
    drives=drive.query.all()
    return render_template("admin/admin_internship.html",drives=drives)

@app.route("/admin/application")
def admin_application():
    applications=application.query.all()
    return render_template("admin/application.html",applications=applications)


@app.route("/admin/applications/approve/<int:id>",methods=['GET','POST'])
def approve_application(id):
    Application = drive.query.get(id)
    if Application:
        Application.status = "Approved"
        db.session.commit()
    
    return redirect("/admin/internship")


@app.route("/admin/applications/reject/<int:id>",methods=['GET','POST'])
def reject_application(id):
    Application = drive.query.get(id)
    if Application:
        Application.status = "Rejected"
        db.session.commit()
    return redirect("/admin/internship")


@app.route("/student/internship/apply/<int:id>",methods=["POST","GET"])
def apply(id):
    user_id=session['user_id']
    s=application.query.filter_by(studennt_id=user_id,drive_id=id).first()

    if s:
        flash ("you are already applied")
    else:
        app=application(studennt_id=user_id,
                        drive_id=id,
                        status="Applied"
                        
                        )
        db.session.add(app)
        db.session.commit()
        flash("Applied successfully")
    
    return redirect("/student/dashboard")


@app.route("/company/da/")
def all_drive():
    company_id = session["company_id"]
    all_drives = drive.query.filter_by(company_id=company_id).all()
    return redirect("/company/all_drive",all_drives=all_drives)


@app.route("/company/delete_drive/<int:id>")
def delete_drive(id):

    drives = drive.query.get(id)

    if drives:
        db.session.delete(drives)
        db.session.commit()
        flash("Drive deleted successfully")

    return redirect("/company/dashboard")




if __name__ =="__main__":
    app.run(debug=True)