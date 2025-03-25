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
        # Default weights for different performance metrics
        self.weights = {
            'academic': 0.6,      # 60% weight for academics
            'cocurricular': 0.25, # 25% weight for co-curricular activities
            'discipline': 0.15    # 15% weight for discipline
        }
        
        # Default grade scale (score to grade mapping)
        self.grade_scale = {
            90: 'A',  # 90-100: A
            80: 'B',  # 80-89: B
            70: 'C',  # 70-79: C
            60: 'D',  # 60-69: D
            0: 'F'    # 0-59: F
        }
        
        # Apply custom weights if provided
        if weights:
            self.update_weights(weights)
            
        # Apply custom grade scale if provided
        if grade_scale:
            self.update_grade_scale(grade_scale)
    
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
        # Calculate the weighted score
        weighted_score = (
            student.academic_score * self.weights['academic'] +
            student.cocurricular_score * self.weights['cocurricular'] +
            student.discipline_score * self.weights['discipline']
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
        # Get the grade for the given score
        for min_score, grade in sorted(self.grade_scale.items(), reverse=True):
            if score >= min_score:
                return grade
                
        # Default to 'F' if no grade matches (should not happen with default scale)
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
        # Calculate the overall score
        student.overall_score = self.calculate_overall_score(student)
        
        # Assign grades based on scores
        student.academic_grade = self.get_grade(student.academic_score)
        student.cocurricular_grade = self.get_grade(student.cocurricular_score)
        student.discipline_grade = self.get_grade(student.discipline_score)
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
        # Validate that weights sum to 1.0
        total_weight = sum(new_weights.values())
        if abs(total_weight - 1.0) > 0.01:
            # If weights don't sum to 1.0, normalize them
            normalized_weights = {k: v / total_weight for k, v in new_weights.items()}
            self.weights.update(normalized_weights)
        else:
            self.weights.update(new_weights)
    
    def update_grade_scale(self, new_grade_scale):
        """
        Update the grade scale used for calculations.
        
        Parameters:
        -----------
        new_grade_scale : dict
            New grade scale for score to grade conversion
        """
        self.grade_scale = new_grade_scale