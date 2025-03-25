import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.visualizations import Visualizer

def show():
    """
    Display the statistics page with data analysis and insights.
    """
    if "dataframe" not in st.session_state or st.session_state.dataframe is None:
        st.warning("Please upload data on the Home page first.")
        return
    
    st.title("Statistical Analysis")
    
    # Prepare data
    df = st.session_state.processor.students_to_dataframe(st.session_state.students)
    
    # Create tabs for different statistical analyses
    tab1, tab2, tab3 = st.tabs(["Descriptive Stats", "Distribution Analysis", "Advanced Insights"])
    
    # Descriptive Stats Tab
    with tab1:
        st.header("Descriptive Statistics")
        
        # Add a description
        st.markdown("""
        This section provides a statistical summary of student performance across different categories.
        """)
        
        # Summary statistics
        st.subheader("Summary Statistics")
        
        score_columns = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        stats_df = df[score_columns].describe().T
        
        # Rename index for better readability
        stats_df.index = [col.replace('_score', '').title() for col in stats_df.index]
        
        # Format the statistics table
        formatted_stats = stats_df.copy()
        for col in formatted_stats.columns:
            if col != 'count':
                formatted_stats[col] = formatted_stats[col].round(2)
        
        st.dataframe(formatted_stats, use_container_width=True)
        
        # Additional statistics
        st.subheader("Additional Statistics")
        
        # Median, Mode, Range, IQR
        additional_stats = pd.DataFrame(index=stats_df.index)
        
        additional_stats['Median'] = [df[col].median() for col in score_columns]
        additional_stats['Mode'] = [df[col].mode()[0] for col in score_columns]
        additional_stats['Range'] = [df[col].max() - df[col].min() for col in score_columns]
        additional_stats['IQR'] = [df[col].quantile(0.75) - df[col].quantile(0.25) for col in score_columns]
        additional_stats['Skewness'] = [df[col].skew() for col in score_columns]
        additional_stats['Kurtosis'] = [df[col].kurt() for col in score_columns]
        
        # Format the additional statistics table
        formatted_additional = additional_stats.copy().round(2)
        
        st.dataframe(formatted_additional, use_container_width=True)
        
        # Show skewness and kurtosis interpretation
        st.markdown("""
        **Interpretation Guide:**
        
        **Skewness**:
        - Values close to 0 indicate symmetric distribution
        - Positive values indicate right-skewed distribution (tail extends to the right)
        - Negative values indicate left-skewed distribution (tail extends to the left)
        
        **Kurtosis**:
        - Values close to 0 indicate normal distribution
        - Positive values indicate heavier tails than normal distribution
        - Negative values indicate lighter tails than normal distribution
        """)
        
        # Correlation matrix
        st.subheader("Correlation Matrix")
        
        corr_matrix = df[score_columns].corr().round(3)
        
        # Rename index and columns for better readability
        readable_names = [col.replace('_score', '').title() for col in corr_matrix.index]
        corr_matrix.index = readable_names
        corr_matrix.columns = readable_names
        
        st.dataframe(corr_matrix, use_container_width=True)
        
        # Visualization of correlation matrix
        fig = Visualizer.plot_correlation_matrix(df)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Correlation Interpretation**:
        - Values close to 1 indicate strong positive correlation
        - Values close to -1 indicate strong negative correlation
        - Values close to 0 indicate little to no correlation
        """)
    
    # Distribution Analysis Tab
    with tab2:
        st.header("Distribution Analysis")
        
        # Score distributions
        st.subheader("Score Distributions")
        
        # Select which distribution to view
        selected_score = st.selectbox(
            "Select Score Category", 
            score_columns, 
            format_func=lambda x: x.replace('_score', '').title()
        )
        
        # Create histogram
        hist_fig = Visualizer.plot_score_histogram(df, selected_score, bins=20)
        st.plotly_chart(hist_fig, use_container_width=True)
        
        # Box plots for score distributions
        st.subheader("Box Plot Analysis")
        
        box_fig = Visualizer.plot_score_comparison(df)
        st.plotly_chart(box_fig, use_container_width=True)
        
        st.markdown("""
        **Box Plot Interpretation**:
        - The box represents the interquartile range (IQR) from the 25th to 75th percentile
        - The line inside the box is the median (50th percentile)
        - Whiskers typically extend to 1.5 times the IQR
        - Points beyond the whiskers are potential outliers
        """)
        
        # Grade distributions
        st.subheader("Grade Distributions")
        
        # Select which grade distribution to view
        grade_columns = ['academic_grade', 'cocurricular_grade', 'discipline_grade', 'overall_grade']
        selected_grade = st.selectbox(
            "Select Grade Category", 
            grade_columns, 
            format_func=lambda x: x.replace('_grade', '').title()
        )
        
        # Create bar chart
        grade_fig = Visualizer.plot_grade_distribution(df, selected_grade)
        st.plotly_chart(grade_fig, use_container_width=True)
    
    # Advanced Insights Tab
    with tab3:
        st.header("Advanced Insights")
        
        # Strengths and weaknesses analysis
        st.subheader("Strengths and Weaknesses Analysis")
        
        # Calculate strengths and weaknesses
        df['academic_diff'] = df['academic_score'] - df[['academic_score', 'cocurricular_score', 'discipline_score']].mean(axis=1)
        df['cocurricular_diff'] = df['cocurricular_score'] - df[['academic_score', 'cocurricular_score', 'discipline_score']].mean(axis=1)
        df['discipline_diff'] = df['discipline_score'] - df[['academic_score', 'cocurricular_score', 'discipline_score']].mean(axis=1)
        
        # Determine strength and weakness for each student
        df['strength'] = df[['academic_diff', 'cocurricular_diff', 'discipline_diff']].idxmax(axis=1)
        df['weakness'] = df[['academic_diff', 'cocurricular_diff', 'discipline_diff']].idxmin(axis=1)
        
        # Clean up the strength and weakness labels
        df['strength'] = df['strength'].str.replace('_diff', '')
        df['weakness'] = df['weakness'].str.replace('_diff', '')
        
        # Count strengths and weaknesses
        strength_counts = df['strength'].value_counts().reset_index()
        strength_counts.columns = ['Category', 'Count']
        strength_counts['Category'] = strength_counts['Category'].apply(lambda x: x.title())
        
        weakness_counts = df['weakness'].value_counts().reset_index()
        weakness_counts.columns = ['Category', 'Count']
        weakness_counts['Category'] = weakness_counts['Category'].apply(lambda x: x.title())
        
        # Display strengths and weaknesses
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Student Strengths Distribution**")
            strength_fig = px.pie(
                strength_counts, 
                values='Count', 
                names='Category', 
                title="Distribution of Student Strengths",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(strength_fig, use_container_width=True)
        
        with col2:
            st.markdown("**Student Weaknesses Distribution**")
            weakness_fig = px.pie(
                weakness_counts, 
                values='Count', 
                names='Category', 
                title="Distribution of Student Weaknesses",
                color_discrete_sequence=px.colors.sequential.Reds
            )
            st.plotly_chart(weakness_fig, use_container_width=True)
        
        # Balance analysis
        st.subheader("Performance Balance Analysis")
        
        # Calculate standard deviation of scores for each student
        df['score_std'] = df[['academic_score', 'cocurricular_score', 'discipline_score']].std(axis=1)
        
        # Create histogram of standard deviations
        balance_fig = px.histogram(
            df, 
            x='score_std',
            nbins=20,
            title="Distribution of Performance Balance",
            labels={'score_std': 'Standard Deviation of Scores', 'count': 'Number of Students'}
        )
        st.plotly_chart(balance_fig, use_container_width=True)
        
        st.markdown("""
        **Balance Interpretation**:
        - Lower standard deviation indicates more balanced performance across categories
        - Higher standard deviation indicates more variability between categories
        """)
        
        # Top 5 most balanced and unbalanced students
        st.subheader("Most Balanced vs. Most Unbalanced Students")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Most Balanced Students**")
            balanced_df = df.sort_values('score_std').head(5)
            st.dataframe(balanced_df[['name', 'academic_score', 'cocurricular_score', 
                                     'discipline_score', 'score_std']], use_container_width=True)
        
        with col2:
            st.markdown("**Most Unbalanced Students**")
            unbalanced_df = df.sort_values('score_std', ascending=False).head(5)
            st.dataframe(unbalanced_df[['name', 'academic_score', 'cocurricular_score', 
                                      'discipline_score', 'score_std']], use_container_width=True)
        
        # Correlation insights
        st.subheader("Relationship Insights")
        
        # Scatter plot with regression line
        x_metric = st.selectbox("X-Axis", score_columns, format_func=lambda x: x.replace('_score', '').title(), index=0)
        y_metric = st.selectbox("Y-Axis", score_columns, format_func=lambda x: x.replace('_score', '').title(), index=3)
        
        scatter_fig = px.scatter(
            df,
            x=x_metric,
            y=y_metric,
            trendline="ols",
            trendline_color_override="red",
            hover_name='name',
            title=f"{y_metric.replace('_score', '').title()} vs {x_metric.replace('_score', '').title()} with Trend Line",
            labels={
                x_metric: x_metric.replace('_score', '').title(),
                y_metric: y_metric.replace('_score', '').title()
            }
        )
        st.plotly_chart(scatter_fig, use_container_width=True)
        
        # Calculate and display correlation value
        correlation = df[x_metric].corr(df[y_metric])
        st.markdown(f"**Correlation coefficient**: {correlation:.3f}")
        
        # Provide interpretation of correlation
        if abs(correlation) < 0.3:
            st.markdown("**Interpretation**: Weak correlation - these performance areas show little relationship.")
        elif abs(correlation) < 0.7:
            st.markdown("**Interpretation**: Moderate correlation - these performance areas show some relationship.")
        else:
            st.markdown("**Interpretation**: Strong correlation - these performance areas show a significant relationship.")
        
        # Suggestions based on analysis
        st.subheader("Improvement Suggestions")
        
        # Generate suggestions based on data patterns
        suggestions = []
        
        # Academic vs Co-curricular correlation
        ac_cc_corr = df['academic_score'].corr(df['cocurricular_score'])
        if ac_cc_corr > 0.5:
            suggestions.append("Consider integrating academic concepts with co-curricular activities as they show positive correlation.")
        elif ac_cc_corr < -0.3:
            suggestions.append("Students might be focusing too much on either academics or co-curricular activities at the expense of the other.")
        
        # Balance analysis
        avg_std = df['score_std'].mean()
        if avg_std > 15:
            suggestions.append("Many students show significant imbalance across performance areas. Consider implementing a more holistic development approach.")
        
        # Weaknesses pattern
        if 'academic' in df['weakness'].values.tolist() and df['weakness'].value_counts().get('academic', 0) > len(df) * 0.4:
            suggestions.append("A significant portion of students show weakness in academics. Consider reviewing teaching methodologies and providing additional support.")
        
        if 'cocurricular' in df['weakness'].values.tolist() and df['weakness'].value_counts().get('cocurricular', 0) > len(df) * 0.4:
            suggestions.append("Many students are underperforming in co-curricular activities. Consider expanding options or making these activities more engaging.")
        
        if 'discipline' in df['weakness'].values.tolist() and df['weakness'].value_counts().get('discipline', 0) > len(df) * 0.4:
            suggestions.append("Discipline appears to be a common weakness. Consider implementing clearer behavior guidelines and positive reinforcement strategies.")
        
        # Display suggestions
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                st.markdown(f"{i}. {suggestion}")
        else:
            st.markdown("No specific improvement suggestions based on current data patterns.")
