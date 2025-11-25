from datetime import date, datetime
from decimal import Decimal, InvalidOperation

from models import UserAccount, Member, Caregiver, Job


def numeric(value):
    """Convert value to Decimal"""
    if value is None or value == "":
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Expecting numeric value") from exc


def parse_date(value):
    """Parse date string to date object"""
    if value in (None, ""):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Invalid date format. Use YYYY-MM-DD") from exc


def parse_time(value):
    """Parse time string to time object"""
    if value in (None, ""):
        return None
    try:
        return datetime.strptime(value, "%H:%M").time()
    except ValueError as exc:
        raise ValueError("Invalid time format. Use HH:MM") from exc


def parse_int(value):
    """Parse integer value"""
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError("Expecting integer value") from exc


def parse_bool(value):
    """Parse boolean value"""
    if value in (None, ""):
        return None
    return value in ("True", "true", "1", True)


# Helper functions for dropdown choices
def get_user_choices():
    """Get all users for dropdown"""
    return [
        (user.user_id, user.display_name())
        for user in UserAccount.query.order_by(UserAccount.user_id).all()
    ]


def get_member_choices():
    """Get all members for dropdown"""
    return [
        (
            member.member_user_id,
            f"{member.user.given_name} {member.user.surname} (ID: {member.member_user_id})",
        )
        for member in Member.query.order_by(Member.member_user_id).all()
    ]


def get_caregiver_choices():
    """Get all caregivers for dropdown"""
    return [
        (
            caregiver.caregiver_user_id,
            f"{caregiver.user.given_name} {caregiver.user.surname} (ID: {caregiver.caregiver_user_id})",
        )
        for caregiver in Caregiver.query.order_by(Caregiver.caregiver_user_id).all()
    ]


def get_job_choices():
    """Get all jobs for dropdown"""
    return [
        (
            job.job_id,
            f"Job #{job.job_id} ({job.required_caregiving_type}) - {job.member.user.given_name}",
        )
        for job in Job.query.order_by(Job.job_id).all()
    ]


# Form field configurations for each model
FORM_CONFIGS = {
    "user_account": {
        "label": "Users",
        "fields": [
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "given_name", "label": "First Name", "type": "text", "required": True},
            {"name": "surname", "label": "Last Name", "type": "text", "required": True},
            {"name": "city", "label": "City", "type": "text"},
            {"name": "phone_number", "label": "Phone Number", "type": "text"},
            {"name": "profile_description", "label": "Profile Description", "type": "textarea"},
            {"name": "password", "label": "Password", "type": "password", "required": True},
        ],
    },
    "caregiver": {
        "label": "Caregivers",
        "fields": [
            {
                "name": "caregiver_user_id",
                "label": "User Account",
                "type": "select",
                "choices": get_user_choices,
                "required": True,
                "coerce": parse_int,
                "show_in": "create",
            },
            {"name": "photo", "label": "Photo URL", "type": "text"},
            {
                "name": "gender",
                "label": "Gender",
                "type": "select",
                "choices": lambda: [("M", "Male"), ("F", "Female"), ("Other", "Other")],
            },
            {
                "name": "caregiving_type",
                "label": "Caregiving Type",
                "type": "select",
                "choices": lambda: [
                    ("babysitter", "Babysitter"),
                    ("elderly", "Elderly Care"),
                    ("playmate", "Playmate"),
                ],
                "required": True,
            },
            {
                "name": "hourly_rate",
                "label": "Hourly Rate",
                "type": "number",
                "required": True,
                "coerce": numeric,
                "step": "0.01",
            },
            {
                "name": "commission_applied",
                "label": "Commission Applied",
                "type": "select",
                "choices": lambda: [(True, "Yes"), (False, "No")],
                "coerce": parse_bool,
            },
        ],
    },
    "member": {
        "label": "Members",
        "fields": [
            {
                "name": "member_user_id",
                "label": "User Account",
                "type": "select",
                "choices": get_user_choices,
                "required": True,
                "coerce": parse_int,
                "show_in": "create",
            },
            {"name": "house_rules", "label": "House Rules", "type": "textarea"},
            {"name": "dependent_description", "label": "Dependent Description", "type": "textarea"},
        ],
    },
    "address": {
        "label": "Addresses",
        "fields": [
            {
                "name": "member_user_id",
                "label": "Member",
                "type": "select",
                "choices": get_member_choices,
                "required": True,
                "coerce": parse_int,
            },
            {"name": "house_number", "label": "House Number", "type": "text"},
            {"name": "street", "label": "Street", "type": "text"},
            {"name": "town", "label": "Town", "type": "text"},
        ],
    },
    "job": {
        "label": "Jobs",
        "fields": [
            {
                "name": "member_user_id",
                "label": "Member",
                "type": "select",
                "choices": get_member_choices,
                "required": True,
                "coerce": parse_int,
            },
            {
                "name": "required_caregiving_type",
                "label": "Required Caregiving Type",
                "type": "select",
                "choices": lambda: [
                    ("babysitter", "Babysitter"),
                    ("elderly", "Elderly Care"),
                    ("playmate", "Playmate"),
                ],
                "required": True,
            },
            {"name": "other_requirements", "label": "Other Requirements", "type": "textarea"},
            {
                "name": "date_posted",
                "label": "Date Posted",
                "type": "date",
                "coerce": parse_date,
                "default": lambda: date.today().isoformat(),
            },
        ],
    },
    "job_application": {
        "label": "Job Applications",
        "fields": [
            {
                "name": "caregiver_user_id",
                "label": "Caregiver",
                "type": "select",
                "choices": get_caregiver_choices,
                "required": True,
                "coerce": parse_int,
            },
            {
                "name": "job_id",
                "label": "Job",
                "type": "select",
                "choices": get_job_choices,
                "required": True,
                "coerce": parse_int,
            },
            {
                "name": "date_applied",
                "label": "Date Applied",
                "type": "date",
                "required": True,
                "coerce": parse_date,
                "default": lambda: date.today().isoformat(),
            },
        ],
    },
    "appointment": {
        "label": "Appointments",
        "fields": [
            {
                "name": "caregiver_user_id",
                "label": "Caregiver",
                "type": "select",
                "choices": get_caregiver_choices,
                "required": True,
                "coerce": parse_int,
            },
            {
                "name": "member_user_id",
                "label": "Member",
                "type": "select",
                "choices": get_member_choices,
                "required": True,
                "coerce": parse_int,
            },
            {
                "name": "appointment_date",
                "label": "Appointment Date",
                "type": "date",
                "required": True,
                "coerce": parse_date,
            },
            {
                "name": "appointment_time",
                "label": "Appointment Time",
                "type": "time",
                "required": True,
                "coerce": parse_time,
            },
            {
                "name": "work_hours",
                "label": "Work Hours",
                "type": "number",
                "required": True,
                "coerce": numeric,
                "step": "0.25",
            },
            {
                "name": "status",
                "label": "Status",
                "type": "select",
                "choices": lambda: [
                    ("pending", "Pending"),
                    ("confirmed", "Confirmed"),
                    ("declined", "Declined"),
                    ("cancelled", "Cancelled"),
                ],
                "required": True,
            },
        ],
    },
}


