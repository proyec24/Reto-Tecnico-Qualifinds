#!/usr/bin/env python3
"""
Challenge Timer and Test Runner

This script measures the time it takes to complete the Chuck Norris API challenge
and provides real-time feedback on progress.
"""

import time
import subprocess
import sys
import os
import json
from datetime import datetime, timedelta

class ChallengeTimer:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.results = {}
        
    def start(self):
        """Start the challenge timer"""
        self.start_time = time.time()
        print("🎯 Chuck Norris API Challenge Started!")
        print("⏱️  Timer is now running...")
        print("📋 Complete the required endpoints:")
        print("   - GET /categories")
        print("   - GET /joke/{category}")
        print("")
        
    def stop(self):
        """Stop the challenge timer"""
        if self.start_time is None:
            print("❌ Timer was never started!")
            return
            
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        print(f"\n⏱️  Challenge completed in {duration:.1f} seconds ({duration/60:.1f} minutes)")
        
        # Save results
        self.results = {
            "start_time": datetime.fromtimestamp(self.start_time).isoformat(),
            "end_time": datetime.fromtimestamp(self.end_time).isoformat(),
            "duration_seconds": duration,
            "duration_minutes": duration / 60
        }
        
        # Save to file
        with open("challenge_results.json", "w") as f:
            json.dump(self.results, f, indent=2)
            
        return duration
        
    def run_minimal_tests(self):
        """Run the minimal required tests"""
        print("\n🧪 Running minimal required tests...")
        
        try:
            # Run categories test
            result1 = subprocess.run([
                sys.executable, "-m", "pytest", 
                "tests/test_categories_endpoint.py::TestCategoriesEndpoint::test_get_categories_success",
                "-v", "--tb=no"
            ], capture_output=True, text=True)
            
            # Run joke test
            result2 = subprocess.run([
                sys.executable, "-m", "pytest",
                "tests/test_joke_endpoint.py::TestJokeEndpoint::test_get_joke_success",
                "-v", "--tb=no"
            ], capture_output=True, text=True)
            
            categories_passed = result1.returncode == 0
            joke_passed = result2.returncode == 0
            
            print(f"📋 Categories endpoint: {'✅ PASSED' if categories_passed else '❌ FAILED'}")
            print(f"📋 Joke endpoint: {'✅ PASSED' if joke_passed else '❌ FAILED'}")
            
            if categories_passed and joke_passed:
                print("🎉 CONGRATULATIONS! You've completed the minimal requirements!")
                return True
            else:
                print("⚠️  Keep working on the required endpoints...")
                return False
                
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False
            
    def run_full_tests(self):
        """Run the full test suite"""
        print("\n🧪 Running full test suite...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest", "tests/",
                "-v", "--tb=short"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("🎉 EXCELLENT! All tests passed including bonus features!")
                return True
            else:
                print("⚠️  Some tests failed. Check the output above.")
                return False
                
        except Exception as e:
            print(f"❌ Error running full tests: {e}")
            return False
            
    def generate_report(self):
        """Generate a completion report"""
        if not self.results:
            print("❌ No results available. Run the challenge first.")
            return
            
        duration = self.results["duration_seconds"]
        minutes = self.results["duration_minutes"]
        
        print("\n" + "="*60)
        print("🎯 CHALLENGE COMPLETION REPORT")
        print("="*60)
        print(f"⏱️  Total Time: {duration:.1f} seconds ({minutes:.1f} minutes)")
        print(f"📅 Started: {self.results['start_time']}")
        print(f"📅 Finished: {self.results['end_time']}")
        
        # Performance evaluation
        if minutes < 10:
            performance = "🚀 EXCELLENT - Very fast completion!"
        elif minutes < 20:
            performance = "✅ GOOD - Reasonable completion time"
        elif minutes < 30:
            performance = "⚠️  SLOW - Could be faster"
        else:
            performance = "🐌 VERY SLOW - Consider optimizing your approach"
            
        print(f"📊 Performance: {performance}")
        
        # Save detailed report
        report = {
            "challenge_results": self.results,
            "performance_evaluation": performance,
            "timestamp": datetime.now().isoformat()
        }
        
        with open("challenge_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        print(f"\n📄 Detailed report saved to: challenge_report.json")
        print("="*60)

def main():
    """Main function to run the challenge timer"""
    timer = ChallengeTimer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            timer.start()
            
        elif command == "test":
            timer.run_minimal_tests()
            
        elif command == "full":
            timer.run_full_tests()
            
        elif command == "stop":
            duration = timer.stop()
            if duration:
                timer.run_minimal_tests()
                timer.generate_report()
                
        elif command == "report":
            timer.generate_report()
            
        else:
            print("Usage: python challenge_timer.py [start|test|full|stop|report]")
            
    else:
        # Interactive mode
        print("🎯 Chuck Norris API Challenge Timer")
        print("="*40)
        print("Commands:")
        print("  start  - Start the timer")
        print("  test   - Run minimal tests")
        print("  full   - Run full test suite")
        print("  stop   - Stop timer and generate report")
        print("  report - Generate completion report")
        print("")
        
        while True:
            try:
                command = input("Enter command (or 'quit' to exit): ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "start":
                    timer.start()
                elif command == "test":
                    timer.run_minimal_tests()
                elif command == "full":
                    timer.run_full_tests()
                elif command == "stop":
                    duration = timer.stop()
                    if duration:
                        timer.run_minimal_tests()
                        timer.generate_report()
                elif command == "report":
                    timer.generate_report()
                else:
                    print("❌ Unknown command. Try: start, test, full, stop, report, or quit")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 