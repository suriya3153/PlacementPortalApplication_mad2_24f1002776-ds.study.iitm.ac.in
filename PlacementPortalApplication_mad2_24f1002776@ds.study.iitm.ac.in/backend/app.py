from flask import Flask, request, jsonify
from flask_cors import CORS




from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token,JWTManager
from application.database import db
from application.models import User, Student, Company, PlacementDrive, Application

from sqlalchemy import func
from datetime import datetime 
app = Flask(__name__)


app.config["SECRET_KEY"] = "simplekey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///placement.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app.config["JWT_SECRET_KEY"] = "my_very_long_32+_character_secret_key_here"


CORS(app)
db.init_app(app)


jwt = JWTManager(app)



with app.app_context():

    db.create_all()

    
    admin = User.query.filter_by(email="admin@admin.com").first()

    if not admin:

        new_admin = User(
            email="admin@admin.com",
            password="admin123",
            role="admin"
        )

        db.session.add(new_admin)
        db.session.commit()

        
    


# -----------------------------
# Run Server
# -----------------------------
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask import request, jsonify


from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads/resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/register/student", methods=["POST"])
def register_student():
    
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    course = request.form.get("course")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password)

   
    user = User(
        email=email,
        password=hashed_password,
        role="student"
    )
    db.session.add(user)
    db.session.commit()

    
    resume_filename = None
    if 'resume' in request.files:
        file = request.files['resume']
        if file.filename.endswith('.pdf'):
            resume_filename = secure_filename(f"user_{user.id}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, resume_filename))

    
    student = Student(
        user_id=user.id,
        name=name,
        phone=phone,
        course=course,
        resume=resume_filename
    )
    db.session.add(student)
    db.session.commit()

    return jsonify({"message": "Student registered successfully!"})


@app.route("/api/register/company", methods=["POST"])
def register_company():
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(data['password'])

    # Create user
    user = User(
        email=data['email'],
        password=hashed_password,
        role="company"
    )
    db.session.add(user)
    db.session.commit()

    # Create company profile
    company = Company(
        user_id=user.id,
        company_name=data['company_name'],
        hr_contact=data.get('hr_contact'),
        website=data.get('website'),
        approval_status="Pending"
    )
    db.session.add(company)
    db.session.commit()

    return jsonify({"message": "Company registered successfully!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # find user using email
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    if not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    # Optional: check if account is active
    if hasattr(user, "is_active_account") and not user.is_active_account:
        return jsonify({"message": "Account disabled"}), 403

    # create JWT token
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "data": {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "access_token": access_token
        }
    })

@app.route("/api/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    print(total_students, total_companies, total_drives, total_applications)
    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    })



@app.route("/api/admin/students", methods=["GET"])
@jwt_required()
def get_students():
    
    students = Student.query.all()

    data = []

    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "email": s.user.email,
            "phone": s.phone,
            "course": s.course,
            "status": "Active" if s.user.is_active_account else "Blacklisted"
        })

    return jsonify(data)



# STUDENT SEARCH ROUTE


from sqlalchemy import or_

@app.route("/api/admin/students/search", methods=["GET"])
@jwt_required()
def search_students():

    query = request.args.get("q", "")

    students = Student.query.join(User).filter(
        or_(
            Student.name.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%"),
            Student.id.like(f"%{query}%")
        )
    ).all()

    data = []

    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "email": s.user.email,
            "phone": s.phone,
            "course": s.course,
            "status": "Active" if s.user.is_active_account else "Blacklisted"
        })

    return jsonify(data)

@app.route("/api/admin/student/<int:id>", methods=["GET"])
@jwt_required()
def get_student_detail(id):

    student = Student.query.get_or_404(id)

    applications = []

    for a in student.applications:
        applications.append({
            "drive": a.drive.job_title,
            "company": a.drive.company.company_name,
            "status": a.status
        })

    data = {
        "id": student.id,
        "name": student.name,
        "email": student.user.email,
        "phone": student.phone,
        "course": student.course,
        "resume": student.resume,
        "applications": applications
    }

    return jsonify(data)

@app.route("/api/admin/student/<int:id>/block", methods=["PUT"])
@jwt_required()
def block_student(id):

    student = Student.query.get_or_404(id)

    student.user.is_active_account = False

    db.session.commit()

    return jsonify({"message": "Student Blacklisted"})


@app.route("/api/admin/student/<int:id>/activate", methods=["PUT"])
@jwt_required()
def activate_student(id):

    student = Student.query.get_or_404(id)

    student.user.is_active_account = True

    db.session.commit()

    return jsonify({"message": "Student activated"})