def validate_form(table_name, form_data, mode="create"):
    """
    Validate form data for a given table
    
    Args:
        table_name: Name of the table
        form_data: Dictionary of form data
        mode: 'create' or 'edit'
    
    Returns:
        Tuple of (parsed_data, errors)
    """
    config = FORM_CONFIGS.get(table_name)
    if not config:
        raise ValueError(f"Unknown table: {table_name}")
    
    data = {}
    errors = {}
    
    for field in config["fields"]:
        # Check if field should be shown in this mode
        show_in = field.get("show_in", "both")
        if mode == "create" and show_in not in ("create", "both"):
            continue
        if mode == "edit" and show_in not in ("edit", "both"):
            continue
        
        field_name = field["name"]
        raw_value = form_data.get(field_name)
        required = field.get("required", False)
        nullable = field.get("nullable", True)
        
        # Check required fields
        if required and not raw_value:
            errors[field_name] = "This field is required."
            continue
        
        # Handle empty values
        if not raw_value:
            if nullable:
                data[field_name] = None
            else:
                errors[field_name] = "This field cannot be empty."
            continue
        
        # Coerce value if needed
        coerce = field.get("coerce")
        try:
            data[field_name] = coerce(raw_value) if coerce else raw_value
        except ValueError as exc:
            errors[field_name] = str(exc)
    
    return data, errors


def prepare_form_fields(table_name, instance=None, form_data=None, mode="create"):
    """
    Prepare form fields with values for rendering
    
    Args:
        table_name: Name of the table
        instance: Database instance (for edit mode)
        form_data: Form data (for validation errors)
        mode: 'create' or 'edit'
    
    Returns:
        List of field dictionaries with values
    """
    config = FORM_CONFIGS.get(table_name)
    if not config:
        raise ValueError(f"Unknown table: {table_name}")
    
    fields = []
    for field in config["fields"]:
        # Check if field should be shown in this mode
        show_in = field.get("show_in", "both")
        if mode == "create" and show_in not in ("create", "both"):
            continue
        if mode == "edit" and show_in not in ("edit", "both"):
            continue
        
        # Prepare field copy
        field_copy = dict(field)
        
        # Set value
        value = None
        if form_data:
            value = form_data.get(field["name"], "")
        elif instance is not None:
            value = getattr(instance, field["name"])
            # Convert special types to strings
            if isinstance(value, Decimal):
                value = str(value)
            elif isinstance(value, (date, datetime)):
                value = value.isoformat()
            elif isinstance(value, bool):
                value = str(value)
        elif callable(field.get("default")):
            value = field["default"]()
        
        field_copy["value"] = value if value is not None else ""
        
        # Resolve choices if callable
        if field.get("type") == "select" and callable(field.get("choices")):
            field_copy["choices"] = field["choices"]()
        
        fields.append(field_copy)
    
    return fields

