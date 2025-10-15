# tests/run_all_tests.py
"""
Comprehensive Test Runner for AI Agent Starter Pack

This script runs all test suites (functional, performance, integration)
to validate the complete system before Git release.

Author: Arkadiusz Słota
Year: 2025
"""

import sys
import os
import asyncio
import time
from datetime import datetime

# Add project root to path
sys.path.append('.')

# Import test suites
from test_functional_comprehensive import FunctionalTestSuite
from test_performance_comprehensive import PerformanceTestSuite
from test_integration_comprehensive import IntegrationTestSuite

class ComprehensiveTestRunner:
    """Comprehensive test runner for all test suites"""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_suites = []
        self.results = {}
        
    async def run_functional_tests(self):
        """Run functional tests"""
        print("🚀 Running Functional Tests...")
        print("=" * 60)
        
        test_suite = FunctionalTestSuite()
        success = await test_suite.run_all_tests()
        
        self.results["functional"] = {
            "success": success,
            "passed": test_suite.passed_tests,
            "failed": test_suite.failed_tests,
            "total": test_suite.passed_tests + test_suite.failed_tests
        }
        
        return success
    
    async def run_performance_tests(self):
        """Run performance tests"""
        print("\n⚡ Running Performance Tests...")
        print("=" * 60)
        
        test_suite = PerformanceTestSuite()
        success = await test_suite.run_all_tests()
        
        self.results["performance"] = {
            "success": success,
            "metrics": test_suite.performance_metrics
        }
        
        return success
    
    async def run_integration_tests(self):
        """Run integration tests"""
        print("\n🔗 Running Integration Tests...")
        print("=" * 60)
        
        test_suite = IntegrationTestSuite()
        success = await test_suite.run_all_tests()
        
        self.results["integration"] = {
            "success": success,
            "passed": test_suite.passed_tests,
            "failed": test_suite.failed_tests,
            "total": test_suite.passed_tests + test_suite.failed_tests
        }
        
        return success
    
    def print_final_summary(self):
        """Print final test summary"""
        total_time = time.time() - self.start_time
        
        print("\n" + "=" * 80)
        print("🎯 COMPREHENSIVE TEST SUMMARY")
        print("=" * 80)
        print(f"⏱️ Total Execution Time: {total_time:.2f} seconds")
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Functional Tests Summary
        if "functional" in self.results:
            func_result = self.results["functional"]
            status = "✅ PASS" if func_result["success"] else "❌ FAIL"
            print(f"{status} Functional Tests:")
            print(f"   📊 Results: {func_result['passed']}/{func_result['total']} passed")
            print(f"   📈 Success Rate: {(func_result['passed'] / func_result['total']) * 100:.1f}%")
        
        # Performance Tests Summary
        if "performance" in self.results:
            perf_result = self.results["performance"]
            status = "✅ PASS" if perf_result["success"] else "❌ FAIL"
            print(f"{status} Performance Tests:")
            print(f"   📊 Status: {'All performance requirements met' if perf_result['success'] else 'Performance issues detected'}")
            if "metrics" in perf_result:
                print(f"   📈 Metrics: {len(perf_result['metrics'])} performance metrics collected")
        
        # Integration Tests Summary
        if "integration" in self.results:
            int_result = self.results["integration"]
            status = "✅ PASS" if int_result["success"] else "❌ FAIL"
            print(f"{status} Integration Tests:")
            print(f"   📊 Results: {int_result['passed']}/{int_result['total']} passed")
            print(f"   📈 Success Rate: {(int_result['passed'] / int_result['total']) * 100:.1f}%")
        
        print()
        
        # Overall Status
        all_passed = all(result["success"] for result in self.results.values())
        
        if all_passed:
            print("🎉 ALL TEST SUITES PASSED!")
            print("✅ Project is ready for Git release!")
            print("🚀 System meets all requirements:")
            print("   • Functional requirements ✅")
            print("   • Performance requirements ✅")
            print("   • Integration requirements ✅")
            return True
        else:
            print("⚠️ SOME TEST SUITES FAILED!")
            print("❌ Project needs fixes before Git release!")
            print("🔧 Issues detected:")
            for suite_name, result in self.results.items():
                if not result["success"]:
                    print(f"   • {suite_name.title()} tests failed ❌")
            return False
    
    async def run_all_tests(self):
        """Run all test suites"""
        print("🧪 Starting Comprehensive Test Suite for AI Agent Starter Pack")
        print("=" * 80)
        print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"👤 Author: Arkadiusz Słota")
        print(f"📦 Project: AI Agent Starter Pack")
        print("=" * 80)
        
        # Run all test suites
        functional_success = await self.run_functional_tests()
        performance_success = await self.run_performance_tests()
        integration_success = await self.run_integration_tests()
        
        # Print final summary
        overall_success = self.print_final_summary()
        
        return overall_success

async def main():
    """Main test runner"""
    test_runner = ComprehensiveTestRunner()
    success = await test_runner.run_all_tests()
    
    if success:
        print("\n🎯 RECOMMENDATION: Proceed with Git release!")
        return 0
    else:
        print("\n🚫 RECOMMENDATION: Fix issues before Git release!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
