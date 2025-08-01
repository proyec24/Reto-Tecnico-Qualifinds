#!/usr/bin/env python3
"""
Test runner script for the Chuck Norris API Backend Challenge

This script provides an easy way to run the test suite with different options.
"""

import sys
import subprocess
import argparse
import os

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print('='*60)
    
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"\n❌ Command not found: {command[0]}")
        print("Please install the required dependencies:")
        print("pip install -r requirements-test.txt")
        return False

def main():
    parser = argparse.ArgumentParser(description='Run tests for Chuck Norris API Backend Challenge')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--categories', action='store_true', help='Run categories endpoint tests')
    parser.add_argument('--joke', action='store_true', help='Run joke endpoint tests')
    parser.add_argument('--bonus', action='store_true', help='Run bonus feature tests')
    parser.add_argument('--requirements', action='store_true', help='Run requirements verification tests')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--install-deps', action='store_true', help='Install test dependencies')
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        print("Installing test dependencies...")
        if not run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-test.txt'], 
                          "Installing test dependencies"):
            return 1
    
    # Build command based on arguments
    cmd = [sys.executable, '-m', 'pytest']
    
    if args.verbose:
        cmd.append('-v')
    
    if args.coverage:
        cmd.extend(['--cov=app', '--cov-report=term-missing', '--cov-report=html'])
    
    if args.unit:
        cmd.append('-m unit')
    elif args.integration:
        cmd.append('-m integration')
    elif args.categories:
        cmd.append('tests/test_categories_endpoint.py')
    elif args.joke:
        cmd.append('tests/test_joke_endpoint.py')
    elif args.bonus:
        cmd.append('tests/test_bonus_endpoints.py')
    elif args.requirements:
        cmd.append('tests/test_requirements.py')
    elif not args.all:
        # Default: run all tests
        cmd.append('tests/')
    else:
        cmd.append('tests/')
    
    # Run the tests
    success = run_command(cmd, "Test Suite")
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n💥 Some tests failed. Please check the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 