#include <stdio.h>
#include "mysql/mysql.h"
#include <string.h>
#include <stdlib.h>
#include <math.h>

#define IP "localhost"
#define USER "root"
#define USER_PASSWD "webDevGawd101"
#define DB_NAME "hospitalDB"

void finish_with_error(MYSQL *con){
    fprintf(stderr, "%s\n", mysql_error(con));
    mysql_close(con);
    exit(1);
}

void prettyPrint(MYSQL_RES *result) {
    int i, j;
    int widths[100];
    int column_count = mysql_num_fields(result);
    MYSQL_FIELD *fields = mysql_fetch_fields(result);
    char tavnit[1024] = "|";
    char separator[1024] = "+"; 

    for (i = 0; i < column_count; i++) {
        widths[i] = fmax(20, strlen(fields[i].name));
    }

    for (i = 0; i < column_count; i++) {
        sprintf(tavnit + strlen(tavnit), " %-*s |", widths[i], fields[i].name);
        for (j = 0; j < widths[i]; j++) {
            strcat(separator, "-");
        }
        strcat(separator, "--+");
    }

    printf("%s\n%s\n%s\n", separator, tavnit, separator);
    MYSQL_ROW row;
    while ((row = mysql_fetch_row(result))) {
        char row_str[1024] = "|";
        unsigned long *lengths = mysql_fetch_lengths(result);
        for (i = 0; i < column_count; i++) {
            sprintf(row_str + strlen(row_str), " %-*s |", widths[i], row[i]);
        }
        printf("%s\n", row_str);
    }
    printf("%s\n", separator);

    mysql_free_result(result);
}

