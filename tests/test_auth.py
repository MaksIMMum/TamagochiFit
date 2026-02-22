import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_register():
    """Test user registration"""
    print("1️⃣ Testing Registration...")

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!",
        "full_name": "Test User"
    }

    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.json() if response.status_code == 201 else None

def test_login():
    """Test user login"""
    print("\n2️⃣ Testing Login...")

    login_data = {
        "username": "testuser",
        "password": "SecurePass123!"
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Status: {response.status_code}")
    response_json = response.json()
    print(f"Response: {json.dumps(response_json, indent=2)}")

    return response_json.get("access_token") if response.status_code == 200 else None

def test_get_current_user(token):
    """Test getting current user info"""
    print("\n3️⃣ Testing Get Current User...")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

def test_with_invalid_token():
    """Test with invalid token"""
    print("\n4️⃣ Testing Invalid Token...")

    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("🚀 Starting Authentication Tests\n")

    # Register
    test_register()

    # Login
    token = test_login()

    if token:
        # Get current user
        test_get_current_user(token)

    # Invalid token
    test_with_invalid_token()

    print("\n✅ Tests Complete!")
