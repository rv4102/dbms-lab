CREATE DATABASE hospitalDB;
USE hospitalDB;

-- Create --
CREATE TABLE Physician(
    EmployeeID    INT NOT NULL,
    Name          TEXT,
    Position      TEXT,
    SSN           INT NOT NULL,
    PRIMARY KEY(EmployeeID)
);

CREATE TABLE Department(
    DepartmentID  INT NOT NULL,
    Name          TEXT,
    Head          INT NOT NULL,
    PRIMARY KEY(DepartmentID),
    FOREIGN KEY(Head) REFERENCES Physician(EmployeeID)
);

CREATE TABLE Affiliated_with(
    Physician     INT NOT NULL,
    Department    INT NOT NULL,
    PrimaryAffiliation    BOOLEAN,
    PRIMARY KEY(Physician, Department),
    FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),
    FOREIGN KEY(Department) REFERENCES Department(DepartmentID)
);

CREATE TABLE Procedures(
    Code         INT NOT NULL,
    Name         TEXT,
    Cost         INT NOT NULL,
    PRIMARY KEY(Code)
);

CREATE TABLE Patient(
    SSN           INT NOT NULL,
    Name          TEXT,
    Address       TEXT,
    Phone         TEXT,
    InsuranceID   INT NOT NULL,
    PCP           INT NOT NULL,
    PRIMARY KEY(SSN),
    FOREIGN KEY(PCP) REFERENCES Physician(EmployeeID)
);

CREATE TABLE Nurse( 
    EmployeeID    INT NOT NULL,
    Name          TEXT,
    Position      TEXT,
    Registered    BOOLEAN,
    SSN           INT NOT NULL,
    PRIMARY KEY(EmployeeID)
);

CREATE TABLE Appointment(
    AppointmentID INT NOT NULL,
    Patient       INT NOT NULL,
    PrepNurse     INT,
    Physician     INT NOT NULL,
    Start         DATE,
    End           DATE,
    ExaminationRoom  TEXT,
    PRIMARY KEY(AppointmentID),
    FOREIGN KEY(Patient) REFERENCES Patient(SSN),
    FOREIGN KEY(PrepNurse) REFERENCES Nurse(EmployeeID),
    FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID)
);

CREATE TABLE Medication(
    Code          INT NOT NULL,
    Name          TEXT,
    Brand         TEXT,
    Description   TEXT,
    PRIMARY KEY(Code)
);

CREATE TABLE Prescribes(
    Physician     INT NOT NULL,
    Patient       INT NOT NULL,
    Medication    INT NOT NULL,
    Date          DATE,
    Appointment   INT,
    Dose          TEXT,
    PRIMARY KEY(Physician, Patient, Medication, Date),
    FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),
    FOREIGN KEY(Patient) REFERENCES Patient(SSN),
    FOREIGN KEY(Medication) REFERENCES Medication(Code),
    FOREIGN KEY(Appointment) REFERENCES Appointment(AppointmentID)
);

CREATE TABLE Block(
    Floor        INT NOT NULL,
    Code         INT NOT NULL,
    PRIMARY KEY(Floor, Code)
);

CREATE TABLE Room(
    Number        INT NOT NULL,
    Type          TEXT,
    BlockFloor    INT NOT NULL,
    BlockCode     INT NOT NULL,
    Unavailable   BOOLEAN,
    PRIMARY KEY(Number),
    FOREIGN KEY(BlockFloor, BlockCode) REFERENCES Block(Floor, Code)
);

CREATE TABLE On_Call(
    Nurse         INT NOT NULL,
    BlockFloor    INT NOT NULL,
    BlockCode     INT NOT NULL,
    Start         DATE,
    End           DATE,
    PRIMARY KEY(Nurse, BlockFloor, BlockCode, Start, End),
    FOREIGN KEY(Nurse) REFERENCES Nurse(EmployeeID),
    FOREIGN KEY(BlockFloor, BlockCode) REFERENCES Block(Floor, Code)
);

CREATE TABLE Stay(
    StayID        INT NOT NULL,
    Patient       INT NOT NULL,
    Room          INT NOT NULL,
    Start         DATE,
    End           DATE,
    PRIMARY KEY(StayID),
    FOREIGN KEY(Patient) REFERENCES Patient(SSN),
    FOREIGN KEY(Room) REFERENCES Room(Number)
);

