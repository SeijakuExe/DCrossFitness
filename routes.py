from flask import Flask, url_for, jsonify, render_template, request, session, flash, redirect, Response
from datetime import datetime, time, timedelta
import MySQLdb.cursors
import paypalrestsdk
import random
import requests
from pyzbar.pyzbar import decode
from PIL import Image
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import app, mysql
from models import Account, Area, Exercise, Equipment, Membership, Transaction, Notification, Schedule, ClassModel

@app.route('/')
def home():
    if 'account' in session:
        return redirect(url_for('menu'))
    else:
        dark_mode = session.get('dark_mode', False)
        return render_template('home.html', dark_mode=dark_mode)

@app.route('/collection')
def collection():
    areas = Area.get_all_areas()
    exercises_dict = {area.id_area: Exercise.get_exercises_by_area(area.id_area) for area in areas}


    areas_json = {
        str(area.id_area): {
            "name": area.name.upper(),
            "description": area.description,
            "note": area.note
        } for area in areas
    }


    exercises_dict_json = {
        str(area_id): [
            {"name": exercise.name, "repetition": exercise.repetition}
            for exercise in exercises
        ] for area_id, exercises in exercises_dict.items()
    }

    return render_template(
        'collection.html',
        areas=areas,
        exercises_dict=exercises_dict,
        areas_json=jsonify(areas_json).get_data(as_text=True),
        exercises_dict_json=jsonify(exercises_dict_json).get_data(as_text=True)
    )


@app.route('/back')
def back():
    if 'account' in session:
        return redirect(url_for('menu'))
    else:
        return redirect(url_for('home'))



@app.route('/menu')
def menu():
    if 'account' in session:
        access = session['account'].get('Access')
        dark_mode = session.get('dark_mode', False)

        if access == 'Customer':
            return render_template('menu.html', account=session['account'], dark_mode=dark_mode)
        elif access == 'Receptionist':
            return render_template('menu_receptionist.html', account=session['account'], dark_mode=dark_mode)
        elif access == 'Manager':
            return render_template('menu_manager.html', account=session['account'], dark_mode=dark_mode)
        elif access == 'Trainer':
            return render_template('menu_trainer.html', account=session['account'], dark_mode=dark_mode)
        elif access == 'Warranty':
            return render_template('menu_warranty.html', account=session['account'], dark_mode=dark_mode)
        else:
            flash("Access level not recognized.", "danger")
            return redirect(url_for('login'))
    else:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))



from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE Username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()

        if user_data and check_password_hash(user_data['Password'], password):
            account = Account.get_account_by_id(user_data['idAccount'])
            if account:
                session['account'] = account.display_info()

                # Gọi expire notification nếu là Customer
                if account.access == 'Customer':
                    check_and_send_expire_notification(account.id_accounts)

                flash("Login successful!", "success")
                return redirect(url_for('menu'))

        flash("Invalid username or password", "error")
        return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('account', None)
    session.pop('membership', None)
    session.pop('transaction', None)
    session['dark_mode'] = False
    flash("You have successfully logged out.", "info")
    return redirect(url_for('home'))


@app.route('/check-session', methods=['GET'])
def check_session():
    return jsonify(dict(session))

@app.route('/profile')
def profile():
    if 'account' in session:
        account = session['account']
        memberships = Membership.get_all_memberships_by_account(account['ID'])
        today = datetime.today().date()
        active_membership = None
        for membership in memberships:
            if membership.start_date <= today <= membership.end_date:
                active_membership = membership
                break
        transactions = Transaction.get_transactions_by_account(account['ID'])
        receives = Transaction.get_transactions_by_receiver(account['ID'])

        return jsonify({
            "status": "success",
            "account": account,
            "memberships": [m.display_info() for m in memberships],
            "transactions": [t.display_info() for t in transactions],
            "receives": [t.display_info() for t in receives],
            "in_use": active_membership.id_membership if active_membership else None,
            "days_left": max((membership.days_left() for membership in memberships), default=0)
        }), 200
    else:
        return jsonify({"status": "error", "message": "Not logged in"}), 401


@app.route('/get-customer')
def get_customer():
    if 'account' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    access = session['account'].get('Access')

    if access in ['Receptionist', 'Manager']:
        customers = Account.get_all_customers()

        customer_list = []
        for customer in customers:
            info = customer.display_info()
            formatted = {
                'id': info['ID'],
                'name': info['Name'],
                'phone': info['Phone'],
                'username': info['Username'],
                'gender': info['Gender'],
                'birth': info['Birth'],
                'access': info['Access']
            }
            customer_list.append(formatted)

        return jsonify({"status": "success", "customers": customer_list})
    else:
        return jsonify({"status": "error", "message": "Access not allowed"}), 403

@app.route('/get-staff')
def get_staff():
    if 'account' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

    access = session['account'].get('Access')

    if access == 'Manager':
        accounts = Account.get_all_staff()

        account_list = []
        for account in accounts:
            info = account.display_info()
            formatted = {
                'id': info['ID'],
                'name': info['Name'],
                'phone': info['Phone'],
                'username': info['Username'],
                'gender': info['Gender'],
                'birth': info['Birth'],
                'access': info['Access']
            }
            account_list.append(formatted)

        return jsonify({"status": "success", "accounts": account_list})
    else:
        return jsonify({"status": "error", "message": "Access not allowed"}), 403

