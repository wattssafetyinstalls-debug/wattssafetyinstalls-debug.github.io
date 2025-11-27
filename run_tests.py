import subprocess
import time
import sys

def run_tests():
    print("WEBSITE TESTING ENVIRONMENT")
    print("=" * 60)
    print("Make sure the test server is running first!")
    print("Run this in a separate terminal: python test_server.py")
    print("=" * 60)
    
    input("Press Enter to start tests...")
    
    tests = [
        ("Performance Test", "python performance_tester.py"),
        ("Website Validator", "python website_validator.py")
    ]
    
    for test_name, command in tests:
        print(f"\n{test_name}")
        print("=" * 40)
        try:
            subprocess.run(command, shell=True)
            print(f"\n{test_name} COMPLETED")
        except Exception as e:
            print(f"\n{test_name} FAILED: {e}")
        
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED")

if __name__ == "__main__":
    run_tests()