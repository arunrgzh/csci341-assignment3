-- INSERT sample data (10+ rows per table), Stranger Things themed + required real names
-- 1) Users - (both members and caregivers)
-- 1) Users - explicitly set user_id values
INSERT INTO user_account (user_id, email, given_name, surname, city, phone_number, profile_description, password) VALUES
(1, 'eleven@upside.com','Eleven','Hopper','Hawkins','+77010000001','Mysterious girl with telekinetic powers','pass1'),
(2, 'mike@upside.com','Mike','Wheeler','Hawkins','+77010000002','Leader of the friend group','pass2'),
(3, 'will@upside.com','Will','Byers','Hawkins','+77010000003','Lost boy who returns changed','pass3'),
(4, 'dustin@upside.com','Dustin','Henderson','Hawkins','+77010000004','Lovable smart kid','pass4'),
(5, 'lucas@upside.com','Lucas','Sinclair','Hawkins','+77010000005','Cautious and brave friend','pass5'),
(6, 'nancy@upside.com','Nancy','Wheeler','Hawkins','+77010000006','Investigative and determined','pass6'),
(7, 'jonathan@upside.com','Jonathan','Byers','Hawkins','+77010000007','Photographer and quiet','pass7'),
(8, 'hopper@upside.com','Jim','Hopper','Hawkins','+77010000008','Local police chief','pass8'),
(9, 'arman@example.com','Arman','Armanov','Astana','+77770000000','Member to be updated phone for assignment','armpass'),
(10, 'amina@example.com','Amina','Aminova','Almaty','+77771112233','Member who posts some jobs','aminapass'),
(11, 'max@upside.com','Max','Mayfield','Hawkins','+77010000009','Skilled skateboarder','pass9'),
(12, 'steve@upside.com','Steve','Harrington','Hawkins','+77010000010','Protector-with-hair','pass10'),
(13, 'dr_owen@example.com','Dr.','Owen','Astana','+77772223344','Elderly care specialist','docpass'),
(14, 'kate@example.com','Kate','Marsh','Almaty','+77773330001','Warm and experienced babysitter','katepass'),
(15, 'olga@example.com','Olga','Sidorova','Astana','+77773330002','Elderly-care specialist','olgapass');

-- Reset the sequence to continue from 16
SELECT setval('user_account_user_id_seq', 15, true);

-- 2) Members 
INSERT INTO member (member_user_id, house_rules, dependent_description) VALUES
(3, 'No smoking. No late-night parties.', 'Will - 12 yo, sensitive to loud noises'),
(6, 'Be respectful to house; no pets allowed.', 'Nancy requests evening help for grandmother'),
(9, 'Please remove shoes at door; No pets.', 'Arman house: wife and 2-year-old son'),
(10, 'Soft-spoken caregiver preferred; No allergens in home.', 'Amina needs care for 4-year-old daughter'),
(11, 'Keep toys organized; no sweets before meals.', 'Max - 10 yo, hyperactive'),
(1, 'No strangers after 20:00', 'Eleven needs supervision and special diet'),
(2, 'Respectful language; no phones during work hours', 'Mike - toddler sibling care'),
(12, 'Flexible schedule on weekends', 'Steve - temporary recovery support at home'),
(13, 'No loud music; clean fridge after use', 'Dr. Owen - elderly patient with light dementia'),
(4, 'No pets; keep medications locked', 'Dustin - small child with asthma');

-- 3) Caregivers 
INSERT INTO caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) VALUES
(5, 'photo_lucas.jpg','M','babysitter',8.50),
(7, 'photo_jonathan.jpg','M','playmate',9.00),
(8, 'photo_hopper.jpg','M','elderly',12.00),
(11,'photo_max.jpg','F','babysitter',7.50),
(12,'photo_steve.jpg','M','babysitter',15.00),
(13,'photo_dr_owen.jpg','M','elderly',20.00),
(14,'photo_kate.jpg','F','babysitter',9.75),
(15,'photo_olga.jpg','F','elderly',8.25),
(4,'photo_dustin.jpg','M','playmate',6.50),
(1,'photo_eleven.jpg','F','playmate',11.00);

