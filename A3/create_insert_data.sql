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

