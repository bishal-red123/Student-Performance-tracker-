"""
Visualizations module for the Student Grading System.
This module provides various visualization functions for analyzing student data.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

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
        # Get grade counts
        grade_counts = df[column].value_counts().sort_index().reset_index()
        grade_counts.columns = ['Grade', 'Count']
        
        # Create figure
        fig = px.bar(
            grade_counts, 
            x='Grade', 
            y='Count',
            color='Grade',
            title=title or f"Distribution of {column.replace('_', ' ').title()}"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Grade",
            yaxis_title="Number of Students",
            showlegend=False
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
        # Create histogram
        fig = px.histogram(
            df, 
            x=column, 
            nbins=bins,
            title=title or f"Distribution of {column.replace('_', ' ').title()}"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title="Number of Students"
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
        # Melt the dataframe to long format
        score_cols = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        melted_df = df[score_cols].melt(var_name='Category', value_name='Score')
        
        # Format category names
        melted_df['Category'] = melted_df['Category'].replace({
            'academic_score': 'Academic',
            'cocurricular_score': 'Co-curricular',
            'discipline_score': 'Discipline',
            'overall_score': 'Overall'
        })
        
        # Create figure
        fig = px.box(
            melted_df, 
            x='Category', 
            y='Score',
            color='Category',
            title=title or "Comparison of Score Categories"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="",
            yaxis_title="Score",
            showlegend=False
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
        # Define categories and values
        categories = ['Academic', 'Co-curricular', 'Discipline']
        values = [student.academic_score, student.cocurricular_score, student.discipline_score]
        
        # Add first point again to close the polygon
        categories = categories + [categories[0]]
        values = values + [values[0]]
        
        # Create figure
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=student.name
        ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
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
        # Define categories
        categories = ['Academic', 'Co-curricular', 'Discipline']
        
        # Create figure
        fig = go.Figure()
        
        # Add trace for each student
        for student in students:
            values = [student.academic_score, student.cocurricular_score, student.discipline_score]
            # Add first point again to close the polygon
            values_closed = values + [values[0]]
            categories_closed = categories + [categories[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill='toself',
                name=student.name
            ))
        
        # Update layout
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=title or "Comparative Performance Profiles"
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
        # Get numeric columns
        numeric_cols = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        
        # Calculate correlation matrix
        corr_matrix = df[numeric_cols].corr()
        
        # Create heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title=title or "Correlation Matrix"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            coloraxis_showscale=True
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
        grouped = df.groupby(time_column)[metric_column].agg(['mean', 'std', 'count']).reset_index()
        
        # Create figure
        fig = go.Figure()
        
        # Add mean line
        fig.add_trace(go.Scatter(
            x=grouped[time_column],
            y=grouped['mean'],
            mode='lines+markers',
            name='Mean Score',
            line=dict(color='royalblue', width=2)
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=np.concatenate([grouped[time_column], grouped[time_column][::-1]]),
            y=np.concatenate([
                grouped['mean'] + 1.96 * grouped['std'] / np.sqrt(grouped['count']),
                (grouped['mean'] - 1.96 * grouped['std'] / np.sqrt(grouped['count']))[::-1]
            ]),
            fill='toself',
            fillcolor='rgba(65, 105, 225, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'
        ))
        
        # Update layout
        fig.update_layout(
            title=title or f"{metric_column.replace('_', ' ').title()} Over Time",
            xaxis_title=time_column.replace('_', ' ').title(),
            yaxis_title=metric_column.replace('_', ' ').title(),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
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
        # Format axis titles
        x_title = x_column.replace('_', ' ').title()
        y_title = y_column.replace('_', ' ').title()
        
        # Create figure
        if color_column:
            fig = px.scatter(
                df, 
                x=x_column, 
                y=y_column,
                color=color_column,
                title=title or f"{y_title} vs {x_title}",
                trendline="ols"  # Add trendline
            )
        else:
            fig = px.scatter(
                df, 
                x=x_column, 
                y=y_column,
                title=title or f"{y_title} vs {x_title}",
                trendline="ols"  # Add trendline
            )
        
        # Update layout
        fig.update_layout(
            xaxis_title=x_title,
            yaxis_title=y_title
        )
        
        return fig