@app.route('/manage-customer/<int:id>')
def manage_customer(id):
    account = Account.get_account_by_id(id)
    memberships = Membership.get_all_memberships_by_account(id)

    if account:
        customer = account.display_info()
        return render_template('manage_customer.html', customer=customer, memberships=memberships)

@app.route('/manage-staff/<int:id>', methods=['GET', 'POST'])
def manage_staff(id):
    session_access = session.get('account', {}).get('Access')
    if session_access != 'Manager':
        flash("Access denied.", "error")
        return redirect(url_for('menu'))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        birth = request.form['birth']
        access = request.form['access']
        username = request.form['username']

        cursor.execute("""
            UPDATE accounts 
            SET Name=%s, Phone=%s, Gender=%s, Birth=%s, Access=%s, Username=%s
            WHERE idAccount=%s
        """, (name, phone, gender, birth, access, username, id))

        # Xử lý schedule với class Schedule
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            start_time = request.form.get(f'start_{day}')
            end_time = request.form.get(f'end_{day}')

            # Kiểm tra nếu có giá trị giờ bắt đầu và kết thúc, tiến hành cập nhật
            if start_time and end_time:
                existing_schedule = Schedule.get_schedule_by_day_and_staff(day, id)
                if existing_schedule:
                    # Cập nhật schedule nếu có tồn tại
                    existing_schedule.Start = start_time
                    existing_schedule.End = end_time
                    existing_schedule.save()  # Giả sử bạn có phương thức save() để lưu vào DB

                else:
                    # Nếu không tồn tại lịch trình, tạo mới
                    new_schedule = Schedule(
                        Day=day,
                        Start=start_time,
                        End=end_time,
                        idStaff=id
                    )
                    new_schedule.save()  # Lưu lịch trình mới vào DB

            else:
                # Nếu không có giá trị giờ bắt đầu và kết thúc, xóa lịch trình cũ (nếu có)
                existing_schedule = Schedule.get_schedule_by_day_and_staff(day, id)
                if existing_schedule:
                    existing_schedule.delete_by_day_and_staff(day, id)  # Xóa lịch trình cũ

        flash("Updated.", "success")
    # GET
    account = Account.get_account_by_id(id)
    staff = account.display_info()

    schedules_raw = Schedule.get_schedules_by_staff(id)
    schedules = {
        s.Day: {
            'Start': datetime.strptime(s.Start, '%H:%M:%S').time() if s.Start else None,
            'End': datetime.strptime(s.End, '%H:%M:%S').time() if s.End else None
        } for s in schedules_raw
    }
    return render_template("manage_staff.html", staff=staff, schedules=schedules)




@app.route('/print-card/<int:id>', methods=['POST'])
def print_card(id):
    if request.method == 'POST':
        account = Account.get_account_by_id(id)
        if account:
            customer = account.display_info()
            return render_template('print_card.html', account=customer)



@app.route('/request-print', methods=['POST'])
def request_print():
    if 'account' not in session:
        return redirect('/login')

    account = session['account']
    account_id = account['ID']
    name = account['Name']

    current_day = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("""
        SELECT s.Start, s.idStaff
        FROM schedule s
        INNER JOIN accounts a ON s.idStaff = a.idAccount
        WHERE a.Access = 'Receptionist'
        AND s.Day = %s
        AND s.Start >= %s
        ORDER BY s.Start ASC
        LIMIT 1
    """, (current_day, current_time))

    schedule = cursor.fetchone()

    # Nếu không có ca nào hôm nay => xét ngày mai
    if not schedule:
        next_day = (datetime.now() + timedelta(days=1)).strftime('%A')
        cursor.execute("""
            SELECT s.Start, s.idStaff
            FROM schedule s
            INNER JOIN accounts a ON s.idStaff = a.idAccount
            WHERE a.Access = 'Receptionist'
            AND s.Day = %s
            ORDER BY s.Start ASC
            LIMIT 1
        """, (next_day,))
        schedule = cursor.fetchone()

    if not schedule:
        flash("No schedule found", "fail")
        return redirect(url_for('menu'))

    receptionist_id = schedule['idStaff']

    description = f"Customer {name}, ID: {account_id} requested membership card print."

    Notification.create(receptionist_id, description)

    cursor.close()

    flash('Membership card print request sent successfully.', 'success')
    return redirect(url_for('menu'))



@app.route('/update-customer/<int:id>', methods=['POST'])
def update_customer(id):
    name = request.form['name']
    phone = request.form['phone']
    gender = request.form['gender']
    birth = request.form['birth']

    account = Account.get_account_by_id(id)

    if account:
        account.update_account(name, phone, gender, birth)

        flash("Customer updated successfully.", "success")

        return redirect(url_for('menu'))
    else:
        flash("Customer not found.", "warning")
        return redirect(url_for('menu'))

@app.route('/delete-customer/<int:id>', methods=['POST'])
def delete_customer(id):
    if 'account' in session:
        Account.delete_account_by_id(id)
        return redirect(url_for('menu'))

@app.route('/account/<int:id_accounts>', methods=['GET'])
def get_account(id_accounts):
    account = Account.get_account_by_id(id_accounts)
    if account:
        return jsonify({"status": "success", "account": account.display_info()})
    else:
        return jsonify({"status": "error", "message": "Account not found"}), 404


