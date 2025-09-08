"""
Log viewer functionality for admin dashboard.
Provides secure access to application logs.
"""

import os
from datetime import datetime
from flask import current_app
from typing import List, Dict, Optional

def get_log_files() -> List[Dict[str, str]]:
    """
    Get list of available log files.
    
    Returns:
        List[Dict[str, str]]: List of log file information
    """
    log_dir = os.path.join(current_app.root_path, '..', 'logs')
    log_files = []
    
    if os.path.exists(log_dir):
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(log_dir, filename)
                if os.path.isfile(filepath):
                    stat = os.stat(filepath)
                    log_files.append({
                        'name': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime),
                        'path': filepath
                    })
    
    return sorted(log_files, key=lambda x: x['modified'], reverse=True)

def read_log_file(filename: str, lines: int = 100) -> Optional[List[str]]:
    """
    Read the last N lines from a log file.
    
    Args:
        filename (str): Name of the log file
        lines (int): Number of lines to read from the end
        
    Returns:
        Optional[List[str]]: List of log lines or None if file not found
    """
    log_dir = os.path.join(current_app.root_path, '..', 'logs')
    filepath = os.path.join(log_dir, filename)
    
    if not os.path.exists(filepath) or not filename.endswith('.log'):
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            return all_lines[-lines:] if len(all_lines) > lines else all_lines
    except Exception:
        return None

def get_log_statistics() -> Dict[str, int]:
    """
    Get basic statistics about log files.
    
    Returns:
        Dict[str, int]: Statistics about log files
    """
    log_files = get_log_files()
    total_size = sum(f['size'] for f in log_files)
    total_files = len(log_files)
    
    return {
        'total_files': total_files,
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2)
    }
