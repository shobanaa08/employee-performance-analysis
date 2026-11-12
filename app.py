import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

st.set_page_config(page_title="Employee Performance Management System", page_icon="📊", layout="wide")
DB = "employee_performance.db"
DEMO_USER, DEMO_PASS = "admin", "admin123"  # Demo only; not production security.

def connect():
    return sqlite3.connect(DB, check_same_thread=False)

def setup_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS employees(
            employee_id TEXT PRIMARY KEY, employee_name TEXT NOT NULL,
            department TEXT NOT NULL, designation TEXT NOT NULL,
            attendance REAL NOT NULL, productivity REAL NOT NULL,
            performance REAL NOT NULL, review_date TEXT NOT NULL)""")
        if con.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
            sample = [
                ("EMP001","Arun","IT","Developer",95,90,92,"2026-10-01"),
                ("EMP002","Priya","HR","HR Associate",98,85,89,"2026-10-01"),
                ("EMP003","Rahul","Sales","Sales Executive",80,75,77,"2026-10-01"),
                ("EMP004","Divya","IT","Tester",92,96,94,"2026-10-01"),
                ("EMP005","Kumar","Finance","Accountant",88,82,84,"2026-10-01"),
                ("EMP006","Meena","HR","Recruiter",94,91,90,"2026-10-01"),
                ("EMP007","Ravi","Sales","Sales Associate",85,79,80,"2026-10-01"),
                ("EMP008","Sneha","Finance","Analyst",97,93,95,"2026-10-01")]
            con.executemany("INSERT INTO employees VALUES(?,?,?,?,?,?,?,?)", sample)

def read_data():
    with connect() as con:
        return pd.read_sql_query("SELECT * FROM employees ORDER BY employee_id", con)

def level(score):
    return "High" if score >= 90 else "Average" if score >= 75 else "Needs Improvement"

setup_db()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Employee Performance Management System")
    st.write("Sign in to access the MCA mini-project application.")
    with st.form("login"):
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        go = st.form_submit_button("Login")
    if go:
        if user == DEMO_USER and pwd == DEMO_PASS:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Incorrect username or password.")
    st.info("Demo login — Username: admin | Password: admin123")
    st.warning("Demo credentials only. This is not production-grade authentication.")
    st.stop()

st.sidebar.title("Project Navigation")
page = st.sidebar.radio("Open module", [
    "Dashboard", "Add Employee", "Manage Employees",
    "Performance Evaluation", "Analytics & Reports"])
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("Employee Performance Management and Analytics System")
st.caption("MCA Mini Project | Python • Streamlit • SQLite")
df = read_data()

if page == "Dashboard":
    st.header("Dashboard")
    a,b,c,d = st.columns(4)
    a.metric("Total Employees", len(df))
    b.metric("Average Performance", f"{df.performance.mean():.1f}%" if len(df) else "0%")
    c.metric("Average Attendance", f"{df.attendance.mean():.1f}%" if len(df) else "0%")
    d.metric("Average Productivity", f"{df.productivity.mean():.1f}%" if len(df) else "0%")
    st.subheader("Employee Records")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if len(df):
        best = df.loc[df.performance.idxmax()]
        st.success(f"Highest score: {best.employee_name} — {best.performance:.0f}%")
    st.info("Initial records are sample data for academic demonstration.")

elif page == "Add Employee":
    st.header("Add New Employee")
    with st.form("add"):
        x,y = st.columns(2)
        empid = x.text_input("Employee ID", placeholder="EMP009").strip().upper()
        name = y.text_input("Employee Name").strip()
        dept = x.selectbox("Department", ["IT","HR","Sales","Finance","Operations","Other"])
        role = y.text_input("Designation").strip()
        att = x.number_input("Attendance (%)", 0.0, 100.0, 90.0)
        prod = y.number_input("Productivity (%)", 0.0, 100.0, 85.0)
        perf = x.number_input("Performance (%)", 0.0, 100.0, 85.0)
        review = y.date_input("Review Date", date.today())
        save = st.form_submit_button("Save Employee")
    if save:
        if not empid or not name or not role:
            st.error("Employee ID, name and designation are required.")
        else:
            try:
                with connect() as con:
                    con.execute("INSERT INTO employees VALUES(?,?,?,?,?,?,?,?)",
                        (empid,name,dept,role,att,prod,perf,review.isoformat()))
                st.success("Employee added successfully.")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error("Employee ID already exists. Enter a unique ID.")

elif page == "Manage Employees":
    st.header("View, Update and Delete Employees")
    st.dataframe(df, use_container_width=True, hide_index=True)
    if len(df):
        empid = st.selectbox("Choose Employee ID", df.employee_id.tolist())
        row = df[df.employee_id == empid].iloc[0]
        with st.form("update"):
            name = st.text_input("Employee Name", str(row.employee_name))
            deptlist = ["IT","HR","Sales","Finance","Operations","Other"]
            olddept = str(row.department)
            dept = st.selectbox("Department", deptlist, index=deptlist.index(olddept) if olddept in deptlist else 5)
            role = st.text_input("Designation", str(row.designation))
            att = st.number_input("Attendance (%)", 0.0, 100.0, float(row.attendance))
            prod = st.number_input("Productivity (%)", 0.0, 100.0, float(row.productivity))
            perf = st.number_input("Performance (%)", 0.0, 100.0, float(row.performance))
            review = st.date_input("Review Date", date.fromisoformat(str(row.review_date)))
            update = st.form_submit_button("Update Record")
        if update:
            if not name.strip() or not role.strip():
                st.error("Name and designation cannot be empty.")
            else:
                with connect() as con:
                    con.execute("""UPDATE employees SET employee_name=?,department=?,designation=?,
                    attendance=?,productivity=?,performance=?,review_date=? WHERE employee_id=?""",
                    (name.strip(),dept,role.strip(),att,prod,perf,review.isoformat(),empid))
                st.success("Record updated.")
                st.rerun()
        confirm = st.checkbox(f"Confirm deletion of {empid}")
        if st.button("Delete Selected Employee", disabled=not confirm):
            with connect() as con:
                con.execute("DELETE FROM employees WHERE employee_id=?", (empid,))
            st.success("Employee deleted.")
            st.rerun()

elif page == "Performance Evaluation":
    st.header("Performance Evaluation")
    if len(df):
        empid = st.selectbox("Select Employee", df.employee_id.tolist())
        row = df[df.employee_id == empid].iloc[0]
        st.write(f"Employee: **{row.employee_name}** | Department: **{row.department}**")
        with st.form("evaluation"):
            att = st.slider("Attendance (%)", 0, 100, int(row.attendance))
            prod = st.slider("Productivity (%)", 0, 100, int(row.productivity))
            perf = st.slider("Performance Score (%)", 0, 100, int(row.performance))
            review = st.date_input("Evaluation Date", date.today())
            save = st.form_submit_button("Save Evaluation")
        if save:
            with connect() as con:
                con.execute("""UPDATE employees SET attendance=?,productivity=?,performance=?,review_date=?
                WHERE employee_id=?""", (att,prod,perf,review.isoformat(),empid))
            st.success("Evaluation saved.")
            st.rerun()
    else:
        st.info("Add an employee first.")

elif page == "Analytics & Reports":
    st.header("Analytics and Reports")
    if len(df):
        df["performance_level"] = df.performance.apply(level)
        departments = ["All"] + sorted(df.department.unique().tolist())
        chosen = st.selectbox("Filter department", departments)
        view = df if chosen == "All" else df[df.department == chosen]
        st.subheader("Performance by Employee")
        st.bar_chart(view.set_index("employee_name")["performance"])
        st.subheader("Attendance")
        st.bar_chart(view.set_index("employee_name")["attendance"])
        st.subheader("Productivity")
        st.bar_chart(view.set_index("employee_name")["productivity"])
        st.subheader("Department Average Performance")
        st.bar_chart(df.groupby("department")["performance"].mean())
        st.subheader("Performance Classification")
        st.dataframe(view[["employee_id","employee_name","department","performance","performance_level"]],
                     use_container_width=True, hide_index=True)
        st.download_button("Download Employee Report (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "employee_performance_report.csv","text/csv")
    else:
        st.info("No employee records available.")
