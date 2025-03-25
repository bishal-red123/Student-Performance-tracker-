import pandas as pd
from models.student import Student
from models.grade_calculator import GradeCalculator
from utils.excel_adapter import ExcelAdapter

class DataProcessor:
    """
    A class for processing student data between different formats.
    """
    def __init__(self):
        """Initialize the data processor with a grade calculator and excel adapter."""
        self.grade_calculator = GradeCalculator()
        self.excel_adapter = ExcelAdapter()
        
    def load_data(self, file_path):
        """
        Load data from a file (CSV or Excel) and convert to a DataFrame.
        
        Parameters:
        -----------
        file_path : str
            Path to the data file
            
        Returns:
        --------
        pandas.DataFrame
            DataFrame containing student data in the required format
        """
        if file_path.lower().endswith('.csv'):
            # Load CSV
            df = pd.read_csv(file_path)
        elif file_path.lower().endswith(('.xlsx', '.xls')):
            # Load Excel and preprocess using the adapter
            df = self.excel_adapter.preprocess_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")
        
        # Validate and clean the dataframe
        return self._validate_and_clean_dataframe(df)
        
    def _validate_and_clean_dataframe(self, df):
        """
        Validate and clean the DataFrame to ensure it has all required columns.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame to validate and clean
            
        Returns:
        --------
        pandas.DataFrame
            Validated and cleaned DataFrame
        """
        # Check required columns
        required_columns = ['student_id', 'name', 'academic_score', 
                           'cocurricular_score', 'discipline_score']
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        
        # Convert scores to numeric values
        for col in ['academic_score', 'cocurricular_score', 'discipline_score']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Remove rows with missing values in required columns
        df = df.dropna(subset=required_columns)
        
        # Ensure scores are within range (0-100)
        for col in ['academic_score', 'cocurricular_score', 'discipline_score']:
            df[col] = df[col].clip(0, 100)
        
        return df
    
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
            # Get required fields
            student_id = row['student_id']
            name = row['name']
            academic_score = row['academic_score']
            cocurricular_score = row['cocurricular_score']
            discipline_score = row['discipline_score']
            
            # Get optional fields as a dictionary
            optional_fields = {}
            for col in df.columns:
                if col not in ['student_id', 'name', 'academic_score', 
                              'cocurricular_score', 'discipline_score']:
                    optional_fields[col] = row[col]
            
            # Create Student object
            student = Student(
                student_id=student_id,
                name=name,
                academic_score=academic_score,
                cocurricular_score=cocurricular_score,
                discipline_score=discipline_score,
                **optional_fields
            )
            
            students.append(student)
        
        # Calculate grades for all students
        return self.grade_calculator.calculate_bulk_grades(students)
    
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
        # Convert each student to a dictionary
        data = [student.to_dict() for student in students]
        
        # Create DataFrame
        return pd.DataFrame(data)
    
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
        
        for key, value in filters.items():
            if key == 'min_academic_score':
                filtered_students = [s for s in filtered_students if s.academic_score >= value]
            elif key == 'min_cocurricular_score':
                filtered_students = [s for s in filtered_students if s.cocurricular_score >= value]
            elif key == 'min_discipline_score':
                filtered_students = [s for s in filtered_students if s.discipline_score >= value]
            elif key == 'min_overall_score':
                filtered_students = [s for s in filtered_students if s.overall_score >= value]
            elif key == 'max_academic_score':
                filtered_students = [s for s in filtered_students if s.academic_score <= value]
            elif key == 'max_cocurricular_score':
                filtered_students = [s for s in filtered_students if s.cocurricular_score <= value]
            elif key == 'max_discipline_score':
                filtered_students = [s for s in filtered_students if s.discipline_score <= value]
            elif key == 'max_overall_score':
                filtered_students = [s for s in filtered_students if s.overall_score <= value]
            elif key == 'grade':
                filtered_students = [s for s in filtered_students if s.overall_grade == value]
            elif key in ['class', 'section', 'batch', 'gender']:
                filtered_students = [s for s in filtered_students if s.get_attribute(key) == value]
        
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
        if sort_by == 'academic_score':
            return sorted(students, key=lambda s: s.academic_score, reverse=not ascending)
        elif sort_by == 'cocurricular_score':
            return sorted(students, key=lambda s: s.cocurricular_score, reverse=not ascending)
        elif sort_by == 'discipline_score':
            return sorted(students, key=lambda s: s.discipline_score, reverse=not ascending)
        elif sort_by == 'overall_score':
            return sorted(students, key=lambda s: s.overall_score, reverse=not ascending)
        elif sort_by == 'name':
            return sorted(students, key=lambda s: s.name, reverse=not ascending)
        elif sort_by == 'student_id':
            return sorted(students, key=lambda s: s.student_id, reverse=not ascending)
        else:
            # Try to sort by optional attribute
            return sorted(students, key=lambda s: s.get_attribute(sort_by, ""), reverse=not ascending)