
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sys


DATABASE_URL = "postgresql://postgres:Aarukow4171@localhost:5432/caregivers"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def is_modifying_sql(sql: str) -> bool:
    if not sql:
        return False
    s = sql.strip().lower()
    return s.startswith(('insert', 'update', 'delete', 'create', 'drop', 'alter', 'truncate'))

def print_rows(rows):
    if not rows:
        print("No results found.")
        return
    for r in rows:
        try:
            print(dict(r))
        except Exception:
            print(tuple(r))

def execute_query(query, description=""):
    if description:
        print(f"\n{'='*60}\n{description}\n{'='*60}")
    try:
        result = session.execute(text(query))
        if result.returns_rows:
            rows = result.mappings().all()
            print_rows(rows)
        else:
            # rowcount may be -1 for some DDL; show message
            try:
                print(f"Affected rows: {result.rowcount}")
            except:
                print("Statement executed.")
        if is_modifying_sql(query):
            session.commit()
        else:
            session.rollback()
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()


# deduplicating job_application 

def deduplicate_job_application():
    check_dup_sql = """
    SELECT caregiver_user_id, job_id, COUNT(*) AS cnt
    FROM job_application
    GROUP BY caregiver_user_id, job_id
    HAVING COUNT(*) > 1;
    """
    print("\n-- Checking for duplicates in job_application --")
    dup = session.execute(text(check_dup_sql)).fetchall()
    if not dup:
        print("No duplicates found in job_application.")
        return
    print("Duplicates found — removing extras.")
    dedupe_sql = """
    WITH numbered AS (
      SELECT job_application_id,
             ROW_NUMBER() OVER (PARTITION BY caregiver_user_id, job_id ORDER BY job_application_id) AS rn
      FROM job_application
    )
    DELETE FROM job_application
    WHERE job_application_id IN (
      SELECT job_application_id FROM numbered WHERE rn > 1
    );
    """
    execute_query(dedupe_sql, "Deduplicating job_application")

# 3. UPDATE num

def update_queries():
    print("\n" + "="*60)
    print("UPDATE QUERIES")
    print("="*60)

    # 3.1 Update Arman safely (prefer email if exists)
    query_find_arman = """
    SELECT user_id, email FROM user_account
    WHERE given_name = 'Arman' AND surname = 'Armanov';
    """
    rows = session.execute(text(query_find_arman)).mappings().all()
    if not rows:
        print("No user Arman Armanov found.")
    else:
        # pick single user if only one; else try to choose by email containing 'arman'
        if len(rows) == 1:
            uid = rows[0]['user_id']
        else:
            uid = None
            for r in rows:
                if r.get('email') and 'arman' in r.get('email'):
                    uid = r['user_id']
                    break
            if uid is None:
                print("Multiple users named Arman Armanov found; please run manual update. Rows:")
                for r in rows:
                    print(dict(r))
        if uid:
            q = f"""
            UPDATE user_account
            SET phone_number = '+77773414141'
            WHERE user_id = {uid};
            """
            execute_query(q, "3.1: Update Arman Armanov phone (by id)")

    # 3.2 Commission: add column if not exists, then apply once
    check_column = """
    SELECT column_name FROM information_schema.columns
    WHERE table_name='caregiver' AND column_name='commission_applied';
    """
    if session.execute(text(check_column)).fetchone() is None:
        # add column default false
        alter_sql = "ALTER TABLE caregiver ADD COLUMN commission_applied BOOLEAN DEFAULT FALSE;"
        execute_query(alter_sql, "Adding commission_applied column to caregiver (default FALSE)")
    # Now apply commission only where commission_applied = FALSE
    apply_commission = """
    UPDATE caregiver
    SET hourly_rate = CASE
        WHEN hourly_rate < 10 THEN ROUND(hourly_rate + 0.3, 2)
        ELSE ROUND(hourly_rate * 1.10, 2)
    END,
    commission_applied = TRUE
    WHERE COALESCE(commission_applied, FALSE) = FALSE;
    """
    execute_query(apply_commission, "3.2: Apply commission idempotently")

# 4. DELETE: safe Kabanbay flow

