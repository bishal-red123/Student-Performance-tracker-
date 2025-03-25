import streamlit as st
import pandas as pd
import os

from models.student import Student
from models.grade_calculator import GradeCalculator
from utils.data_processor import DataProcessor

# Set page configuration
st.set_page_config(
    page_title="Student Grading System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables if they don't exist
if "students" not in st.session_state:
    st.session_state.students = []
if "dataframe" not in st.session_state:
    st.session_state.dataframe = None
if "calculator" not in st.session_state:
    st.session_state.calculator = GradeCalculator()
if "processor" not in st.session_state:
    st.session_state.processor = DataProcessor()

# Application title and description
st.title("Comprehensive Student Grading System")
st.markdown("""
This system evaluates student performance based on multiple criteria:
- Academic Performance
- Co-curricular Activities
- Discipline Records
""")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Home", "Dashboard", "Student Profiles", "Statistics"]
)

# File upload section
st.sidebar.header("Data Import")
uploaded_file = st.sidebar.file_uploader("Upload Student Data", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Save the uploaded file temporarily
        with open(f"temp_{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        file_path = f"temp_{uploaded_file.name}"
        
        # Use the DataProcessor to load and process the file
        data = st.session_state.processor.load_data(file_path)
        
        # Process the data
        st.session_state.dataframe = data
        st.session_state.students = st.session_state.processor.dataframe_to_students(data)
        st.success(f"Successfully loaded data for {len(st.session_state.students)} students!")
        
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Show sample of the data
        st.subheader("Preview of Uploaded Data")
        st.dataframe(data.head())
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")

# Export data option
if st.session_state.dataframe is not None:
    if st.sidebar.button("Export Processed Data"):
        processed_df = st.session_state.processor.students_to_dataframe(st.session_state.students)
        processed_csv = processed_df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Download CSV",
            data=processed_csv,
            file_name="processed_student_data.csv",
            mime="text/csv"
        )

# Display appropriate page content based on selection
if page == "Home":
    # Home page content
    if st.session_state.dataframe is None:
        st.info("👈 Please upload a file (CSV or Excel) with student data to begin.")
        
        # Example data format
        st.subheader("Expected Data Format")
        example_data = {
            'student_id': ['S001', 'S002', 'S003'],
            'name': ['John Doe', 'Jane Smith', 'Alex Johnson'],
            'academic_score': [85, 92, 78],
            'cocurricular_score': [75, 80, 92],
            'discipline_score': [90, 88, 85]
        }
        example_df = pd.DataFrame(example_data)
        st.dataframe(example_df)
        
        st.markdown("""
        ### Required Columns:
        - **student_id**: Unique identifier for each student
        - **name**: Student's full name
        - **academic_score**: Score representing academic performance (0-100)
        - **cocurricular_score**: Score representing co-curricular activities (0-100)
        - **discipline_score**: Score representing discipline record (0-100)
        
        ### Optional Columns:
        - **class**: Student's class or grade level
        - **section**: Student's section within the class
        - **attendance**: Attendance percentage
        - Any other relevant metrics
        """)
    else:
        # Display summary statistics
        st.subheader("Data Summary")
        total_students = len(st.session_state.students)
        avg_academic = st.session_state.dataframe['academic_score'].mean()
        avg_cocurricular = st.session_state.dataframe['cocurricular_score'].mean()
        avg_discipline = st.session_state.dataframe['discipline_score'].mean()
        
        # Creating columns for metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Students", f"{total_students}")
        col2.metric("Avg. Academic Score", f"{avg_academic:.2f}")
        col3.metric("Avg. Co-curricular Score", f"{avg_cocurricular:.2f}")
        col4.metric("Avg. Discipline Score", f"{avg_discipline:.2f}")
        
        # Display overall grade distribution
        processed_df = st.session_state.processor.students_to_dataframe(st.session_state.students)
        
        st.subheader("Overall Grade Distribution")
        grade_counts = processed_df['overall_grade'].value_counts().sort_index()
        st.bar_chart(grade_counts)
        
        # Quick actions section
        st.subheader("Quick Actions")
        quick_action = st.selectbox("Select Action", [
            "View Top 5 Students",
            "View Students Needing Improvement", 
            "View Balanced Performers"
        ])
        
        if quick_action == "View Top 5 Students":
            top_students = processed_df.sort_values('overall_score', ascending=False).head(5)
            st.dataframe(top_students[['name', 'academic_score', 'cocurricular_score', 
                                       'discipline_score', 'overall_score', 'overall_grade']])
        
        elif quick_action == "View Students Needing Improvement":
            low_performers = processed_df[processed_df['overall_grade'].isin(['D', 'F'])].sort_values('overall_score')
            st.dataframe(low_performers[['name', 'academic_score', 'cocurricular_score', 
                                         'discipline_score', 'overall_score', 'overall_grade']])
        
        elif quick_action == "View Balanced Performers":
            # Students with relatively balanced scores across all metrics
            processed_df['score_std'] = processed_df[['academic_score', 'cocurricular_score', 'discipline_score']].std(axis=1)
            balanced = processed_df.sort_values('score_std').head(5)
            st.dataframe(balanced[['name', 'academic_score', 'cocurricular_score', 
                                   'discipline_score', 'overall_score', 'overall_grade']])

elif page == "Dashboard":
    import importlib
    dashboard = importlib.import_module("pages.dashboard")
    dashboard.show()

elif page == "Student Profiles":
    import importlib
    profiles = importlib.import_module("pages.student_profiles")
    profiles.show()

elif page == "Statistics":
    import importlib
    statistics = importlib.import_module("pages.statistics")
    statistics.show()