@app.route('/register', methods=['GET', 'POST'])
def register():
    access = session.get('account', {}).get('Access', None)

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        birth = request.form.get('birth') or None  # optional

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM accounts WHERE Phone = %s", (phone,))
            existing_user = cursor.fetchone()

            if access in ['Receptionist', 'Manager']:
                if existing_user:
                    flash("Phone number already exists!", "error")
                    return redirect(url_for('register'))

                cursor.execute("""
                    INSERT INTO accounts (Name, Phone, Gender, Birth) 
                    VALUES (%s, %s, %s, %s)
                """, (name, phone, gender, birth))
                mysql.connection.commit()
                flash("Customer added.", "success")
                return redirect(url_for('menu'))

            else:
                username = request.form['username']
                form_password = request.form['password']
                password = generate_password_hash(form_password)

                if existing_user:
                    if not existing_user['Username'] and not existing_user['Password']:
                        # Update blank account
                        cursor.execute("""
                            UPDATE accounts 
                            SET Name=%s, Username=%s, Password=%s, Gender=%s, Birth=%s
                            WHERE Phone=%s
                        """, (name, username, password, gender, birth, phone))
                        mysql.connection.commit()
                        flash("Account updated successfully. Please log in.", "success")
                        return redirect(url_for('login'))
                    else:
                        flash("Phone number already exists!", "error")
                        return redirect(url_for('register'))

                cursor.execute("""
                    INSERT INTO accounts (Name, Phone, Username, Password, Gender, Birth) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, phone, username, password, gender, birth))
                mysql.connection.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('login'))

        except MySQLdb.IntegrityError:
            flash("Username already exists!", "error")
            return redirect(url_for('register'))

        finally:
            cursor.close()

    return render_template('register.html', access=access)

@app.route('/add-staff', methods=['GET', 'POST'])
def add_staff():
    session_access = session.get('account', {}).get('Access')

    if not session_access:
        flash("Unauthorized access.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        birth = request.form.get('birth') or None
        username = request.form['username']
        form_password = request.form['password']
        password = generate_password_hash(form_password)
        new_access = request.form.get('access')

        if session_access != 'Manager' and new_access == 'Manager':
            flash("You are not allowed to create a Manager account.", "error")
            return redirect(url_for('add_staff'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        try:
            cursor.execute("SELECT * FROM accounts WHERE Phone = %s", (phone,))
            if cursor.fetchone():
                flash("Phone number already exists!", "error")
                return redirect(url_for('add_staff'))

            cursor.execute("SELECT * FROM accounts WHERE Username = %s", (username,))
            if cursor.fetchone():
                flash("Username already exists!", "error")
                return redirect(url_for('add_staff'))

            cursor.execute("""
                INSERT INTO accounts (Name, Phone, Username, Password, Gender, Birth, Access) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, phone, username, password, gender, birth, new_access))

            mysql.connection.commit()
            flash("Staff added.", "success")
            return redirect(url_for('menu'))

        except Exception as e:
            print("❌ Error:", e)
            flash("Unexpected error occurred.", "error")
            return redirect(url_for('add_staff'))

        finally:
            cursor.close()

    return render_template('add_staff.html', session_access=session_access)








@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'account' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    account = session['account']

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        gender = request.form['gender']
        birth = request.form.get('birth')

        cursor = mysql.connection.cursor()
        try:
            cursor.execute("""
                UPDATE accounts 
                SET Name = %s, Phone = %s, Gender = %s, Birth = %s 
                WHERE idAccount = %s
            """, (name, phone, gender, birth, account['ID']))
            mysql.connection.commit()

            account['Name'] = name
            account['Phone'] = phone
            account['Gender'] = gender
            account['Birth'] = birth
            session['account'] = account

            flash("Profile updated successfully!", "success")
            return redirect(url_for('menu'))

        except Exception as e:
            flash("Error updating profile. Please try again.", "danger")
        finally:
            cursor.close()

    return render_template('edit_profile.html', account=account)


@app.route('/change-password', methods=['GET', 'POST'])
def change_password():
    if 'account' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    account = session['account']

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT Password FROM accounts WHERE idAccount = %s", (account['ID'],))
        user_data = cursor.fetchone()

        if not user_data or not check_password_hash(user_data['Password'], old_password):
            flash("Incorrect old password.", "danger")
            cursor.close()
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            cursor.close()
            return redirect(url_for('change_password'))

        hashed_new_password = generate_password_hash(new_password)
        cursor.execute("UPDATE accounts SET Password = %s WHERE idAccount = %s", (hashed_new_password, account['ID']))
        mysql.connection.commit()
        cursor.close()

        flash("Password changed successfully!", "success")
        return redirect(url_for('menu'))

    return render_template('change_password.html')

@app.route('/toggle-theme')
def toggle_theme():
    dark_mode = session.get('dark_mode', False)
    session['dark_mode'] = not dark_mode
    return redirect(url_for('menu'))


@app.route('/transactions')
def transactions():
    if 'account' not in session:
        flash("You need to log in first.", "warning")
        return redirect(url_for('login'))

    account_id = session['account']['ID']
    transactions = Transaction.get_transactions_by_account(account_id)

    return render_template('transactions.html', transactions=transactions)









@app.route('/equipment')
def equipment():
    equipment = Equipment.get_all_equipment()
    if equipment:
        return jsonify({
            "status": "success",
            "equipment": [item.display_info() for item in equipment],
        })

@app.route('/facilities')
def facilities():
    equipment_list = Equipment.get_all_equipment()
    return render_template('facilities.html', equipment=equipment_list)


@app.route('/facilities/<int:id>')
def facility_detail(id):
    equipment = Equipment.get_equipment(id)

    if not equipment:
        return "Equipment doesn't exist!", 404

    return render_template('facility_detail.html', equipment=equipment)


