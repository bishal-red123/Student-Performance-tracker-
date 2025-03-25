import streamlit as st
import pandas as pd
import plotly.express as px
from utils.visualizations import Visualizer

def show():
    """
    Display the dashboard page with overview visualizations.
    """
    if "dataframe" not in st.session_state or st.session_state.dataframe is None:
        st.warning("Please upload data on the Home page first.")
        return
    
    st.title("Student Performance Dashboard")
    
    # Create tabs for different dashboard sections
    tab1, tab2, tab3 = st.tabs(["Overview", "Grade Analysis", "Performance Comparison"])
    
    # Prepare data
    df = st.session_state.processor.students_to_dataframe(st.session_state.students)
    
    # Overview Tab
    with tab1:
        st.header("Performance Overview")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", len(df))
        with col2:
            st.metric("Average Academic", f"{df['academic_score'].mean():.1f}")
        with col3:
            st.metric("Average Co-curricular", f"{df['cocurricular_score'].mean():.1f}")
        with col4:
            st.metric("Average Discipline", f"{df['discipline_score'].mean():.1f}")
        
        # Score distribution
        st.subheader("Score Distribution")
        score_cols = ['academic_score', 'cocurricular_score', 'discipline_score']
        selected_score = st.selectbox("Select Score Category", score_cols, format_func=lambda x: x.replace('_score', '').title())
        
        fig = Visualizer.plot_score_histogram(df, selected_score)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Correlation Between Performance Metrics")
        corr_fig = Visualizer.plot_correlation_matrix(df)
        st.plotly_chart(corr_fig, use_container_width=True)
    
    # Grade Analysis Tab
    with tab2:
        st.header("Grade Analysis")
        
        # Grade distribution
        st.subheader("Grade Distribution")
        grade_cols = ['academic_grade', 'cocurricular_grade', 'discipline_grade', 'overall_grade']
        selected_grade = st.selectbox("Select Grade Category", grade_cols, format_func=lambda x: x.replace('_grade', '').title())
        
        grade_fig = Visualizer.plot_grade_distribution(df, selected_grade)
        st.plotly_chart(grade_fig, use_container_width=True)
        
        # Top and bottom performers
        st.subheader("Top and Bottom Performers")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 5 Overall Performers**")
            top_df = df.sort_values('overall_score', ascending=False).head(5)
            st.dataframe(top_df[['name', 'overall_score', 'overall_grade']], use_container_width=True)
        
        with col2:
            st.markdown("**Students Needing Improvement**")
            bottom_df = df[df['overall_grade'].isin(['D', 'F'])].sort_values('overall_score')
            st.dataframe(bottom_df[['name', 'overall_score', 'overall_grade']], use_container_width=True)
        
        # Grade breakdown
        st.subheader("Detailed Grade Breakdown")
        
        grade_breakdown = df['overall_grade'].value_counts().reset_index()
        grade_breakdown.columns = ['Grade', 'Count']
        
        # Calculate percentages
        grade_breakdown['Percentage'] = (grade_breakdown['Count'] / grade_breakdown['Count'].sum() * 100).round(1)
        grade_breakdown['Percentage'] = grade_breakdown['Percentage'].astype(str) + '%'
        
        st.dataframe(grade_breakdown, use_container_width=True)
    
    # Performance Comparison Tab
    with tab3:
        st.header("Performance Comparison")
        
        # Box plot comparing performance categories
        st.subheader("Score Comparison Across Categories")
        box_fig = Visualizer.plot_score_comparison(df)
        st.plotly_chart(box_fig, use_container_width=True)
        
        # Scatter plot to compare two metrics
        st.subheader("Relationship Between Different Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_metric = st.selectbox("X-Axis", score_cols, format_func=lambda x: x.replace('_score', '').title())
        
        with col2:
            y_metric = st.selectbox("Y-Axis", score_cols, format_func=lambda x: x.replace('_score', '').title(), index=1)
        
        with col3:
            color_by = st.selectbox("Color By", ['overall_grade', 'None'], format_func=lambda x: x.replace('_grade', '').title() if x != 'None' else x)
        
        scatter_fig = Visualizer.plot_scatter_comparison(
            df, 
            x_metric, 
            y_metric, 
            color_column=None if color_by == 'None' else color_by
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
        
        # Radar chart for comparative analysis
        st.subheader("Compare Selected Students")
        
        # Let user select students to compare
        selected_students = st.multiselect(
            "Select students to compare (max 5):",
            options=df['name'].tolist(),
            max_selections=5
        )
        
        if selected_students:
            # Get the selected student objects
            selected_student_objects = [
                student for student in st.session_state.students 
                if student.name in selected_students
            ]
            
            radar_fig = Visualizer.plot_comparative_radar(selected_student_objects)
            st.plotly_chart(radar_fig, use_container_width=True)
        else:
            st.info("Select at least one student to see the comparison.")
