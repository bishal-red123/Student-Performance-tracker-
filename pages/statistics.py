"""
Statistics page for the Student Grading System.
This page provides detailed statistical analysis of student performance data.
"""

import streamlit as st
import pandas as pd
import numpy as np
from utils.visualizations import Visualizer

def show():
    """
    Display the statistics page with data analysis and insights.
    """
    st.title("Statistics & Analysis")
    
    if "students" not in st.session_state or not st.session_state.students:
        st.warning("No data available. Please upload student data from the Home page.")
        return
    
    # Get processed dataframe
    processor = st.session_state.processor
    students_df = processor.students_to_dataframe(st.session_state.students)
    
    # Create tabs for different statistical analyses
    tab1, tab2, tab3, tab4 = st.tabs([
        "Descriptive Statistics", 
        "Correlation Analysis", 
        "Performance Gaps",
        "Grade Analysis"
    ])
    
    # Tab 1: Descriptive Statistics
    with tab1:
        st.header("Descriptive Statistics")
        st.write("This section provides basic statistical measures for all performance metrics.")
        
        # Calculate descriptive statistics
        numeric_cols = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        desc_stats = students_df[numeric_cols].describe().round(2)
        
        # Rename columns for better readability
        desc_stats.columns = ['Academic', 'Co-curricular', 'Discipline', 'Overall']
        
        # Display statistics table
        st.dataframe(desc_stats)
        
        # Additional statistics not included in describe()
        additional_stats = pd.DataFrame({
            'Metric': ['Variance', 'Skewness', 'Kurtosis', 'Range'],
            'Academic': [
                students_df['academic_score'].var().round(2),
                students_df['academic_score'].skew().round(2),
                students_df['academic_score'].kurt().round(2),
                (students_df['academic_score'].max() - students_df['academic_score'].min()).round(2)
            ],
            'Co-curricular': [
                students_df['cocurricular_score'].var().round(2),
                students_df['cocurricular_score'].skew().round(2),
                students_df['cocurricular_score'].kurt().round(2),
                (students_df['cocurricular_score'].max() - students_df['cocurricular_score'].min()).round(2)
            ],
            'Discipline': [
                students_df['discipline_score'].var().round(2),
                students_df['discipline_score'].skew().round(2),
                students_df['discipline_score'].kurt().round(2),
                (students_df['discipline_score'].max() - students_df['discipline_score'].min()).round(2)
            ],
            'Overall': [
                students_df['overall_score'].var().round(2),
                students_df['overall_score'].skew().round(2),
                students_df['overall_score'].kurt().round(2),
                (students_df['overall_score'].max() - students_df['overall_score'].min()).round(2)
            ]
        })
        
        st.write("### Additional Statistics")
        st.dataframe(additional_stats.set_index('Metric'))
        
        # Histograms
        st.write("### Distribution Visualization")
        metric = st.selectbox(
            "Select performance metric",
            ["academic_score", "cocurricular_score", "discipline_score", "overall_score"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="desc_stats_metric"
        )
        
        bins = st.slider("Number of bins", min_value=5, max_value=50, value=20, key="desc_stats_bins")
        
        fig = Visualizer.plot_score_histogram(students_df, metric, bins=bins)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary insights
        st.write("### Key Insights")
        
        # Calculate insights
        highest_mean = desc_stats.loc['mean'].idxmax()
        lowest_mean = desc_stats.loc['mean'].idxmin()
        highest_std = desc_stats.loc['std'].idxmax()
        
        most_skewed = additional_stats.set_index('Metric').loc['Skewness'].abs().idxmax()
        skew_value = additional_stats.set_index('Metric').loc['Skewness'][most_skewed]
        skew_direction = "positively" if skew_value > 0 else "negatively"
        
        st.write(f"• Students perform best in **{highest_mean}** with an average score of {desc_stats.loc['mean', highest_mean]:.2f}.")
        st.write(f"• Students show lowest performance in **{lowest_mean}** with an average score of {desc_stats.loc['mean', lowest_mean]:.2f}.")
        st.write(f"• The greatest variation is seen in **{highest_std}** scores (std. dev. = {desc_stats.loc['std', highest_std]:.2f}).")
        st.write(f"• The **{most_skewed}** scores are {skew_direction} skewed ({skew_value:.2f}), indicating {"a longer tail on the upper end" if skew_value > 0 else "a longer tail on the lower end"}.")
    
    # Tab 2: Correlation Analysis
    with tab2:
        st.header("Correlation Analysis")
        st.write("This section analyzes relationships between different performance metrics.")
        
        # Display correlation matrix
        fig = Visualizer.plot_correlation_matrix(students_df)
        st.plotly_chart(fig, use_container_width=True)
        
        # Scatter plot for relationship exploration
        st.write("### Explore Relationships")
        st.write("Select two metrics to visualize their relationship:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_metric = st.selectbox(
                "X-axis metric",
                ["academic_score", "cocurricular_score", "discipline_score"],
                format_func=lambda x: x.replace('_', ' ').title(),
                key="corr_x_metric"
            )
        
        with col2:
            y_metric = st.selectbox(
                "Y-axis metric",
                ["academic_score", "cocurricular_score", "discipline_score", "overall_score"],
                index=3,
                format_func=lambda x: x.replace('_', ' ').title(),
                key="corr_y_metric"
            )
        
        color_by = st.selectbox(
            "Color points by grade",
            [None, "academic_grade", "cocurricular_grade", "discipline_grade", "overall_grade"],
            format_func=lambda x: x.replace('_', ' ').title() if x else "No Color Coding",
            key="corr_color"
        )
        
        fig = Visualizer.plot_scatter_comparison(
            students_df, 
            x_metric, 
            y_metric,
            color_column=color_by
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate correlation coefficient
        corr = students_df[x_metric].corr(students_df[y_metric])
        
        # Interpretation of correlation
        st.write(f"**Correlation coefficient:** {corr:.4f}")
        
        if abs(corr) < 0.3:
            st.write("**Interpretation:** There is a weak correlation between these metrics.")
        elif abs(corr) < 0.7:
            st.write("**Interpretation:** There is a moderate correlation between these metrics.")
        else:
            st.write("**Interpretation:** There is a strong correlation between these metrics.")
        
        # Correlation insights
        st.write("### Key Insights")
        
        # Calculate all pairwise correlations
        corr_matrix = students_df[numeric_cols].corr()
        
        # Find the strongest correlation (excluding self-correlations)
        corr_matrix_no_self = corr_matrix.copy()
        np.fill_diagonal(corr_matrix_no_self.values, 0)
        max_corr_idx = corr_matrix_no_self.abs().stack().idxmax()
        max_corr = corr_matrix.loc[max_corr_idx]
        
        # Find the weakest correlation
        min_corr_idx = corr_matrix.abs().replace(0, 1).stack().idxmin()
        min_corr = corr_matrix.loc[min_corr_idx]
        
        # Format metric names for readability
        metric_names = {
            'academic_score': 'Academic',
            'cocurricular_score': 'Co-curricular',
            'discipline_score': 'Discipline',
            'overall_score': 'Overall'
        }
        
        max_corr_formatted = (metric_names[max_corr_idx[0]], metric_names[max_corr_idx[1]])
        min_corr_formatted = (metric_names[min_corr_idx[0]], metric_names[min_corr_idx[1]])
        
        st.write(f"• The strongest relationship is between **{max_corr_formatted[0]}** and **{max_corr_formatted[1]}** scores (r = {max_corr:.4f}).")
        st.write(f"• The weakest relationship is between **{min_corr_formatted[0]}** and **{min_corr_formatted[1]}** scores (r = {min_corr:.4f}).")
        
        # Calculate which metric has the strongest correlation with overall score
        overall_corrs = corr_matrix['overall_score'].drop('overall_score')
        strongest_predictor = overall_corrs.abs().idxmax()
        strongest_corr = overall_corrs[strongest_predictor]
        
        st.write(f"• **{metric_names[strongest_predictor]}** is the strongest predictor of overall performance (r = {strongest_corr:.4f}).")
        
        if strongest_corr > 0.8:
            st.write("• This suggests the grading system might be placing too much weight on this category.")
    
    # Tab 3: Performance Gaps
    with tab3:
        st.header("Performance Gaps")
        st.write("This section analyzes gaps in student performance across different metrics.")
        
        # Calculate performance gaps for each student
        students_df['academic_cocurricular_gap'] = (students_df['academic_score'] - students_df['cocurricular_score']).abs()
        students_df['academic_discipline_gap'] = (students_df['academic_score'] - students_df['discipline_score']).abs()
        students_df['cocurricular_discipline_gap'] = (students_df['cocurricular_score'] - students_df['discipline_score']).abs()
        
        # Calculate the maximum gap for each student
        students_df['max_gap'] = students_df[['academic_cocurricular_gap', 'academic_discipline_gap', 'cocurricular_discipline_gap']].max(axis=1)
        
        # Display distribution of maximum gaps
        st.write("### Distribution of Maximum Performance Gaps")
        fig = Visualizer.plot_score_histogram(students_df, 'max_gap', bins=15, title='Distribution of Maximum Performance Gaps')
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics about gaps
        avg_max_gap = students_df['max_gap'].mean()
        median_max_gap = students_df['max_gap'].median()
        max_max_gap = students_df['max_gap'].max()
        
        st.write(f"• Average maximum gap: {avg_max_gap:.2f} points")
        st.write(f"• Median maximum gap: {median_max_gap:.2f} points")
        st.write(f"• Largest maximum gap: {max_max_gap:.2f} points")
        
        # Identify students with the largest gaps
        st.write("### Students with Largest Performance Gaps")
        
        # Get top 5 students with largest gaps
        top_gap_students = students_df.sort_values('max_gap', ascending=False).head(5)
        
        # Create dataframe for display
        gap_display = pd.DataFrame({
            'Student Name': top_gap_students['name'],
            'Academic Score': top_gap_students['academic_score'].round(2),
            'Co-curricular Score': top_gap_students['cocurricular_score'].round(2),
            'Discipline Score': top_gap_students['discipline_score'].round(2),
            'Maximum Gap': top_gap_students['max_gap'].round(2)
        })
        
        st.dataframe(gap_display)
        
        # Identify students with the most balanced performance
        st.write("### Students with Most Balanced Performance")
        
        # Get top 5 students with smallest gaps
        balanced_students = students_df.sort_values('max_gap').head(5)
        
        # Create dataframe for display
        balanced_display = pd.DataFrame({
            'Student Name': balanced_students['name'],
            'Academic Score': balanced_students['academic_score'].round(2),
            'Co-curricular Score': balanced_students['cocurricular_score'].round(2),
            'Discipline Score': balanced_students['discipline_score'].round(2),
            'Maximum Gap': balanced_students['max_gap'].round(2)
        })
        
        st.dataframe(balanced_display)
        
        # Gap analysis
        st.write("### Gap Analysis")
        
        # Calculate the most common type of gap
        gap_types = {
            'Academic-Cocurricular': (students_df['academic_cocurricular_gap'] == students_df['max_gap']).sum(),
            'Academic-Discipline': (students_df['academic_discipline_gap'] == students_df['max_gap']).sum(),
            'Cocurricular-Discipline': (students_df['cocurricular_discipline_gap'] == students_df['max_gap']).sum()
        }
        
        most_common_gap = max(gap_types.items(), key=lambda x: x[1])[0]
        most_common_count = gap_types[most_common_gap]
        most_common_percent = (most_common_count / len(students_df)) * 100
        
        st.write(f"• The most common maximum gap is between **{most_common_gap.replace('-', ' and ')}** ({most_common_percent:.1f}% of students).")
        
        # Calculate percentage of students with significant gaps (>20 points)
        significant_gap_count = (students_df['max_gap'] > 20).sum()
        significant_gap_percent = (significant_gap_count / len(students_df)) * 100
        
        st.write(f"• {significant_gap_percent:.1f}% of students have significant performance gaps (>20 points difference).")
    
    # Tab 4: Grade Analysis
    with tab4:
        st.header("Grade Analysis")
        st.write("This section analyzes the distribution and relationships between grades.")
        
        # Grade distribution for each category
        st.write("### Grade Distribution by Category")
        
        # Create a dataframe with grade counts for each category
        grade_counts = {}
        
        for col, name in zip(['academic_grade', 'cocurricular_grade', 'discipline_grade', 'overall_grade'],
                           ['Academic', 'Co-curricular', 'Discipline', 'Overall']):
            grade_counts[name] = students_df[col].value_counts().sort_index()
        
        grade_distribution = pd.DataFrame(grade_counts)
        
        # Fill missing grades with 0
        all_grades = sorted(set().union(*[grade_counts[cat].index for cat in grade_counts]))
        for grade in all_grades:
            for category in grade_counts:
                if grade not in grade_counts[category]:
                    grade_counts[category][grade] = 0
        
        # Recreate dataframe with all grades for all categories
        grade_distribution = pd.DataFrame({cat: grade_counts[cat].sort_index() for cat in grade_counts})
        
        # Display the distribution
        st.dataframe(grade_distribution)
        
        # Visualize grade distribution
        st.write("### Grade Distribution Visualization")
        
        grade_category = st.selectbox(
            "Select grade category",
            ["academic_grade", "cocurricular_grade", "discipline_grade", "overall_grade"],
            format_func=lambda x: x.replace('_', ' ').title(),
            key="grade_dist_category"
        )
        
        fig = Visualizer.plot_grade_distribution(students_df, grade_category)
        st.plotly_chart(fig, use_container_width=True)
        
        # Grade correlations
        st.write("### Grade Consistency Analysis")
        
        # Calculate number of students with consistent grades across all categories
        students_df['consistent_grades'] = (
            (students_df['academic_grade'] == students_df['cocurricular_grade']) & 
            (students_df['academic_grade'] == students_df['discipline_grade'])
        )
        
        consistent_count = students_df['consistent_grades'].sum()
        consistent_percent = (consistent_count / len(students_df)) * 100
        
        st.write(f"• {consistent_count} students ({consistent_percent:.1f}%) have consistent grades across all three categories.")
        
        # Calculate number of students with same overall grade as their predominant category grade
        students_df['matches_overall'] = (
            (students_df['academic_grade'] == students_df['overall_grade']) | 
            (students_df['cocurricular_grade'] == students_df['overall_grade']) | 
            (students_df['discipline_grade'] == students_df['overall_grade'])
        )
        
        matches_count = students_df['matches_overall'].sum()
        matches_percent = (matches_count / len(students_df)) * 100
        
        st.write(f"• {matches_count} students ({matches_percent:.1f}%) have an overall grade that matches at least one of their category grades.")
        
        # Calculate which category most commonly matches overall grade
        academic_matches = (students_df['academic_grade'] == students_df['overall_grade']).sum()
        cocurricular_matches = (students_df['cocurricular_grade'] == students_df['overall_grade']).sum()
        discipline_matches = (students_df['discipline_grade'] == students_df['overall_grade']).sum()
        
        matches = {
            'Academic': academic_matches,
            'Co-curricular': cocurricular_matches,
            'Discipline': discipline_matches
        }
        
        most_matched = max(matches.items(), key=lambda x: x[1])[0]
        most_matched_count = matches[most_matched]
        most_matched_percent = (most_matched_count / len(students_df)) * 100
        
        st.write(f"• The **{most_matched}** grade most frequently matches the overall grade ({most_matched_percent:.1f}% of students).")
        
        # Check for grade inflation/deflation
        st.write("### Grade Inflation/Deflation Analysis")
        
        # Calculate average numerical scores for each letter grade
        grade_score_mapping = {}
        
        for grade in all_grades:
            grade_mask = students_df['overall_grade'] == grade
            if grade_mask.any():
                avg_score = students_df.loc[grade_mask, 'overall_score'].mean()
                grade_score_mapping[grade] = avg_score
        
        # Create dataframe for display
        grade_scores = pd.DataFrame({
            'Grade': list(grade_score_mapping.keys()),
            'Average Score': [round(score, 2) for score in grade_score_mapping.values()]
        }).sort_values('Grade')
        
        st.dataframe(grade_scores)
        
        # Calculate grade boundaries from the data
        st.write("### Inferred Grade Boundaries")
        
        # Sort grades by average score
        sorted_grades = sorted(grade_score_mapping.items(), key=lambda x: x[1])
        
        # Calculate boundaries between consecutive grades
        boundaries = []
        for i in range(len(sorted_grades) - 1):
            current_grade, current_score = sorted_grades[i]
            next_grade, next_score = sorted_grades[i + 1]
            boundary = (current_score + next_score) / 2
            boundaries.append({
                'Lower Grade': current_grade,
                'Upper Grade': next_grade,
                'Approximate Boundary': round(boundary, 2)
            })
        
        if boundaries:
            st.dataframe(pd.DataFrame(boundaries))
        else:
            st.write("Insufficient data to infer grade boundaries.")