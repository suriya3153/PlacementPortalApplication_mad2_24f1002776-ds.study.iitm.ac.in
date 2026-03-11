from .database import db
from datetime import datetime


# ==============================
# USER TABLE (COMMON LOGIN TABLE)
# ==============================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin / company / student
    is_active_account = db.Column(db.Boolean, default=True)

    # Relationships
    student_profile = db.relationship("Student", backref="user", uselist=False)
    company_profile = db.relationship("Company", backref="user", uselist=False)


# ==============================
# STUDENT PROFILE TABLE
# ==============================
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15))
    course = db.Column(db.String(100))
    resume = db.Column(db.String(255))  # file path

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "Application",
        backref="student",
        cascade="all, delete"
    )


# ==============================
# COMPANY PROFILE TABLE
# ==============================
class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(150))

    approval_status = db.Column(db.String(20), default="Pending")
    # Pending / Approved / Rejected / Blacklisted

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    drives = db.relationship(
        "PlacementDrive",
        backref="company",
        cascade="all, delete"
    )


# ==============================
# PLACEMENT DRIVE TABLE
# ==============================
class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)

    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility = db.Column(db.String(255))
    application_deadline = db.Column(db.DateTime)

    status = db.Column(db.String(20), default="Pending")
    # Pending / Approved / Closed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship(
        "Application",
        backref="drive",
        cascade="all, delete"
    )


# ==============================
# APPLICATION TABLE
# ==============================
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)

    application_date = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.String(20), default="Applied")
    # Applied / Shortlisted / Selected / Rejected

    # Prevent duplicate applications
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="unique_application"),
    )