@app.route("/api/admin/student/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({"message": "Student Deleted"})








@app.route("/api/admin/companies", methods=["GET"])
@jwt_required()
def get_companies():

    companies = Company.query.all()

    data = []

    for c in companies:
        data.append({
            "id": c.id,
            "company_name": c.company_name,
            "email": c.user.email,
            "status": c.approval_status
        })

    return jsonify(data)


@app.route("/api/admin/company/<int:id>/status", methods=["PUT"])
@jwt_required()
def update_company_status(id):

    company = Company.query.get_or_404(id)

    data = request.get_json()

    new_status = data.get("status")

    if new_status not in ["Approved", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400


    # Prevent duplicate action
    if company.approval_status == new_status:
        return jsonify({
            "message": f"Company already {new_status}"
        }), 400


    company.approval_status = new_status

    db.session.commit()

    return jsonify({
        "message": f"Company {new_status} successfully"
    })


@app.route("/api/admin/drives", methods=["GET"])
def get_drives():

    drives = PlacementDrive.query.all()

    data = []

    for d in drives:

        data.append({
            "id": d.id,
            "job_title": d.job_title,
            "company": d.company.company_name,
            "deadline": str(d.application_deadline),
            "status": d.status
        })

    return jsonify(data)

@app.route("/api/admin/drive/<int:id>/status", methods=["PUT"])
def update_drive_status(id):

    drive = PlacementDrive.query.get_or_404(id)

    data = request.get_json()

    new_status = data.get("status")

    if new_status not in ["Approved", "Closed"]:
        return jsonify({"error": "Invalid status"}), 400

    drive.status = new_status

    db.session.commit()

    return jsonify({
        "message": f"Drive {new_status}"
    })

@app.route("/api/admin/applications", methods=["GET"])
def get_all_applications():
    applications = Application.query.join(Student).join(PlacementDrive).join(Company).all()

    data = []

    for a in applications:
        data.append({
            "id": a.id,
            "student_name": a.student.name,
            "student_email": a.student.user.email,
            "company_name": a.drive.company.company_name,
            "job_title": a.drive.job_title,
            "application_date": a.application_date.strftime("%Y-%m-%d"),
            "status": a.status
        })

    return jsonify(data)




# Helper function to check approval and give JSON view

def check_company_approval(user_id):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        # No company profile
        return None, jsonify({
            "view_page": True,
            "company_status": "Not Found",
            "allowed": False,
            "message": "Company profile not found."
        }), 404

    if company.approval_status != "Approved":
        # Any non-approved status
        status_messages = {
            "Pending": "Your account is pending approval. Please wait for admin verification.",
            "Rejected": "Your account has been rejected. Contact support for more info.",
            "Blacklisted": "Your account is blacklisted. Access denied."
        }
        message = status_messages.get(company.approval_status, "Access denied.")

        return None, jsonify({
            "view_page": True,               
            "company_status": company.approval_status,
            "allowed": False,
            "message": message
        }), 403

    # If approved, return company object and no error
    return company, None, None


# ==============================
# Get company profile
# ==============================
@app.route("/api/company/me", methods=["GET"])
@jwt_required()
def get_my_company():
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    return jsonify({
        "company_name": company.company_name,
        "hr_contact": company.hr_contact,
        "website": company.website,
        "approval_status": company.approval_status
    })


# ==============================
# Company stats
# ==============================
@app.route("/api/company/stats", methods=["GET"])
@jwt_required()
def company_stats():
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    total_drives = len(company.drives)
    total_applicants = sum(len(d.applications) for d in company.drives)
    return jsonify({"drives": total_drives, "applicants": total_applicants})


# ==============================
# My drives
# ==============================
@app.route("/api/company/drives", methods=["GET"])
@jwt_required()
def company_drives():
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    drives = []
    for d in company.drives:
        drives.append({
            "id": d.id,
            "job_title": d.job_title,
            "applicants": len(d.applications),
            "status": d.status
        })
    return jsonify(drives)


# ==============================
# Applications for company drives
# ==============================
@app.route("/api/company/applications", methods=["GET"])
@jwt_required()
def company_applications():
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    applications = []
    for drive in company.drives:
        for a in drive.applications:
            applications.append({
                "id": a.id,
                "student_name": a.student.name,
                "student_email": a.student.user.email,
                "drive_title": drive.job_title,
                "status": a.status,
                "resume": a.student.resume  
            })

    return jsonify(applications)


# ==============================
# Create new drive
# ==============================
@app.route("/api/company/drives", methods=["POST"])
@jwt_required()
def create_drive():
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    data = request.get_json()
    job_title = data.get("job_title")
    job_description = data.get("job_description")
    eligibility = data.get("eligibility")
    deadline = data.get("deadline") 

    if not all([job_title, job_description, eligibility, deadline]):
        return jsonify({"error": "All fields are required"}), 400

    
    try:
        application_deadline = datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    new_drive = PlacementDrive(
        company_id=company.id,
        job_title=job_title,
        job_description=job_description,
        eligibility=eligibility,
        application_deadline=application_deadline,
        status="Pending"
    )

    db.session.add(new_drive)
    db.session.commit()

    return jsonify({
        "message": "Placement drive created successfully",
        "drive_id": new_drive.id
    }), 201

# Update application status

@app.route("/api/company/applications/<int:application_id>/status", methods=["PUT"])
@jwt_required()
def update_application_status(application_id):
    current_user_id = get_jwt_identity()
    company, error_response, status_code = check_company_approval(current_user_id)
    if error_response:
        return error_response, status_code

    
    application = (
        db.session.query(Application)
        .join(PlacementDrive)
        .filter(
            Application.id == application_id,
            PlacementDrive.company_id == company.id
        )
        .first()
    )

    if not application:
        return jsonify({"error": "Application not found"}), 404

    data = request.get_json()
    new_status = data.get("status")
    if new_status not in ["Pending", "Shortlisted", "Selected", "Rejected"]:
        return jsonify({"error": "Invalid status"}), 400

    application.status = new_status
    db.session.commit()

    return jsonify({"message": f"Application status updated to {new_status}"})

# --- STUDENT DASHBOARD ROUTES ---
# ==============================
# Helper function for student status
# ==============================
def check_student_active(user_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return None, jsonify({"error": "Student profile not found"}), 404

    if not student.user.is_active_account:
        return None, jsonify({
            "error": "Your account is inactive. Please contact admin."
        }), 403

    return student, None, None


# ==============================
# Get student profile
# ==============================
@app.route("/api/student/me", methods=["GET"])
@jwt_required()
def get_student_profile():
    current_user_id = get_jwt_identity()
    student, error_response, status_code = check_student_active(current_user_id)
    if error_response:
        return error_response, status_code

    return jsonify({
        "name": student.name,
        "email": student.user.email,
        "phone": student.phone,
        "course": student.course,
        "resume": student.resume
    })


# ==============================
# Available drives for student
# ==============================
@app.route("/api/student/available-drives", methods=["GET"])
@jwt_required()
def get_available_drives():
    now = datetime.utcnow()
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "Approved",
        PlacementDrive.application_deadline >= now
    ).all()

    return jsonify([{
        "id": d.id,
        "company_name": d.company.company_name,
        "job_title": d.job_title,
        "eligibility": d.eligibility,
        "deadline": d.application_deadline.strftime("%Y-%m-%d")
    } for d in drives])


# ==============================
# Get student's applications
# ==============================
@app.route("/api/student/my-applications", methods=["GET"])
@jwt_required()
def get_my_applications():
    current_user_id = get_jwt_identity()
    student, error_response, status_code = check_student_active(current_user_id)
    if error_response:
        return error_response, status_code

    apps = Application.query.filter_by(student_id=student.id).all()
    return jsonify([{
        "id": a.id,
        "job_title": a.drive.job_title,
        "company_name": a.drive.company.company_name,
        "status": a.status,
        "applied_on": a.application_date.strftime("%Y-%m-%d")
    } for a in apps])


# ==============================
# Apply for a drive
# ==============================
@app.route("/api/student/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_for_drive(drive_id):
    current_user_id = get_jwt_identity()
    student, error_response, status_code = check_student_active(current_user_id)
    if error_response:
        return error_response, status_code

    # Check if already applied
    existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
    if existing:
        return jsonify({"error": "You have already applied for this drive"}), 400

    new_app = Application(
        student_id=student.id,
        drive_id=drive_id,
        status="Applied"
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "Application submitted successfully!"}), 201


# ==============================
# Update student profile
# ==============================
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads/resumes'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/api/student/profile/update", methods=["PUT"])
@jwt_required()
def update_student_profile():
    current_user_id = get_jwt_identity()
    student, error_response, status_code = check_student_active(current_user_id)
    if error_response:
        return error_response, status_code

    # Form data
    name = request.form.get("name")
    phone = request.form.get("phone")
    course = request.form.get("course")
    email = request.form.get("email")

    if name: student.name = name
    if phone: student.phone = phone
    if course: student.course = course
    if email: student.user.email = email

    # Resume upload
    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(f"user_{current_user_id}_{file.filename}")
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            student.resume = filename

    db.session.commit()
    return jsonify({"message": "Profile and Resume updated successfully"}), 200
from flask import send_from_directory
UPLOAD_FOLDER = 'uploads/resumes'  # same folder you use for saving resumes

@app.route("/download/<filename>", methods=["GET"])
def download_resume(filename):
    """
    Serve the PDF resume for download.
    `as_attachment=True` forces download instead of opening in browser
    """
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)