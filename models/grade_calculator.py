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
        self.weights = {
            'academic': 0.5,      # 50% weight for academic performance
            'cocurricular': 0.3,  # 30% weight for co-curricular activities
            'discipline': 0.2     # 20% weight for discipline record
        }
        
        # Default grade scale
        self.grade_scale = {
            'A+': 95,  # Score >= 95
            'A': 90,   # Score >= 90
            'A-': 85,  # Score >= 85
            'B+': 80,  # Score >= 80
            'B': 75,   # Score >= 75
            'B-': 70,  # Score >= 70
            'C+': 65,  # Score >= 65
            'C': 60,   # Score >= 60
            'C-': 55,  # Score >= 55
            'D+': 50,  # Score >= 50
            'D': 45,   # Score >= 45
            'F': 0     # Score >= 0
        }
        
        # Update weights if provided
        if weights:
            self.weights.update(weights)
            
        # Update grade scale if provided
        if grade_scale:
            self.grade_scale.update(grade_scale)
    
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
        # Calculate weighted score
        weighted_score = (
            self.weights['academic'] * student.academic_score +
            self.weights['cocurricular'] * student.cocurricular_score +
            self.weights['discipline'] * student.discipline_score
        )
        
        return weighted_score
    
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
        # Sort grade thresholds in descending order
        sorted_grades = sorted(self.grade_scale.items(), key=lambda x: x[1], reverse=True)
        
        # Find the appropriate grade
        for grade, threshold in sorted_grades:
            if score >= threshold:
                return grade
                
        # Default grade for scores below lowest threshold
        return 'F'
    
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
        # Calculate individual grades
        student.academic_grade = self.get_grade(student.academic_score)
        student.cocurricular_grade = self.get_grade(student.cocurricular_score)
        student.discipline_grade = self.get_grade(student.discipline_score)
        
        # Calculate overall score and grade
        student.overall_score = self.calculate_overall_score(student)
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
    
    def update_grade_scale(self, new_grade_scale):
        """
        Update the grade scale used for calculations.
        
        Parameters:
        -----------
        new_grade_scale : dict
            New grade scale for score to grade conversion
        """
        self.grade_scale.update(new_grade_scale)