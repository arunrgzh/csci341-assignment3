import os
from datetime import date, time
from decimal import Decimal

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from sqlalchemy import text

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


def parse_sql_statements(sql_content):
    """Parse SQL content into individual statements, respecting string boundaries"""
    statements = []
    current_statement = []
    in_string = False
    string_char = None
    i = 0
    
    while i < len(sql_content):
        char = sql_content[i]
        
        # Handle string boundaries
        if char in ("'", '"') and (i == 0 or sql_content[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None
        
        # Handle statement terminator (semicolon outside of strings)
        if char == ';' and not in_string:
            statement = ''.join(current_statement).strip()
            if statement:
                statements.append(statement)
            current_statement = []
        else:
            current_statement.append(char)
        
        i += 1
    
    # Add any remaining statement
    statement = ''.join(current_statement).strip()
    if statement:
        statements.append(statement)
    
    return statements


def insert_initial_data(app):
    """Insert initial data from SQL file if tables are empty"""
    # Check if data already exists - check multiple tables to be sure
    if (UserAccount.query.count() > 0 and 
        Member.query.count() > 0 and 
        Caregiver.query.count() > 0 and
        Job.query.count() > 0):
        app.logger.info("Data already exists, skipping insertion")
        return  # Data already exists
    
    # Read and execute insert_data.sql
    sql_file_path = os.path.join(os.path.dirname(__file__), "sql files", "insert_data.sql")
    
    if not os.path.exists(sql_file_path):
        app.logger.warning(f"SQL file not found: {sql_file_path}")
        return
    
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Remove comment lines (lines that start with --)
        lines = []
        for line in sql_content.split('\n'):
            stripped = line.lstrip()
            # Only remove lines that START with -- (not inline comments in strings)
            if not stripped.startswith('--'):
                lines.append(line)
        sql_content = '\n'.join(lines)
        
        # Parse SQL statements properly (respecting string boundaries)
        statements = parse_sql_statements(sql_content)
        
        success_count = 0
        error_count = 0
        
        for idx, statement in enumerate(statements):
            statement = statement.strip()
            # Skip empty statements
            if statement:
                try:
                    db.session.execute(text(statement))
                    db.session.commit()  # Commit each statement individually
                    success_count += 1
                    # Log successful inserts
                    if statement.upper().startswith('INSERT'):
                        table_name = statement.split()[2] if len(statement.split()) > 2 else 'unknown'
                        app.logger.info(f"✓ Statement {idx+1}: Inserted into {table_name}")
                except Exception as e:
                    db.session.rollback()  # Rollback failed statement
                    error_count += 1
                    # Log but continue for sequence operations (setval) - they might fail
                    # if sequences have different names, but this is not critical
                    error_msg = str(e).lower()
                    if 'setval' in statement.lower() or 'sequence' in error_msg or 'does not exist' in error_msg:
                        app.logger.debug(f"Sequence operation skipped (non-critical): {str(e)}")
                    else:
                        # For other errors, log with more detail
                        app.logger.error(f"✗ Statement {idx+1} FAILED: {str(e)}")
                        app.logger.error(f"Failed SQL: {statement[:200]}...")
        
        app.logger.info(f"Data insertion complete: {success_count} succeeded, {error_count} failed")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error inserting initial data: {str(e)}")


def create_app():
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Create tables if they don't exist (for Railway deployment)
    with app.app_context():
        db.create_all()
        # Insert initial data if tables are empty
        insert_initial_data(app)
    
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
