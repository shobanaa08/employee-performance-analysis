import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Employee Performance Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("Employee Performance Analysis System")
st.write("Analyse employee attendance, productivity and performance.")

data = {
    "Employee": ["Arun", "Priya", "Rahul", "Divya", "Kumar"],
    "Department": ["IT", "HR", "Sales", "IT", "Finance"],
    "Attendance": [95, 98, 80, 92, 88],
    "Productivity": [90, 85, 75, 96, 82],
    "Performance": [92, 89, 77, 94, 84]
}

df = pd.DataFrame(data)

st.subheader("Employee Performance Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Employees", len(df))
col2.metric("Average Performance", f"{df['Performance'].mean():.1f}%")
col3.metric("Average Attendance", f"{df['Attendance'].mean():.1f}%")

st.subheader("Employee Details")
st.dataframe(df, use_container_width=True)

st.subheader("Department Filter")

departments = ["All"] + sorted(df["Department"].unique().tolist())
selected = st.selectbox("Select Department", departments)

if selected == "All":
    filtered_df = df
else:
    filtered_df = df[df["Department"] == selected]

st.subheader("Performance Analysis")

st.bar_chart(
    filtered_df.set_index("Employee")["Performance"]
)

st.subheader("Attendance Analysis")

st.bar_chart(
    filtered_df.set_index("Employee")["Attendance"]
)

st.subheader("Top Performing Employee")

top_employee = df.loc[df["Performance"].idxmax()]

st.success(
    f"{top_employee['Employee']} - "
    f"{top_employee['Performance']}%"
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Employee Report",
    data=csv,
    file_name="employee_performance_report.csv",
    mime="text/csv"
)
