from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint

db = SQLAlchemy()


class UserAccount(db.Model):
    """User account model - base for both caregivers and members"""
    __tablename__ = "user_account"

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    given_name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    city = db.Column(db.String)
    phone_number = db.Column(db.String)
    profile_description = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    # Relationships
    caregivers = db.relationship("Caregiver", back_populates="user", cascade="all,delete")
    members = db.relationship("Member", back_populates="user", cascade="all,delete")

    def display_name(self):
        """Return formatted display name"""
        return f"{self.given_name} {self.surname} (ID: {self.user_id})"

    def __repr__(self):
        return f"<UserAccount {self.user_id}: {self.email}>"


class Caregiver(db.Model):
    """Caregiver model - extends user account"""
    __tablename__ = "caregiver"

    caregiver_user_id = db.Column(
        db.Integer, 
        db.ForeignKey("user_account.user_id", ondelete="CASCADE"), 
        primary_key=True
    )
    photo = db.Column(db.String)
    gender = db.Column(db.String)
    caregiving_type = db.Column(db.String, nullable=False)
    hourly_rate = db.Column(db.Numeric(6, 2), nullable=False)
    commission_applied = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship("UserAccount", back_populates="caregivers")
    applications = db.relationship("JobApplication", back_populates="caregiver", cascade="all,delete")
    appointments = db.relationship("Appointment", back_populates="caregiver", cascade="all,delete")

    def __repr__(self):
        return f"<Caregiver {self.caregiver_user_id}: {self.caregiving_type}>"


class Member(db.Model):
    """Member model - extends user account"""
    __tablename__ = "member"

    member_user_id = db.Column(
        db.Integer, 
        db.ForeignKey("user_account.user_id", ondelete="CASCADE"), 
        primary_key=True
    )
    house_rules = db.Column(db.String)
    dependent_description = db.Column(db.String)

    # Relationships
    user = db.relationship("UserAccount", back_populates="members")
    addresses = db.relationship("Address", back_populates="member", cascade="all,delete")
    jobs = db.relationship("Job", back_populates="member", cascade="all,delete")
    appointments = db.relationship("Appointment", back_populates="member", cascade="all,delete")

    def __repr__(self):
        return f"<Member {self.member_user_id}>"


class Address(db.Model):
    """Address model for members"""
    __tablename__ = "address"

    address_id = db.Column(db.Integer, primary_key=True)
    member_user_id = db.Column(
        db.Integer,
        db.ForeignKey("member.member_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    house_number = db.Column(db.String)
    street = db.Column(db.String)
    town = db.Column(db.String)

    # Relationships
    member = db.relationship("Member", back_populates="addresses")

    def full_address(self):
        """Return formatted full address"""
        parts = [self.house_number, self.street, self.town]
        return ", ".join(filter(None, parts))

    def __repr__(self):
        return f"<Address {self.address_id}: {self.full_address()}>"


class Job(db.Model):
    """Job posting model"""
    __tablename__ = "job"

    job_id = db.Column(db.Integer, primary_key=True)
    member_user_id = db.Column(
        db.Integer,
        db.ForeignKey("member.member_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    required_caregiving_type = db.Column(db.String, nullable=False)
    other_requirements = db.Column(db.String)
    date_posted = db.Column(db.Date, nullable=False, default=date.today)

    # Relationships
    member = db.relationship("Member", back_populates="jobs")
    applications = db.relationship("JobApplication", back_populates="job", cascade="all,delete")

    def __repr__(self):
        return f"<Job {self.job_id}: {self.required_caregiving_type}>"


class JobApplication(db.Model):
    """Job application model - links caregivers to jobs"""
    __tablename__ = "job_application"
    __table_args__ = (
        UniqueConstraint("caregiver_user_id", "job_id", name="uq_caregiver_job"),
    )

    job_application_id = db.Column(db.Integer, primary_key=True)
    caregiver_user_id = db.Column(
        db.Integer,
        db.ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job.job_id", ondelete="CASCADE"),
        nullable=False,
    )
    date_applied = db.Column(db.Date, nullable=False, default=date.today)

    # Relationships
    caregiver = db.relationship("Caregiver", back_populates="applications")
    job = db.relationship("Job", back_populates="applications")

    def __repr__(self):
        return f"<JobApplication {self.job_application_id}: Caregiver {self.caregiver_user_id} -> Job {self.job_id}>"


class Appointment(db.Model):
    """Appointment model - scheduled caregiving sessions"""
    __tablename__ = "appointment"
    __table_args__ = (
        CheckConstraint("status IN ('pending','confirmed','declined','cancelled')", name="ck_status"),
    )

    appointment_id = db.Column(db.Integer, primary_key=True)
    caregiver_user_id = db.Column(
        db.Integer,
        db.ForeignKey("caregiver.caregiver_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    member_user_id = db.Column(
        db.Integer,
        db.ForeignKey("member.member_user_id", ondelete="CASCADE"),
        nullable=False,
    )
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    work_hours = db.Column(db.Numeric(4, 2), nullable=False)
    status = db.Column(db.String, nullable=False)

    # Relationships
    caregiver = db.relationship("Caregiver", back_populates="appointments")
    member = db.relationship("Member", back_populates="appointments")

    def total_cost(self):
        """Calculate total cost of appointment"""
        if self.caregiver and self.work_hours:
            return float(self.work_hours) * float(self.caregiver.hourly_rate)
        return 0

    def __repr__(self):
        return f"<Appointment {self.appointment_id}: {self.status}>"

