import mysql.connector

def prettyPrint(cursor, results):
    widths = []
    columns = []
    tavnit = '|'
    separator = '+' 

    for cd in cursor.description:
        widths.append(max(20, len(cd[0])))
        columns.append(cd[0])

    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    print(separator)
    print(tavnit % tuple(columns))
    print(separator)
    for row in results:
        print(tavnit % row)
    print(separator)

def main():
    dataBase = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "webDevGawd101",
        database = "hospitalDB"
    )

    cursorObject = dataBase.cursor()

    while(True):
        print("Select your query:\n")
        print("1. Names of all physicians who are trained in procedure name 'bypass surgery'.\n")
        print("2. Names of all physicians affiliated with the department name 'cardiology' and trained in 'bypass surgery'.\n")
        print("3. Name of all nurses who have even been on call for room 123.\n")
        print("4. Names and addresses of all patients who were prescribed the medication named 'remdesivir'.\n")
        print("5. Name and insurance id of all patients who stayed in the 'icu' room type for more than 15 days.\n")
        print("6. Names of all nurses who assisted in the procedure name 'bypass surgery'.\n")
        print("7. Name and position of all nurses who assisted in the procedure name 'bypass surgery' along with the names of and the accompanying physicians.\n")
        print("8. Obtain the names of all physicians who have performed a medical procedure they have never been trained to perform.\n")
        print("9. Names of all physicians who have performed a medical procedure that they are trained to perform, but such that the procedure was done at a date (Undergoes.Date) after the physician's certification expired (Trained_In.CertificationExpires).\n")
        print("10. Same as the previous query, but include the following information in the results: Physician name, name of procedure, date when the procedure was carried out, name of the patient the procedure was carried out on.\n")
        print("11. Names of all patients (also include, for each patient, the name of the patient's physician), such that all the following are true:\n\tThe patient has been prescribed some medication by his/her physician\n\tThe patient has undergone a procedure with a cost larger that 5000\n\tThe patient has had at least two appointment where the physician was affiliated with the cardiology department\n\tThe patient's physician is not the head of any department\n")
        print("12. Name and brand of the medication which has been prescribed to the highest number of patients\n")
        print("13. Enter procedure name to find name of all physicians trained in that procedure.\n")

        query_no = int(input("Enter your query number: "))
        successful = True

        if query_no == 1:
            query = "SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = 'bypass surgery'"
            
        elif query_no == 2:
            query = "SELECT Name AS Physician_Name FROM Physician WHERE Physician.EmployeeID IN (SELECT Trained_In.Physician FROM ((Trained_In JOIN Procedures ON Trained_In.Treatment = Procedures.Code) JOIN Affiliated_With ON Affiliated_With.Physician = Trained_In.Physician) JOIN Department ON Affiliated_With.Department = Department.DepartmentID WHERE Department.Name = 'cardiology' AND Procedures.Name = 'bypass surgery')"
            
        elif query_no == 3:
            query = "SELECT Nurse.Name AS Nurse_Name FROM ((Nurse JOIN On_Call ON Nurse.EmployeeID = On_Call.Nurse) JOIN Block ON Block.Code = On_Call.BlockCode AND Block.Floor = On_Call.BlockFloor) JOIN Room ON Block.Code = Room.BlockCode AND Block.Floor = Room.BlockFloor WHERE Room.Number = 123"
            
        elif query_no == 4:
            query = "SELECT Name AS Patient_Name, Address FROM Patient WHERE Patient.SSN IN (SELECT Prescribes.Patient FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code WHERE Medication.Name = 'remdesivir')"

        elif query_no == 5:
            query = "SELECT Name AS Patient_Name, InsuranceID FROM Patient WHERE Patient.SSN IN (SELECT Stay.Patient FROM Stay JOIN Room ON Stay.Room = Room.Number WHERE Room.Type = 'icu' AND DATEDIFF(Stay.End, Stay.Start) > 15)"
            
        elif query_no == 6:
            query = "SELECT Nurse.Name AS Nurse_Name FROM (Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code WHERE Procedures.Name = 'bypass surgery'"
                
        elif query_no == 7:
            query = "SELECT Nurse.Name AS Nurse_Name, Nurse.Position AS Nurse_Position, Physician.Name AS Physician_Name FROM ((Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Physician ON Undergoes.Physician = Physician.EmployeeID WHERE Procedures.Name = 'bypass surgery'"
            
        elif query_no == 8:
            query = "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS ((SELECT Procedures FROM Undergoes WHERE Undergoes.Physician = P.EmployeeID)  EXCEPT(SELECT Treatment FROM Trained_In WHERE Trained_In.Physician = P.EmployeeID))"
            
        elif query_no == 9:
            query = "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS((SELECT Trained_In.Physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires))"
            
        elif query_no == 10:
            query = "SELECT P.Name AS Physician_Name, Procedures.Name AS Proc_Name, Undergoes.Date, Patient.Name AS Patient_Name FROM ((Physician AS P JOIN Undergoes ON P.EmployeeID = Undergoes.Physician) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Patient ON Undergoes.Patient = Patient.SSN WHERE EXISTS(SELECT Trained_In.physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires)"
            
        elif query_no == 11:
            query = "SELECT DISTINCT Patient.Name AS Patient_Name, Physician.Name AS Physician_Name FROM (Patient JOIN Physician ON Patient.PCP = Physician.EmployeeID) WHERE Patient.SSN IN (SELECT GR1 FROM (SELECT Patient AS GR1 FROM Prescribes GROUP BY Patient HAVING COUNT(Medication) > 0) AS T1 INNER JOIN (SELECT Undergoes.Patient AS GR2 FROM (Undergoes JOIN Procedures ON Undergoes.Procedures = Procedures.Code) WHERE Procedures.Cost > 5000) AS T2 ON GR1 = GR2 INNER JOIN (SELECT Appointment.Patient AS GR3 FROM (Appointment JOIN Affiliated_With ON Affiliated_With.Physician = Appointment.Physician) JOIN Department ON Department.DepartmentID = Affiliated_With.Department WHERE Department.Name = 'cardiology' GROUP BY Appointment.Patient HAVING COUNT(Appointment.Patient) > 1) AS T3 ON GR1 = GR3 INNER JOIN (SELECT SSN AS GR4 FROM Patient WHERE Patient.PCP NOT IN (SELECT Department.Head FROM Department)) AS T4 ON GR1 = GR4)"
            
        elif query_no == 12:
            query = "SELECT Medication.Name AS Med_Name, Medication.Brand AS Med_Brand FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code GROUP BY Medication ORDER BY COUNT(Medication) DESC LIMIT 1"
            
        elif query_no == 13:
            procedure_name = input("Enter procedure name: ")
            query = "SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = '" + procedure_name + "'"
            
        else:
            print("Wrong query number entered.")
            successful = False

        if(successful):
            cursorObject.execute(query)
            result = cursorObject.fetchall()

            prettyPrint(cursorObject, result)
        
        choice = input("Do you want to run more queries (y/n): ")
        if(choice == 'n'):
            break

    dataBase.close()

if __name__ == "__main__":
    main()