CREATE TABLE Undergoes(
    Patient       INT NOT NULL,
    Procedures    INT NOT NULL,
    Stay          INT NOT NULL,
    Date          DATE,
    Physician     INT NOT NULL,
    AssistingNurse    INT,
    PRIMARY KEY(Patient, Procedures, Stay, Date),
    FOREIGN KEY(Patient) REFERENCES Patient(SSN),
    FOREIGN KEY(Procedures) REFERENCES Procedures(Code),
    FOREIGN KEY(Stay) REFERENCES Stay(StayID),
    FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),
    FOREIGN KEY(AssistingNurse) REFERENCES Nurse(EmployeeID)
);

CREATE TABLE Trained_In(
    Physician     INT NOT NULL,
    Treatment     INT NOT NULL,
    CertificationDate DATE,
    CertificationExpires DATE,
    PRIMARY KEY(Physician, Treatment),
    FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),
    FOREIGN KEY(Treatment) REFERENCES Procedures(Code)
);



-- Populate --
-- These values are a little different from those in Sample_Data.txt --
INSERT INTO Physician VALUES(1,'Alan Donald','Intern',111111111);
INSERT INTO Physician VALUES(2,'Bruce Reid','Attending Physician',222222222);
INSERT INTO Physician VALUES(3,'Courtney Walsh','Surgeon Physician',333333333);
INSERT INTO Physician VALUES(4,'Malcom Marshall','Senior Physician',444444444);
INSERT INTO Physician VALUES(5,'Dennis Lillee','Head Chief of Medicine',555555555);
INSERT INTO Physician VALUES(6,'Jeff Thomson','Surgeon Physician',666666666);
INSERT INTO Physician VALUES(7,'Richard Hadlee','Surgeon Physician',777777777);
INSERT INTO Physician VALUES(8,'Kapil  Dev','Resident',888888888);
INSERT INTO Physician VALUES(9,'Ishant Sharma','Psychiatrist',999999999);

INSERT INTO Department VALUES(1,'medicine',4);
INSERT INTO Department VALUES(2,'surgery',7);
INSERT INTO Department VALUES(3,'psychiatry',9);
INSERT INTO Department VALUES(4,'cardiology',8);

INSERT INTO Affiliated_With VALUES(1,1,1);
INSERT INTO Affiliated_With VALUES(2,1,1);
INSERT INTO Affiliated_With VALUES(3,1,0);
INSERT INTO Affiliated_With VALUES(3,2,1);
INSERT INTO Affiliated_With VALUES(4,1,1);
INSERT INTO Affiliated_With VALUES(5,1,1);
INSERT INTO Affiliated_With VALUES(6,2,1);
INSERT INTO Affiliated_With VALUES(7,1,0);
INSERT INTO Affiliated_With VALUES(7,2,1);
INSERT INTO Affiliated_With VALUES(8,1,1);
INSERT INTO Affiliated_With VALUES(9,3,1);
INSERT INTO Affiliated_With VALUES(9,4,0);

INSERT INTO Procedures VALUES(1,'bypass surgery',1500.0);
INSERT INTO Procedures VALUES(2,'angioplasty',3750.0);
INSERT INTO Procedures VALUES(3,'arthoscopy',4500.0);
INSERT INTO Procedures VALUES(4,'carotid endarterectomy',10000.0);
INSERT INTO Procedures VALUES(5,'cholecystectomy',4899.0);
INSERT INTO Procedures VALUES(6,'tonsillectomy',5600.0);
INSERT INTO Procedures VALUES(7,'cataract surgery',25.0);

INSERT INTO Patient VALUES(100000001,'Dilip Vengsarkar','42 Foobar Lane','555-0256',68476213,1);
INSERT INTO Patient VALUES(100000002,'Richie Richardson','37 Infinite Loop','555-0512',36546321,2);
INSERT INTO Patient VALUES(100000003,'Mark Waugh','101 Parkway Street','555-1204',65465421,2);
INSERT INTO Patient VALUES(100000004,'Ramiz Raza','1100 Sparks Avenue','555-2048',68421879,3);

