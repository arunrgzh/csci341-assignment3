CREATE TABLE "user_account" (
  user_id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  given_name TEXT NOT NULL,
  surname TEXT NOT NULL,
  city TEXT,
  phone_number TEXT,
  profile_description TEXT,
  password TEXT NOT NULL
);

CREATE TABLE caregiver (
  caregiver_user_id INTEGER PRIMARY KEY REFERENCES user_account(user_id) ON DELETE CASCADE,
  photo TEXT,
  gender TEXT CHECK (gender IN ('M','F','Other')) DEFAULT 'Other',
  caregiving_type TEXT CHECK (caregiving_type IN ('babysitter','elderly','playmate')) NOT NULL,
  hourly_rate NUMERIC(6,2) NOT NULL
);

CREATE TABLE member (
  member_user_id INTEGER PRIMARY KEY REFERENCES user_account(user_id) ON DELETE CASCADE,
  house_rules TEXT,
  dependent_description TEXT
);

CREATE TABLE address (
  address_id SERIAL PRIMARY KEY,
  member_user_id INTEGER NOT NULL REFERENCES member(member_user_id) ON DELETE CASCADE,
  house_number TEXT,
  street TEXT,
  town TEXT
);

CREATE TABLE job (
  job_id SERIAL PRIMARY KEY,
  member_user_id INTEGER NOT NULL REFERENCES member(member_user_id) ON DELETE CASCADE,
  required_caregiving_type TEXT CHECK (required_caregiving_type IN ('babysitter','elderly','playmate')) NOT NULL,
  other_requirements TEXT,
  date_posted DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE job_application (
  job_application_id SERIAL PRIMARY KEY,
  caregiver_user_id INTEGER NOT NULL REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
  job_id INTEGER NOT NULL REFERENCES job(job_id) ON DELETE CASCADE,
  date_applied DATE NOT NULL DEFAULT CURRENT_DATE,
  UNIQUE (caregiver_user_id, job_id)
);

CREATE TABLE appointment (
  appointment_id SERIAL PRIMARY KEY,
  caregiver_user_id INTEGER NOT NULL REFERENCES caregiver(caregiver_user_id) ON DELETE CASCADE,
  member_user_id INTEGER NOT NULL REFERENCES member(member_user_id) ON DELETE CASCADE,
  appointment_date DATE NOT NULL,
  appointment_time TIME NOT NULL,
  work_hours NUMERIC(4,2) NOT NULL,
  status TEXT NOT NULL CHECK (status IN ('pending','confirmed','declined','cancelled'))
);

-- mentioned indexes to help performance of queries
CREATE INDEX idx_user_city ON user_account(city);
CREATE INDEX idx_caregiver_type ON caregiver(caregiving_type);
CREATE INDEX idx_job_required_type ON job(required_caregiving_type);
CREATE INDEX idx_appointment_status_date ON appointment(status, appointment_date);
