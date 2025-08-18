#!/usr/bin/env python3
"""
Master Test Runner for All Application Features
Runs comprehensive tests for backend, frontend, and integration
"""

import subprocess
import sys
import os
import time
import json
from pathlib import Path

class MasterTestRunner:
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        
        self.test_results[test_name] = {
            "success": success,
            "details": details,
            "timestamp": time.time()
        }
    
    def check_server_status(self, url: str, name: str) -> bool:
        """Check if a server is running"""
        try:
            import requests
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.log_test(f"{name} Server Status", True, f"Server is running at {url}")
                return True
            else:
                self.log_test(f"{name} Server Status", False, f"Server responded with status {response.status_code}")
                return False
        except Exception as e:
            self.log_test(f"{name} Server Status", False, f"Server not accessible: {str(e)}")
            return False
    
    def run_backend_tests(self):
        """Run backend tests"""
        print("\n🔧 Running Backend Tests")
        print("=" * 50)
        
        try:
            # Check if backend server is running
            if not self.check_server_status("http://localhost:8000/health", "Backend"):
                print("❌ Backend server is not running. Please start it first:")
                print("   cd adobev4")
                print("   python main.py")
                return False
            
            # Run backend tests
            result = subprocess.run([
                sys.executable, "test_all_features.py"
            ], capture_output=True, text=True, cwd="adobev4")
            
            if result.returncode == 0:
                self.log_test("Backend Test Suite", True, "All backend tests completed successfully")
                print(result.stdout)
                return True
            else:
                self.log_test("Backend Test Suite", False, f"Backend tests failed: {result.stderr}")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            self.log_test("Backend Test Suite", False, f"Error running backend tests: {str(e)}")
            return False
    
    def run_frontend_tests(self):
        """Run frontend tests"""
        print("\n🌐 Running Frontend Tests")
        print("=" * 50)
        
        try:
            # Check if frontend server is running
            if not self.check_server_status("http://localhost:5173", "Frontend"):
                print("❌ Frontend server is not running. Please start it first:")
                print("   cd HARSHALADOBE")
                print("   npm run dev")
                return False
            
            # Run frontend tests
            result = subprocess.run([
                sys.executable, "test_frontend_features.py"
            ], capture_output=True, text=True, cwd="adobev4")
            
            if result.returncode == 0:
                self.log_test("Frontend Test Suite", True, "All frontend tests completed successfully")
                print(result.stdout)
                return True
            else:
                self.log_test("Frontend Test Suite", False, f"Frontend tests failed: {result.stderr}")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            self.log_test("Frontend Test Suite", False, f"Error running frontend tests: {str(e)}")
            return False
    
    def run_integration_tests(self):
        """Run integration tests"""
        print("\n🔗 Running Integration Tests")
        print("=" * 50)
        
        try:
            # Check if both servers are running
            backend_ok = self.check_server_status("http://localhost:8000/health", "Backend")
            frontend_ok = self.check_server_status("http://localhost:5173", "Frontend")
            
            if not backend_ok or not frontend_ok:
                self.log_test("Integration Test Suite", False, "Both servers must be running for integration tests")
                return False
            
            # Run integration tests
            result = subprocess.run([
                sys.executable, "test_frontend_integration.py"
            ], capture_output=True, text=True, cwd="adobev4")
            
            if result.returncode == 0:
                self.log_test("Integration Test Suite", True, "All integration tests completed successfully")
                print(result.stdout)
                return True
            else:
                self.log_test("Integration Test Suite", False, f"Integration tests failed: {result.stderr}")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            self.log_test("Integration Test Suite", False, f"Error running integration tests: {str(e)}")
            return False
    
    def run_related_sections_tests(self):
        """Run enhanced related sections tests"""
        print("\n🔗 Running Enhanced Related Sections Tests")
        print("=" * 50)
        
        try:
            # Check if backend server is running
            if not self.check_server_status("http://localhost:8000/health", "Backend"):
                self.log_test("Related Sections Test Suite", False, "Backend server not running")
                return False
            
            # Run related sections tests
            result = subprocess.run([
                sys.executable, "test_related_sections.py"
            ], capture_output=True, text=True, cwd="adobev4")
            
            if result.returncode == 0:
                self.log_test("Related Sections Test Suite", True, "Enhanced related sections tests completed successfully")
                print(result.stdout)
                return True
            else:
                self.log_test("Related Sections Test Suite", False, f"Related sections tests failed: {result.stderr}")
                print(result.stdout)
                print(result.stderr)
                return False
                
        except Exception as e:
            self.log_test("Related Sections Test Suite", False, f"Error running related sections tests: {str(e)}")
            return False
    
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("\n📦 Checking Dependencies")
        print("=" * 50)
        
        required_packages = [
            "requests",
            "fastapi",
            "uvicorn",
            "sentence-transformers",
            "faiss-cpu",
            "google-generativeai"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                self.log_test(f"Package: {package}", True, "Installed")
            except ImportError:
                missing_packages.append(package)
                self.log_test(f"Package: {package}", False, "Not installed")
        
        if missing_packages:
            print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
            print("Please install missing packages:")
            print(f"   pip install {' '.join(missing_packages)}")
            return False
        
        return True
    
    def check_environment(self):
        """Check environment setup"""
        print("\n🔧 Checking Environment")
        print("=" * 50)
        
        # Check if we're in the right directory
        if not os.path.exists("adobev4"):
            self.log_test("Directory Structure", False, "adobev4 directory not found")
            return False
        
        if not os.path.exists("HARSHALADOBE"):
            self.log_test("Directory Structure", False, "HARSHALADOBE directory not found")
            return False
        
        self.log_test("Directory Structure", True, "Both adobev4 and HARSHALADOBE directories found")
        
        # Check if test files exist
        test_files = [
            "adobev4/test_all_features.py",
            "adobev4/test_frontend_features.py",
            "adobev4/test_frontend_integration.py",
            "adobev4/test_related_sections.py"
        ]
        
        for test_file in test_files:
            if os.path.exists(test_file):
                self.log_test(f"Test File: {test_file}", True, "Found")
            else:
                self.log_test(f"Test File: {test_file}", False, "Not found")
                return False
        
        return True
    
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print("\n📊 Generating Test Report")
        print("=" * 50)
        
        end_time = time.time()
        total_time = end_time - self.start_time
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = total_tests - passed_tests
        
        # Create report
        report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_duration_seconds": total_time,
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            "test_results": self.test_results,
            "recommendations": []
        }
        
        # Add recommendations based on test results
        if failed_tests > 0:
            report["recommendations"].append("Fix failed tests before deployment")
        
        if not any("Backend" in key and result["success"] for key, result in self.test_results.items()):
            report["recommendations"].append("Backend server needs to be started")
        
        if not any("Frontend" in key and result["success"] for key, result in self.test_results.items()):
            report["recommendations"].append("Frontend server needs to be started")
        
        # Save report
        report_file = f"test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log_test("Test Report Generation", True, f"Report saved to {report_file}")
        
        return report
    
    def print_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        
        end_time = time.time()
        total_time = end_time - self.start_time
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"⏱️  Total Test Duration: {total_time:.2f} seconds")
        print(f"📊 Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"📈 Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Group tests by category
        categories = {
            "Environment": [],
            "Backend": [],
            "Frontend": [],
            "Integration": [],
            "Related Sections": []
        }
        
        for test_name, result in self.test_results.items():
            if "Environment" in test_name or "Directory" in test_name or "Package" in test_name:
                categories["Environment"].append((test_name, result))
            elif "Backend" in test_name:
                categories["Backend"].append((test_name, result))
            elif "Frontend" in test_name:
                categories["Frontend"].append((test_name, result))
            elif "Integration" in test_name:
                categories["Integration"].append((test_name, result))
            elif "Related Sections" in test_name:
                categories["Related Sections"].append((test_name, result))
            else:
                categories["Backend"].append((test_name, result))
        
        # Print results by category
        for category, tests in categories.items():
            if tests:
                print(f"\n🎯 {category} Tests:")
                passed = sum(1 for _, result in tests if result["success"])
                failed = len(tests) - passed
                print(f"   ✅ Passed: {passed}, ❌ Failed: {failed}")
                
                if failed > 0:
                    print("   Failed tests:")
                    for test_name, result in tests:
                        if not result["success"]:
                            print(f"     - {test_name}: {result['details']}")
        
        # Print recommendations
        if failed_tests > 0:
            print(f"\n⚠️  {failed_tests} test(s) failed. Recommendations:")
            
            if not any("Backend" in key and result["success"] for key, result in self.test_results.items()):
                print("   • Start backend server: cd adobev4 && python main.py")
            
            if not any("Frontend" in key and result["success"] for key, result in self.test_results.items()):
                print("   • Start frontend server: cd HARSHALADOBE && npm run dev")
            
            if not any("Package" in key and result["success"] for key, result in self.test_results.items()):
                print("   • Install missing packages: pip install -r requirements.txt")
            
            print("   • Check error logs for specific issues")
            print("   • Verify API endpoints are working")
            print("   • Test manual user interactions")
        else:
            print("\n🎉 All tests passed! The application is ready for use.")
        
        print(f"\n📄 Detailed report saved to: test_report_{int(time.time())}.json")
    
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Comprehensive Application Test Suite")
        print("=" * 80)
        print("This will test all features including:")
        print("   • Environment setup and dependencies")
        print("   • Backend API functionality")
        print("   • Frontend connectivity and features")
        print("   • Integration between frontend and backend")
        print("   • Enhanced related sections functionality")
        print("=" * 80)
        
        # Check environment first
        if not self.check_environment():
            print("\n❌ Environment check failed. Please fix issues before running tests.")
            return
        
        if not self.check_dependencies():
            print("\n❌ Dependency check failed. Please install missing packages.")
            return
        
        # Run all test suites
        test_suites = [
            ("Backend Tests", self.run_backend_tests),
            ("Frontend Tests", self.run_frontend_tests),
            ("Integration Tests", self.run_integration_tests),
            ("Enhanced Related Sections Tests", self.run_related_sections_tests)
        ]
        
        for suite_name, test_function in test_suites:
            try:
                test_function()
                time.sleep(2)  # Brief pause between test suites
            except Exception as e:
                self.log_test(suite_name, False, f"Test suite failed with exception: {str(e)}")
        
        # Generate report and summary
        self.generate_test_report()
        self.print_summary()

def main():
    """Main function"""
    runner = MasterTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()