int main(){
    size_t maxsize=100;
    char *procedure;
    procedure = (char *)(malloc(sizeof(char) * maxsize));
    char query[2000];
    MYSQL *con = mysql_init(NULL);
    if (con == NULL)
        finish_with_error(con);

    if (mysql_real_connect(con, IP, USER, USER_PASSWD, DB_NAME, 0, NULL, CLIENT_MULTI_STATEMENTS) == NULL)
        finish_with_error(con);

    // // queries to create the tables
    // if( mysql_query(con, "CREATE DATABASE hospitalDB") )
    //     finish_with_error(con);
    // if( mysql_query(con, "USE hospitalDB") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Physician(EmployeeID INT NOT NULL, Name TEXT, Position TEXT, SSN INT NOT NULL, PRIMARY KEY(EmployeeID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Department(DepartmentID INT NOT NULL, Name TEXT, Head INT NOT NULL, PRIMARY KEY(DepartmentID), FOREIGN KEY(Head) REFERENCES Physician(EmployeeID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Affiliated_with(Physician INT NOT NULL, Department INT NOT NULL, PrimaryAffiliation BOOLEAN, PRIMARY KEY(Physician, Department), FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID), FOREIGN KEY(Department) REFERENCES Department(DepartmentID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Procedures( Code INT NOT NULL, Name TEXT, Cost INT NOT NULL, PRIMARY KEY(Code))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Patient(SSN INT NOT NULL, Name TEXT, Address TEXT, Phone TEXT, InsuranceID INT NOT NULL, PCP INT NOT NULL, PRIMARY KEY(SSN), FOREIGN KEY(PCP) REFERENCES Physician(EmployeeID));") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Nurse(EmployeeID INT NOT NULL, Name TEXT, Position TEXT, Registered BOOLEAN, SSN INT NOT NULL, PRIMARY KEY(EmployeeID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Appointment(AppointmentID INT NOT NULL, Patient INT NOT NULL, PrepNurse INT, Physician INT NOT NULL, Start DATE, End DATE, ExaminationRoom TEXT, PRIMARY KEY(AppointmentID), FOREIGN KEY(Patient) REFERENCES Patient(SSN), FOREIGN KEY(PrepNurse) REFERENCES Nurse(EmployeeID), FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Medication(Code INT NOT NULL, Name TEXT, Brand TEXT,Description TEXT, PRIMARY KEY(Code))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Prescribes(Physician INT NOT NULL, Patient INT NOT NULL, Medication INT NOT NULL, Date DATE, Appointment INT, Dose TEXT, PRIMARY KEY(Physician, Patient, Medication, Date), FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID), FOREIGN KEY(Patient) REFERENCES Patient(SSN), FOREIGN KEY(Medication) REFERENCES Medication(Code), FOREIGN KEY(Appointment) REFERENCES Appointment(AppointmentID)))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Block(Floor INT NOT NULL, Code INT NOT NULL, PRIMARY KEY(Floor, Code))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Room(Number INT NOT NULL,Type TEXT,BlockFloor INT NOT NULL,BlockCode INT NOT NULL,Unavailable BOOLEAN,PRIMARY KEY(Number),FOREIGN KEY(BlockFloor, BlockCode) REFERENCES Block(Floor, Code))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE On_Call(Nurse INT NOT NULL,BlockFloor INT NOT NULL,BlockCode INT NOT NULL,Start DATE,End DATE,PRIMARY KEY(Nurse, BlockFloor, BlockCode, Start, End),FOREIGN KEY(Nurse) REFERENCES Nurse(EmployeeID),FOREIGN KEY(BlockFloor, BlockCode) REFERENCES Block(Floor, Code))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Stay(StayID INT NOT NULL,Patient INT NOT NULL,Room INT NOT NULL,Start DATE,End DATE,PRIMARY KEY(StayID),FOREIGN KEY(Patient) REFERENCES Patient(SSN),FOREIGN KEY(Room) REFERENCES Room(Number))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Undergoes(Patient INT NOT NULL,Procedures INT NOT NULL,Stay INT NOT NULL,Date DATE,Physician INT NOT NULL,AssistingNurse INT,PRIMARY KEY(Patient, Procedures, Stay, Date),FOREIGN KEY(Patient) REFERENCES Patient(SSN),FOREIGN KEY(Procedures) REFERENCES Procedures(Code),FOREIGN KEY(Stay) REFERENCES Stay(StayID),FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),FOREIGN KEY(AssistingNurse) REFERENCES Nurse(EmployeeID))") )
    //     finish_with_error(con);
    // if( mysql_query(con, "CREATE TABLE Trained_In(Physician INT NOT NULL,Treatment INT NOT NULL,CertificationDate DATE,CertificationExpires DATE,PRIMARY KEY(Physician, Treatment),FOREIGN KEY(Physician) REFERENCES Physician(EmployeeID),FOREIGN KEY(Treatment) REFERENCES Procedures(Code))") )
    //     finish_with_error(con);

    while(true){
        printf("Select your query:\n");
        printf("1. Names of all physicians who are trained in procedure name 'bypass surgery'.\n");
        printf("2. Names of all physicians affiliated with the department name 'cardiology' and trained in 'bypass surgery'.\n");
        printf("3. Name of all nurses who have even been on call for room 123.\n");
        printf("4. Names and addresses of all patients who were prescribed the medication named 'remdesivir'.\n");
        printf("5. Name and insurance id of all patients who stayed in the 'icu' room type for more than 15 days.\n");
        printf("6. Names of all nurses who assisted in the procedure name 'bypass surgery'.\n");
        printf("7. Name and position of all nurses who assisted in the procedure name 'bypass surgery' along with the names of and the accompanying physicians.\n");
        printf("8. Obtain the names of all physicians who have performed a medical procedure they have never been trained to perform.\n");
        printf("9. Names of all physicians who have performed a medical procedure that they are trained to perform, but such that the procedure was done at a date (Undergoes.Date) after the physician's certification expired (Trained_In.CertificationExpires).\n");
        printf("10. Same as the previous query, but include the following information in the results: Physician name, name of procedure, date when the procedure was carried out, name of the patient the procedure was carried out on.\n");
        printf("11. Names of all patients (also include, for each patient, the name of the patient's physician), such that all the following are true:\n\tThe patient has been prescribed some medication by his/her physician\n\tThe patient has undergone a procedure with a cost larger that 5000\n\tThe patient has had at least two appointment where the physician was affiliated with the cardiology department\n\tThe patient's physician is not the head of any department\n");
        printf("12. Name and brand of the medication which has been prescribed to the highest number of patients\n");
        printf("13. Enter procedure name to find name of all physicians trained in that procedure.\n");

        int choice=0;
        char c;
        int successful = 1;
        scanf("%d", &choice);
        while(getchar() != '\n'); // consume the newlines
        switch(choice){
            case 1:
                strcpy(query, "SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = 'bypass surgery'");
            break;
            case 2:
                strcpy(query, "SELECT Name AS Physician_Name FROM Physician WHERE Physician.EmployeeID IN (SELECT Trained_In.Physician FROM ((Trained_In JOIN Procedures ON Trained_In.Treatment = Procedures.Code) JOIN Affiliated_With ON Affiliated_With.Physician = Trained_In.Physician) JOIN Department ON Affiliated_With.Department = Department.DepartmentID WHERE Department.Name = 'cardiology' AND Procedures.Name = 'bypass surgery')");
            break;
            case 3:
                strcpy(query, "SELECT Nurse.Name AS Nurse_Name FROM ((Nurse JOIN On_Call ON Nurse.EmployeeID = On_Call.Nurse) JOIN Block ON Block.Code = On_Call.BlockCode AND Block.Floor = On_Call.BlockFloor) JOIN Room ON Block.Code = Room.BlockCode AND Block.Floor = Room.BlockFloor WHERE Room.Number = 123");
            break;
            case 4:
                strcpy(query, "SELECT Name AS Patient_Name, Address FROM Patient WHERE Patient.SSN IN (SELECT Prescribes.Patient FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code WHERE Medication.Name = 'remdesivir')");
            break;
            case 5:
                strcpy(query, "SELECT Name AS Patient_Name, InsuranceID FROM Patient WHERE Patient.SSN IN (SELECT Stay.Patient FROM Stay JOIN Room ON Stay.Room = Room.Number WHERE Room.Type = 'icu' AND DATEDIFF(Stay.End, Stay.Start) > 15)");
            break;
            case 6:
                strcpy(query, "SELECT Nurse.Name AS Nurse_Name FROM (Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code WHERE Procedures.Name = 'bypass surgery'");
            break;
            case 7:
                strcpy(query, "SELECT Nurse.Name AS Nurse_Name, Nurse.Position as Nurse_Position, Physician.Name AS Physician_Name FROM ((Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Physician ON Undergoes.Physician = Physician.EmployeeID WHERE Procedures.Name = 'bypass surgery'");
            break;
            case 8:
                strcpy(query, "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS ((SELECT Procedures FROM Undergoes WHERE Undergoes.Physician = P.EmployeeID)  EXCEPT(SELECT Treatment FROM Trained_In WHERE Trained_In.Physician = P.EmployeeID))");
            break;
            case 9:
                strcpy(query, "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS((SELECT Trained_In.Physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires))");
            break;
            case 10:
                strcpy(query, "SELECT P.Name AS Physician_Name, Procedures.Name AS Proc_Name, Undergoes.Date, Patient.Name AS Patient_Name FROM ((Physician AS P JOIN Undergoes ON P.EmployeeID = Undergoes.Physician) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Patient ON Undergoes.Patient = Patient.SSN WHERE EXISTS(SELECT Trained_In.physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires)");
            break;
            case 11:
                strcpy(query, "SELECT DISTINCT Patient.Name AS Patient_Name, Physician.Name AS Physician_Name FROM (Patient JOIN Physician ON Patient.PCP = Physician.EmployeeID) WHERE Patient.SSN IN (SELECT GR1 FROM (SELECT Patient AS GR1 FROM Prescribes GROUP BY Patient HAVING COUNT(Medication) > 0) AS T1 INNER JOIN (SELECT Undergoes.Patient AS GR2 FROM (Undergoes JOIN Procedures ON Undergoes.Procedures = Procedures.Code) WHERE Procedures.Cost > 5000) AS T2 ON GR1 = GR2 INNER JOIN (SELECT Appointment.Patient AS GR3 FROM (Appointment JOIN Affiliated_With ON Affiliated_With.Physician = Appointment.Physician) JOIN Department ON Department.DepartmentID = Affiliated_With.Department WHERE Department.Name = 'cardiology' GROUP BY Appointment.Patient HAVING COUNT(Appointment.Patient) > 1) AS T3 ON GR1 = GR3 INNER JOIN (SELECT SSN AS GR4 FROM Patient WHERE Patient.PCP NOT IN (SELECT Department.Head FROM Department)) AS T4 ON GR1 = GR4)");
            break;
            case 12:
                strcpy(query, "SELECT Medication.Name AS Med_Name, Medication.Brand AS Med_Brand FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code GROUP BY Medication ORDER BY COUNT(Medication) DESC LIMIT 1");
            break;
            case 13:
                printf("Enter the name of the procedure.\n");
                getline(&procedure, &maxsize, stdin);
                // replace the newline with \0
                for(int i=0; i<maxsize; i++){
                    if(procedure[i] == '\n') {
                        procedure[i] = '\0';
                        break;
                    }
                }
                sprintf(query, "SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = '%s'", procedure);
            break;
            default:
                printf("Wrong choice.\n");
                successful = 0;
        }
        if(successful){
            if( mysql_query(con, query) )
                finish_with_error(con);
                
            prettyPrint(mysql_store_result(con));
        }
        printf("Do you want to run more queries (y/n)?\n");
        scanf("%c", &c);
        while(getchar() != '\n'); // consume the newlines
        if(c == 'n'){
            break;
        }
    }
    mysql_close(con);
    exit(0);
}