"""
Dashboard page for the Student Grading System.
This page displays overview visualizations of all student data.
"""

import streamlit as st
from utils.visualizations import Visualizer

def show():
    """
    Display the dashboard page with overview visualizations.
    """
    st.title("Dashboard")
    
    if "students" not in st.session_state or not st.session_state.students:
        st.warning("No data available. Please upload student data from the Home page.")
        return
    
    # Get processed dataframe
    processor = st.session_state.processor
    students_df = processor.students_to_dataframe(st.session_state.students)
    
    # Create dashboard layout
    st.write("### Performance Overview")
    st.write("This dashboard provides an overview of student performance based on multiple criteria.")
    
    # Score distribution section
    st.subheader("Score Distributions")
    metric_option = st.selectbox(
        "Select performance metric",
        ["Overall", "Academic", "Co-curricular", "Discipline"],
        key="dashboard_metric"
    )
    
    col1, col2 = st.columns(2)
    
    if metric_option == "Overall":
        # Overall score histogram
        with col1:
            fig = Visualizer.plot_score_histogram(
                students_df, 
                'overall_score', 
                bins=20, 
                title='Overall Score Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Overall grade distribution
        with col2:
            fig = Visualizer.plot_grade_distribution(
                students_df, 
                'overall_grade', 
                title='Overall Grade Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif metric_option == "Academic":
        # Academic score histogram
        with col1:
            fig = Visualizer.plot_score_histogram(
                students_df, 
                'academic_score', 
                bins=20, 
                title='Academic Score Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Academic grade distribution
        with col2:
            fig = Visualizer.plot_grade_distribution(
                students_df, 
                'academic_grade', 
                title='Academic Grade Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif metric_option == "Co-curricular":
        # Co-curricular score histogram
        with col1:
            fig = Visualizer.plot_score_histogram(
                students_df, 
                'cocurricular_score', 
                bins=20, 
                title='Co-curricular Score Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Co-curricular grade distribution
        with col2:
            fig = Visualizer.plot_grade_distribution(
                students_df, 
                'cocurricular_grade', 
                title='Co-curricular Grade Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif metric_option == "Discipline":
        # Discipline score histogram
        with col1:
            fig = Visualizer.plot_score_histogram(
                students_df, 
                'discipline_score', 
                bins=20, 
                title='Discipline Score Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Discipline grade distribution
        with col2:
            fig = Visualizer.plot_grade_distribution(
                students_df, 
                'discipline_grade', 
                title='Discipline Grade Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Category comparison
    st.subheader("Performance Category Comparison")
    fig = Visualizer.plot_score_comparison(students_df, title="Comparison of Performance Categories")
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation matrix
    st.subheader("Correlation Matrix")
    fig = Visualizer.plot_correlation_matrix(students_df, title="Correlation Between Performance Metrics")
    st.plotly_chart(fig, use_container_width=True)
    
    # Grade distribution by category
    st.subheader("Grade Distribution by Category")
    
    # Melt the grade columns into a single column for easier visualization
    grade_cols = ['academic_grade', 'cocurricular_grade', 'discipline_grade', 'overall_grade']
    category_names = ['Academic', 'Co-curricular', 'Discipline', 'Overall']
    
    # Display grade counts per category
    grade_counts = {}
    for col, name in zip(grade_cols, category_names):
        grade_counts[name] = students_df[col].value_counts().sort_index().to_dict()
    
    # Create a table of grade counts
    import pandas as pd
    grade_table = pd.DataFrame(grade_counts)
    st.write(grade_table)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    
    # Calculate metrics
    total_students = len(students_df)
    
    # Excellent students (A and above in overall grade)
    excellent_count = len(students_df[students_df['overall_grade'].isin(['A+', 'A', 'A-'])])
    excellent_percent = (excellent_count / total_students) * 100
    
    # Average students (B range in overall grade)
    average_count = len(students_df[students_df['overall_grade'].isin(['B+', 'B', 'B-'])])
    average_percent = (average_count / total_students) * 100
    
    # Below average students (C range and below in overall grade)
    below_average_count = len(students_df[students_df['overall_grade'].isin(['C+', 'C', 'C-', 'D+', 'D', 'F'])])
    below_average_percent = (below_average_count / total_students) * 100
    
    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Excellent (A range)", f"{excellent_count} ({excellent_percent:.1f}%)")
    
    with col2:
        st.metric("Average (B range)", f"{average_count} ({average_percent:.1f}%)")
    
    with col3:
        st.metric("Below Average (C and below)", f"{below_average_count} ({below_average_percent:.1f}%)")
    
    # Top and bottom performers
    st.subheader("Top and Bottom Performers")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Top 5 Students")
        top_5 = students_df.sort_values('overall_score', ascending=False).head(5)
        st.dataframe(top_5[['name', 'overall_score', 'overall_grade']])
    
    with col2:
        st.write("#### Bottom 5 Students")
        bottom_5 = students_df.sort_values('overall_score').head(5)
        st.dataframe(bottom_5[['name', 'overall_score', 'overall_grade']])