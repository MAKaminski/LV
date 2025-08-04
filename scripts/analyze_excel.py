#!/usr/bin/env python3
"""
Script to analyze the Excel file structure and identify entities for Feature 1
"""

import pandas as pd
import os
from pathlib import Path

def analyze_excel_file(file_path):
    """Analyze the Excel file structure and identify entities"""
    
    print(f"🔍 Analyzing Excel file: {file_path}")
    print("=" * 60)
    
    try:
        # Read all sheets from the Excel file
        excel_file = pd.ExcelFile(file_path)
        
        print(f"📊 Found {len(excel_file.sheet_names)} sheets:")
        for i, sheet_name in enumerate(excel_file.sheet_names, 1):
            print(f"  {i}. {sheet_name}")
        
        print("\n" + "=" * 60)
        
        # Analyze each sheet
        entities = {}
        relationships = []
        
        for sheet_name in excel_file.sheet_names:
            print(f"\n📋 Analyzing sheet: {sheet_name}")
            
            # Read the sheet
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            print(f"  📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"  📝 Columns: {list(df.columns)}")
            
            # Identify potential entities
            entity_name = sheet_name.replace(' ', '_').lower()
            entities[entity_name] = {
                'sheet_name': sheet_name,
                'columns': list(df.columns),
                'row_count': len(df),
                'sample_data': df.head(3).to_dict('records')
            }
            
            # Look for relationships (foreign keys)
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['id', 'code', 'ref', 'brand', 'category', 'supplier']):
                    relationships.append({
                        'entity': entity_name,
                        'column': col,
                        'type': 'potential_foreign_key'
                    })
            
            print(f"  🔗 Potential relationships: {[r['column'] for r in relationships if r['entity'] == entity_name]}")
        
        return entities, relationships
        
    except Exception as e:
        print(f"❌ Error analyzing Excel file: {str(e)}")
        return {}, []

def generate_erd_insights(entities, relationships):
    """Generate ERD insights based on the analysis"""
    
    print("\n" + "=" * 60)
    print("🏗️  ERD Design Insights")
    print("=" * 60)
    
    print("\n📋 Identified Entities:")
    for entity_name, data in entities.items():
        print(f"  • {entity_name} ({data['row_count']} records)")
        print(f"    Columns: {', '.join(data['columns'])}")
    
    print("\n🔗 Potential Relationships:")
    for rel in relationships:
        print(f"  • {rel['entity']}.{rel['column']} → {rel['type']}")
    
    print("\n💡 Recommended Database Schema:")
    print("  Based on the analysis, we should create the following tables:")
    
    # Generate table recommendations
    for entity_name, data in entities.items():
        print(f"\n  📊 Table: {entity_name}")
        print(f"    Primary columns: {', '.join(data['columns'][:5])}")
        if len(data['columns']) > 5:
            print(f"    Additional columns: {', '.join(data['columns'][5:])}")

if __name__ == "__main__":
    file_path = "/Users/makaminski1337/Developer/LV/data/inputs/LaceLuxx Inventory May 26 2025 (2).xlsx"
    
    if os.path.exists(file_path):
        entities, relationships = analyze_excel_file(file_path)
        generate_erd_insights(entities, relationships)
        
        # Save analysis results
        analysis_file = "data/excel_analysis.json"
        os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
        
        import json
        with open(analysis_file, 'w') as f:
            json.dump({
                'entities': entities,
                'relationships': relationships,
                'analysis_date': pd.Timestamp.now().isoformat()
            }, f, indent=2, default=str)
        
        print(f"\n✅ Analysis saved to: {analysis_file}")
        
    else:
        print(f"❌ File not found: {file_path}") 