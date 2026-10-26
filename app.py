
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Employee Performance Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Employee Performance Analysis System")
st.write(
    "Analyse employee attendance, productivity, "
    "and overall performance."
)

# Sample employee dataset
data = {
    "Employee": [
        "Arun", "Priya", "Rahul", "Divya",
        "Kumar", "Meena", "Ravi", "Sneha"
    ],
    "Department": [
        "IT", "HR", "Sales", "IT",
        "Finance", "HR", "Sales", "Finance"
    ],
    "Attendance": [95, 98, 80, 92, 88, 94, 85, 97],
    "Productivity": [90, 85, 75, 96, 82, 91, 79, 93],
    "Performance": [92, 89, 77, 94, 84, 90, 80, 95]
}

df = pd.DataFrame(data)

# Dashboard summary
st.header("Employee Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", len(df))
col2.metric(
    "Average Performance",
    f"{df['Performance'].mean():.1f}%"
)
col3.metric(
    "Average Attendance",
    f"{df['Attendance'].mean():.1f}%"
)
col4.metric(
    "Average Productivity",
    f"{df['Productivity'].mean():.1f}%"
)

# Employee details
st.header("Employee Details")
st.dataframe(df, use_container_width=True)

# Department filter
st.header("Filter Employees")

departments = ["All"] + sorted(df["Department"].unique().tolist())

selected_department = st.selectbox(
    "Select Department",
    departments
)

if selected_department == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[
        df["Department"] == selected_department
    ].copy()

# Performance chart
st.header("1. Employee Performance Chart")

performance_chart = filtered_df.set_index("Employee")[
    "Performance"
]
st.bar_chart(performance_chart)

# Attendance chart
st.header("2. Employee Attendance Chart")

attendance_chart = filtered_df.set_index("Employee")[
    "Attendance"
]
st.bar_chart(attendance_chart)

# Productivity chart
st.header("3. Employee Productivity Chart")

productivity_chart = filtered_df.set_index("Employee")[
    "Productivity"
]
st.bar_chart(productivity_chart)

# Department comparison
st.header("4. Department-wise Performance")

department_scores = df.groupby("Department")[
    "Performance"
].mean()

st.bar_chart(department_scores)

# Performance classification
st.header("5. Performance Classification")

def classify_performance(score):
    if score >= 90:
        return "High"
    elif score >= 75:
        return "Average"
    else:
        return "Needs Improvement"

report_df = df.copy()

report_df["Performance Level"] = report_df[
    "Performance"
].apply(classify_performance)

st.dataframe(report_df, use_container_width=True)

# Top performer
top_employee = df.loc[df["Performance"].idxmax()]

st.success(
    f"Top Performer: {top_employee['Employee']} "
    f"({top_employee['Performance']}%)"
)

# Download report
st.header("6. Download Performance Report")

csv_data = report_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Full Employee Report (CSV)",
    data=csv_data,
    file_name="employee_performance_report.csv",
    mime="text/csv"
)

st.info(
    "Note: This project uses sample employee data "
    "for academic demonstration."
)
