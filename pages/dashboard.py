"""
Dashboard page for the Student Grading System.
This page displays overview visualizations of all student data.
"""

import streamlit as st
from utils.visualizations import Visualizer
import numpy as np

def show():
    """
    Display the dashboard page with overview visualizations.
    """
    st.title("Dashboard")
    
    # Check if data is loaded
    if st.session_state.dataframe is None:
        st.info("Please upload a file with student data to view the dashboard.")
        return
    
    # Get the data from session state
    df = st.session_state.dataframe
    students = st.session_state.students
    
    # Basic metrics
    st.header("Key Metrics")
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Display metrics
    col1.metric("Total Students", f"{len(students)}")
    col2.metric("Average Academic Score", f"{df['academic_score'].mean():.2f}")
    col3.metric("Average Co-curricular Score", f"{df['cocurricular_score'].mean():.2f}")
    col4.metric("Average Discipline Score", f"{df['discipline_score'].mean():.2f}")
    
    # Performance Overview
    st.header("Performance Overview")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["Score Distribution", "Score Comparison", "Grade Distribution"])
    
    # Tab 1: Score Distribution
    with tab1:
        # Distribution of scores for different metrics
        metric_option = st.selectbox(
            "Select metric to visualize",
            ["academic_score", "cocurricular_score", "discipline_score", "overall_score"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="dist_metric"
        )
        
        # Display histogram
        fig = Visualizer.plot_score_histogram(df, metric_option, bins=20)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display basic statistics
        st.write("### Summary Statistics")
        
        # Calculate and display statistics
        mean = df[metric_option].mean()
        median = df[metric_option].median()
        std_dev = df[metric_option].std()
        min_val = df[metric_option].min()
        max_val = df[metric_option].max()
        
        stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
        stat_col1.metric("Mean", f"{mean:.2f}")
        stat_col2.metric("Median", f"{median:.2f}")
        stat_col3.metric("Std Dev", f"{std_dev:.2f}")
        stat_col4.metric("Min", f"{min_val:.2f}")
        stat_col5.metric("Max", f"{max_val:.2f}")
    
    # Tab 2: Score Comparison
    with tab2:
        # Box plot comparing different score categories
        fig = Visualizer.plot_score_comparison(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        st.write("### Correlation Analysis")
        
        # Correlation matrix heatmap
        fig = Visualizer.plot_correlation_matrix(df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot for selected metrics
        st.write("### Score Relationship")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_metric = st.selectbox(
                "X-axis metric",
                ["academic_score", "cocurricular_score", "discipline_score"],
                format_func=lambda x: x.replace('_', ' ').title(),
                key="scatter_x_metric"
            )
        
        with col2:
            y_metric = st.selectbox(
                "Y-axis metric",
                ["academic_score", "cocurricular_score", "discipline_score", "overall_score"],
                index=3,
                format_func=lambda x: x.replace('_', ' ').title(),
                key="scatter_y_metric"
            )
        
        fig = Visualizer.plot_scatter_comparison(df, x_metric, y_metric)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Grade Distribution
    with tab3:
        # Convert students list to DataFrame for easier processing
        students_df = st.session_state.processor.students_to_dataframe(students)
        
        # Select grade category
        grade_category = st.selectbox(
            "Select grade category",
            ["academic_grade", "cocurricular_grade", "discipline_grade", "overall_grade"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="grade_category"
        )
        
        # Display bar chart
        fig = Visualizer.plot_grade_distribution(students_df, grade_category)
        st.plotly_chart(fig, use_container_width=True)
        
        # Grade distribution analysis
        st.write("### Grade Distribution Analysis")
        
        # Calculate grade counts and percentages
        grade_counts = students_df[grade_category].value_counts().sort_index()
        grade_percentages = (grade_counts / len(students_df) * 100).round(1)
        
        # Display grade distribution table
        import pandas as pd
        grade_table = pd.DataFrame({
            'Grade': grade_counts.index,
            'Count': grade_counts.values,
            'Percentage': grade_percentages.values
        })
        st.dataframe(grade_table)
        
        # Calculate percentage of students with passing grades (C or better)
        passing_grades = ['A', 'B', 'C']
        passing_count = students_df[students_df[grade_category].isin(passing_grades)].shape[0]
        passing_percentage = (passing_count / len(students_df) * 100).round(1)
        
        # Display passing percentage
        st.metric("Students with Passing Grades (C or better)", f"{passing_percentage}%")
    
    # Performance By Category
    st.header("Performance By Category")
    
    # Compare performance across different metrics
    st.write("This section allows you to explore how students perform across different categories.")
    
    # Create columns for category comparison metrics
    cat_col1, cat_col2, cat_col3 = st.columns(3)
    
    # Academic vs. Co-curricular
    academic_mean = df['academic_score'].mean()
    cocurricular_mean = df['cocurricular_score'].mean()
    ac_diff = cocurricular_mean - academic_mean
    ac_diff_icon = "↑" if ac_diff > 0 else "↓"
    
    cat_col1.metric(
        "Academic vs. Co-curricular",
        f"{academic_mean:.2f} / {cocurricular_mean:.2f}",
        f"{ac_diff_icon} {abs(ac_diff):.2f}"
    )
    
    # Academic vs. Discipline
    discipline_mean = df['discipline_score'].mean()
    ad_diff = discipline_mean - academic_mean
    ad_diff_icon = "↑" if ad_diff > 0 else "↓"
    
    cat_col2.metric(
        "Academic vs. Discipline",
        f"{academic_mean:.2f} / {discipline_mean:.2f}",
        f"{ad_diff_icon} {abs(ad_diff):.2f}"
    )
    
    # Co-curricular vs. Discipline
    cd_diff = discipline_mean - cocurricular_mean
    cd_diff_icon = "↑" if cd_diff > 0 else "↓"
    
    cat_col3.metric(
        "Co-curricular vs. Discipline",
        f"{cocurricular_mean:.2f} / {discipline_mean:.2f}",
        f"{cd_diff_icon} {abs(cd_diff):.2f}"
    )
    
    # Performance gap analysis
    st.write("### Performance Gap Analysis")
    st.write("This graph shows the distribution of performance gaps between different metrics.")
    
    # Calculate performance gaps
    df['academic_cocurricular_gap'] = abs(df['academic_score'] - df['cocurricular_score'])
    df['academic_discipline_gap'] = abs(df['academic_score'] - df['discipline_score'])
    df['cocurricular_discipline_gap'] = abs(df['cocurricular_score'] - df['discipline_score'])
    
    # Average gap
    avg_gap = (
        df['academic_cocurricular_gap'].mean() + 
        df['academic_discipline_gap'].mean() + 
        df['cocurricular_discipline_gap'].mean()
    ) / 3
    
    st.metric("Average Performance Gap", f"{avg_gap:.2f} points")
    
    # Gap visualization
    gap_option = st.selectbox(
        "Select gap to visualize",
        [
            "academic_cocurricular_gap", 
            "academic_discipline_gap", 
            "cocurricular_discipline_gap"
        ],
        format_func=lambda x: x.replace('_', ' ').title().replace('Gap', 'Gap'),
        key="gap_option"
    )
    
    # Display histogram of selected gap
    fig = Visualizer.plot_score_histogram(
        df, 
        gap_option, 
        bins=15,
        title=f"Distribution of {gap_option.replace('_', ' ').title()}"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Identify students with significant gaps
    significant_gap_threshold = 20  # 20 points threshold
    
    # Find students with significant gaps
    significant_gaps = df[df[gap_option] > significant_gap_threshold]
    
    if not significant_gaps.empty:
        st.write(f"### Students with Significant {gap_option.replace('_', ' ').title()}")
        st.write(f"{len(significant_gaps)} students have a gap > {significant_gap_threshold} points.")
        
        # Display top 5 students with largest gaps
        top_gap_students = significant_gaps.sort_values(gap_option, ascending=False).head(5)
        
        if 'cocurricular' in gap_option:
            cols = ['name', 'academic_score', 'cocurricular_score']
        elif 'discipline' in gap_option:
            if 'academic' in gap_option:
                cols = ['name', 'academic_score', 'discipline_score']
            else:
                cols = ['name', 'cocurricular_score', 'discipline_score']
        
        st.dataframe(top_gap_students[cols + [gap_option]])
    else:
        st.write(f"No students have a {gap_option.replace('_', ' ')} greater than {significant_gap_threshold} points.")
    
    # Performance Distribution
    st.header("Performance Distribution")
    
    # Get the top 10% and bottom 10% of students
    top_threshold = np.percentile(df['overall_score'], 90)
    bottom_threshold = np.percentile(df['overall_score'], 10)
    
    # Count students in each category
    top_count = (students_df['overall_score'] >= top_threshold).sum()
    bottom_count = (students_df['overall_score'] <= bottom_threshold).sum()
    middle_count = len(students_df) - top_count - bottom_count
    
    # Create a pie chart
    import plotly.express as px
    
    distribution_data = pd.DataFrame({
        'Category': ['Top 10%', 'Middle 80%', 'Bottom 10%'],
        'Count': [top_count, middle_count, bottom_count]
    })
    
    fig = px.pie(
        distribution_data,
        values='Count',
        names='Category',
        title='Student Performance Distribution',
        color='Category',
        color_discrete_map={
            'Top 10%': 'green',
            'Middle 80%': 'blue',
            'Bottom 10%': 'red'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)