INSERT INTO Nurse VALUES(101,'Eknath Solkar','Head Nurse',1,111111110);
INSERT INTO Nurse VALUES(102,'David Boon','Nurse',1,222222220);
INSERT INTO Nurse VALUES(103,'Andy Flowers','Nurse',0,333333330);

INSERT INTO Appointment VALUES(13216584,100000001,101,1,'2018-04-24 10:00','2018-04-24 11:00','A');
INSERT INTO Appointment VALUES(26548913,100000002,101,2,'2018-04-24 10:00','2018-04-24 11:00','B');
INSERT INTO Appointment VALUES(36549879,100000001,102,1,'2018-04-25 10:00','2018-04-25 11:00','A');
INSERT INTO Appointment VALUES(46846589,100000004,103,4,'2018-04-25 10:00','2018-04-25 11:00','B');
INSERT INTO Appointment VALUES(59871321,100000004,NULL,4,'2018-04-26 10:00','2018-04-26 11:00','C');
INSERT INTO Appointment VALUES(69879231,100000003,103,2,'2018-04-26 11:00','2018-04-26 12:00','C');
INSERT INTO Appointment VALUES(76983231,100000001,NULL,3,'2018-04-26 12:00','2018-04-26 13:00','C');
INSERT INTO Appointment VALUES(86213939,100000004,102,9,'2018-04-27 10:00','2018-04-21 11:00','A');
INSERT INTO Appointment VALUES(93216548,100000002,101,2,'2018-04-27 10:00','2018-04-27 11:00','B');

INSERT INTO Medication VALUES(1,'Paracetamol','Z','N/A');
INSERT INTO Medication VALUES(2,'Actemra','Foolki Labs','N/A');
INSERT INTO Medication VALUES(3,'Molnupiravir','Bale Laboratories','N/A');
INSERT INTO Medication VALUES(4,'Paxlovid','Bar Industries','N/A');
INSERT INTO Medication VALUES(5,'Remdesivir','Donald Pharmaceuticals','N/A');

INSERT INTO Prescribes VALUES(1,100000001,1,'2018-04-24 10:47',13216584,'5');
INSERT INTO Prescribes VALUES(9,100000004,2,'2018-04-27 10:53',86213939,'10');
INSERT INTO Prescribes VALUES(9,100000004,2,'2018-04-30 16:53',NULL,'5');

INSERT INTO Block VALUES(1,1);
INSERT INTO Block VALUES(1,2);
INSERT INTO Block VALUES(1,3);
INSERT INTO Block VALUES(2,1);
INSERT INTO Block VALUES(2,2);
INSERT INTO Block VALUES(2,3);
INSERT INTO Block VALUES(3,1);
INSERT INTO Block VALUES(3,2);
INSERT INTO Block VALUES(3,3);
INSERT INTO Block VALUES(4,1);
INSERT INTO Block VALUES(4,2);
INSERT INTO Block VALUES(4,3);

INSERT INTO Room VALUES(101,'Single',1,1,0);
INSERT INTO Room VALUES(102,'Single',1,1,0);
INSERT INTO Room VALUES(103,'Single',1,1,0);
INSERT INTO Room VALUES(111,'Single',1,2,0);
INSERT INTO Room VALUES(112,'icu',1,2,1);
INSERT INTO Room VALUES(113,'Single',1,2,0);
INSERT INTO Room VALUES(121,'Single',1,3,0);
INSERT INTO Room VALUES(122,'Single',1,3,0);
INSERT INTO Room VALUES(123,'Single',1,3,0);
INSERT INTO Room VALUES(201,'Single',2,1,1);
INSERT INTO Room VALUES(202,'Single',2,1,0);
INSERT INTO Room VALUES(203,'Single',2,1,0);
INSERT INTO Room VALUES(211,'Single',2,2,0);
INSERT INTO Room VALUES(212,'Single',2,2,0);
INSERT INTO Room VALUES(213,'Single',2,2,1);
INSERT INTO Room VALUES(221,'Single',2,3,0);
INSERT INTO Room VALUES(222,'Single',2,3,0);
INSERT INTO Room VALUES(223,'Single',2,3,0);
INSERT INTO Room VALUES(301,'Single',3,1,0);
INSERT INTO Room VALUES(302,'Single',3,1,1);
INSERT INTO Room VALUES(303,'Single',3,1,0);
INSERT INTO Room VALUES(311,'Single',3,2,0);
INSERT INTO Room VALUES(312,'Single',3,2,0);
INSERT INTO Room VALUES(313,'icu',3,2,0);
INSERT INTO Room VALUES(321,'Single',3,3,1);
INSERT INTO Room VALUES(322,'Single',3,3,0);
INSERT INTO Room VALUES(323,'Single',3,3,0);
INSERT INTO Room VALUES(401,'Single',4,1,0);
INSERT INTO Room VALUES(402,'Single',4,1,1);
INSERT INTO Room VALUES(403,'Single',4,1,0);
INSERT INTO Room VALUES(411,'Single',4,2,0);
INSERT INTO Room VALUES(412,'Single',4,2,0);
INSERT INTO Room VALUES(413,'Single',4,2,0);
INSERT INTO Room VALUES(421,'Single',4,3,1);
INSERT INTO Room VALUES(422,'Single',4,3,0);
INSERT INTO Room VALUES(423,'icu',4,3,0);

