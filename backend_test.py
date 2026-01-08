import requests
import sys
from datetime import datetime

class TravelAPITester:
    def __init__(self, base_url="https://wanderwise-72.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, expected_count=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, timeout=10)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                
                # Additional validation for expected count
                if expected_count is not None:
                    try:
                        data = response.json()
                        if isinstance(data, list) and len(data) == expected_count:
                            print(f"✅ Count validation passed: {len(data)} items")
                        elif isinstance(data, list):
                            print(f"⚠️  Count mismatch: expected {expected_count}, got {len(data)}")
                            success = False
                        else:
                            print(f"✅ Response data: {type(data)}")
                    except Exception as e:
                        print(f"⚠️  Could not validate count: {e}")
                
                return success, response.json() if success else {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append(f"{name}: Expected {expected_status}, got {response.status_code}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append(f"{name}: {str(e)}")
            return False, {}

    def test_seed_endpoint(self):
        """Test seed endpoint"""
        success, response = self.run_test(
            "Seed Database",
            "POST",
            "seed",
            200
        )
        if success and 'count' in response:
            print(f"✅ Seeded {response['count']} countries")
            return response['count'] == 5
        return False

    def test_get_all_countries(self):
        """Test get all countries"""
        success, response = self.run_test(
            "Get All Countries",
            "GET",
            "countries",
            200,
            expected_count=5
        )
        if success and isinstance(response, list):
            print(f"✅ Retrieved {len(response)} countries")
            # Verify country structure
            for country in response:
                if 'id' in country and 'name' in country and 'places' in country:
                    places_count = len(country['places'])
                    print(f"   - {country['name']}: {places_count} places")
                    if places_count != 5:
                        print(f"⚠️  {country['name']} has {places_count} places, expected 5")
                        return False
                else:
                    print(f"⚠️  Country missing required fields: {country.keys()}")
                    return False
            return True
        return False

    def test_get_country_by_id(self):
        """Test get country by ID"""
        success, response = self.run_test(
            "Get Country by ID (India)",
            "GET",
            "countries/india",
            200
        )
        if success:
            if response.get('id') == 'india' and response.get('name') == 'India':
                places = response.get('places', [])
                print(f"✅ India has {len(places)} places")
                if len(places) == 5:
                    # Check if Taj Mahal is present
                    taj_mahal = next((p for p in places if p['id'] == 'taj-mahal'), None)
                    if taj_mahal:
                        print(f"✅ Found Taj Mahal with price: {taj_mahal.get('price')}")
                        return True
                    else:
                        print("⚠️  Taj Mahal not found in India places")
                        return False
                else:
                    print(f"⚠️  India has {len(places)} places, expected 5")
                    return False
            else:
                print(f"⚠️  Unexpected country data: {response}")
                return False
        return False

    def test_get_all_places(self):
        """Test get all places"""
        success, response = self.run_test(
            "Get All Places",
            "GET",
            "places",
            200,
            expected_count=25
        )
        if success and isinstance(response, list):
            print(f"✅ Retrieved {len(response)} total places")
            # Verify place structure and pricing
            places_with_pricing = 0
            places_with_coordinates = 0
            for place in response:
                if 'price' in place and place['price']:
                    places_with_pricing += 1
                if 'location' in place and 'lat' in place['location'] and 'lng' in place['location']:
                    places_with_coordinates += 1
            
            print(f"✅ Places with pricing: {places_with_pricing}/25")
            print(f"✅ Places with coordinates: {places_with_coordinates}/25")
            
            return len(response) == 25 and places_with_pricing == 25 and places_with_coordinates == 25
        return False

    def test_get_specific_place(self):
        """Test get specific place"""
        success, response = self.run_test(
            "Get Specific Place (Taj Mahal)",
            "GET",
            "places/taj-mahal",
            200
        )
        if success:
            if response.get('id') == 'taj-mahal' and response.get('name') == 'Taj Mahal':
                required_fields = ['price', 'rating', 'location', 'best_time', 'duration']
                missing_fields = [field for field in required_fields if field not in response]
                if not missing_fields:
                    print(f"✅ Taj Mahal has all required fields")
                    print(f"   Price: {response['price']}")
                    print(f"   Rating: {response['rating']}")
                    print(f"   Location: {response['location']}")
                    return True
                else:
                    print(f"⚠️  Taj Mahal missing fields: {missing_fields}")
                    return False
            else:
                print(f"⚠️  Unexpected place data: {response}")
                return False
        return False

    def test_invalid_endpoints(self):
        """Test invalid endpoints return 404"""
        success, _ = self.run_test(
            "Invalid Country ID",
            "GET",
            "countries/invalid",
            404
        )
        
        success2, _ = self.run_test(
            "Invalid Place ID", 
            "GET",
            "places/invalid",
            404
        )
        
        return success and success2

def main():
    print("🚀 Starting Travel Recommendation API Tests")
    print("=" * 50)
    
    # Setup
    tester = TravelAPITester()
    
    # Run tests in sequence
    test_results = []
    
    # 1. Test seed endpoint
    test_results.append(("Seed Database", tester.test_seed_endpoint()))
    
    # 2. Test get all countries
    test_results.append(("Get All Countries", tester.test_get_all_countries()))
    
    # 3. Test get country by ID
    test_results.append(("Get Country by ID", tester.test_get_country_by_id()))
    
    # 4. Test get all places
    test_results.append(("Get All Places", tester.test_get_all_places()))
    
    # 5. Test get specific place
    test_results.append(("Get Specific Place", tester.test_get_specific_place()))
    
    # 6. Test invalid endpoints
    test_results.append(("Invalid Endpoints", tester.test_invalid_endpoints()))
    
    # Print results summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed_tests = sum(1 for _, result in test_results if result)
    total_tests = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\n📈 Overall: {passed_tests}/{total_tests} tests passed")
    print(f"🔧 API Tests: {tester.tests_passed}/{tester.tests_run} individual API calls passed")
    
    if tester.failed_tests:
        print("\n❌ Failed API calls:")
        for failure in tester.failed_tests:
            print(f"   - {failure}")
    
    # Return exit code
    return 0 if passed_tests == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())