@app.route('/manage-equipment/<int:id>', methods=['GET', 'POST'])
def manage_equipment(id):
    if 'account' not in session or session['account']['Access'] not in ['Receptionist', 'Manager']:
        return redirect(url_for('home'))

    equipment = Equipment.get_equipment(id)
    if not equipment:
        return "Equipment not found", 404

    if request.method == 'POST':
        name = request.form.get("Name")
        category = request.form.get("Category")
        brand = request.form.get("Brand")
        purchase_date = request.form.get("PurchaseDate")
        quantity = request.form.get("Quantity")
        quantity_available = request.form.get("QuantityAvailable")
        image = request.form.get("ImageUrl")
        size = request.form.get("Size")
        weight = request.form.get("Weight")

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE equipment 
            SET Name=%s, Category=%s, Brand=%s, PurchaseDate=%s, 
                Quantity=%s, QuantityAvailable=%s, Image=%s, Size=%s, Weight=%s 
            WHERE idEquipment=%s
        """, (name, category, brand, purchase_date, quantity, quantity_available, image, size, weight, id))
        mysql.connection.commit()
        cursor.close()

        flash("Equipment updated successfully!", "success")
        return redirect(url_for('manage_equipment', id=id))

    return render_template("manage_equipment.html", equipment=equipment)

@app.route('/delete-equipment/<int:id>')
def delete_equipment(id):
    if 'account' not in session or session['account'].get('Access') not in ['Receptionist', 'Manager']:
        flash("Unauthorized access", "error")
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM equipment WHERE idEquipment = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    flash("Equipment deleted successfully", "success")
    return redirect(url_for('home'))


@app.route('/add-equipment', methods=['GET', 'POST'])
def add_equipment():
    account = session.get("account")
    if not account or account.get("Access") not in ["Receptionist", "Manager"]:
        flash("Unauthorized access", "danger")
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("Name")
        category = request.form.get("Category")
        brand = request.form.get("Brand")
        purchase_date = request.form.get("PurchaseDate")
        quantity = request.form.get("Quantity")
        quantity_available = request.form.get("QuantityAvailable")
        image_url = request.form.get("ImageUrl")
        size = request.form.get("Size")
        weight = request.form.get("Weight")

        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                INSERT INTO equipment (Name, Category, Brand, PurchaseDate, Quantity, QuantityAvailable, Image, Size, Weight)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, category, brand, purchase_date, quantity, quantity_available, image_url, size, weight))
            mysql.connection.commit()
            cursor.close()
            flash("New equipment added successfully!", "success")
            return redirect("/facilities")
        except Exception as e:
            mysql.connection.rollback()
            flash("Failed to add equipment: " + str(e), "danger")

    return render_template("add_equipment.html")





@app.route('/select-plan')
def select_plan():
    plan = request.args.get('plan', 'basic')
    return render_template('select_plan.html', plan=plan)

@app.route('/contact-info')
def contact_info():
    return render_template('contact.html')

@app.route('/add-membership', methods=['POST'])
def add_membership():
    if 'account' in session:
        id = request.form.get('id')
        return render_template('add_membership.html', id=id)




@app.route('/confirm-plan', methods=['POST'])
def confirm_plan():
    session.pop('membership', None)
    session.pop('transaction', None)

    if 'account' in session:
        access = session['account'].get('Access')

        if access == 'Customer':
            plan = request.form.get('plan')
            duration = int(request.form.get('duration', 1))
            payment_method = request.form.get('payment_method', 'Cash')


            valid_plans = ["Basic", "Premium"]
            if plan not in valid_plans:
                return "Error: Invalid membership plan.", 400

            account = session.get('account', {})
            account_id = account.get('ID')

            amount_vnd = Membership.calculate_price(plan, duration)


            new_membership = Membership.create_membership(account_id, plan, duration)

            new_transaction = {
                "idAccount": account_id,
                "TransactionDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Amount": amount_vnd,
                "PaymentMethod": payment_method,
                "Description": f"{plan} Membership for {duration} months",
                "idReceiver": 1
            }

            session['membership'] = new_membership
            session['transaction'] = new_transaction
            session.modified = True

            return redirect(url_for('create_payment', amount=amount_vnd, plan=plan, duration=duration))

        elif access in ['Receptionist', 'Manager']:
            plan = request.form.get('plan')
            duration = int(request.form.get('duration', 1))
            payment_method = request.form.get('payment_method', 'Cash')
            account_id = int(request.form.get('idCustomer'))

            valid_plans = ["Basic", "Premium"]
            if plan not in valid_plans:
                return "Error: Invalid membership plan.", 400

            amount_vnd = Membership.calculate_price(plan, duration)

            new_membership = Membership.create_membership(account_id, plan, duration)

            new_transaction = {
                "idAccount": account_id,
                "TransactionDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "Amount": amount_vnd,
                "PaymentMethod": payment_method,
                "Description": f"{plan} Membership for {duration} months",
                "idReceiver": 1
            }

            Membership.add_membership(new_membership)
            Transaction.add_transaction(new_transaction)

            return redirect(url_for('manage_customer', id=account_id))



def get_exchange_rate():
    url = "https://api.exchangerate-api.com/v4/latest/VND"
    response = requests.get(url)
    return response.json().get("rates", {}).get("USD") if response.status_code == 200 else None


@app.route('/create-payment', methods=['GET'])
def create_payment():
    if 'transaction' not in session:
        return jsonify({"error": "No transaction data in session"}), 400

    amount_vnd = request.args.get('amount', type=float)
    plan = request.args.get('plan')
    duration = request.args.get('duration', type=int)

    try:
        exchange_rate = get_exchange_rate()
        amount = round(amount_vnd * exchange_rate, 2)
    except:
        return jsonify({"error": "Failed to fetch exchange rate"}), 500

    if not amount or not plan or not duration:
        return jsonify({"error": "Invalid payment data"}), 400

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": url_for("execute_payment", _external=True),
            "cancel_url": url_for("cancel_payment", _external=True),
        },
        "transactions": [{
            "amount": {"total": f"{amount:.2f}", "currency": "USD"},
            "description": f"{plan} Membership for {duration} months"
        }]
    })

    if payment.create():
        session['payment_id'] = payment.id
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    else:
        return jsonify({"error": payment.error}), 500



@app.route('/execute-payment', methods=['GET'])
def execute_payment():
    payment_id = session.get('payment_id')
    payer_id = request.args.get('PayerID')

    if not payment_id or not payer_id:
        return jsonify({"error": "Missing payment details"}), 400

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        membership_data = session.get('membership')
        transaction_data = session.get('transaction')

        if not membership_data or not transaction_data:
            return jsonify({"error": "Missing membership or transaction data"}), 400

        Membership.add_membership(membership_data)
        Transaction.add_transaction(transaction_data)

        session.pop('membership', None)
        session.pop('transaction', None)
        session.pop('payment_id', None)
        flash("Payment succeeded.", "success")

        return redirect(url_for('menu'))
    else:
        return jsonify({"error": "Payment execution failed"}), 500


@app.route('/cancel-payment', methods=['GET'])
def cancel_payment():
    session.pop('payment_id', None)
    session.pop('membership', None)
    session.pop('transaction', None)
    flash("Payment canceled", "cancel")
    return redirect(url_for('menu'))





@app.context_processor
def inject_notification_count():
    if 'account' in session:
        user_id = session['account']['ID']
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM notifications WHERE idAccount = %s AND Status = 'Uncheck'",
            (user_id,)
        )
        count = cursor.fetchone()[0]
        cursor.close()
        return dict(notification_count=count)
    return dict(notification_count=0)

# --- Flask route example usage ---
@app.route('/api/notifications')
def get_notifications():
    account = session.get('account')
    if not account:
        return jsonify({'error': 'Unauthorized'}), 401

    id_account = account['ID']
    notifications = Notification.get_all_notifications_by_account(id_account)
    return jsonify(notifications)


@app.route('/api/notifications/mark-read', methods=['POST'])
def mark_notifications_as_read():
    account = session.get('account')
    if not account:
        return jsonify({'error': 'Unauthorized'}), 401

    id_account = account['ID']
    Notification.mark_all_as_read(id_account)
    return jsonify({'success': True})



@app.route('/forget-password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        otp_input = request.form.get('otp')


        otp_session = session.get('otp_code')
        otp_username = session.get('otp_username')

        if not otp_session or not otp_username:
            flash("Please send OTP first.", "error")
            return redirect(url_for('forget_password'))

        if username != otp_username:
            flash("Username does not match with OTP session.", "error")
            return redirect(url_for('forget_password'))

        if otp_input != otp_session:
            flash("Incorrect OTP. Please try again.", "error")
            return redirect(url_for('forget_password'))

        session.pop('otp_code', None)
        session.pop('otp_username', None)

        flash("OTP verified successfully. You can now reset your password.", "success")
        return redirect(url_for('reset_password'))

    return render_template('forget_password.html')


@app.route('/send-otp', methods=['POST'])
def send_otp():
    username = request.form.get('username')
    phone = request.form.get('phone')

    if not username or not phone:
        return jsonify({"status": "error", "message": "Please provide both Username and Phone."}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM accounts WHERE Username = %s", (username,))
    account = cursor.fetchone()
    cursor.close()

    if not account:
        return jsonify({"status": "error", "message": "Username does not exist."}), 400

    if str(account['Phone']) != phone:
        return jsonify({"status": "error", "message": "Phone number does not match."}), 400

    otp_code = str(random.randint(100000, 999999))
    session['otp_code'] = otp_code
    session['otp_username'] = username

    print(f"[DEBUG] OTP for {username}: {otp_code}")

    return jsonify({"status": "success", "message": "OTP has been sent. Please check your phone."})

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    otp = request.form.get('otp')

    # Kiểm tra xem OTP có tồn tại trong session không
    if not otp or otp != session.get('otp_code'):
        return jsonify({"status": "error", "message": "Invalid OTP."}), 400

    # OTP hợp lệ, bạn có thể thực hiện hành động (ví dụ chuyển sang trang reset password)
    return jsonify({"status": "success", "message": "OTP verified successfully."})


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    username = session.get('otp_username')  # Đảm bảo đã lưu từ bước xác nhận OTP

    if not username:
        flash("Session expired. Please try again.", "error")
        return redirect(url_for('forget_password'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('reset_password'))

        # Cập nhật mật khẩu
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE accounts SET Password = %s WHERE Username = %s", (new_password, username))
        mysql.connection.commit()
        cursor.close()

        # Lấy lại thông tin tài khoản
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE Username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()

        # Gọi class Account và lưu session
        account = Account.get_account_by_id(user_data['idAccount'])
        session['account'] = account.display_info()

        # Xóa session OTP
        session.pop('otp_code', None)
        session.pop('otp_username', None)

        flash("Password has been reset and you are now logged in.", "success")
        return redirect(url_for('menu'))

    return render_template('reset_password.html', username=username)







@app.route('/api/schedule')
def get_schedule_by_staff():
    if 'account' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    account = session['account']
    idStaff = account['ID']

    schedules = Schedule.get_schedules_by_staff(idStaff)
    if schedules:
        return jsonify([s.to_dict() for s in schedules])
    else:
        return jsonify([])



def serialize_schedule_row(row):
    return {
        "idSchedule": row["idSchedule"],
        "Day": row["Day"],
        "Start": row["Start"].strftime("%H:%M") if isinstance(row["Start"], time) else str(row["Start"]),
        "End": row["End"].strftime("%H:%M") if isinstance(row["End"], time) else str(row["End"]),
        "idStaff": row["idStaff"]
    }

@app.route('/api/class-info')
def get_class_info():
    if 'account' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    account = session['account']
    id_class = account.get('idClass')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if not id_class:
        cursor.execute("SELECT * FROM classes")
        class_rows = cursor.fetchall()
        result = []
        for class_row in class_rows:
            trainer_id = class_row['idTrainer']

            cursor.execute("SELECT * FROM accounts WHERE idAccount = %s", (trainer_id,))
            trainer = cursor.fetchone()

            cursor.execute("SELECT * FROM schedule WHERE idStaff = %s", (trainer_id,))
            schedule_rows = cursor.fetchall()
            schedules = [serialize_schedule_row(row) for row in schedule_rows]

            result.append({
                'Class': class_row,
                'Trainer': trainer,
                'Schedule': schedules
            })
        cursor.close()
        return jsonify(result)

    cursor.execute("SELECT * FROM classes WHERE idClass = %s", (id_class,))
    class_row = cursor.fetchone()

    if not class_row:
        cursor.close()
        return jsonify({'error': 'Class not found'}), 404

    trainer_id = class_row['idTrainer']

    cursor.execute("SELECT * FROM accounts WHERE idAccount = %s", (trainer_id,))
    trainer = cursor.fetchone()

    cursor.execute("SELECT * FROM schedule WHERE idStaff = %s", (trainer_id,))
    schedule_rows = cursor.fetchall()
    schedules = [serialize_schedule_row(row) for row in schedule_rows]

    cursor.close()

    return jsonify({
        'Class': class_row,
        'Trainer': trainer,
        'Schedule': schedules
    })


@app.route('/enroll-form', methods=['GET', 'POST'])
def enroll_form():
    if 'account' not in session:
        return redirect('/login')

    account = session['account']
    id_account = account['ID']

    if request.method == 'POST':
        class_id = request.form.get('idClass', type=int)
    else:
        class_id = request.args.get('idClass', type=int)

    if not class_id:
        return "Missing or invalid class ID", 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM classes WHERE idClass = %s", (class_id,))
    class_row = cursor.fetchone()

    if not class_row:
        cursor.close()
        return jsonify({'error': 'Class not found'}), 404

    cursor.execute("SELECT COUNT(*) AS count FROM accounts WHERE idClass = %s", (class_id,))
    result = cursor.fetchone()
    enrolled_count = result['count']

    cursor.execute("""
        SELECT COUNT(*) AS active_count
        FROM membership
        WHERE idAccount = %s AND Status = 'Active'
    """, (id_account,))
    active_result = cursor.fetchone()
    active_membership = active_result['active_count']

    if request.method == 'POST':
        if active_membership == 0:
            flash("You must have an active membership to enroll in a class.", "danger")
            cursor.close()
            return redirect('/menu')

        if enrolled_count >= 10:
            flash("This class is full. Please choose another.", "danger")
            cursor.close()
            return redirect('/menu')

        account_obj = Account.get_account_by_id(id_account)
        account_obj.enroll_in_class(class_id)

        account_data = session['account']
        account_data['idClass'] = class_id
        session['account'] = account_data

        flash("Enrolled Successfully!", "success")
        cursor.close()
        return redirect('/menu')

    cursor.close()
    return render_template('enroll_form.html', class_info=class_row)






@app.route('/unenroll-form', methods=['GET', 'POST'])
def unenroll_form():
    if 'account' not in session:
        return redirect('/login')

    account = session['account']
    id_account = account['ID']
    current_class_id = account.get('idClass')

    if not current_class_id:
        return "You are not enrolled in any class.", 400

    if request.method == 'POST':
        account_obj = Account.get_account_by_id(id_account)
        account_obj.unenroll_from_class()

        account_data = session['account']
        account_data['idClass'] = None
        session['account'] = account_data
        flash("Unenrolled Successfully!", "success")
        return redirect('/menu')

    return render_template('unenroll_form.html', class_id=current_class_id)


@app.route('/scan-barcode-image', methods=['GET', 'POST'])
def scan_barcode_image():
    if 'account' not in session or session['account']['Access'] != 'Receptionist':
        flash("Unauthorized access", "error")
        return redirect('/menu')

    if request.method == 'POST':
        file = request.files.get('barcode_image')
        if not file:
            flash("No image uploaded", "error")
            return redirect('/scan-barcode-image')

        image = Image.open(file.stream)
        decoded = decode(image)

        if not decoded:
            flash("No barcode found", "error")
            return redirect('/scan-barcode-image')

        barcode_data = decoded[0].data.decode("utf-8")

        if '-' not in barcode_data:
            flash("Invalid barcode format", "error")
            return redirect('/scan-barcode-image')

        account_id, phone = barcode_data.split('-', 1)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE idAccount = %s AND Phone = %s", (account_id, phone))
        account = cursor.fetchone()

        if not account:
            flash("Account not found", "error")
            cursor.close()
            return redirect('/scan-barcode-image')

        cursor.execute("SELECT COUNT(*) AS active_count FROM membership WHERE idAccount = %s AND Status = 'Active'", (account_id,))
        result = cursor.fetchone()
        cursor.close()

        if result['active_count'] == 0:
            flash("No active membership for this customer", "error")
        else:
            flash(f"Welcome {account['Name']} (ID: {account['idAccount']})", "success")

        return redirect('/scan-barcode-image')

    return render_template('scan_barcode.html')

@app.route('/trainer/my-class')
def trainer_my_class():
    if 'account' not in session or session['account']['Access'] != 'Trainer':
        return jsonify({'status': 'error', 'message': 'Unauthorized access'}), 403

    trainer_id = session['account']['ID']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT * FROM classes WHERE idTrainer = %s", (trainer_id,))
    class_info = cursor.fetchone()

    if not class_info:
        cursor.close()
        return jsonify({'status': 'error', 'message': 'No class found for this trainer'}), 404

    cursor.execute("""
        SELECT idAccount, Name, Phone, Gender, Birth 
        FROM accounts 
        WHERE idClass = %s AND Access = 'Customer'
    """, (class_info['idClass'],))
    students = cursor.fetchall()

    cursor.close()

    return jsonify({
        'status': 'success',
        'class': class_info,
        'students': students
    })

@app.route('/trainer/attendance', methods=['POST'])
def trainer_attendance():
    if 'account' not in session or session['account']['Access'] != 'Trainer':
        return redirect('/login')

    present_ids = request.form.getlist('present_ids')
    present_ids = set(map(int, present_ids))

    trainer_id = session['account']['ID']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute("SELECT idClass FROM classes WHERE idTrainer = %s", (trainer_id,))
    result = cursor.fetchone()
    if not result:
        cursor.close()
        return "No class found", 400

    class_id = result['idClass']
    cursor.execute("SELECT idAccount FROM accounts WHERE idClass = %s", (class_id,))
    all_students = [row['idAccount'] for row in cursor.fetchall()]
    cursor.close()

    absent_ids = [sid for sid in all_students if sid not in present_ids]

    for student_id in absent_ids:
        Notification.create(student_id, "You were marked absent today")
    flash(f"Absent notifications sent!", "success")
    return redirect('/menu')

@app.route('/removeStudent/<int:id>', methods=['GET'])
def remove_student(id):
    if 'account' not in session or session['account']['Access'] != 'Trainer':
        return redirect('/login')

    account = Account.get_account_by_id(id)
    if account:
        account.unenroll_from_class()
        flash(f"Removed student {account.name} from class", "success")
    else:
        flash("Student not found", "error")

    return redirect('/menu')



@app.route('/revenue')
def revenue():
    if 'account' not in session or session['account']['Access'] != 'Manager':
        flash('Access denied. Managers only.', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    query = """
        SELECT t.TransactionDate, t.Amount, t.idAccount, t.idReceiver,
               acc1.Access AS AccountAccess,
               acc2.Access AS ReceiverAccess
        FROM transactions t
        LEFT JOIN accounts acc1 ON t.idAccount = acc1.idAccount
        LEFT JOIN accounts acc2 ON t.idReceiver = acc2.idAccount
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    from collections import defaultdict

    summary = defaultdict(lambda: {
        "income": 0,
        "salary": 0,
        "refund": 0,
        "purchase": 0,
        "total": 0
    })

    for date, amount, id_account, id_receiver, acc_access, recv_access in rows:
        month = date.strftime('%Y-%m')
        amount = float(amount)

        if id_receiver == 1:
            summary[month]["income"] += amount
        elif id_account == 1 and recv_access in ['Receptionist', 'Trainer', 'Warranty']:
            summary[month]["salary"] += amount
        elif id_account == 1 and recv_access == 'Customer':
            summary[month]["refund"] += amount
        elif id_account == 1 and id_receiver is None:
            summary[month]["purchase"] += amount

    # Tính tổng
    for month in summary:
        s = summary[month]
        s["total"] = s["income"] - (s["salary"] + s["refund"] + s["purchase"])

    # Chuyển sang list để truyền vào template
    summary_list = [
        {
            "month": m,
            "income": round(s["income"]),
            "salary": round(s["salary"]),
            "refund": round(s["refund"]),
            "purchase": round(s["purchase"]),
            "total": round(s["total"]),
        }
        for m, s in sorted(summary.items())
    ]

    return render_template('revenue.html', summary=summary_list)
