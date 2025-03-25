class GradeCalculator:
    """
    A class to calculate grades based on various performance metrics.
    """
    def __init__(self, weights=None, grade_scale=None):
        """
        Initialize the grade calculator with custom weights and grade scale.
        
        Parameters:
        -----------
        weights : dict
            Custom weights for different performance metrics
        grade_scale : dict
            Custom grade scale for score to grade conversion
        """
        # Default weights for different metrics
        self.weights = weights or {
            'academic': 0.6,
            'cocurricular': 0.2,
            'discipline': 0.2
        }
        
        # Default grade scale
        self.grade_scale = grade_scale or {
            'A+': 95,  # 95-100
            'A': 90,   # 90-94.99
            'A-': 85,  # 85-89.99
            'B+': 80,  # 80-84.99
            'B': 75,   # 75-79.99
            'B-': 70,  # 70-74.99
            'C+': 65,  # 65-69.99
            'C': 60,   # 60-64.99
            'C-': 55,  # 55-59.99
            'D+': 50,  # 50-54.99
            'D': 45,   # 45-49.99
            'F': 0     # 0-44.99
        }
    
    def calculate_overall_score(self, student):
        """
        Calculate the overall score for a student.
        
        Parameters:
        -----------
        student : Student
            The student object with performance metrics
            
        Returns:
        --------
        float
            The overall weighted score
        """
        overall_score = (
            self.weights['academic'] * student.academic_score +
            self.weights['cocurricular'] * student.cocurricular_score +
            self.weights['discipline'] * student.discipline_score
        )
        
        return overall_score
    
    def get_grade(self, score):
        """
        Convert a numerical score to a letter grade.
        
        Parameters:
        -----------
        score : float
            Numerical score (0-100)
            
        Returns:
        --------
        str
            Letter grade based on the grade scale
        """
        for grade, min_score in sorted(self.grade_scale.items(), key=lambda x: x[1], reverse=True):
            if score >= min_score:
                return grade
        return 'F'  # Default if score is below all thresholds
    
    def calculate_grades(self, student):
        """
        Calculate all grades for a student.
        
        Parameters:
        -----------
        student : Student
            The student object with performance metrics
            
        Returns:
        --------
        Student
            The updated student object with calculated grades
        """
        # Calculate overall score
        student.overall_score = self.calculate_overall_score(student)
        
        # Calculate individual grades
        student.academic_grade = self.get_grade(student.academic_score)
        student.cocurricular_grade = self.get_grade(student.cocurricular_score)
        student.discipline_grade = self.get_grade(student.discipline_score)
        
        # Calculate overall grade
        student.overall_grade = self.get_grade(student.overall_score)
        
        return student
    
    def calculate_bulk_grades(self, students):
        """
        Calculate grades for multiple students.
        
        Parameters:
        -----------
        students : list
            List of Student objects
            
        Returns:
        --------
        list
            Updated list of Student objects with calculated grades
        """
        return [self.calculate_grades(student) for student in students]
    
    def update_weights(self, new_weights):
        """
        Update the weights used for calculations.
        
        Parameters:
        -----------
        new_weights : dict
            New weights for different performance metrics
        """
        self.weights.update(new_weights)
        
        # Normalize weights to ensure they sum to 1
        total = sum(self.weights.values())
        if total != 1.0:
            for key in self.weights:
                self.weights[key] /= total
    
    def update_grade_scale(self, new_grade_scale):
        """
        Update the grade scale used for calculations.
        
        Parameters:
        -----------
        new_grade_scale : dict
            New grade scale for score to grade conversion
        """
        self.grade_scale.update(new_grade_scale)
