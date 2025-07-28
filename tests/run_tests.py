#!/usr/bin/env python3
"""
Gaia AI Test Runner
Organized test execution for the modular Gaia system
"""

import sys
import os
from pathlib import Path
import importlib.util
import traceback

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class TestRunner:
    """Test runner for Gaia AI modules"""
    
    def __init__(self):
        self.tests_dir = Path(__file__).parent
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def run_all_tests(self):
        """Run all tests in all categories"""
        print("🧪 Running Gaia AI Test Suite")
        print("=" * 50)
        
        # Test categories
        categories = [
            ("Core Tests", "core"),
            ("LLM Tests", "llm"), 
            ("Hotel Tests", "hotel"),
            ("Interface Tests", "interfaces"),
            ("Architecture Tests", "architecture")
        ]
        
        for category_name, category_dir in categories:
            print(f"\n📂 {category_name}")
            print("-" * 30)
            self.run_category_tests(category_dir)
        
        self.print_summary()
    
    def run_category_tests(self, category):
        """Run tests in a specific category"""
        category_path = self.tests_dir / category
        
        if not category_path.exists():
            print(f"⚠️  Category {category} not found")
            return
        
        test_files = list(category_path.glob("test_*.py"))
        
        if not test_files:
            print(f"📝 No test files found in {category}")
            return
        
        for test_file in test_files:
            self.run_test_file(test_file)
    
    def run_test_file(self, test_file):
        """Run a single test file"""
        test_name = test_file.stem
        
        try:
            # Import the test module
            spec = importlib.util.spec_from_file_location(test_name, test_file)
            if spec is None or spec.loader is None:
                print(f"⚠️  Could not load {test_name}")
                return
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for test functions or main function
            test_functions = [func for func in dir(module) if func.startswith('test_')]
            
            if hasattr(module, 'main'):
                print(f"🔄 Running {test_name}...")
                module.main()
                print(f"✅ {test_name} completed")
                self.passed += 1
            elif test_functions:
                for func_name in test_functions:
                    print(f"🔄 Running {test_name}.{func_name}...")
                    func = getattr(module, func_name)
                    func()
                    print(f"✅ {test_name}.{func_name} passed")
                    self.passed += 1
            else:
                print(f"⚠️  No test functions found in {test_name}")
                
        except Exception as e:
            print(f"❌ {test_name} failed: {str(e)}")
            self.failed += 1
            self.errors.append((test_name, str(e), traceback.format_exc()))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📈 Total: {self.passed + self.failed}")
        
        if self.errors:
            print("\n🐛 Error Details:")
            for test_name, error, traceback_str in self.errors:
                print(f"\n❌ {test_name}:")
                print(f"   Error: {error}")
                if "--verbose" in sys.argv:
                    print(f"   Traceback:\n{traceback_str}")
        
        success_rate = (self.passed / (self.passed + self.failed) * 100) if (self.passed + self.failed) > 0 else 0
        print(f"\n🎯 Success Rate: {success_rate:.1f}%")


def main():
    """Main test runner entry point"""
    runner = TestRunner()
    
    if len(sys.argv) > 1:
        # Run specific category
        category = sys.argv[1]
        if category in ["core", "llm", "hotel", "interfaces", "architecture"]:
            print(f"🧪 Running {category.title()} Tests")
            print("=" * 50)
            runner.run_category_tests(category)
            runner.print_summary()
        else:
            print(f"❌ Unknown test category: {category}")
            print("Available categories: core, llm, hotel, interfaces, architecture")
    else:
        # Run all tests
        runner.run_all_tests()


if __name__ == "__main__":
    main()
