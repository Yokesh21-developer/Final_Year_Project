from flask import Flask, render_template, request, redirect, session, send_file
import mysql.connector
import pandas as pd
import pickle
import os
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.mixture import GaussianMixture
from lightgbm import LGBMClassifier

app = Flask(__name__)
app.secret_key = "telecom"

# ---------------- DATABASE ------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="telecom_db",
    charset="utf8"
)
cursor = db.cursor()

# ---------------- FOLDERS ------------------
os.makedirs("uploads", exist_ok=True)
os.makedirs("models", exist_ok=True)

# ---------------- INDEX ------------------
@app.route('/')
def index():
    return render_template("index.html")

# ---------------- ADMIN LOGIN ------------------
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (u, p))
        if cursor.fetchone():
            session['admin'] = u
            return redirect('/admin_dashboard')
    return render_template("admin_login.html")

# ---------------- TBA LOGIN ------------------
@app.route('/tba_login', methods=['GET','POST'])
def tba_login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']
        cursor.execute("SELECT * FROM telecom_analyst WHERE username=%s AND password=%s", (u, p))
        row = cursor.fetchone()
        if row:
            session['tba'] = row[0]
            session['network'] = row[4]
            return redirect('/tba_dashboard')
    return render_template("tba_login.html")

# ---------------- MARKETING LOGIN ------------------
@app.route('/marketing_login', methods=['GET','POST'])
def marketing_login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']
        cursor.execute("SELECT * FROM marketing_manager WHERE username=%s AND password=%s", (u, p))
        row = cursor.fetchone()
        if row:
            session['marketing'] = row[0]
            session['network'] = row[4]
            return redirect('/marketing_dashboard')
    return render_template("marketing_login.html")

# ---------------- CRM LOGIN ------------------
@app.route('/crm_login', methods=['GET','POST'])
def crm_login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']

        cursor.execute(
            "SELECT * FROM crm_user WHERE username=%s AND password=%s",
            (u, p)
        )
        row = cursor.fetchone()

        if row:
            session['crm'] = row[0]
            session['network'] = row[4]
            return redirect('/crm_dashboard')

    return render_template("crm_login.html")

# ---------------- ADMIN DASHBOARD ------------------
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template("admin_dashboard.html")

@app.route('/add_tba', methods=['GET','POST'])
def add_tba():
    if request.method == "POST":
        data = tuple(request.form.values())
        cursor.execute(
            "INSERT INTO telecom_analyst(name,email,mobile,network_type,username,password) VALUES(%s,%s,%s,%s,%s,%s)",
            data
        )
        db.commit()
    return render_template("add_tba.html")

@app.route('/add_marketing', methods=['GET','POST'])
def add_marketing():
    if request.method == "POST":
        data = tuple(request.form.values())
        cursor.execute(
            "INSERT INTO marketing_manager(name,email,mobile,network_type,username,password) VALUES(%s,%s,%s,%s,%s,%s)",
            data
        )
        db.commit()
    return render_template("add_marketing.html")

# ---------------- ADD CRM ------------------
@app.route('/add_crm', methods=['GET','POST'])
def add_crm():
    if request.method == "POST":
        data = tuple(request.form.values())
        cursor.execute(
            "INSERT INTO crm_user(name,email,mobile,network_type,username,password) VALUES(%s,%s,%s,%s,%s,%s)",
            data
        )
        db.commit()
    return render_template("add_crm.html")

