#!/usr/bin/env python3
"""
Test runner script for Portfolio Analyzer tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_tests(test_path=None, verbose=False, coverage=False, parallel=False):
    """Run tests with specified options."""
    
    # Add project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    # Base pytest command
    cmd = ['python', '-m', 'pytest']
    
    # Add test path
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append('tests/')
    
    # Add verbose flag
    if verbose:
        cmd.append('-v')
    
    # Add coverage flag
    if coverage:
        cmd.extend(['--cov=app', '--cov-report=html', '--cov-report=term'])
    
    # Add parallel flag
    if parallel:
        cmd.extend(['-n', 'auto'])
    
    # Add other useful flags
    cmd.extend([
        '--tb=short',  # Short traceback format
        '--strict-markers',  # Strict marker handling
        '--disable-warnings',  # Disable warnings
        '--color=yes'  # Colored output
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=project_root)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Run Portfolio Analyzer tests')
    parser.add_argument('test_path', nargs='?', help='Specific test file or directory to run')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-c', '--coverage', action='store_true', help='Run with coverage')
    parser.add_argument('-p', '--parallel', action='store_true', help='Run tests in parallel')
    parser.add_argument('--auth-only', action='store_true', help='Run only authentication tests')
    parser.add_argument('--portfolio-only', action='store_true', help='Run only portfolio tests')
    parser.add_argument('--admin-only', action='store_true', help='Run only admin tests')
    parser.add_argument('--api-only', action='store_true', help='Run only API tests')
    parser.add_argument('--logging-only', action='store_true', help='Run only logging tests')
    parser.add_argument('--integration-only', action='store_true', help='Run only integration tests')
    parser.add_argument('--validation-only', action='store_true', help='Run only validation tests')
    parser.add_argument('--error-handling-only', action='store_true', help='Run only error handling tests')
    
    args = parser.parse_args()
    
    # Determine test path
    test_path = args.test_path
    
    if args.auth_only:
        test_path = 'tests/unit/test_auth.py'
    elif args.portfolio_only:
        test_path = 'tests/unit/test_portfolio.py'
    elif args.admin_only:
        test_path = 'tests/unit/test_admin.py'
    elif args.api_only:
        test_path = 'tests/unit/test_api.py'
    elif args.logging_only:
        test_path = 'tests/unit/test_logging.py'
    elif args.integration_only:
        test_path = 'tests/unit/test_integration.py'
    elif args.validation_only:
        test_path = 'tests/unit/test_input_validation.py'
    elif args.error_handling_only:
        test_path = 'tests/unit/test_error_handling.py'
    
    # Run tests
    return run_tests(
        test_path=test_path,
        verbose=args.verbose,
        coverage=args.coverage,
        parallel=args.parallel
    )

if __name__ == '__main__':
    sys.exit(main())
