from . import mysql
from flask_login import UserMixin

class Administrator(UserMixin):
    def __init__(self, id, username, password, name, District, PIN, House, Age, Gender, Personal_Contact):
        self.Admin_ID = id
        self.Username = username
        self.Password = password
        self.Name = name
        self.District = District
        self.PIN = PIN
        self.House = House
        self.Age = Age
        self.Gender = Gender
        self.Personal_Contact = Personal_Contact
        self.AccessLevel = 1

    @staticmethod
    def get(Admin_ID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Administrator WHERE Admin_ID = %s", (Admin_ID,))
        row = cur.fetchone()
        print('before')
        if row is not None:
            temp = Administrator(*row)
            return temp
        print('after')
        return None

    @staticmethod
    def get_by_username(username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Administrator WHERE Username = %s", (username,))
        Admin_ID_List = []
        while True:
            row = cur.fetchone()
            if row is None:
                break
            temp = Administrator(*row)
            Admin_ID_List.append(temp)
        if Admin_ID_List is not None:
            return Admin_ID_List
        return None

    @staticmethod
    def create(id, username, name, password):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Administrator(Admin_ID, Username, Name, Password) VALUES (%s, %s, %s, %s)", (id, username, name, password))
        mysql.connection.commit()
        return Administrator.get(id)
    
    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Administrator")
        rows = cur.fetchall()
        for row in rows:
            row = Administrator(*row)
        return rows
    
    def get_id(self):
        return self.Admin_ID

class Doctor(UserMixin):
    def __init__(self, id, username, password, name, District, PIN, House, Age, Gender, Personal_Contact):
        self.Doctor_ID = id
        self.Username = username
        self.Password = password
        self.Name = name
        self.District = District
        self.PIN = PIN
        self.House = House
        self.Age = Age
        self.Gender = Gender
        self.Personal_Contact = Personal_Contact
        self.AccessLevel = 2


    @staticmethod
    def get(Doctor_ID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctor WHERE Doctor_ID = %s", (Doctor_ID,))
        row = cur.fetchone()
        if row is not None:
            temp = Doctor(*row)
            temp.AccessLevel = 2
            return temp
        return None

    @staticmethod
    def get_by_username(username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctor WHERE Username = %s", (username,))
        Doctor_ID_List = []
        while True:
            row = cur.fetchone()
            if row is None:
                break
            temp = Doctor(*row)
            temp.AccessLevel = 2
            Doctor_ID_List.append(temp)
        if Doctor_ID_List is not None:
            return Doctor_ID_List
        return None

    @staticmethod
    def create(id, username, name, password):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Doctor(Doctor_ID, Username, Name, Password) VALUES (%s, %s, %s, %s)", (id, username, name, password))
        mysql.connection.commit()
        return Doctor.get(id)

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Doctor")
        rows = cur.fetchall()
        for row in rows:
            row = Doctor(*row)
        return rows
    
    def get_id(self):
        return self.Doctor_ID

class FD_Operator(UserMixin):
    def __init__(self, id, username, name, password, District, PIN, House, Age, Gender):
        self.FD_Operator_ID = id
        self.Username = username
        self.Password = password
        self.Name = name
        self.District = District
        self.PIN = PIN
        self.House = House
        self.Age = Age
        self.Gender = Gender
        self.AccessLevel = 3

    @staticmethod
    def get(FD_Operator_ID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM FD_Operator WHERE FD_Operator_ID = %s", (FD_Operator_ID,))
        row = cur.fetchone()
        if row is not None:
            temp = FD_Operator(*row)
            return temp
        return None

    @staticmethod
    def get_by_username(username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM FD_Operator WHERE Username = %s", (username,))
        FD_Operator_List = []
        while True:
            row = cur.fetchone()
            if row is None:
                break
            temp = FD_Operator(*row)
            FD_Operator_List.append(temp)
        if FD_Operator_List is not None:
            return FD_Operator_List
        return None

    @staticmethod
    def create(id, username, name, password):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO FD_Operator VALUES (%s, %s, %s, %s)", (id, username, name, password))
        mysql.connection.commit()
        return FD_Operator(id, username, name, password)

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM FD_Operator")
        rows = cur.fetchall()
        for row in rows:
            row = FD_Operator(*row)
        return rows
    
    def get_id(self):
        return self.FD_Operator_ID

class DE_Operator(UserMixin):
    def __init__(self, id, username, name, password, District, PIN, House, Age, Gender, Personal_Contact):
        self.DE_Operator_ID = id
        self.Username = username
        self.Password = password
        self.Name = name
        self.District = District
        self.PIN = PIN
        self.House = House
        self.Age = Age
        self.Gender = Gender
        self.Personal_Contact = Personal_Contact
        self.AccessLevel = 4

    @staticmethod
    def get(DE_Operator_ID):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM DE_Operator WHERE DE_Operator_ID = %s", (DE_Operator_ID,))
        row = cur.fetchone()
        if row is not None:
            temp = DE_Operator(*row)
            return temp
        return None

    @staticmethod
    def get_by_username(username):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM DE_Operator WHERE Username = %s", (username,))
        DE_Operator_List = []
        while True:
            row = cur.fetchone()
            if row is None:
                break
            temp = DE_Operator(*row)
            DE_Operator_List.append(temp)
        if DE_Operator_List is not None:
            return DE_Operator_List
        return None

    @staticmethod
    def create(id, username, name, password):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO DE_Operator VALUES (%s, %s, %s, %s)", (id, username, name, password))
        mysql.connection.commit()
        return DE_Operator(id, username, name, password)

    @staticmethod
    def get_all():
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM DE_Operator")
        rows = cur.fetchall()
        for row in rows:
            row = DE_Operator(*row)
        return rows
    
    def get_id(self):
        return self.DE_Operator_ID

def identify_class(name):
    if name == 'Administrator':
        return Administrator
    elif name == 'Doctor':
        return Doctor
    elif name == 'FD_Operator':
        return FD_Operator
    elif name == 'DE_Operator':
        return DE_Operator
    else:
        return None