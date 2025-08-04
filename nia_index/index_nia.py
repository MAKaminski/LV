#!/usr/bin/env python3
"""
Script to index the LV repository in NIA
"""

import os
import requests
import json

# NIA API configuration from your MCP setup
NIA_API_KEY = "nk_TUZCa0eZA0IvWb0E1DBUsUThMiw8IG3G"
NIA_API_URL = "https://apigcp.trynia.ai/"

# GitHub repository details
GITHUB_REPO = "MAKaminski/LV"
GITHUB_URL = f"https://github.com/{GITHUB_REPO}"

def index_repository():
    """Index the GitHub repository in NIA"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Prepare the indexing request
    payload = {
        "repository_url": GITHUB_URL,
        "repository_name": "LV",
        "description": "LV Project repository",
        "index_type": "github"
    }
    
    try:
        # Make the API call to index the repository
        response = requests.post(
            f"{NIA_API_URL}/index",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully indexed repository: {GITHUB_URL}")
            print(f"Index ID: {response.json().get('index_id', 'N/A')}")
        else:
            print(f"❌ Failed to index repository. Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error indexing repository: {str(e)}")

def check_index_status():
    """Check the status of indexed repositories"""
    
    headers = {
        "Authorization": f"Bearer {NIA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            f"{NIA_API_URL}/indices",
            headers=headers
        )
        
        if response.status_code == 200:
            indices = response.json()
            print(f"📋 Current indices in NIA:")
            for index in indices:
                print(f"  - {index.get('name', 'Unknown')}: {index.get('status', 'Unknown')}")
        else:
            print(f"❌ Failed to get indices. Status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking indices: {str(e)}")

if __name__ == "__main__":
    print(f"🚀 Indexing repository: {GITHUB_URL}")
    index_repository()
    
    print("\n" + "="*50 + "\n")
    
    print("📊 Checking current indices...")
    check_index_status() 