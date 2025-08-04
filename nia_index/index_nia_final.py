#!/usr/bin/env python3
"""
Final script to index the LV repository in NIA using the correct v2 API
"""

import requests
import json

# NIA API configuration from your MCP setup
NIA_API_KEY = "nk_TUZCa0eZA0IvWb0E1DBUsUThMiw8IG3G"
NIA_API_URL = "https://apigcp.trynia.ai/"

# GitHub repository details
GITHUB_REPO = "MAKaminski/LV"

def index_repository():
    """Index the GitHub repository in NIA using the v2 API"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the indexing request using the correct v2 API format
    payload = {
        "repository": GITHUB_REPO,
        "branch": "main"  # Optional, defaults to repository's default branch
    }
    
    try:
        print(f"🚀 Indexing repository: {GITHUB_REPO}")
        print(f"📡 Using endpoint: {NIA_API_URL}/v2/repositories")
        
        # Make the API call to index the repository
        response = requests.post(
            f"{NIA_API_URL}/v2/repositories",
            headers=headers,
            json=payload
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Successfully initiated indexing!")
            print(f"📋 Response: {response.text}")
            
            # Try to get the repository ID from the response
            try:
                response_data = response.json()
                if 'id' in response_data:
                    repository_id = response_data['id']
                    print(f"🆔 Repository ID: {repository_id}")
                    
                    # Check the status
                    check_repository_status(repository_id)
                    
            except json.JSONDecodeError:
                print("⚠️  Could not parse response JSON")
                
        else:
            print(f"❌ Failed to index repository. Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error indexing repository: {str(e)}")

def check_repository_status(repository_id):
    """Check the status of a repository"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"\n📊 Checking status for repository ID: {repository_id}")
        
        response = requests.get(
            f"{NIA_API_URL}/v2/repositories/{repository_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status: {status_data.get('status', 'Unknown')}")
            print(f"📁 Repository: {status_data.get('repository', 'Unknown')}")
            print(f"🌿 Branch: {status_data.get('branch', 'Unknown')}")
            
            if 'progress' in status_data:
                print(f"📈 Progress: {status_data['progress']}")
                
            if 'error' in status_data and status_data['error']:
                print(f"❌ Error: {status_data['error']}")
                
        else:
            print(f"❌ Failed to get status. Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking status: {str(e)}")

def list_repositories():
    """List all repositories in NIA"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("\n📋 Listing all repositories in NIA...")
        
        response = requests.get(
            f"{NIA_API_URL}/v2/repositories",
            headers=headers
        )
        
        if response.status_code == 200:
            repositories = response.json()
            print(f"✅ Found {len(repositories)} repositories:")
            
            for repo in repositories:
                print(f"  - {repo.get('repository', 'Unknown')}: {repo.get('status', 'Unknown')}")
                
        else:
            print(f"❌ Failed to list repositories. Status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error listing repositories: {str(e)}")

if __name__ == "__main__":
    print("🔧 NIA Repository Indexing Tool (v2 API)")
    print("=" * 50)
    
    # Index the repository
    index_repository()
    
    print("\n" + "=" * 50 + "\n")
    
    # List all repositories
    list_repositories()
    
    print("\n" + "=" * 50)
    print("🎉 Indexing process completed!")
    print("💡 You can now use NIA to query your repository.") 