@app.route('/revenue/export')
def export_revenue_csv():
    if 'account' not in session or session['account']['Access'] != 'Manager':
        flash('Access denied. Managers only.', 'danger')
        return redirect(url_for('home'))

    cursor = mysql.connection.cursor()
    query = """
        SELECT t.TransactionDate, t.Amount, t.idAccount, t.idReceiver,
               acc1.Access AS AccountAccess,
               acc2.Access AS ReceiverAccess
        FROM transactions t
        LEFT JOIN accounts acc1 ON t.idAccount = acc1.idAccount
        LEFT JOIN accounts acc2 ON t.idReceiver = acc2.idAccount
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()

    from collections import defaultdict
    from io import StringIO
    import csv

    summary = defaultdict(lambda: {
        "income": 0,
        "salary": 0,
        "refund": 0,
        "purchase": 0,
        "total": 0
    })

    for date, amount, id_account, id_receiver, acc_access, recv_access in rows:
        month = date.strftime('%Y-%m')
        amount = float(amount)

        if id_receiver == 1:
            summary[month]["income"] += amount
        elif id_account == 1 and recv_access in ['Receptionist', 'Trainer', 'Warranty']:
            summary[month]["salary"] += amount
        elif id_account == 1 and recv_access == 'Customer':
            summary[month]["refund"] += amount
        elif id_account == 1 and id_receiver is None:
            summary[month]["purchase"] += amount

    for m in summary:
        s = summary[m]
        s["total"] = s["income"] - (s["salary"] + s["refund"] + s["purchase"])

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Month', 'Income', 'Salary', 'Refund', 'Purchase', 'Total'])

    for m in sorted(summary.keys()):
        s = summary[m]
        writer.writerow([
            m,
            round(s["income"]),
            round(s["salary"]),
            round(s["refund"]),
            round(s["purchase"]),
            round(s["total"]),
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=monthly_revenue.csv'}
    )


@app.route('/create-transaction', methods=['GET', 'POST'])
def create_transaction():
    if 'account' not in session or session['account']['Access'] != 'Manager':
        flash('Access denied. Managers only.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        amount = request.form['amount']
        method = request.form['method']
        description = request.form['description'] or "Facility Purchase"
        receiver_id = request.form.get('receiver') or None
        account_id = session['account']['ID']

        transaction_data = {
            "idAccount": account_id,
            "TransactionDate": datetime.now(),
            "Amount": amount,
            "PaymentMethod": method,
            "Description": description,
            "idReceiver": receiver_id
        }

        Transaction.add_transaction(transaction_data)
        flash('Transaction created successfully.', 'success')
        return redirect(url_for('revenue'))

    receivers = Account.get_all()

    return render_template('create_transaction.html', receivers=receivers)

@app.route('/class-manage-form', methods=['GET', 'POST'])
def class_manage_form():
    access = session.get('account', {}).get('Access')
    if access != 'Manager':
        flash("Access denied.", "error")
        return redirect(url_for('menu'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        action = request.form.get('action')
        id_class = request.form.get('idClass')
        name = request.form.get('name')
        id_trainer = request.form.get('idTrainer')
        id_area = request.form.get('idArea') or None

        try:
            if action == 'add':
                cursor.execute("SELECT * FROM classes WHERE idTrainer = %s", (id_trainer,))
                if cursor.fetchone():
                    flash("This trainer is already assigned to a class!", "error")
                    return redirect(url_for('class_manage_form'))
                cursor.execute("""
                    INSERT INTO classes (idTrainer, Name, idArea)
                    VALUES (%s, %s, %s)
                """, (id_trainer, name, id_area))

            elif action == 'update':
                cursor.execute("""
                    UPDATE classes SET idTrainer=%s, Name=%s, idArea=%s
                    WHERE idClass=%s
                """, (id_trainer, name, id_area, id_class))

            elif action == 'delete':
                cursor.execute("DELETE FROM classes WHERE idClass=%s", (id_class,))

            mysql.connection.commit()
            flash("Action completed successfully!", "success")
        except Exception as e:
            print("❌ Error:", e)
            flash("An error occurred.", "error")
        return redirect(url_for('class_manage_form'))

    # Lấy danh sách lớp, huấn luyện viên và khu vực
    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()

    cursor.execute("SELECT idAccount, Name FROM accounts WHERE Access = 'Trainer'")
    trainers = cursor.fetchall()

    cursor.execute("SELECT * FROM areas")
    areas = cursor.fetchall()

    cursor.close()
    return render_template('class_manage_form.html', classes=classes, trainers=trainers, areas=areas)


@app.route('/expire-notification')
def expire_notification():
    if 'account' in session:
        account = session['account']
        memberships = Membership.get_all_memberships_by_account(account['ID'])
        today = datetime.today().date()
        active_membership = None

        for membership in memberships:
            if membership.start_date <= today <= membership.end_date:
                active_membership = membership
                break

        if active_membership:
            days_left = (active_membership.end_date - today).days
            if days_left < 3:
                description = f"You membership will expire in {days_left} days!"

                cursor = mysql.connection.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM notifications
                    WHERE idAccount = %s AND Description = %s AND DATE(Time) = CURDATE()
                """, (account['ID'], description))
                (count,) = cursor.fetchone()
                cursor.close()

                if count == 0:
                    Notification.create(account['ID'], description)

        return redirect('/menu')
    else:
        return jsonify({"status": "error", "message": "Not logged in"}), 401

def check_and_send_expire_notification(id_accounts):
    memberships = Membership.get_all_memberships_by_account(id_accounts)
    today = datetime.today().date()
    active_membership = None

    for membership in memberships:
        if membership.start_date <= today <= membership.end_date:
            active_membership = membership
            break

    if active_membership:
        days_left = (active_membership.end_date - today).days
        if days_left < 3:
            description = f"Your membership will expire in {days_left} day(s). Please renew soon to avoid interruption."

            cursor = mysql.connection.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM notifications
                WHERE idAccount = %s AND Description = %s AND DATE(Time) = CURDATE()
            """, (id_accounts, description))
            (count,) = cursor.fetchone()
            cursor.close()

            if count == 0:
                Notification.create(id_accounts, description)

