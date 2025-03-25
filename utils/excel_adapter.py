"""
Excel adapter module for the Student Grading System.
This module provides functionality to adapt the specific Excel file format
used in the dataset to the format required by the application.
"""

import pandas as pd
import numpy as np
from models.student import Student

class ExcelAdapter:
    """
    Class to adapt the specific Excel file format to the application's required format.
    """
    
    def __init__(self):
        """Initialize the Excel adapter with default mappings."""
        # Mapping for CCA (Co-Curricular Activities) values to scores
        self.cca_mapping = {
            'MUSIC': 90,
            'DRAMA': 85,
            'SPORTS': 95,
            'ART': 88,
            'DESIGN': 86,
            'DANCE': 87,
            'ATHLETE': 95,
            'DEBATE': 92,
            'LITERATURE': 89,
            'DESIGNING': 86
        }
        
        # Mapping for BEHAVIOR values to scores
        self.behavior_mapping = {
            'A': 95,  # Excellent
            'B': 85,  # Very Good
            'C': 75,  # Good
            'O': 80,  # Outstanding
            'E': 90,  # Exceptional
            'X': 70   # Needs Improvement
        }
    
    def preprocess_excel(self, file_path):
        """
        Preprocess the Excel file to transform it into the required format.
        
        Parameters:
        -----------
        file_path : str
            Path to the Excel file
            
        Returns:
        --------
        pandas.DataFrame
            Preprocessed DataFrame in the required format
        """
        # Read the Excel file, skipping the header rows
        df = pd.read_excel(file_path, header=None, skiprows=2)
        
        # Rename the columns based on the expected column positions
        column_mapping = {
            0: 'student_id',
            1: 'name',
            2: 'academic_score',
            3: 'cca_category',
            4: 'behavior_category',
            5: 'overall_original'
        }
        
        # Apply the column mapping
        df = df.rename(columns=column_mapping)
        
        # Drop any rows where student_id is NaN (likely header or empty rows)
        df = df.dropna(subset=['student_id'])
        
        # Convert academic scores (0-10 scale) to 0-100 scale
        df['academic_score'] = df['academic_score'].apply(lambda x: float(x) * 10 if pd.notna(x) else np.nan)
        
        # Process CCA categories to get numerical scores
        df['cocurricular_score'] = df['cca_category'].apply(self._process_cca_category)
        
        # Process BEHAVIOR categories to get numerical scores
        df['discipline_score'] = df['behavior_category'].apply(self._process_behavior_category)
        
        # Keep only the required columns
        result_df = df[['student_id', 'name', 'academic_score', 'cocurricular_score', 'discipline_score']]
        
        # Ensure all score columns are numeric
        for col in ['academic_score', 'cocurricular_score', 'discipline_score']:
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
            # Fill any remaining NaN values with a default score of 70
            result_df[col] = result_df[col].fillna(70)
        
        return result_df
    
    def _process_cca_category(self, cca_value):
        """
        Process CCA category string to get a numerical score.
        If multiple categories are provided (comma-separated),
        the average score is returned.
        
        Parameters:
        -----------
        cca_value : str
            CCA category string (e.g., 'MUSIC', 'DRAMA,SPORTS')
            
        Returns:
        --------
        float
            Numerical score for the CCA category
        """
        if pd.isna(cca_value):
            return 75  # Default score for NA values
        
        categories = str(cca_value).split(',')
        total_score = 0
        valid_categories = 0
        
        for category in categories:
            category = category.strip().upper()
            if category in self.cca_mapping:
                total_score += self.cca_mapping[category]
                valid_categories += 1
        
        if valid_categories > 0:
            return total_score / valid_categories
        else:
            return 75  # Default score if no valid categories found
    
    def _process_behavior_category(self, behavior_value):
        """
        Process BEHAVIOR category to get a numerical score.
        
        Parameters:
        -----------
        behavior_value : str
            BEHAVIOR category string (e.g., 'A', 'B', 'C')
            
        Returns:
        --------
        float
            Numerical score for the BEHAVIOR category
        """
        if pd.isna(behavior_value):
            return 80  # Default score for NA values
        
        behavior = str(behavior_value).strip().upper()
        return self.behavior_mapping.get(behavior, 80)  # Default score if not found