INSERT INTO On_Call VALUES(101,1,1,'2018-11-04 11:00','2018-11-04 19:00');
INSERT INTO On_Call VALUES(101,1,2,'2018-11-04 11:00','2018-11-04 19:00');
INSERT INTO On_Call VALUES(102,1,3,'2018-11-04 11:00','2018-11-04 19:00');
INSERT INTO On_Call VALUES(103,1,1,'2018-11-04 19:00','2018-11-05 03:00');
INSERT INTO On_Call VALUES(103,1,2,'2018-11-04 19:00','2018-11-05 03:00');
INSERT INTO On_Call VALUES(103,1,3,'2018-11-04 19:00','2018-11-05 03:00');

INSERT INTO Stay VALUES(3215,100000001,111,'2018-05-01','2018-05-04');
INSERT INTO Stay VALUES(3216,100000003,123,'2018-05-03','2018-05-14');
INSERT INTO Stay VALUES(3217,100000004,112,'2018-05-02','2018-05-03');

INSERT INTO Undergoes VALUES(100000001,6,3215,'2018-05-02',3,101);
INSERT INTO Undergoes VALUES(100000001,2,3215,'2018-05-03',7,101);
INSERT INTO Undergoes VALUES(100000004,1,3217,'2018-05-07',3,102);
INSERT INTO Undergoes VALUES(100000004,5,3217,'2018-05-09',6,NULL);
INSERT INTO Undergoes VALUES(100000001,7,3217,'2018-05-10',7,101);
INSERT INTO Undergoes VALUES(100000004,4,3217,'2018-05-13',3,103);

