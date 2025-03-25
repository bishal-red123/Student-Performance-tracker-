class Student:
    """
    A class to represent a student with multiple performance metrics.
    """
    def __init__(self, student_id, name, academic_score, cocurricular_score, discipline_score, **kwargs):
        """
        Initialize a student with required and optional attributes.
        
        Parameters:
        -----------
        student_id : str
            Unique identifier for the student
        name : str
            Full name of the student
        academic_score : float
            Score for academic performance (0-100)
        cocurricular_score : float
            Score for co-curricular activities (0-100)
        discipline_score : float
            Score for discipline record (0-100)
        **kwargs : dict
            Additional attributes for the student (class, section, etc.)
        """
        # Required attributes
        self.student_id = student_id
        self.name = name
        self.academic_score = float(academic_score)
        self.cocurricular_score = float(cocurricular_score)
        self.discipline_score = float(discipline_score)
        
        # Grade attributes (to be calculated)
        self.academic_grade = None
        self.cocurricular_grade = None
        self.discipline_grade = None
        self.overall_score = None
        self.overall_grade = None
        
        # Optional attributes
        self.attributes = {}
        for key, value in kwargs.items():
            self.attributes[key] = value
            
    def get_attribute(self, key, default=None):
        """
        Safely get an optional attribute.
        
        Parameters:
        -----------
        key : str
            The attribute key to retrieve
        default : any
            Default value if attribute doesn't exist
            
        Returns:
        --------
        any
            The attribute value or default
        """
        return self.attributes.get(key, default)
    
    def set_attribute(self, key, value):
        """
        Set an optional attribute.
        
        Parameters:
        -----------
        key : str
            The attribute key to set
        value : any
            The value to set
        """
        self.attributes[key] = value
    
    def to_dict(self):
        """
        Convert student object to dictionary.
        
        Returns:
        --------
        dict
            Dictionary representation of student
        """
        # Start with required fields
        student_dict = {
            'student_id': self.student_id,
            'name': self.name,
            'academic_score': self.academic_score,
            'cocurricular_score': self.cocurricular_score,
            'discipline_score': self.discipline_score,
            'academic_grade': self.academic_grade,
            'cocurricular_grade': self.cocurricular_grade,
            'discipline_grade': self.discipline_grade,
            'overall_score': self.overall_score,
            'overall_grade': self.overall_grade
        }
        
        # Add optional attributes
        for key, value in self.attributes.items():
            student_dict[key] = value
            
        return student_dict
    
    def __repr__(self):
        """String representation of the student."""
        return f"Student(id={self.student_id}, name={self.name}, overall_grade={self.overall_grade})"