from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from decimal import Decimal
import MySQLdb.cursors
from extensions import app
mysql = MySQL(app)

class Account:
    def __init__(self, id_accounts, name, phone, username, password, gender, birth, access, id_class):
        self.id_accounts = id_accounts
        self.name = name
        self.phone = phone
        self.username = username
        self.password = password
        self.gender = gender
        self.birth = birth
        self.access = access
        self.id_class = id_class

    @staticmethod
    def get_account_by_id(id_accounts):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE idAccount = %s", (id_accounts,))
        account_data = cursor.fetchone()
        if account_data:
            return Account(
                id_accounts=account_data['idAccount'],
                name=account_data['Name'],
                phone=account_data['Phone'],
                username=account_data['Username'],
                password=account_data['Password'],
                gender=account_data['Gender'],
                birth=account_data['Birth'],
                access=account_data['Access'],
                id_class=account_data.get('idClass')
            )
        else:
            return None

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE idAccount !=1")
        accounts_data = cursor.fetchall()
        accounts = []
        for account_data in accounts_data:
            accounts.append(Account(
                id_accounts=account_data['idAccount'],
                name=account_data['Name'],
                phone=account_data['Phone'],
                username=account_data['Username'],
                password=account_data['Password'],
                gender=account_data['Gender'],
                birth=account_data['Birth'],
                access=account_data['Access'],
                id_class=account_data.get('idClass')
            ))
        return accounts

    @staticmethod
    def get_all_staff():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE Access = 'Trainer' OR Access = 'Receptionist' OR Access = 'Warranty'")
        accounts_data = cursor.fetchall()
        accounts = []
        for account_data in accounts_data:
            accounts.append(Account(
                id_accounts=account_data['idAccount'],
                name=account_data['Name'],
                phone=account_data['Phone'],
                username=account_data['Username'],
                password=account_data['Password'],
                gender=account_data['Gender'],
                birth=account_data['Birth'],
                access=account_data['Access'],
                id_class=account_data.get('idClass')
            ))
        return accounts

    @staticmethod
    def get_all_customers():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE Access = 'Customer'")
        accounts_data = cursor.fetchall()
        customers = []
        for account_data in accounts_data:
            customers.append(Account(
                id_accounts=account_data['idAccount'],
                name=account_data['Name'],
                phone=account_data['Phone'],
                username=account_data['Username'],
                password=account_data['Password'],
                gender=account_data['Gender'],
                birth=account_data['Birth'],
                access=account_data['Access'],
                id_class=account_data.get('idClass')
            ))
        return customers

    @staticmethod
    def delete_account_by_id(id_accounts):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM accounts WHERE idAccount = %s", (id_accounts,))
        mysql.connection.commit()
        cursor.close()

    def update_account(self, name, phone, gender, birth):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE accounts
            SET Name = %s, Phone = %s, Gender = %s, Birth = %s
            WHERE idAccount = %s
        """, (name, phone, gender, birth, self.id_accounts))
        mysql.connection.commit()

    def enroll_in_class(self, class_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE accounts
            SET idClass = %s
            WHERE idAccount = %s
        """, (class_id, self.id_accounts))
        mysql.connection.commit()
        cursor.close()

    def unenroll_from_class(self):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE accounts
            SET idClass = NULL
            WHERE idAccount = %s
        """, (self.id_accounts,))
        mysql.connection.commit()
        cursor.close()

    def display_info(self):
        return {
            "ID": self.id_accounts,
            "Name": self.name,
            "Phone": self.phone,
            "Username": self.username,
            "Gender": self.gender,
            "Birth": str(self.birth) if self.birth else None,
            "Access": self.access,
            "idClass": self.id_class
        }

class Area:
    def __init__(self, idArea, Name, Description, Note):
        self.id_area = idArea
        self.name = Name
        self.description = Description
        self.note = Note

    @staticmethod
    def get_all_areas():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM areas")
        areas_data = cursor.fetchall()
        return [Area(**area) for area in areas_data]


    def display_info(self):
        return {
            "ID": self.id_area,
            "Name": self.name,
            "Description": self.description,
            "Note": self.note
        }

class Exercise:
    def __init__(self, idExercise, idArea, Name, Repetition):
        self.id_exercise = idExercise
        self.id_area = idArea
        self.name = Name
        self.repetition = Repetition

    @staticmethod
    def get_exercises_by_area(id_area):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM exercises WHERE idArea = %s", (id_area,))
        exercises_data = cursor.fetchall()
        return [Exercise(**exercise) for exercise in exercises_data]

    def display_info(self):
        return {
            "ID": self.id_exercise,
            "Area ID": self.id_area,
            "Name": self.name,
            "Repetition": self.repetition
        }

class Membership:
    def __init__(self, id_membership, id_accounts, membership_type, start_date, end_date, status):
        self.id_membership = id_membership
        self.id_accounts = id_accounts
        self.membership_type = membership_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

    @staticmethod
    def get_all_memberships_by_account(id_accounts):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM membership WHERE idAccount = %s", (id_accounts,))
        memberships_data = cursor.fetchall()
        cursor.close()

        return [
            Membership(
                id_membership=m['idMembership'],
                id_accounts=m['idAccount'],
                membership_type=m['MembershipType'],
                start_date=m['StartDate'],
                end_date=m['EndDate'],
                status=m['Status']
            )
            for m in memberships_data
        ]

    @classmethod
    def create_membership(cls, account_id, plan, duration):
        today = datetime.today().date()

        memberships = cls.get_all_memberships_by_account(account_id)

        latest_end_date = None
        if memberships:
            latest_end_date = max(m.end_date for m in memberships if m.end_date)

        if latest_end_date and latest_end_date > today:
            start_date = latest_end_date
        else:
            start_date = today

        end_date = start_date + timedelta(days=30 * duration)

        return {
            "idAccount": account_id,
            "MembershipType": plan,
            "StartDate": start_date.strftime('%Y-%m-%d'),
            "EndDate": end_date.strftime('%Y-%m-%d'),
            "Status": "Active"
        }

    @staticmethod
    def add_membership(membership_data):
        cursor = mysql.connection.cursor()
        cursor.execute("""
                INSERT INTO membership (idAccount, MembershipType, StartDate, EndDate, Status)
                VALUES (%s, %s, %s, %s, %s)
            """, (
            membership_data["idAccount"],
            membership_data["MembershipType"],
            membership_data["StartDate"],
            membership_data["EndDate"],
            membership_data["Status"]
        ))
        mysql.connection.commit()
        cursor.close()


    @staticmethod
    def calculate_price(plan, duration):
        membership_pricing = {
            "Basic": 200000,
            "Premium": 300000
        }

        discount_rates = {
            3: 0.10,
            6: 0.20,
            12: 0.30
        }

        base_price = membership_pricing.get(plan)
        if base_price is None:
            return Decimal("0.00")

        total_price = Decimal(base_price * duration)

        discount = discount_rates.get(duration, 0)
        discounted_price = total_price * (1 - Decimal(discount))

        return round(discounted_price, 2)

    def days_left(self):

        if not self.end_date:
            return None
        today = datetime.today().date()
        remaining_days = (self.end_date - today).days
        return max(0, remaining_days)

    def display_info(self):
        return {
            "ID": self.id_membership,
            "Account ID": self.id_accounts,
            "Membership Type": self.membership_type,
            "Start Date": str(self.start_date),
            "End Date": str(self.end_date) if self.end_date else "N/A",
            "Status": self.status
        }

class Transaction:
    def __init__(self, id_transaction, id_accounts, transaction_date, amount, payment_method, description, id_receiver):
        self.id_transaction = id_transaction
        self.id_accounts = id_accounts
        self.transaction_date = transaction_date
        self.amount = amount
        self.payment_method = payment_method
        self.description = description
        self.id_receiver = id_receiver

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM transactions ORDER BY TransactionDate DESC"
        )
        transactions_data = cursor.fetchall()
        cursor.close()

        return [
            Transaction(
                id_transaction=t["idTransaction"],
                id_accounts=t["idAccount"],
                transaction_date=t["TransactionDate"],
                amount=t["Amount"],
                payment_method=t["PaymentMethod"],
                description=t["Description"],
                id_receiver=t["idReceiver"]
            )
            for t in transactions_data
        ]

    @staticmethod
    def get_transactions_by_account(id_accounts):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM transactions WHERE idAccount = %s ORDER BY TransactionDate DESC",
            (id_accounts,)
        )
        transactions_data = cursor.fetchall()
        cursor.close()

        return [
            Transaction(
                id_transaction=t["idTransaction"],
                id_accounts=t["idAccount"],
                transaction_date=t["TransactionDate"],
                amount=t["Amount"],
                payment_method=t["PaymentMethod"],
                description=t["Description"],
                id_receiver=t["idReceiver"]
            )
            for t in transactions_data
        ]

    @staticmethod
    def get_transactions_by_receiver(id_receiver):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            "SELECT * FROM transactions WHERE idReceiver = %s ORDER BY TransactionDate DESC",
            (id_receiver,)
        )
        transactions_data = cursor.fetchall()
        cursor.close()

        return [
            Transaction(
                id_transaction=t["idTransaction"],
                id_accounts=t["idAccount"],
                transaction_date=t["TransactionDate"],
                amount=t["Amount"],
                payment_method=t["PaymentMethod"],
                description=t["Description"],
                id_receiver=t["idReceiver"]
            )
            for t in transactions_data
        ]

    @staticmethod
    def add_transaction(transaction_data):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (idAccount, TransactionDate, Amount, PaymentMethod, Description, idReceiver)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transaction_data["idAccount"],
            transaction_data["TransactionDate"],
            transaction_data["Amount"],
            transaction_data["PaymentMethod"],
            transaction_data.get("Description", ""),
            transaction_data.get("idReceiver")
        ))
        mysql.connection.commit()
        cursor.close()

    def display_info(self):
        return {
            "ID": self.id_transaction,
            "Transaction Date": str(self.transaction_date),
            "Amount": float(self.amount),
            "Payment Method": self.payment_method,
            "Description": self.description or "",
            "Receiver ID": self.id_receiver,
        }

class Equipment:
    def __init__(self, idEquipment, Name, Category, Brand, PurchaseDate, Quantity, QuantityAvailable, Image, Size, Weight):
        self.id_equipment = idEquipment
        self.name = Name
        self.category = Category
        self.brand = Brand
        self.purchase_date = PurchaseDate
        self.quantity = Quantity
        self.quantity_available = QuantityAvailable
        self.image = Image
        self.size = Size
        self.weight = Weight

    @staticmethod
    def get_all_equipment():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM equipment")
        equipment_data = cursor.fetchall()
        return [Equipment(**equipment) for equipment in equipment_data]

    @staticmethod
    def get_equipment(idEquipment):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM equipment WHERE idEquipment = %s", (idEquipment,))
        equipment_data = cursor.fetchone()
        cursor.close()

        if equipment_data:
            return Equipment(**equipment_data)
        return None

    def display_info(self):
        return {
            "ID": self.id_equipment,
            "Name": str(self.name),
            "Category": str(self.category),
            "Brand": str(self.brand),
            "Quantity": float(self.quantity),
            "Quantity Available": float(self.quantity_available),
            "Image": str(self.image),
            "Size": str(self.size),
            "Weight": str(self.weight),
        }

class Notification:
    @staticmethod
    def get_all_notifications_by_account(account_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT idNotification, Time, Description, Status
            FROM notifications
            WHERE idAccount = %s
            ORDER BY Time DESC
        """, (account_id,))
        notifications = cursor.fetchall()
        cursor.close()
        return notifications

    @staticmethod
    def mark_all_as_read(account_id):
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE notifications
            SET Status = 'Checked'
            WHERE idAccount = %s AND Status = 'Uncheck'
        """, (account_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def create(account_id, description, status='Uncheck'):
        cursor = mysql.connection.cursor()
        cursor.execute("""
                INSERT INTO notifications (idAccount, Time, Description, Status)
                VALUES (%s, NOW(), %s, %s)
            """, (account_id, description, status))
        mysql.connection.commit()
        cursor.close()

class Schedule:
    def __init__(self, Day, Start, End, idStaff, idSchedule=None):
        self.idSchedule = idSchedule
        self.Day = Day
        self.Start = str(Start)
        self.End = str(End)
        self.idStaff = idStaff

    def to_dict(self):
        return {
            "idSchedule": self.idSchedule,
            "Day": self.Day,
            "Start": self.Start,
            "End": self.End,
            "idStaff": self.idStaff
        }

    @staticmethod
    def get_all():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM schedule")
        rows = cursor.fetchall()
        cursor.close()
        return [Schedule(**row) for row in rows]

    @staticmethod
    def get_schedules_by_staff(idStaff):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM schedule WHERE idStaff = %s", (idStaff,))
        rows = cursor.fetchall()
        cursor.close()
        return [Schedule(**row) for row in rows]

    @staticmethod
    def get_schedule_by_day_and_staff(day, idStaff):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM schedule WHERE Day = %s AND idStaff = %s", (day, idStaff))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Schedule(**row)
        return None

    @staticmethod
    def update(idSchedule, start, end):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE schedule SET Start = %s, End = %s WHERE idSchedule = %s", (start, end, idSchedule))
        mysql.connection.commit()

    @staticmethod
    def create(day, start, end, idStaff):
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO schedule (Day, Start, End, idStaff) VALUES (%s, %s, %s, %s)",
                       (day, start, end, idStaff))
        mysql.connection.commit()

    @staticmethod
    def delete_by_day_and_staff(day, idStaff):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM schedule WHERE Day = %s AND idStaff = %s", (day, idStaff))
        mysql.connection.commit()

    def save(self):
        """Lưu hoặc cập nhật lịch trình"""
        if self.idSchedule:
            # Nếu idSchedule đã có, thì cập nhật
            Schedule.update(self.idSchedule, self.Start, self.End)
        else:
            # Nếu không có idSchedule (tức là lịch trình chưa được lưu vào DB), thì tạo mới
            Schedule.create(self.Day, self.Start, self.End, self.idStaff)

class ClassModel:
    @staticmethod
    def get_all_classes():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM classes")
        result = cursor.fetchall()
        cursor.close()
        return result

    @staticmethod
    def get_class_by_id(id_class):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM classes WHERE idClass = %s", (id_class,))
        result = cursor.fetchone()
        cursor.close()
        return result