INSERT INTO Trained_In VALUES(3,1,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(3,2,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(3,5,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(3,6,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(3,7,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(6,2,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(6,5,'2017-01-01','2017-12-31');
INSERT INTO Trained_In VALUES(6,6,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,1,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,2,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,3,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,4,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,5,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,6,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(7,7,'2018-01-01','2018-12-31');
INSERT INTO Trained_In VALUES(9,1,'2018-01-01','2018-12-31');




-- Queries --
-- 1. Names of all physicians who are trained in procedure name “bypass surgery” --
SELECT Physician.Name
FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code
WHERE Procedures.Name = 'bypass surgery';

-- 2. Names of all physicians affiliated with the department name “cardiology” and trained in “bypass surgery” --
SELECT Name
FROM Physician
WHERE Physician.EmployeeID IN (
    SELECT Trained_In.Physician
    FROM ((Trained_In JOIN Procedures ON Trained_In.Treatment = Procedures.Code) JOIN Affiliated_With ON Affiliated_With.Physician = Trained_In.Physician) JOIN Department ON Affiliated_With.Department = Department.DepartmentID
    WHERE Department.Name = 'cardiology' AND Procedures.Name = 'bypass surgery'
);

-- 3. Names of all the nurses who have ever been on call for room 123 --
SELECT Nurse.Name
FROM ((Nurse JOIN On_Call ON Nurse.EmployeeID = On_Call.Nurse) JOIN Block ON Block.Code = On_Call.BlockCode AND Block.Floor = On_Call.BlockFloor) JOIN Room ON Block.Code = Room.BlockCode AND Block.Floor = Room.BlockFloor
WHERE Room.Number = 123;

-- 4. Names and addresses of all patients who were prescribed the medication named “remdesivir” --
SELECT Name, Address
FROM Patient
WHERE Patient.SSN IN (
    SELECT Prescribes.Patient
    FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code
    WHERE Medication.Name = 'remdesivir'
);

-- 5. Name and insurance id of all patients who stayed in the “icu” room type for more than 15 days --
SELECT Name, InsuranceID
FROM Patient
WHERE Patient.SSN IN (
    SELECT Stay.Patient
    FROM Stay JOIN Room ON Stay.Room = Room.Number
    WHERE Room.Type = 'icu' AND DATEDIFF(Stay.End, Stay.Start) > 15
);

-- 6. Names of all nurses who assisted in the procedure name “bypass surgery” --
SELECT Nurse.Name
FROM (Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code
WHERE Procedures.Name = 'bypass surgery';

-- 7. Name and position of all nurses who assisted in the procedure name “bypass surgery” along with the names of and the accompanying physicians --
SELECT Nurse.Name AS Nurse_Name, Nurse.Position as Nurse_Position, Physician.Name AS Physician_Name
FROM ((Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Physician ON Undergoes.Physician = Physician.EmployeeID
WHERE Procedures.Name = 'bypass surgery';

-- 8. Obtain the names of all physicians who have performed a medical procedure they have never been trained to perform --
SELECT DISTINCT Name
FROM Physician AS P
WHERE EXISTS (
    (SELECT Procedures
    FROM Undergoes
    WHERE Undergoes.Physician = P.EmployeeID) 
    EXCEPT
    (SELECT Treatment
    FROM Trained_In
    WHERE Trained_In.Physician = P.EmployeeID)
);

-- 9. Names of all physicians who have performed a medical procedure that they are trained to perform, but such that the procedure was done at a date (Undergoes.Date) after the physician's certification expired (Trained_In.CertificationExpires) --
SELECT DISTINCT Name
FROM Physician AS P
WHERE EXISTS(
    (SELECT Trained_In.Physician
    FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures
    WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires)
);

-- 10. Same as the previous query, but include the following information in the results: Physician name, name of procedure, date when the procedure was carried out, name of the patient the procedure was carried out on --
SELECT P.Name AS Physician_Name, Procedures.Name AS Proc_Name, Undergoes.Date, Patient.Name AS Patient_Name
FROM ((Physician AS P JOIN Undergoes ON P.EmployeeID = Undergoes.Physician) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Patient ON Undergoes.Patient = Patient.SSN
WHERE EXISTS(
    SELECT Trained_In.physician
    FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures
    WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires
);

/* 11. Get Names of all patients and the names of their physicians such that:
    - The patient has been prescribed some medication by his/her physician
    - The patient has undergone a procedure with a cost larger that 5000
    - The patient has had at least two appointment where the physician was affiliated with the cardiology department
    - The patient's physician is not the head of any department
*/
SELECT DISTINCT Patient.Name, Physician.Name
FROM (Patient JOIN Physician ON Patient.PCP = Physician.EmployeeID)
WHERE Patient.SSN IN (
    SELECT GR1 FROM (SELECT Patient AS GR1 FROM Prescribes GROUP BY Patient HAVING COUNT(Medication) > 0) AS T1
    INNER JOIN (SELECT Undergoes.Patient AS GR2 FROM (Undergoes JOIN Procedures ON Undergoes.Procedures = Procedures.Code) WHERE Procedures.Cost > 5000) AS T2
    ON GR1 = GR2
    INNER JOIN (SELECT Appointment.Patient AS GR3
    FROM (Appointment JOIN Affiliated_With ON Affiliated_With.Physician = Appointment.Physician) JOIN Department ON Department.DepartmentID = Affiliated_With.Department
    WHERE Department.Name = 'cardiology' GROUP BY Appointment.Patient HAVING COUNT(Appointment.Patient) > 1) AS T3
    ON GR1 = GR3
    INNER JOIN (SELECT SSN AS GR4 FROM Patient WHERE Patient.PCP NOT IN (SELECT Department.Head FROM Department)) AS T4
    ON GR1 = GR4
);

-- 12. Name and brand of the medication which has been prescribed to the highest number of patients --
SELECT Medication.Name, Medication.Brand
FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code
GROUP BY Medication
ORDER BY COUNT(Medication) DESC LIMIT 1;