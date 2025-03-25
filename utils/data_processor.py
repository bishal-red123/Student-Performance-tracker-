import pandas as pd
from models.student import Student
from models.grade_calculator import GradeCalculator

class DataProcessor:
    """
    A class for processing student data between different formats.
    """
    def __init__(self):
        """Initialize the data processor with a grade calculator."""
        self.calculator = GradeCalculator()
    
    def dataframe_to_students(self, df):
        """
        Convert a pandas DataFrame to a list of Student objects.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            DataFrame containing student data
            
        Returns:
        --------
        list
            List of Student objects with calculated grades
        """
        students = []
        
        for _, row in df.iterrows():
            # Extract required attributes
            student_id = row['student_id']
            name = row['name']
            academic_score = row['academic_score']
            cocurricular_score = row['cocurricular_score']
            discipline_score = row['discipline_score']
            
            # Extract optional attributes
            optional_attrs = {}
            for col in row.index:
                if col not in ['student_id', 'name', 'academic_score', 'cocurricular_score', 'discipline_score']:
                    optional_attrs[col] = row[col]
            
            # Create student object
            student = Student(student_id, name, academic_score, cocurricular_score, discipline_score, **optional_attrs)
            
            # Calculate grades
            self.calculator.calculate_grades(student)
            
            students.append(student)
        
        return students
    
    def students_to_dataframe(self, students):
        """
        Convert a list of Student objects to a pandas DataFrame.
        
        Parameters:
        -----------
        students : list
            List of Student objects
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame containing student data
        """
        student_dicts = [student.to_dict() for student in students]
        return pd.DataFrame(student_dicts)
    
    def filter_students(self, students, filters):
        """
        Filter a list of students based on criteria.
        
        Parameters:
        -----------
        students : list
            List of Student objects
        filters : dict
            Dictionary of filter criteria
            
        Returns:
        --------
        list
            Filtered list of Student objects
        """
        filtered_students = students.copy()
        
        for attribute, value in filters.items():
            if attribute in ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']:
                # Handle range filters for scores
                min_val, max_val = value
                filtered_students = [s for s in filtered_students if min_val <= getattr(s, attribute) <= max_val]
            
            elif attribute in ['academic_grade', 'cocurricular_grade', 'discipline_grade', 'overall_grade']:
                # Handle grade filters
                if isinstance(value, list):
                    filtered_students = [s for s in filtered_students if getattr(s, attribute) in value]
                else:
                    filtered_students = [s for s in filtered_students if getattr(s, attribute) == value]
            
            else:
                # Handle other attributes
                filtered_students = [s for s in filtered_students if s.get_attribute(attribute) == value]
        
        return filtered_students
    
    def sort_students(self, students, sort_by, ascending=True):
        """
        Sort a list of students based on a given attribute.
        
        Parameters:
        -----------
        students : list
            List of Student objects
        sort_by : str
            Attribute to sort by
        ascending : bool
            Sort in ascending order if True, descending if False
            
        Returns:
        --------
        list
            Sorted list of Student objects
        """
        if sort_by in ['academic_score', 'cocurricular_score', 'discipline_score', 'overall_score']:
            return sorted(students, key=lambda s: getattr(s, sort_by), reverse=not ascending)
        else:
            # Try to sort by optional attribute
            return sorted(students, key=lambda s: s.get_attribute(sort_by, ""), reverse=not ascending)
