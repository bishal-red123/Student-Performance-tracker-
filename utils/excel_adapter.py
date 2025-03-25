"""
Excel adapter module for the Student Grading System.
This module provides functionality to adapt the specific Excel file format
used in the dataset to the format required by the application.
"""

import pandas as pd
import numpy as np
import os

class ExcelAdapter:
    """
    Class to adapt the specific Excel file format to the application's required format.
    """
    
    def __init__(self):
        """Initialize the Excel adapter with default mappings."""
        # Mapping of CCA categories to scores
        self.cca_mapping = {
            'MUSIC': 90,
            'DRAMA': 85,
            'SPORTS': 95,
            'ART': 88,
            'DESIGN': 87,
            'DANCE': 92,
            'DEBATE': 89,
            'CODING': 94
        }
        
        # Mapping of BEHAVIOR categories to scores
        self.behavior_mapping = {
            'A': 95,  # Excellent behavior
            'B': 85,  # Good behavior
            'C': 75,  # Average behavior
            'D': 65,  # Below average behavior
            'E': 55,  # Poor behavior
            'O': 80,  # Other/Not specified
            'X': 50   # Problematic behavior
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
        temp_file_path = None
        try:
            # Save a temporary copy of the file in case we need to modify it
            temp_file_path = f"temp_{os.path.basename(file_path)}"
            with open(file_path, 'rb') as src, open(temp_file_path, 'wb') as dst:
                dst.write(src.read())
            
            # Read the Excel file, skipping the first few rows if they contain metadata
            # First, try to read with default settings
            df = pd.read_excel(temp_file_path)
            
            # Check if the dataframe has appropriate columns
            if not self._has_necessary_columns(df):
                # Try different starting rows
                for i in range(1, 10):
                    try:
                        df = pd.read_excel(temp_file_path, skiprows=i)
                        if self._has_necessary_columns(df):
                            break
                    except:
                        continue
            
            # Process the dataframe
            result_df = self._process_dataframe(df)
            
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            return result_df
            
        except Exception as e:
            # Clean up temporary file if it exists
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            
            raise Exception(f"Error preprocessing Excel file: {str(e)}")
    
    def _has_necessary_columns(self, df):
        """Check if the dataframe has columns that we can work with."""
        # Look for columns that might contain student, name, or score information
        potential_columns = [col.lower() for col in df.columns]
        
        # Check if we have enough potentially useful columns
        student_col = any('id' in col or 'roll' in col or 'student' in col for col in potential_columns)
        name_col = any('name' in col for col in potential_columns)
        acad_col = any('acad' in col or 'score' in col or 'mark' in col for col in potential_columns)
        
        return student_col and name_col and len(df.columns) >= 5
    
    def _process_dataframe(self, df):
        """Process the dataframe to extract and format the required data."""
        # Create a copy of the dataframe to avoid modifying the original
        result_df = df.copy()
        
        # Standardize column names (make lowercase and replace spaces with underscores)
        result_df.columns = [col.lower().replace(' ', '_') for col in result_df.columns]
        
        # Try to identify key columns
        student_id_col = next((col for col in result_df.columns if 'id' in col or 'roll' in col), None)
        name_col = next((col for col in result_df.columns if 'name' in col), None)
        acad_col = next((col for col in result_df.columns if 'acad' in col or 'mark' in col or 'score' in col), None)
        cca_col = next((col for col in result_df.columns if 'cca' in col or 'co' in col or 'extra' in col), None)
        behavior_col = next((col for col in result_df.columns if 'behav' in col or 'disc' in col or 'conduct' in col), None)
        
        # If we couldn't find key columns, try to use positional columns
        if student_id_col is None:
            student_id_col = result_df.columns[0]  # Assume first column is student ID
        if name_col is None:
            name_col = result_df.columns[1]  # Assume second column is name
        
        # Rename columns to the required format
        column_mapping = {
            student_id_col: 'student_id',
            name_col: 'name'
        }
        
        if acad_col:
            column_mapping[acad_col] = 'academic_score'
        if cca_col:
            column_mapping[cca_col] = 'cocurricular_score'
        if behavior_col:
            column_mapping[behavior_col] = 'discipline_score'
            
        # Rename the columns we've identified
        result_df = result_df.rename(columns=column_mapping)
        
        # Ensure all required columns exist
        for col in ['student_id', 'name', 'academic_score', 'cocurricular_score', 'discipline_score']:
            if col not in result_df.columns:
                # If academic_score is missing, try to find an alternative column
                if col == 'academic_score':
                    alt_col = next((c for c in result_df.columns if 'mark' in c or 'grade' in c), None)
                    if alt_col:
                        result_df['academic_score'] = result_df[alt_col]
                    else:
                        result_df['academic_score'] = 70  # Default value
                
                # If cocurricular_score is missing, look for CCA or similar column
                elif col == 'cocurricular_score':
                    cca_cols = [c for c in result_df.columns if any(x in c for x in ['cca', 'activity', 'extra'])]
                    if cca_cols:
                        # Process CCA data if found
                        result_df['cocurricular_score'] = result_df[cca_cols[0]].apply(self._process_cca_category)
                    else:
                        result_df['cocurricular_score'] = 70  # Default value
                
                # If discipline_score is missing, look for behavior or conduct column
                elif col == 'discipline_score':
                    behavior_cols = [c for c in result_df.columns if any(x in c for x in ['behav', 'conduct', 'disc'])]
                    if behavior_cols:
                        # Process behavior data if found
                        result_df['discipline_score'] = result_df[behavior_cols[0]].apply(self._process_behavior_category)
                    else:
                        result_df['discipline_score'] = 70  # Default value
                
                # For other missing columns, add with default values
                else:
                    result_df[col] = 'Unknown' if col == 'name' else 0
        
        # Convert score columns to numeric
        for col in ['academic_score', 'cocurricular_score', 'discipline_score']:
            result_df[col] = pd.to_numeric(result_df[col], errors='coerce')
            # Fill missing values with a default score
            result_df[col] = result_df[col].fillna(70)
        
        # Remove rows with missing or invalid student_id or name
        result_df = result_df.dropna(subset=['student_id', 'name'])
        
        # Convert student_id to string
        result_df['student_id'] = result_df['student_id'].astype(str)
        
        # Ensure valid score ranges (0-100)
        for col in ['academic_score', 'cocurricular_score', 'discipline_score']:
            result_df[col] = result_df[col].clip(0, 100)
        
        return result_df[['student_id', 'name', 'academic_score', 'cocurricular_score', 'discipline_score'] + 
                         [col for col in result_df.columns if col not in ['student_id', 'name', 'academic_score', 
                                                                         'cocurricular_score', 'discipline_score']]]
    
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
        # If value is already numeric, return it
        if pd.notnull(cca_value) and (isinstance(cca_value, (int, float)) or (isinstance(cca_value, str) and cca_value.replace('.', '', 1).isdigit())):
            try:
                return float(cca_value)
            except:
                pass
        
        # If value is not a string, return default
        if not isinstance(cca_value, str) or pd.isnull(cca_value):
            return 70.0  # Default score
        
        # Convert to uppercase for mapping
        cca_value = cca_value.upper().strip()
        
        # If exactly matching a category, return its score
        if cca_value in self.cca_mapping:
            return float(self.cca_mapping[cca_value])
        
        # If comma-separated list, split and average the scores
        if ',' in cca_value:
            categories = [cat.strip() for cat in cca_value.split(',')]
            scores = []
            
            for cat in categories:
                # Try to find a close match in our mapping
                for key in self.cca_mapping:
                    if key in cat or cat in key:
                        scores.append(self.cca_mapping[key])
                        break
                else:
                    # If no match found, use default score
                    scores.append(70)
            
            # Return average score if we have any, otherwise default
            return float(sum(scores) / len(scores)) if scores else 70.0
        
        # Try to match with a substring
        for key in self.cca_mapping:
            if key in cca_value or cca_value in key:
                return float(self.cca_mapping[key])
        
        # Default score if no match found
        return 70.0
    
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
        # If value is already numeric, return it
        if pd.notnull(behavior_value) and (isinstance(behavior_value, (int, float)) or (isinstance(behavior_value, str) and behavior_value.replace('.', '', 1).isdigit())):
            try:
                return float(behavior_value)
            except:
                pass
        
        # If value is not a string or null, return default
        if not isinstance(behavior_value, str) or pd.isnull(behavior_value):
            return 70.0  # Default score
        
        # Convert to uppercase for mapping
        behavior_value = behavior_value.upper().strip()
        
        # If exactly matching a category, return its score
        if behavior_value in self.behavior_mapping:
            return float(self.behavior_mapping[behavior_value])
        
        # Default score if no match found
        return 70.0