def delete_queries():
    print("\n" + "="*60)
    print("DELETE QUERIES")
    print("="*60)

    # 4.1 Delete jobs posted by Amina Aminova (safe USING)
    q4_1 = """
    DELETE FROM job j
    USING member m
    JOIN user_account u ON m.member_user_id = u.user_id
    WHERE j.member_user_id = m.member_user_id
      AND u.given_name = 'Amina' AND u.surname = 'Aminova';
    """
    execute_query(q4_1, "4.1: Delete jobs posted by Amina Aminova")

    # 4.2 Delete members who live on Kabanbay Batyr (safe sequence):
    # Step A: collect member_user_ids that *currently* have address on that street
    collect_sql = """
    CREATE TEMP TABLE tmp_kabanbay_members AS
    SELECT DISTINCT member_user_id FROM address WHERE street = 'Kabanbay Batyr';
    """
    execute_query(collect_sql, "4.2.a: Collect member_user_id(s) living on Kabanbay Batyr (TEMP TABLE)")

    # Step B: delete addresses on that street
    del_addr = "DELETE FROM address WHERE street = 'Kabanbay Batyr';"
    execute_query(del_addr, "4.2.b: Delete addresses on Kabanbay Batyr")

    # Step C: delete members whose ids are in temp table
    del_members = """
    DELETE FROM member WHERE member_user_id IN (SELECT member_user_id FROM tmp_kabanbay_members);
    """
    execute_query(del_members, "4.2.c: Delete members who were on Kabanbay Batyr (using temp table)")

    # Drop temp table
    execute_query("DROP TABLE IF EXISTS tmp_kabanbay_members;", "4.2.d: Drop temp table tmp_kabanbay_members")

# 5. SIMPLE QUERIES

def simple_queries():
    print("\n" + "="*60)
    print("SIMPLE QUERIES")
    print("="*60)

    # 5.1 Select caregiver and member names for accepted appointments (confirmed)
    query_5_1 = """
    SELECT 
      c.caregiver_user_id,
      uc.given_name AS caregiver_first_name,
      uc.surname AS caregiver_last_name,
      m.member_user_id,
      um.given_name AS member_first_name,
      um.surname AS member_last_name,
      a.appointment_date,
      a.appointment_time
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    JOIN member m ON a.member_user_id = m.member_user_id
    JOIN user_account um ON m.member_user_id = um.user_id
    WHERE a.status = 'confirmed'
    ORDER BY a.appointment_date DESC, a.appointment_time DESC;
    """
    execute_query(query_5_1, "5.1: Caregiver and member names for confirmed appointments")

    # 5.2 List job ids that contain 'soft-spoken' in other requirements
    query_5_2 = """
    SELECT job_id, other_requirements
    FROM job
    WHERE other_requirements ILIKE '%soft-spoken%';
    """
    execute_query(query_5_2, "5.2: Jobs containing 'soft-spoken' requirement")

    # 5.3 List the work hours of all babysitter positions (appointments with babysitter caregivers)
    query_5_3 = """
    SELECT a.appointment_id, a.appointment_date, a.work_hours, c.caregiving_type, uc.given_name || ' ' || uc.surname AS caregiver_name
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    WHERE c.caregiving_type = 'babysitter';
    """
    execute_query(query_5_3, "5.3: Work hours of babysitter positions")

    # 5.4 Members looking for Elderly Care in Astana and have "No pets." rule
    query_5_4 = """
    SELECT u.user_id, u.given_name, u.surname, u.city, m.house_rules
    FROM member m
    JOIN user_account u ON m.member_user_id = u.user_id
    WHERE u.city ILIKE 'Astana'
      AND m.house_rules ILIKE '%No pets%';
    """
    execute_query(query_5_4, "5.4: Members in Astana looking for elderly care with 'No pets' rule")


