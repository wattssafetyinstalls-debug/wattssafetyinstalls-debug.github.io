import time
import requests

def test_performance():
    test_urls = [
        "http://localhost:8000",
        "http://localhost:8000/services.html",
        "http://localhost:8000/services/ada-compliant-showers.html"
    ]
    
    print("WEBSITE PERFORMANCE TEST")
    print("=" * 50)
    
    for url in test_urls:
        print(f"\nTesting: {url}")
        print("-" * 30)
        
        try:
            start_time = time.time()
            response = requests.get(url)
            load_time = time.time() - start_time
            
            if response.status_code == 200:
                size_kb = len(response.content) / 1024
                
                print(f"Load Time: {load_time:.2f} seconds")
                print(f"Page Size: {size_kb:.1f} KB")
                print(f"Status: {response.status_code}")
                
                if load_time < 2:
                    print("PERFORMANCE: EXCELLENT")
                elif load_time < 4:
                    print("PERFORMANCE: GOOD")
                else:
                    print("PERFORMANCE: SLOW - Needs optimization")
            else:
                print(f"ERROR: Status code {response.status_code}")
                
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_performance()