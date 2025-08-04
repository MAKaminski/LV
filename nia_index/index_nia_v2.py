#!/usr/bin/env python3
"""
Improved script to index the LV repository in NIA
"""

import requests
import json

# NIA API configuration from your MCP setup
NIA_API_KEY = "nk_TUZCa0eZA0IvWb0E1DBUsUThMiw8IG3G"
NIA_API_URL = "https://apigcp.trynia.ai/"

# GitHub repository details
GITHUB_REPO = "MAKaminski/LV"
GITHUB_URL = f"https://github.com/{GITHUB_REPO}"

def test_api_endpoints():
    """Test different API endpoints to find the correct ones"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Common API endpoints to test
    endpoints = [
        "/api/v1/index",
        "/api/index",
        "/index",
        "/api/v1/repositories",
        "/api/repositories",
        "/repositories",
        "/api/v1/",
        "/api/",
        "/"
    ]
    
    print("🔍 Testing NIA API endpoints...")
    
    for endpoint in endpoints:
        try:
            url = f"{NIA_API_URL.rstrip('/')}{endpoint}"
            response = requests.get(url, headers=headers, timeout=10)
            print(f"  {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✅ Found working endpoint: {endpoint}")
                return endpoint
                
        except Exception as e:
            print(f"  {endpoint}: Error - {str(e)}")
    
    return None

def index_repository_v2():
    """Try different approaches to index the repository"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try different payload structures
    payloads = [
        {
            "url": GITHUB_URL,
            "name": "LV",
            "type": "github"
        },
        {
            "repository_url": GITHUB_URL,
            "repository_name": "LV",
            "description": "LV Project repository"
        },
        {
            "source": GITHUB_URL,
            "name": "LV"
        }
    ]
    
    # Try different endpoints
    endpoints = [
        "/api/v1/index",
        "/api/index", 
        "/index",
        "/api/v1/repositories",
        "/api/repositories"
    ]
    
    print(f"🚀 Attempting to index repository: {GITHUB_URL}")
    
    for endpoint in endpoints:
        for i, payload in enumerate(payloads):
            try:
                url = f"{NIA_API_URL.rstrip('/')}{endpoint}"
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                
                print(f"  Trying {endpoint} with payload {i+1}: {response.status_code}")
                
                if response.status_code in [200, 201, 202]:
                    print(f"    ✅ Success! Response: {response.text}")
                    return True
                elif response.status_code == 404:
                    print(f"    ❌ Endpoint not found")
                else:
                    print(f"    ⚠️  Status {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"    ❌ Error: {str(e)}")
    
    return False

def check_api_documentation():
    """Try to get API documentation or info"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Try common documentation endpoints
    doc_endpoints = [
        "/docs",
        "/api/docs", 
        "/swagger",
        "/api/swagger",
        "/openapi.json",
        "/api/openapi.json"
    ]
    
    print("📚 Checking for API documentation...")
    
    for endpoint in doc_endpoints:
        try:
            url = f"{NIA_API_URL.rstrip('/')}{endpoint}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"  ✅ Found documentation at: {endpoint}")
                return url
                
        except Exception as e:
            print(f"  ❌ {endpoint}: {str(e)}")
    
    return None

if __name__ == "__main__":
    print("🔧 NIA Repository Indexing Tool")
    print("=" * 50)
    
    # Test API endpoints
    working_endpoint = test_api_endpoints()
    
    print("\n" + "=" * 50 + "\n")
    
    # Try to index the repository
    success = index_repository_v2()
    
    print("\n" + "=" * 50 + "\n")
    
    # Check for documentation
    doc_url = check_api_documentation()
    
    if doc_url:
        print(f"📖 API Documentation available at: {doc_url}")
    
    if not success:
        print("\n❌ Could not index repository automatically.")
        print("💡 You may need to:")
        print("   1. Check the NIA API documentation")
        print("   2. Verify your API key is correct")
        print("   3. Contact NIA support for the correct endpoints")
        print("   4. Use the NIA web interface to manually add the repository") 