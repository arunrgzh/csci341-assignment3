from datetime import date, time
from decimal import Decimal

from flask import Flask, abort, flash, redirect, render_template, request, url_for

from config import Config
from models import (
    Address,
    Appointment,
    Caregiver,
    Job,
    JobApplication,
    Member,
    UserAccount,
    db,
)
from forms import FORM_CONFIGS, prepare_form_fields, validate_form


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    return app


app = create_app()


# Table configuration mapping
TABLE_MODELS = {
    "user_account": {"model": UserAccount, "pk": "user_id"},
    "caregiver": {"model": Caregiver, "pk": "caregiver_user_id"},
    "member": {"model": Member, "pk": "member_user_id"},
    "address": {"model": Address, "pk": "address_id"},
    "job": {"model": Job, "pk": "job_id"},
    "job_application": {"model": JobApplication, "pk": "job_application_id"},
    "appointment": {"model": Appointment, "pk": "appointment_id"},
}


def get_table_config(table_name):
    """Get table configuration or abort with 404"""
    if table_name not in TABLE_MODELS:
        abort(404)
    return TABLE_MODELS[table_name]


def serialize_value(value):
    """Convert database value to display string"""
    if isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, (date, time)):
        return value.isoformat()
    elif value is None:
        return ""
    return value


@app.route("/")
def index():
    """Homepage with statistics"""
    stats = []
    for table_name, config in TABLE_MODELS.items():
        count = config["model"].query.count()
        stats.append({
            "name": table_name,
            "label": FORM_CONFIGS[table_name]["label"],
            "count": count,
        })
    return render_template("index.html", stats=stats)


@app.route("/<table_name>")
def list_records(table_name):
    """List all records for a table"""
    config = get_table_config(table_name)
    form_config = FORM_CONFIGS[table_name]
    
    records = config["model"].query.order_by(
        getattr(config["model"], config["pk"])
    ).all()
    
    return render_template(
        f"{table_name}.html",
        records=records,
        table_name=table_name,
        label=form_config["label"],
        pk=config["pk"],
    )


@app.route("/<table_name>/create", methods=["GET", "POST"])
def create_record(table_name):
    """Create a new record"""
    config = get_table_config(table_name)
    form_config = FORM_CONFIGS[table_name]
    
    if request.method == "POST":
        data, errors = validate_form(table_name, request.form, mode="create")
        
        if not errors:
            try:
                instance = config["model"](**data)
                db.session.add(instance)
                db.session.commit()
                flash(f"{form_config['label']} record created successfully!", "success")
                return redirect(url_for("list_records", table_name=table_name))
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating record: {str(e)}", "error")
                errors["_general"] = str(e)
        else:
            flash("Please fix the errors below.", "error")
        
        fields = prepare_form_fields(table_name, form_data=request.form, mode="create")
        return render_template(
            "form.html",
            table_name=table_name,
            label=form_config["label"],
            fields=fields,
            errors=errors,
            mode="create",
        )
    
    fields = prepare_form_fields(table_name, mode="create")
    return render_template(
        "form.html",
        table_name=table_name,
        label=form_config["label"],
        fields=fields,
        errors={},
        mode="create",
    )


@app.route("/<table_name>/<int:record_id>/edit", methods=["GET", "POST"])
def edit_record(table_name, record_id):
    """Edit an existing record"""
    config = get_table_config(table_name)
    form_config = FORM_CONFIGS[table_name]
    
    instance = config["model"].query.get_or_404(record_id)
    
    if request.method == "POST":
        data, errors = validate_form(table_name, request.form, mode="edit")
        
        if not errors:
            try:
                for key, value in data.items():
                    setattr(instance, key, value)
                db.session.commit()
                flash(f"{form_config['label']} record updated successfully!", "success")
                return redirect(url_for("list_records", table_name=table_name))
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating record: {str(e)}", "error")
                errors["_general"] = str(e)
        else:
            flash("Please fix the errors below.", "error")
        
        fields = prepare_form_fields(
            table_name, instance=instance, form_data=request.form, mode="edit"
        )
        return render_template(
            "form.html",
            table_name=table_name,
            label=form_config["label"],
            fields=fields,
            errors=errors,
            mode="edit",
            record_id=record_id,
        )
    
    fields = prepare_form_fields(table_name, instance=instance, mode="edit")
    return render_template(
        "form.html",
        table_name=table_name,
        label=form_config["label"],
        fields=fields,
        errors={},
        mode="edit",
        record_id=record_id,
    )


@app.route("/<table_name>/<int:record_id>/delete", methods=["POST"])
def delete_record(table_name, record_id):
    """Delete a record"""
    config = get_table_config(table_name)
    form_config = FORM_CONFIGS[table_name]
    
    instance = config["model"].query.get_or_404(record_id)
    
    try:
        db.session.delete(instance)
        db.session.commit()
        flash(f"{form_config['label']} record deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting record: {str(e)}", "error")
    
    return redirect(url_for("list_records", table_name=table_name))


# Template filters
@app.template_filter("serialize")
def serialize_filter(value):
    """Template filter to serialize values"""
    return serialize_value(value)


if __name__ == "__main__":
    app.run(debug=True)
