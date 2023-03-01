DROP DATABASE IF EXISTS hospital_db;

CREATE DATABASE hospital_db;
USE hospital_db;

-- tables --
CREATE TABLE Patient(
    Patient_ID      INT NOT NULL,
    Name            TEXT,
    District        TEXT,
    PIN             TEXT,
    House           TEXT,
    Age             INT NOT NULL,
    Gender          TEXT,
    Personal_Contact TEXT,
    Emergency_Contact TEXT,
    PRIMARY KEY(Patient_ID)
);

CREATE TABLE Patient_longTermAilments(
    longTermAilment     TEXT,
    Patient_ID          TEXT,
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID),
    PRIMARY KEY(longTermAilment, Patient_ID)
);

CREATE TABLE Room(
    Room_Num        INT NOT NULL,
    Floor           INT NOT NULL,
    PRIMARY KEY(Room_Num)
);

CREATE TABLE Administrator(
    Admin_ID        TEXT,
    Name            TEXT,
    District        TEXT,
    PIN             TEXT,
    House           TEXT,
    Age             INT NOT NULL,
    Gender          TEXT,
    Personal_Contact    TEXT,
    PRIMARY KEY(Admin_ID)
);

CREATE TABLE DE_Operator(
    DEOp_ID         TEXT,
    Name            TEXT,
    District        TEXT,
    PIN             TEXT,
    House           TEXT,
    Age             INT NOT NULL,
    Gender          TEXT,
    Personal_Contact    TEXT,
    PRIMARY KEY(DEOp_ID)
);

CREATE TABLE FD_Operator(
    FDOp_ID         TEXT,
    Name            TEXT,
    District        TEXT,
    PIN             TEXT,
    House           TEXT,
    Age             INT NOT NULL,
    Gender          TEXT,
    Personal_Contact    TEXT,
    PRIMARY KEY(DEOp_ID)
);

CREATE TABLE Doctor(
    Doctor_ID       TEXT,
    Name            TEXT,
    District        TEXT,
    PIN             TEXT,
    House           TEXT,
    Age             INT NOT NULL,
    Gender          TEXT,
    Personal_Contact    TEXT,
    PRIMARY KEY(Doctor_ID)
);

CREATE TABLE Test(
    Test_ID         TEXT,
    Name            TEXT,
    Result          TEXT,
    Patient_ID      TEXT,
    PRIMARY KEY(Test_ID),
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID)
);

CREATE TABLE Admitted(
    Date_Admitted   DATE,
    Patient_ID      TEXT,
    Room_Num        INT NOT NULL,
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY(Room_Num) REFERENCES Room(Room_Num),
    PRIMARY KEY(Date_Admitted, Patient_ID, Room_Num)
);

CREATE TABLE Discharged(
    Date_Discharged   DATE,
    Patient_ID      TEXT,
    Room_Num        INT NOT NULL,
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID),
    FOREIGN KEY(Room_Num) REFERENCES Room(Room_Num),
    PRIMARY KEY(Date_Discharged, Patient_ID, Room_Num)
);

CREATE TABLE Treatment(
    Treatment_ID        TEXT,
    Name                TEXT,
    Doctor_ID           TEXT,
    Patient_ID          TEXT,
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID),
    PRIMARY KEY(Treatment_ID)
);

CREATE TABLE Appointment(
    Appointment_ID        TEXT,
    Name                TEXT,
    Doctor_ID           TEXT,
    Patient_ID          TEXT,
    FOREIGN KEY(Doctor_ID) REFERENCES Doctor(Doctor_ID),
    FOREIGN KEY(Patient_ID) REFERENCES Patient(Patient_ID),
    PRIMARY KEY(Appointment_ID)
);

