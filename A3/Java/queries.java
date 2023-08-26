import java.sql.*;
import java.util.Scanner;

public class queries {
    public static void prettyPrint(ResultSet rs) throws SQLException {
        ResultSetMetaData rsmd = rs.getMetaData();
        int columnsNumber = rsmd.getColumnCount();
        String[] columns = new String[columnsNumber];
        int[] widths = new int[columnsNumber];
        StringBuilder tavnit = new StringBuilder("|");
        StringBuilder separator = new StringBuilder("+");
        
        for (int i = 1; i <= columnsNumber; i++) {
            columns[i - 1] = rsmd.getColumnLabel(i);
            widths[i - 1] = Math.max(20, columns[i - 1].length());
        }
        
        for (int w : widths) {
            tavnit.append(" %-" + w + "s|");
            separator.append(String.format("%-" + w + "s +", "").replace(" ", "-"));
        }
        
        System.out.println(separator);
        System.out.println(String.format(tavnit.toString(), (Object[]) columns));
        System.out.println(separator);
        while (rs.next()) {
            Object[] row = new Object[columnsNumber];
            for (int i = 1; i <= columnsNumber; i++) {
                row[i - 1] = rs.getObject(i);
            }
            System.out.println(String.format(tavnit.toString(), row));
        }
        System.out.println(separator);
    }

