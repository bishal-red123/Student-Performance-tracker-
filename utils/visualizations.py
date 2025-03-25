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
        grade_counts = df[column].value_counts().sort_index()
        
        fig = px.bar(
            x=grade_counts.index,
            y=grade_counts.values,
            title=title or f'Distribution of {column}',
            labels={'x': column, 'y': 'Count'},
            color=grade_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='Number of Students',
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
        fig = px.histogram(
            df, 
            x=column,
            nbins=bins,
            title=title or f'Distribution of {column}',
            color_discrete_sequence=['lightblue']
        )
        
        fig.update_layout(
            xaxis_title=column,
            yaxis_title='Number of Students',
            bargap=0.1
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
        # Melt the dataframe to get a format suitable for boxplot
        score_columns = ['academic_score', 'cocurricular_score', 'discipline_score']
        melted_df = pd.melt(
            df, 
            value_vars=score_columns,
            var_name='Category', 
            value_name='Score'
        )
        
        # Rename categories for better readability
        category_map = {
            'academic_score': 'Academic',
            'cocurricular_score': 'Co-curricular',
            'discipline_score': 'Discipline'
        }
        melted_df['Category'] = melted_df['Category'].map(category_map)
        
        fig = px.box(
            melted_df,
            x='Category',
            y='Score',
            color='Category',
            title=title or 'Comparison of Score Categories',
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='Score (0-100)',
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
        categories = ['Academic', 'Co-curricular', 'Discipline']
        values = [student.academic_score, student.cocurricular_score, student.discipline_score]
        
        # Close the radar by appending the first value at the end
        categories = categories + [categories[0]]
        values = values + [values[0]]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=student.name,
            line_color='rgb(31, 119, 180)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            title=title or f'Performance Profile for {student.name}'
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
        
        # Color palette for multiple students
        colors = px.colors.qualitative.Plotly
        
        # Add trace for each student
        for i, student in enumerate(students):
            values = [student.academic_score, student.cocurricular_score, student.discipline_score]
            
            # Close the radar by appending the first value at the end
            cat = categories + [categories[0]]
            val = values + [values[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=val,
                theta=cat,
                fill='toself',
                name=student.name,
                line_color=colors[i % len(colors)]
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=title or 'Comparative Performance Profiles',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
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
        # Calculate correlation matrix
        corr_columns = ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']
        corr_df = df[corr_columns].corr()
        
        # Rename columns for better readability
        column_names = {
            'academic_score': 'Academic',
            'cocurricular_score': 'Co-curricular',
            'discipline_score': 'Discipline',
            'overall_score': 'Overall'
        }
        
        corr_df = corr_df.rename(index=column_names, columns=column_names)
        
        # Create heatmap
        fig = px.imshow(
            corr_df,
            text_auto='.2f',
            color_continuous_scale='RdBu_r',
            title=title or 'Correlation Matrix of Performance Metrics',
            range_color=[-1, 1],
            labels=dict(color='Correlation')
        )
        
        fig.update_layout(
            xaxis_title='',
            yaxis_title='',
            coloraxis_colorbar=dict(
                title='Correlation',
                thicknessmode="pixels", thickness=15,
                lenmode="pixels", len=300,
                yanchor="top", y=1,
                ticks="outside", ticksuffix=" "
            )
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
        # Group by time and calculate mean
        df_grouped = df.groupby(time_column)[metric_column].mean().reset_index()
        
        fig = px.line(
            df_grouped,
            x=time_column,
            y=metric_column,
            markers=True,
            title=title or f'{metric_column} over {time_column}',
            color_discrete_sequence=['royalblue']
        )
        
        fig.update_layout(
            xaxis_title=time_column,
            yaxis_title=metric_column
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
        if color_column:
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                color=color_column,
                title=title or f'{y_column} vs {x_column}',
                hover_name='name'
            )
        else:
            fig = px.scatter(
                df,
                x=x_column,
                y=y_column,
                title=title or f'{y_column} vs {x_column}',
                hover_name='name',
                color_discrete_sequence=['royalblue']
            )
        
        # Add trend line
        fig.update_layout(
            xaxis_title=x_column,
            yaxis_title=y_column
        )
        
        # Add trend line
        fig.add_trace(
            go.Scatter(
                x=df[x_column],
                y=np.poly1d(np.polyfit(df[x_column], df[y_column], 1))(df[x_column]),
                mode='lines',
                name='Trend',
                line=dict(color='rgba(255, 0, 0, 0.5)', dash='dash')
            )
        )
        
        return fig