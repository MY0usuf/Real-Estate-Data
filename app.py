from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_login import LoginManager, login_user, current_user, login_required, logout_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import search_transaction as st
import search_rental as sr

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
users = [
    User(1, 'user1', 'password1'),
    User(2, 'user2', 'password2'),
    User(3, 'user3', 'password3')
]

def get_user(username):
    for user in users:
        if user.username == username:
            return user
    return None

app = Flask(__name__)

app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    else:
        return render_template('login-test.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transaction', methods = ['GET','POST'])
@login_required
def transaction():
        if request.method == "POST":
            transaction_column_name = ['Transaction Type', 'Registration type', 'Project', 'Area', 'Usage', 'Property Type','Property Sub Type', 'Property Size (sq.ft)', 'Property Size (sq.m)','Transaction Date']
            
            transaction_type = request.form["transaction_pTrxType"]
            registration_type = request.form["transaction_pIsOffPlan"]
            Project = request.form["transaction_pProjectId"]
            Area = request.form["transaction_pAreaId"]
            Usage = request.form["transaction_pUsageId"]
            Property_type = request.form["transaction_pPropType"]
            property_size_sq_ft = request.form["PropertySizeSqFt"]
            property_size_sq_mt = request.form["PropertySizeSqM"]
            property_sub_type = request.form["transaction_pPropertysubtypeId"]
            start_date = request.form["startDate"]
            session['transaction_transaction_type'] = transaction_type
            session['transaction_registration_type'] = registration_type
            session['transaction_Project'] = Project
            session['transaction_Area'] = Area
            session['transaction_Usage'] = Usage
            session['transaction_Property_type'] = Property_type
            session['transaction_property_size_sq_ft'] = property_size_sq_ft
            session['transaction_property_size_sq_mt'] = property_size_sq_mt
            session['transaction_property_sub_type'] = property_sub_type
            session['transaction_start_date'] = start_date

            print(type(start_date))

            search_value = [transaction_type, registration_type, Project, Area, Usage, Property_type, property_sub_type, property_size_sq_ft, property_size_sq_mt,start_date]
            search_value = st.change(search_value)
            print(search_value)
            matching_rows = st.search(search_value, transaction_column_name)
            matching_rows = matching_rows.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
            matching_rows.reset_index(inplace = True)
            matching_rows.drop("index",axis=1,inplace=True)
            print(matching_rows.shape[0])
            print(matching_rows.head(10))
            if not matching_rows.empty:
                transaction_table = matching_rows.to_html()
                session['transaction_table'] = transaction_table
                print(type(transaction_table))
                return render_template('transaction_table.html', table = transaction_table, property_sub_type_list = st.property_sub_type_list, area_list = st.area_list, area_length = st.area_length, project_list = st.project_list, project_length = st.project_length, property_sub_type_length = st.property_sub_type_length)
            else:
                return "No Data for it"
        return render_template('transaction.html', property_sub_type_list = st.property_sub_type_list, area_list = st.area_list, area_length = st.area_length, project_list = st.project_list, project_length = st.project_length, property_sub_type_length = st.property_sub_type_length)

@app.route('/return_transaction_file')
def return_transaction_file():
    return send_file('C:\\Users\\yousu\\Desktop\\Python Projects\\main-flask\\transaction_results.csv',as_attachment=True)

@app.route('/return_rental_file')
def return_rental_file():
    return send_file('C:\\Users\\yousu\\Desktop\\Python Projects\\main-flask\\rental_results.csv',as_attachment=True)

@app.route('/rental', methods = ['GET','POST'])
@login_required
def rental():
        if request.method == 'POST':
            rental_column_name = ['Version','Area','Property Type','Usage','Project','Property Size (sq.m)','Property Size (sq.ft)']

            version = request.form["rental_pversion"]
            area = request.form["rental_pAreaId"]
            property_type = request.form["rental_pPropType"]
            usage = request.form["rental_pUsageId"]
            project = request.form["rental_pProjectId"]
            property_size_sq_mt = request.form["PropertySizeSqM"]
            property_size_sq_ft = request.form["PropertySizeSqFt"]
            start_date = request.form["startDate"]
            
            session['rental_version'] = version
            session['rental_project'] = project
            session['rental_area'] = area
            session['rental_usage'] = usage
            session['rental_property_type'] = property_type
            session['rental_property_size_sq_ft'] = property_size_sq_ft
            session['rental_property_size_sq_mt'] = property_size_sq_mt
            session['rental_start_date'] = start_date

            search_value = [version, area, property_type, usage, project, property_size_sq_mt, property_size_sq_ft,start_date]
            search_value = sr.change(search_value)
            print(search_value)
            matching_rows = sr.search(search_value, rental_column_name)
            matching_rows = matching_rows.applymap(lambda x: round(x, 2) if isinstance(x, (int, float)) else x)
            matching_rows.reset_index(inplace = True)
            matching_rows.drop("index",axis=1,inplace=True)
            print(matching_rows.head(10))
            if not matching_rows.empty:
                rental_table = matching_rows.to_html()
                print(type(rental_table))
                return render_template('rental_table.html', table = rental_table, area_list = sr.area_list, area_length = sr.area_length, project_list = sr.project_list, project_length = sr.project_length)
            else:
                return "No Data for it"
        return render_template('rental.html', area_list = sr.area_list, area_length = sr.area_length, project_list = sr.project_list, project_length = sr.project_length)

if __name__ == '__main__':
    app.run(debug = True)