-- 4) Addresses 
INSERT INTO address (address_id, member_user_id, house_number, street, town) VALUES
(1, 3, '12','Kabanbay Batyr','Astana'),
(2, 6, '5A','Kabanbay Batyr','Astana'),
(3, 9, '21','Abylay Khan','Almaty'),
(4, 10,'34','Baikonur','Almaty'),
(5, 11,'7','Lenin','Hawkins'),
(6, 1, '2','Elm Street','Hawkins'),
(7, 2, '9','Maple Ave','Hawkins'),
(8, 12,'101','Central Ave','Almaty'),
(9, 13,'11','Kabanbay Batyr','Astana'),
(10, 4,'88','Oak Lane','Hawkins');

-- Reset the sequence
SELECT setval('address_address_id_seq', 10, true);

-- 5) Jobs 
INSERT INTO job (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(1, 10, 'babysitter', 'soft-spoken, experience with toddlers, first-aid certified', '2025-11-01'),
(2, 3, 'elderly', 'patient needs low-sodium diet, soft-spoken preferred', '2025-10-25'),
(3, 6, 'elderly', 'must be patient; no pets in house', '2025-11-03'),
(4, 9, 'babysitter', 'must like children; night shifts sometimes', '2025-09-15'),
(5, 11,'babysitter','must be playful and creative', '2025-10-01'),
(6, 1, 'playmate', 'likes board games; encourage reading', '2025-11-10'),
(7, 12,'babysitter','temporary weekend sitter needed', '2025-11-12'),
(8, 13,'elderly','medical knowledge preferred; soft-spoken', '2025-07-20'),
(9, 4,'playmate','outdoor play experience', '2025-08-05'),
(10, 6,'elderly','no smoking; gentle communicator', '2025-11-05'),
(11, 10,'babysitter','soft-spoken, experience with separation anxiety', '2025-11-04');

-- Reset the sequence to continue from 12
SELECT setval('job_job_id_seq', 11, true);

-- 6) Job applications
INSERT INTO job_application (caregiver_user_id, job_id, date_applied) VALUES
(5, 1, '2025-11-02'),
(7, 1, '2025-11-02'),
(11,1, '2025-11-03'),
(8,  2, '2025-10-26'),
(13, 2, '2025-10-27'),
(15, 2, '2025-10-28'),
(4,  3, '2025-11-04'),
(1,  3, '2025-11-04'),
(14, 4, '2025-09-16'),
(12, 5, '2025-10-02'),
(5,  6, '2025-11-11'),
(7,  6, '2025-11-12'),
(11, 7, '2025-11-13'),
(15, 8, '2025-07-21'),
(13, 8, '2025-07-22'),
(1,  9, '2025-08-06'),
(4, 10, '2025-11-06'),
(5, 10, '2025-11-07'),
(14,11, '2025-11-05'),
(15,11, '2025-11-05'),
(4,  1, '2025-11-06');

-- 7) confirmed appointments for aggregation queries
INSERT INTO appointment (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(5, 3, '2025-11-15','09:00', 3.00, 'confirmed'),
(7, 1, '2025-11-10','14:00', 2.50, 'confirmed'),
(8, 6, '2025-11-12','10:00', 4.00, 'confirmed'),
(11,9, '2025-11-13','08:00', 3.50, 'pending'),
(12,10,'2025-11-14','16:00', 5.00, 'declined'),
(13,4, '2025-11-16','11:00', 2.00, 'confirmed'),
(14,2, '2025-11-17','12:00', 6.00, 'confirmed'),
(15,3, '2025-11-18','09:30', 3.00, 'confirmed'),
(4,11, '2025-11-19','15:00', 2.75, 'confirmed'),
(1,12, '2025-11-20','10:00', 1.50, 'confirmed'),
(5,3, '2025-11-21','09:00', 4.00, 'confirmed'),
(7,1, '2025-11-22','14:00', 2.00, 'cancelled');