# 6. COMPLEX QUERIES 
def complex_queries():
    print("\n" + "="*60)
    print("COMPLEX QUERIES")
    print("="*60)

    # 6.1 Count the number of applicants for each job posted by a member
    query_6_1 = """
    SELECT 
      j.job_id,
      u.given_name || ' ' || u.surname AS member_name,
      j.required_caregiving_type,
      COUNT(ja.caregiver_user_id) AS applicant_count
    FROM job j
    JOIN member m ON j.member_user_id = m.member_user_id
    JOIN user_account u ON m.member_user_id = u.user_id
    LEFT JOIN job_application ja ON j.job_id = ja.job_id
    GROUP BY j.job_id, u.given_name, u.surname, j.required_caregiving_type
    ORDER BY applicant_count DESC, j.job_id;
    """
    execute_query(query_6_1, "6.1: Number of applicants for each job")

    # 6.2 Total hours spent by caregivers for all confirmed appointments (group by caregiver id)
    query_6_2 = """
    SELECT 
      c.caregiver_user_id,
      uc.given_name || ' ' || uc.surname AS caregiver_name,
      c.caregiving_type,
      SUM(a.work_hours) AS total_hours
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    WHERE a.status = 'confirmed'
    GROUP BY c.caregiver_user_id, uc.given_name, uc.surname, c.caregiving_type
    ORDER BY total_hours DESC;
    """
    execute_query(query_6_2, "6.2: Total hours by caregivers for confirmed appointments")

    # 6.3 Average pay of caregivers based on confirmed appointments
    query_6_3 = """
    SELECT 
      c.caregiver_user_id,
      uc.given_name || ' ' || uc.surname AS caregiver_name,
      c.caregiving_type,
      c.hourly_rate,
      AVG(a.work_hours * c.hourly_rate) AS avg_payment
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    WHERE a.status = 'confirmed'
    GROUP BY c.caregiver_user_id, uc.given_name, uc.surname, c.caregiving_type, c.hourly_rate
    ORDER BY avg_payment DESC;
    """
    execute_query(query_6_3, "6.3: Average pay of caregivers for confirmed appointments")

    # 6.4 Caregivers who earn above average based on confirmed appointments
    query_6_4 = """
    SELECT 
      c.caregiver_user_id,
      uc.given_name || ' ' || uc.surname AS caregiver_name,
      c.caregiving_type,
      SUM(a.work_hours * c.hourly_rate) AS total_earnings
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    WHERE a.status = 'confirmed'
    GROUP BY c.caregiver_user_id, uc.given_name, uc.surname, c.caregiving_type
    HAVING SUM(a.work_hours * c.hourly_rate) > (
      SELECT AVG(total_pay) FROM (
        SELECT SUM(a2.work_hours * c2.hourly_rate) AS total_pay
        FROM appointment a2
        JOIN caregiver c2 ON a2.caregiver_user_id = c2.caregiver_user_id
        WHERE a2.status = 'confirmed'
        GROUP BY c2.caregiver_user_id
      ) AS subquery
    )
    ORDER BY total_earnings DESC;
    """
    execute_query(query_6_4, "6.4: Caregivers earning above average")

# 7. DERIVED ATTRIBUTE
def derived_attribute_query():
    print("\n" + "="*60)
    print("DERIVED ATTRIBUTE QUERY")
    print("="*60)

    query_7 = """
    SELECT 
      a.appointment_id,
      c.caregiver_user_id,
      uc.given_name || ' ' || uc.surname AS caregiver_name,
      m.member_user_id,
      um.given_name || ' ' || um.surname AS member_name,
      a.work_hours,
      c.hourly_rate,
      ROUND(a.work_hours * c.hourly_rate, 2) AS total_cost
    FROM appointment a
    JOIN caregiver c ON a.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    JOIN member m ON a.member_user_id = m.member_user_id
    JOIN user_account um ON m.member_user_id = um.user_id
    WHERE a.status = 'confirmed'
    ORDER BY total_cost DESC;
    """
    execute_query(query_7, "7: Total cost for each confirmed appointment")


# 8. VIEW OPERATION

def view_operation():
    print("\n" + "="*60)
    print("VIEW OPERATION")
    print("="*60)

    # Create or replace view
    create_view = """
    CREATE OR REPLACE VIEW job_applications_view AS
    SELECT 
      ja.job_application_id,
      j.job_id,
      j.required_caregiving_type,
      um.given_name || ' ' || um.surname AS employer_name,
      uc.given_name || ' ' || uc.surname AS applicant_name,
      c.caregiving_type AS applicant_type,
      c.hourly_rate,
      ja.date_applied
    FROM job_application ja
    JOIN job j ON ja.job_id = j.job_id
    JOIN member m ON j.member_user_id = m.member_user_id
    JOIN user_account um ON m.member_user_id = um.user_id
    JOIN caregiver c ON ja.caregiver_user_id = c.caregiver_user_id
    JOIN user_account uc ON c.caregiver_user_id = uc.user_id
    ORDER BY ja.date_applied DESC;
    """
    execute_query(create_view, "8: Creating or replacing view job_applications_view")

    # Query the view
    query_view = "SELECT * FROM job_applications_view LIMIT 50;"
    execute_query(query_view, "8: Querying job_applications_view (first 50 rows)")


# MAIN

if __name__ == "__main__":
    try:
        print("\n" + "="*60)
        print("QUERIES")
        print("="*60)

        deduplicate_job_application()
        update_queries()
        delete_queries()
        simple_queries()
        complex_queries()
        derived_attribute_query()
        view_operation()
        print("\nDone. Queries executed successfully.")

    except Exception as e:
        print(f"Unhandled error: {e}")
    finally:
        session.close()
        engine.dispose()
