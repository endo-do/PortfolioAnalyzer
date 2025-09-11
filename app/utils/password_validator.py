# Password validation utilities for Portfolio Analyzer - provides comprehensive password policy enforcement and strength analysis
"""
Password validation utilities for Portfolio Analyzer application.
Provides comprehensive password policy enforcement.
"""

import re
from typing import Tuple, List
from config import PASSWORD_MAX_LENGTH

class PasswordValidator:
    """
    Password validation class with configurable requirements.
    """
    
    def __init__(self):
        # Password policy configuration - no requirements
        self.min_length = 1
        self.max_length = PASSWORD_MAX_LENGTH
        self.require_uppercase = False
        self.require_lowercase = False
        self.require_digits = False
        self.require_special_chars = False
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.forbidden_patterns = []
    
    def validate_password(self, password: str, username: str = None) -> Tuple[bool, List[str]]:
        """
        Validate password against policy requirements.
        
        Args:
            password (str): Password to validate
            username (str): Username to check against password (optional)
            
        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        errors = []
        
        if not password:
            errors.append("Password is required")
            return False, errors
        
        # Length validation
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        if len(password) > self.max_length:
            errors.append(f"Password must be no more than {self.max_length} characters long")
        
        # Character type validation
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        return len(errors) == 0, errors
    
    def _has_sequential_chars(self, password: str) -> bool:
        """Check for sequential characters in password."""
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i]) + 2):
                return True
        return False
    
    def _has_repeated_chars(self, password: str) -> bool:
        """Check for more than 2 consecutive identical characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def get_password_strength(self, password: str) -> Tuple[str, int]:
        """
        Calculate password strength score and description.
        
        Args:
            password (str): Password to analyze
            
        Returns:
            Tuple[str, int]: (strength_description, score_out_of_100)
        """
        if not password:
            return "No password", 0
        
        score = 0
        max_score = 100
        
        # Length score (0-30 points)
        length_score = min(30, len(password) * 2)
        score += length_score
        
        # Character variety score (0-40 points)
        variety_score = 0
        if re.search(r'[a-z]', password):
            variety_score += 10
        if re.search(r'[A-Z]', password):
            variety_score += 10
        if re.search(r'\d', password):
            variety_score += 10
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            variety_score += 10
        score += variety_score
        
        # Complexity score (0-30 points)
        complexity_score = 0
        if len(password) >= 12:
            complexity_score += 10
        if len(set(password)) >= len(password) * 0.7:  # 70% unique characters
            complexity_score += 10
        if not self._has_sequential_chars(password):
            complexity_score += 5
        if not self._has_repeated_chars(password):
            complexity_score += 5
        score += complexity_score
        
        # Determine strength description
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Medium"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return strength, min(score, max_score)

def validate_password_strength(password: str, username: str = None) -> Tuple[bool, List[str], str, int]:
    """
    Convenience function to validate password and get strength information.
    
    Args:
        password (str): Password to validate
        username (str): Username to check against password (optional)
        
    Returns:
        Tuple[bool, List[str], str, int]: (is_valid, errors, strength, score)
    """
    validator = PasswordValidator()
    is_valid, errors = validator.validate_password(password, username)
    strength, score = validator.get_password_strength(password)
    
    return is_valid, errors, strength, score

def generate_password_requirements_text() -> str:
    """
    Generate a user-friendly text describing password requirements.
    
    Returns:
        str: Formatted password requirements text
    """
    validator = PasswordValidator()
    
    requirements = [
        f"• At least {validator.min_length} character long",
        f"• Maximum {validator.max_length} characters"
    ]
    
    return "\n".join(requirements)
