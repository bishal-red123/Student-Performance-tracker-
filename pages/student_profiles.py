import streamlit as st
import pandas as pd
import plotly.express as px
from utils.visualizations import Visualizer

def show():
    """
    Display the student profiles page for individual student analysis.
    """
    if "dataframe" not in st.session_state or st.session_state.dataframe is None:
        st.warning("Please upload data on the Home page first.")
        return
    
    st.title("Student Profiles")
    
    # Prepare data
    df = st.session_state.processor.students_to_dataframe(st.session_state.students)
    
    # Create a sidebar for student selection
    st.sidebar.subheader("Student Selection")
    
    # Search by name
    search_name = st.sidebar.text_input("Search by Name")
    
    # Filter by grade
    st.sidebar.subheader("Filter Options")
    selected_grade = st.sidebar.multiselect(
        "Filter by Overall Grade",
        options=sorted(df['overall_grade'].unique()),
        default=[]
    )
    
    # Apply filters to the dataframe
    filtered_df = df.copy()
    
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False)]
    
    if selected_grade:
        filtered_df = filtered_df[filtered_df['overall_grade'].isin(selected_grade)]
    
    # Display filtered student list
    st.sidebar.subheader("Student List")
    if len(filtered_df) == 0:
        st.sidebar.info("No students match the filters.")
    else:
        selected_student_name = st.sidebar.selectbox(
            "Select Student",
            options=filtered_df['name'].tolist(),
            index=0
        )
        
        # Find the selected student
        selected_student_data = filtered_df[filtered_df['name'] == selected_student_name].iloc[0]
        selected_student = next(
            (s for s in st.session_state.students if s.name == selected_student_name), 
            None
        )
        
        if selected_student:
            # Display student profile
            st.header(f"Profile: {selected_student.name}")
            
            # Student ID and basic info
            col1, col2, col3 = st.columns(3)
            col1.metric("Student ID", selected_student.student_id)
            
            # Check if class and section are available
            if 'class' in selected_student.attributes:
                col2.metric("Class", selected_student.get_attribute('class'))
            
            if 'section' in selected_student.attributes:
                col3.metric("Section", selected_student.get_attribute('section'))
            
            # Performance summary
            st.subheader("Performance Summary")
            
            # Create columns for the different performance metrics
            cols = st.columns(4)
            
            with cols[0]:
                st.markdown("**Academic**")
                st.metric("Score", f"{selected_student.academic_score:.1f}")
                st.metric("Grade", selected_student.academic_grade)
            
            with cols[1]:
                st.markdown("**Co-curricular**")
                st.metric("Score", f"{selected_student.cocurricular_score:.1f}")
                st.metric("Grade", selected_student.cocurricular_grade)
            
            with cols[2]:
                st.markdown("**Discipline**")
                st.metric("Score", f"{selected_student.discipline_score:.1f}")
                st.metric("Grade", selected_student.discipline_grade)
            
            with cols[3]:
                st.markdown("**Overall**")
                st.metric("Score", f"{selected_student.overall_score:.1f}")
                st.metric("Grade", selected_student.overall_grade)
            
            # Radar chart
            st.subheader("Performance Profile")
            radar_fig = Visualizer.plot_student_radar(selected_student)
            st.plotly_chart(radar_fig, use_container_width=True)
            
            # Additional attributes
            st.subheader("Additional Information")
            
            additional_attrs = {k: v for k, v in selected_student.attributes.items()
                              if k not in ['class', 'section']}
            
            if additional_attrs:
                attr_df = pd.DataFrame({
                    'Attribute': additional_attrs.keys(),
                    'Value': additional_attrs.values()
                })
                st.dataframe(attr_df, use_container_width=True)
            else:
                st.info("No additional information available.")
            
            # Performance comparison with class average
            st.subheader("Comparison with Class Average")
            
            # Calculate class averages
            class_avg = {
                'Academic': df['academic_score'].mean(),
                'Co-curricular': df['cocurricular_score'].mean(),
                'Discipline': df['discipline_score'].mean(),
                'Overall': df['overall_score'].mean()
            }
            
            student_scores = {
                'Academic': selected_student.academic_score,
                'Co-curricular': selected_student.cocurricular_score,
                'Discipline': selected_student.discipline_score,
                'Overall': selected_student.overall_score
            }
            
            # Create dataframe for comparison
            comparison_data = {
                'Category': list(class_avg.keys()),
                'Student Score': list(student_scores.values()),
                'Class Average': list(class_avg.values())
            }
            comparison_df = pd.DataFrame(comparison_data)
            
            # Create a bar chart for comparison
            comparison_fig = px.bar(
                comparison_df,
                x='Category',
                y=['Student Score', 'Class Average'],
                barmode='group',
                title=f"Performance Comparison: {selected_student.name} vs. Class Average",
                labels={'value': 'Score', 'variable': ''}
            )
            
            st.plotly_chart(comparison_fig, use_container_width=True)
            
            # Ranking information
            st.subheader("Class Ranking")
            
            # Calculate rankings
            academic_rank = df.sort_values('academic_score', ascending=False)['name'].tolist().index(selected_student.name) + 1
            cocurr_rank = df.sort_values('cocurricular_score', ascending=False)['name'].tolist().index(selected_student.name) + 1
            discipline_rank = df.sort_values('discipline_score', ascending=False)['name'].tolist().index(selected_student.name) + 1
            overall_rank = df.sort_values('overall_score', ascending=False)['name'].tolist().index(selected_student.name) + 1
            
            # Display rankings
            rank_cols = st.columns(4)
            total_students = len(df)
            
            rank_cols[0].metric("Academic Rank", f"{academic_rank}/{total_students}")
            rank_cols[1].metric("Co-curricular Rank", f"{cocurr_rank}/{total_students}")
            rank_cols[2].metric("Discipline Rank", f"{discipline_rank}/{total_students}")
            rank_cols[3].metric("Overall Rank", f"{overall_rank}/{total_students}")
            
            # Percentile calculation
            academic_percentile = round((total_students - academic_rank) / total_students * 100, 1)
            cocurr_percentile = round((total_students - cocurr_rank) / total_students * 100, 1)
            discipline_percentile = round((total_students - discipline_rank) / total_students * 100, 1)
            overall_percentile = round((total_students - overall_rank) / total_students * 100, 1)
            
            st.write("**Percentile Ranking:**")
            percentile_cols = st.columns(4)
            percentile_cols[0].metric("Academic", f"{academic_percentile}%")
            percentile_cols[1].metric("Co-curricular", f"{cocurr_percentile}%")
            percentile_cols[2].metric("Discipline", f"{discipline_percentile}%")
            percentile_cols[3].metric("Overall", f"{overall_percentile}%")
