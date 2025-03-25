import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

class Visualizer:
    """
    A class for creating various visualizations of student data.
    """
    
    @staticmethod
    def plot_grade_distribution(df, column, title=None):
        """
        Create a bar chart of grade distribution.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        column : str
            Column name containing grade data
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        grade_counts = df[column].value_counts().reset_index()
        grade_counts.columns = ['Grade', 'Count']
        
        # Get the grades in proper order
        grade_order = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        grade_counts['Grade'] = pd.Categorical(grade_counts['Grade'], categories=grade_order, ordered=True)
        grade_counts = grade_counts.sort_values('Grade')
        
        fig = px.bar(
            grade_counts, 
            x='Grade', 
            y='Count',
            color='Grade',
            title=title or f"Distribution of {column.replace('_', ' ').title()}",
            labels={'Count': 'Number of Students', 'Grade': 'Grade'}
        )
        
        return fig
    
    @staticmethod
    def plot_score_histogram(df, column, bins=10, title=None):
        """
        Create a histogram of score distribution.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        column : str
            Column name containing score data
        bins : int, optional
            Number of bins for histogram
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        fig = px.histogram(
            df, 
            x=column,
            nbins=bins,
            title=title or f"Distribution of {column.replace('_', ' ').title()}",
            labels={column: column.replace('_', ' ').title(), 'count': 'Number of Students'}
        )
        
        return fig
    
    @staticmethod
    def plot_score_comparison(df, title=None):
        """
        Create a box plot comparing different score categories.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        # Melt the dataframe to get it in the right format for the box plot
        score_cols = ['academic_score', 'cocurricular_score', 'discipline_score']
        melted_df = pd.melt(df, id_vars=['name'], value_vars=score_cols, 
                           var_name='Category', value_name='Score')
        
        # Make the category names more readable
        melted_df['Category'] = melted_df['Category'].apply(
            lambda x: x.replace('_score', '').title()
        )
        
        fig = px.box(
            melted_df,
            x='Category',
            y='Score',
            color='Category',
            title=title or "Comparison of Performance Categories",
            labels={'Score': 'Score (0-100)', 'Category': 'Performance Category'}
        )
        
        return fig
    
    @staticmethod
    def plot_student_radar(student, title=None):
        """
        Create a radar chart for an individual student.
        
        Parameters:
        -----------
        student : models.Student
            Student object
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        categories = ['Academic', 'Co-curricular', 'Discipline']
        scores = [student.academic_score, student.cocurricular_score, student.discipline_score]
        
        # Create radar chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=scores,
            theta=categories,
            fill='toself',
            name=student.name
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=title or f"Performance Profile: {student.name}"
        )
        
        return fig
    
    @staticmethod
    def plot_comparative_radar(students, title=None):
        """
        Create a comparative radar chart for multiple students.
        
        Parameters:
        -----------
        students : list
            List of Student objects
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        categories = ['Academic', 'Co-curricular', 'Discipline']
        
        # Create radar chart
        fig = go.Figure()
        
        for student in students:
            scores = [student.academic_score, student.cocurricular_score, student.discipline_score]
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name=student.name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=title or f"Comparative Performance Profile ({len(students)} students)"
        )
        
        return fig
    
    @staticmethod
    def plot_correlation_matrix(df, title=None):
        """
        Create a correlation matrix heatmap.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        score_cols = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        corr_matrix = df[score_cols].corr()
        
        # Create labels for the heatmap
        labels = [col.replace('_score', '').title() for col in score_cols]
        
        fig = px.imshow(
            corr_matrix,
            x=labels,
            y=labels,
            color_continuous_scale='RdBu_r',
            title=title or "Correlation Between Performance Metrics",
            labels={'color': 'Correlation'}
        )
        
        return fig
    
    @staticmethod
    def plot_performance_over_time(df, time_column, metric_column, title=None):
        """
        Create a line chart for performance over time.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        time_column : str
            Column name containing time data
        metric_column : str
            Column name containing performance metric
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        # Group by time and calculate average
        time_df = df.groupby(time_column)[metric_column].mean().reset_index()
        
        fig = px.line(
            time_df,
            x=time_column,
            y=metric_column,
            markers=True,
            title=title or f"{metric_column.replace('_', ' ').title()} Over {time_column.title()}",
            labels={
                time_column: time_column.replace('_', ' ').title(),
                metric_column: metric_column.replace('_', ' ').title()
            }
        )
        
        return fig
    
    @staticmethod
    def plot_scatter_comparison(df, x_column, y_column, color_column=None, title=None):
        """
        Create a scatter plot comparing two metrics.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
        x_column : str
            Column name for x-axis
        y_column : str
            Column name for y-axis
        color_column : str, optional
            Column name for color coding
        title : str, optional
            Chart title
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Plotly figure object
        """
        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            color=color_column,
            hover_name='name',
            title=title or f"{y_column.replace('_', ' ').title()} vs {x_column.replace('_', ' ').title()}",
            labels={
                x_column: x_column.replace('_', ' ').title(),
                y_column: y_column.replace('_', ' ').title(),
                color_column: color_column.replace('_', ' ').title() if color_column else None
            }
        )
        
        return fig