    public static void main(String[] args){
        try{
            // Establish a connection to the MySQL database
            String url = "jdbc:mysql://localhost/hospitalDB";
            String username = "root";
            String password = "webDevGawd101";

            Connection con = DriverManager.getConnection(url, username, password);

            System.out.println("Connection Successful");
            Scanner stringScanner = new Scanner(System.in);

            while(true){
                System.out.println("Select your query:");
                System.out.println("1. Names of all physicians who are trained in procedure name 'bypass surgery'.");
                System.out.println("2. Names of all physicians affiliated with the department name 'cardiology' and trained in 'bypass surgery'.");
                System.out.println("3. Name of all nurses who have even been on call for room 123.");
                System.out.println("4. Names and addresses of all patients who were prescribed the medication named 'remdesivir'.");
                System.out.println("5. Name and insurance id of all patients who stayed in the 'icu' room type for more than 15 days.");
                System.out.println("6. Names of all nurses who assisted in the procedure name 'bypass surgery'.");
                System.out.println("7. Name and position of all nurses who assisted in the procedure name 'bypass surgery' along with the names of and the accompanying physicians.");
                System.out.println("8. Obtain the names of all physicians who have performed a medical procedure they have never been trained to perform.");
                System.out.println("9. Names of all physicians who have performed a medical procedure that they are trained to perform, but such that the procedure was done at a date (Undergoes.Date) after the physician's certification expired (Trained_In.CertificationExpires).");
                System.out.println("10. Same as the previous query, but include the following information in the results: Physician name, name of procedure, date when the procedure was carried out, name of the patient the procedure was carried out on.");
                System.out.println("11. Names of all patients (also include, for each patient, the name of the patient's physician), such that all the following are true:");
                System.out.println("\tThe patient has been prescribed some medication by his/her physician");
                System.out.println("\tThe patient has undergone a procedure with a cost larger that 5000");
                System.out.println("\tThe patient has had at least two appointment where the physician was affiliated with the cardiology department");
                System.out.println("\tThe patient's physician is not the head of any department");
                System.out.println("12. Name and brand of the medication which has been prescribed to the highest number of patients");
                System.out.println("13. Enter procedure name to find name of all physicians trained in that procedure.");
                
                System.out.println("Enter your query number: ");
                
                int n = Integer.parseInt(System.console().readLine());
                boolean successful = true;
                Statement cursor = con.createStatement();

                // ResultSet rs;
                String query = "";
                switch(n){
                    case 1:
                        query = "SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = 'bypass surgery'";
                    break;
                    case 2:
                        query = "SELECT Name AS Physician_Name FROM Physician WHERE Physician.EmployeeID IN (SELECT Trained_In.Physician FROM ((Trained_In JOIN Procedures ON Trained_In.Treatment = Procedures.Code) JOIN Affiliated_With ON Affiliated_With.Physician = Trained_In.Physician) JOIN Department ON Affiliated_With.Department = Department.DepartmentID WHERE Department.Name = 'cardiology' AND Procedures.Name = 'bypass surgery')";
                    break;
                    case 3:
                        query = "SELECT Nurse.Name AS Nurse_Name FROM ((Nurse JOIN On_Call ON Nurse.EmployeeID = On_Call.Nurse) JOIN Block ON Block.Code = On_Call.BlockCode AND Block.Floor = On_Call.BlockFloor) JOIN Room ON Block.Code = Room.BlockCode AND Block.Floor = Room.BlockFloor WHERE Room.Number = 123";
                    break;
                    case 4:
                        query = "SELECT Name AS Patient_Name, Address FROM Patient WHERE Patient.SSN IN (SELECT Prescribes.Patient FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code WHERE Medication.Name = 'remdesivir')";
                    break;
                    case 5:
                        query = "SELECT Name AS Patient_Name, InsuranceID FROM Patient WHERE Patient.SSN IN (SELECT Stay.Patient FROM Stay JOIN Room ON Stay.Room = Room.Number WHERE Room.Type = 'icu' AND DATEDIFF(Stay.End, Stay.Start) > 15)";
                    break;
                    case 6:
                        query = "SELECT Nurse.Name AS Nurse_Name FROM (Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code WHERE Procedures.Name = 'bypass surgery'";
                    break;
                    case 7:
                        query = "SELECT Nurse.Name AS Nurse_Name, Nurse.Position as Nurse_Position, Physician.Name AS Physician_Name FROM ((Nurse JOIN Undergoes ON Nurse.EmployeeID = Undergoes.AssistingNurse) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Physician ON Undergoes.Physician = Physician.EmployeeID WHERE Procedures.Name = 'bypass surgery'";
                    break;
                    case 8:
                        query = "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS ((SELECT Procedures FROM Undergoes WHERE Undergoes.Physician = P.EmployeeID)  EXCEPT(SELECT Treatment FROM Trained_In WHERE Trained_In.Physician = P.EmployeeID))";
                    break;
                    case 9:
                        query = "SELECT DISTINCT Name AS Physician_Name FROM Physician AS P WHERE EXISTS((SELECT Trained_In.Physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires))";
                    break;
                    case 10:
                        query = "SELECT P.Name AS Physician_Name, Procedures.Name AS Proc_Name, Undergoes.Date, Patient.Name AS Patient_Name FROM ((Physician AS P JOIN Undergoes ON P.EmployeeID = Undergoes.Physician) JOIN Procedures ON Undergoes.Procedures = Procedures.Code) JOIN Patient ON Undergoes.Patient = Patient.SSN WHERE EXISTS(SELECT Trained_In.physician FROM Trained_In JOIN Undergoes ON Trained_In.Treatment = Undergoes.Procedures WHERE Trained_In.Physician = P.EmployeeID AND Undergoes.Physician = P.EmployeeID AND Undergoes.Date > Trained_In.CertificationExpires)";
                    break;
                    case 11:
                        query = "SELECT DISTINCT Patient.Name AS Patient_Name, Physician.Name AS Physician_Name FROM (Patient JOIN Physician ON Patient.PCP = Physician.EmployeeID) WHERE Patient.SSN IN (SELECT GR1 FROM (SELECT Patient AS GR1 FROM Prescribes GROUP BY Patient HAVING COUNT(Medication) > 0) AS T1 INNER JOIN (SELECT Undergoes.Patient AS GR2 FROM (Undergoes JOIN Procedures ON Undergoes.Procedures = Procedures.Code) WHERE Procedures.Cost > 5000) AS T2 ON GR1 = GR2 INNER JOIN (SELECT Appointment.Patient AS GR3 FROM (Appointment JOIN Affiliated_With ON Affiliated_With.Physician = Appointment.Physician) JOIN Department ON Department.DepartmentID = Affiliated_With.Department WHERE Department.Name = 'cardiology' GROUP BY Appointment.Patient HAVING COUNT(Appointment.Patient) > 1) AS T3 ON GR1 = GR3 INNER JOIN (SELECT SSN AS GR4 FROM Patient WHERE Patient.PCP NOT IN (SELECT Department.Head FROM Department)) AS T4 ON GR1 = GR4)";
                    break;
                    case 12:
                        query = "SELECT Medication.Name AS Med_Name, Medication.Brand AS Med_Brand FROM Prescribes JOIN Medication ON Prescribes.Medication = Medication.Code GROUP BY Medication ORDER BY COUNT(Medication) DESC LIMIT 1";
                    break;
                    case 13:
                        System.out.println("Enter the name of the procedure");
                        String proc = stringScanner.nextLine();
                        query = String.format("SELECT Physician.Name AS Physician_Name FROM (Physician JOIN Trained_In ON Physician.EmployeeID = Trained_In.Physician) JOIN Procedures ON Trained_In.Treatment = Procedures.Code WHERE Procedures.Name = '%s'", proc);
                    break;
                    default:
                        System.out.println("Wrong query number entered.");
                        successful = false;
                }

                if(successful == true){
                    ResultSet res = cursor.executeQuery(query);
                    prettyPrint(res);
                }

                System.out.println("Do you want to run more queries? (y/n)");
                String str = System.console().readLine();
                if(str.equals("n")){
                    break;
                }
            }
            stringScanner.close();

            con.close();
        }
        catch (Exception e){
            System.out.println(e.getMessage());
        }
    }
}