# ---------------- UPLOAD DATASET ------------------
@app.route('/upload_dataset', methods=['GET','POST'])
def upload_dataset():
    if request.method == "POST":
        file = request.files['file']
        path = "uploads/dataset.csv"
        file.save(path)

        df = pd.read_csv(path)
        df = df.where(pd.notnull(df), None)

        cursor.execute("DELETE FROM customers")
        db.commit()

        sql = """INSERT INTO customers(
            customer_id, gender, senior_citizen, partner, dependents, tenure,
            contract_type, paperless_billing, payment_method,
            monthly_call_minutes, monthly_data_usage_gb, number_of_calls,
            international_calls, roaming_usage, monthly_charges,
            total_charges, avg_revenue_per_user, internet_service,
            online_security, tech_support, streaming_tv, streaming_movies,
            network_type, churn_risk, churn, segment, churn_prediction
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        cursor.executemany(sql, df.values.tolist())
        db.commit()

    return render_template("upload_dataset.html")

# ---------------- TRAIN MODEL ------------------
@app.route('/train_model')
def train_model():
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()
    cols = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=cols)

    le = LabelEncoder()
    for col in df.select_dtypes(include='object').columns:
        df[col] = le.fit_transform(df[col].astype(str))

    X = df[['tenure','monthly_data_usage_gb','monthly_charges']]
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    gmm = GaussianMixture(n_components=3)
    df['segment'] = gmm.fit_predict(Xs)
    pickle.dump(gmm, open("models/gmm_model.pkl", "wb"))

    y = df['churn']
    X2 = df.drop(['churn','churn_prediction'], axis=1)

    lgb = LGBMClassifier()
    lgb.fit(X2, y)
    df['churn_prediction'] = lgb.predict(X2)
    pickle.dump(lgb, open("models/lgbm_model.pkl", "wb"))

    cursor.execute("DELETE FROM customers")
    db.commit()

    sql = """INSERT INTO customers(
        customer_id, gender, senior_citizen, partner, dependents, tenure,
        contract_type, paperless_billing, payment_method,
        monthly_call_minutes, monthly_data_usage_gb, number_of_calls,
        international_calls, roaming_usage, monthly_charges,
        total_charges, avg_revenue_per_user, internet_service,
        online_security, tech_support, streaming_tv, streaming_movies,
        network_type, churn_risk, churn, segment, churn_prediction
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cursor.executemany(sql, df.values.tolist())
    db.commit()

    return redirect('/admin_dashboard')

# ---------------- TBA ------------------
@app.route("/tba_dashboard")
def tba_dashboard():
    net = session.get("network")
    return render_template("tba_dashboard.html", network=net)

@app.route('/export_report')
def export_report():
    net = session['network']
    cursor.execute("SELECT * FROM customers WHERE network_type=%s", (net,))
    rows = cursor.fetchall()
    cols = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=cols)
    path = "uploads/report.csv"
    df.to_csv(path, index=False)
    return send_file(path, as_attachment=True)

# ---------------- MARKETING ------------------
import pandas as pd
import random
from flask import session, render_template

@app.route('/marketing_dashboard')
def marketing_dashboard():
    net = session.get("network")

    df = pd.read_csv("static/data/customers.csv")

    if "network_type" in df.columns:
        df = df[df["network_type"] == net]

    if "churn_prediction" in df.columns:
        df = df[df["churn_prediction"] > 0]

    df = df.sample(frac=1)

    limit = random.randint(100, 120)
    df = df.head(limit)

    data = df.to_dict(orient="records")

    return render_template(
        "marketing_dashboard.html",
        tables=data,
        network=net
    )

@app.route("/download_campaign")
def download_campaign():
    net = session.get("network")

    df = pd.read_csv("static/data/customer_churn_data.csv")

    df_filtered = df[
        (df["network_type"] == net) &
        (df["churn_prediction"] == "Yes")
    ]

    df_filtered = df_filtered.sample(n=120)

    path = "static/data/campaign_list.csv"
    df_filtered.to_csv(path, index=False)

    return send_file(path, as_attachment=True)


# ---------------- CRM DASHBOARD ------------------
@app.route('/crm_dashboard')
def crm_dashboard():
    # Ensure CRM user is logged in
    if 'crm' not in session:
        return redirect('/crm_login')

    # Get network for this session
    net = session.get("network")

    # Load dataset
    df = pd.read_csv("static/data/customers.csv")

    # Filter for this network only
    if "network_type" in df.columns:
        df = df[df["network_type"] == net]

    # Filter only high-risk customers
    if "churn_prediction" in df.columns:
        df = df[df["churn_prediction"] >= 0.75]  # High risk threshold

    # Shuffle the high-risk customers
    df = df.sample(frac=1)

    # Limit the number of customers randomly (like marketing dashboard)
    limit = random.randint(50, 100)  # adjust as needed
    df = df.head(limit)

    # Convert to dict for template
    data = df.to_dict(orient="records")

    return render_template(
        "crm_dashboard.html",
        tables=data,
        network=net
    )
# ---------------- LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

app.run(debug=True)
