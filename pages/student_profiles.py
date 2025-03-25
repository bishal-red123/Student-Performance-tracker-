"""
Student profiles page for the Student Grading System.
This page allows viewing and analyzing individual student profiles.
"""

import streamlit as st
import pandas as pd
from utils.visualizations import Visualizer

def show():
    """
    Display the student profiles page for individual student analysis.
    """
    st.title("Student Profiles")
    
    if "students" not in st.session_state or not st.session_state.students:
        st.warning("No data available. Please upload student data from the Home page.")
        return
    
    # Get processed dataframe
    processor = st.session_state.processor
    students_df = processor.students_to_dataframe(st.session_state.students)
    
    # Student selection
    st.subheader("Select a Student")
    
    # Get list of names and IDs for selection
    student_names = sorted(students_df['name'].tolist())
    student_ids = sorted([str(id) for id in students_df['student_id'].tolist()])
    
    # Two methods of selection: by ID or by name
    selection_method = st.radio(
        "Selection method",
        ["Select by Name", "Select by ID"],
        horizontal=True
    )
    
    selected_student = None
    
    if selection_method == "Select by Name":
        selected_name = st.selectbox("Select student name", student_names)
        selected_student = students_df[students_df['name'] == selected_name].iloc[0]
        
    else:  # Select by ID
        selected_id = st.selectbox("Select student ID", student_ids)
        selected_student = students_df[students_df['student_id'].astype(str) == selected_id].iloc[0]
    
    # Display student profile
    if selected_student is not None:
        st.subheader(f"Profile for {selected_student['name']}")
        
        # Create two columns for basic info and grade summary
        col1, col2 = st.columns(2)
        
        # Basic information
        with col1:
            st.write("#### Basic Information")
            st.write(f"**Student ID:** {selected_student['student_id']}")
            st.write(f"**Name:** {selected_student['name']}")
            
            # Display any additional attributes the student may have
            for key, value in selected_student.items():
                if key not in ['student_id', 'name', 'academic_score', 'cocurricular_score',
                              'discipline_score', 'overall_score', 'academic_grade',
                              'cocurricular_grade', 'discipline_grade', 'overall_grade']:
                    # Skip NaN values and internal attributes
                    if pd.notna(value) and not key.startswith('_'):
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
        
        # Grade summary
        with col2:
            st.write("#### Performance Summary")
            st.write(f"**Overall Grade:** {selected_student['overall_grade']}")
            st.write(f"**Overall Score:** {selected_student['overall_score']:.2f}")
            
            # Create a grades and scores table
            grades_data = {
                "Category": ["Academic", "Co-curricular", "Discipline"],
                "Score": [
                    f"{selected_student['academic_score']:.2f}",
                    f"{selected_student['cocurricular_score']:.2f}",
                    f"{selected_student['discipline_score']:.2f}"
                ],
                "Grade": [
                    selected_student['academic_grade'],
                    selected_student['cocurricular_grade'],
                    selected_student['discipline_grade']
                ]
            }
            
            grades_df = pd.DataFrame(grades_data)
            st.table(grades_df)
        
        # Performance radar chart
        st.subheader("Performance Profile")
        
        # Get the student object from session state
        student_obj = next(
            (s for s in st.session_state.students 
             if str(s.student_id) == str(selected_student['student_id'])),
            None
        )
        
        if student_obj:
            radar_chart = Visualizer.plot_student_radar(student_obj)
            st.plotly_chart(radar_chart, use_container_width=True)
        
        # Comparative analysis
        st.subheader("Comparative Analysis")
        
        # Compare with average, top student, and bottom student
        avg_student = students_df.mean()
        top_student = students_df.loc[students_df['overall_score'].idxmax()]
        
        # Create comparison dataframe
        comparison_data = {
            "Metric": ["Academic Score", "Co-curricular Score", "Discipline Score", "Overall Score"],
            f"{selected_student['name']}": [
                selected_student['academic_score'],
                selected_student['cocurricular_score'],
                selected_student['discipline_score'],
                selected_student['overall_score']
            ],
            "Class Average": [
                avg_student['academic_score'],
                avg_student['cocurricular_score'],
                avg_student['discipline_score'],
                avg_student['overall_score']
            ],
            f"Top Student ({top_student['name']})": [
                top_student['academic_score'],
                top_student['cocurricular_score'],
                top_student['discipline_score'],
                top_student['overall_score']
            ]
        }
        
        comparison_df = pd.DataFrame(comparison_data)
        st.table(comparison_df)
        
        # Calculate and display percentile rankings
        st.subheader("Percentile Rankings")
        
        # Calculate percentiles for each score category
        percentiles = {}
        
        for category in ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']:
            # Calculate the number of students with lower scores
            count_lower = (students_df[category] < selected_student[category]).sum()
            
            # Calculate percentile
            percentile = (count_lower / len(students_df)) * 100
            
            # Store in dictionary
            percentiles[category] = percentile
        
        # Display percentiles
        percentile_data = {
            "Category": ["Academic", "Co-curricular", "Discipline", "Overall"],
            "Percentile": [
                f"{percentiles['academic_score']:.1f}%",
                f"{percentiles['cocurricular_score']:.1f}%",
                f"{percentiles['discipline_score']:.1f}%",
                f"{percentiles['overall_score']:.1f}%"
            ]
        }
        
        percentile_df = pd.DataFrame(percentile_data)
        st.table(percentile_df)
        
        # Comparative radar with peers
        st.subheader("Compare with Peers")
        
        # Allow selecting peers for comparison
        peer_selection = st.multiselect(
            "Select peers to compare with",
            [name for name in student_names if name != selected_student['name']],
            max_selections=3
        )
        
        if peer_selection:
            # Get student objects for the selected peers
            peer_objs = [
                next((s for s in st.session_state.students if s.name == name), None)
                for name in peer_selection
            ]
            
            # Filter out any None values
            peer_objs = [p for p in peer_objs if p is not None]
            
            # Only proceed if we have valid peer objects
            if peer_objs:
                # Create a list with the selected student first, then the peers
                comparison_students = [student_obj] + peer_objs
                
                # Create comparative radar chart
                radar_chart = Visualizer.plot_comparative_radar(comparison_students)
                st.plotly_chart(radar_chart, use_container_width=True)
        
        # Recommendations section
        st.subheader("Recommendations")
        
        # Generate recommendations based on scores
        recommendations = []
        
        # Academic recommendations
        if selected_student['academic_score'] < 60:
            recommendations.append("Consider arranging academic intervention or additional tutoring.")
        elif selected_student['academic_score'] < 75:
            recommendations.append("Academic performance needs improvement. Suggest focused study in weak areas.")
        elif selected_student['academic_score'] < 90:
            recommendations.append("Good academic performance with room for improvement in specific subjects.")
        else:
            recommendations.append("Excellent academic performance. Consider advanced/enrichment programs.")
        
        # Co-curricular recommendations
        if selected_student['cocurricular_score'] < 60:
            recommendations.append("Encourage participation in more co-curricular activities to develop soft skills.")
        elif selected_student['cocurricular_score'] < 75:
            recommendations.append("Consider guiding the student towards activities that align with their interests.")
        elif selected_student['cocurricular_score'] < 90:
            recommendations.append("Good co-curricular involvement. Consider leadership roles in current activities.")
        else:
            recommendations.append("Excellent co-curricular involvement. Encourage mentoring junior students.")
        
        # Discipline recommendations
        if selected_student['discipline_score'] < 60:
            recommendations.append("Behavior needs significant improvement. Consider behavioral intervention.")
        elif selected_student['discipline_score'] < 75:
            recommendations.append("Occasional behavioral issues. Regular counseling might be beneficial.")
        elif selected_student['discipline_score'] < 90:
            recommendations.append("Generally good behavior with minor concerns. Positive reinforcement recommended.")
        else:
            recommendations.append("Excellent discipline record. Consider student for prefect/monitor roles.")
        
        # Display recommendations
        for recommendation in recommendations:
            st.write(f"• {recommendation}")
        
        # Personalized recommendation based on overall profile
        st.write("#### Personalized Recommendation:")
        
        # Identify the lowest scoring area
        scores = {
            "Academic": float(selected_student['academic_score']),
            "Co-curricular": float(selected_student['cocurricular_score']),
            "Discipline": float(selected_student['discipline_score'])
        }
        
        # Find lowest and highest scoring areas
        lowest_area = min(scores.items(), key=lambda x: x[1])[0]
        highest_area = max(scores.items(), key=lambda x: x[1])[0]
        
        if max(scores.values()) - min(scores.values()) > 20:
            st.write(f"The student shows a significant gap between {highest_area} ({scores[highest_area]:.1f}) and {lowest_area} ({scores[lowest_area]:.1f}). "
                    f"Consider a focused development plan to improve performance in {lowest_area} area while maintaining strengths.")
        else:
            st.write("The student shows a balanced performance profile. Consider providing opportunities that build on this balanced foundation while encouraging excellence in all areas.")