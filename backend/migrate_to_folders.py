#!/usr/bin/env python3
"""
Migration script to organize existing course files into topic folders.
This script analyzes existing markdown files in the course_content directory
and organizes them into topic-based folders.
"""

import os
import re
import shutil
from pathlib import Path
import argparse

def sanitize_folder_name(name: str) -> str:
    """Convert a topic name to a valid folder name"""
    # Replace spaces and special characters with underscores
    sanitized = re.sub(r'[^\w\s-]', '', name.lower())
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    return sanitized

def organize_courses_into_folders(dry_run=False):
    """Organize existing courses into topic folders based on filename patterns"""
    course_dir = Path("course_content")
    
    if not course_dir.exists():
        print(f"Error: Course directory '{course_dir}' not found")
        return {"status": "error", "message": "Course directory not found"}
    
    print(f"Scanning directory: {course_dir}")
    
    # Find all markdown files in the root directory
    md_files = list(course_dir.glob("*.md"))
    print(f"Found {len(md_files)} markdown files in root directory")
    
    # Group files by topic
    topic_groups = {}
    for md_file in md_files:
        # Extract topic from filename (e.g., "matlab" from "02_matlab_module_2.md")
        match = re.search(r'(\d+)_([a-zA-Z0-9_]+)_', md_file.name)
        if match:
            topic = match.group(2)
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(md_file)
            print(f"Assigned '{md_file.name}' to topic '{topic}'")
        else:
            # Handle files that don't match the pattern (like introduction_roadmap)
            if "introduction_roadmap" in md_file.name:
                # Try to find which topic it belongs to based on other files
                for topic in topic_groups:
                    if any(f"_{topic}_" in file.name for file in md_files):
                        if topic not in topic_groups:
                            topic_groups[topic] = []
                        topic_groups[topic].append(md_file)
                        print(f"Assigned introduction file '{md_file.name}' to topic '{topic}'")
                        break
                else:
                    # If no match, put in "general" folder
                    if "general" not in topic_groups:
                        topic_groups["general"] = []
                    topic_groups["general"].append(md_file)
                    print(f"Assigned introduction file '{md_file.name}' to 'general' topic")
            elif "expert_roadmap" in md_file.name:
                # Similar logic for expert_roadmap
                for topic in topic_groups:
                    if any(f"_{topic}_" in file.name for file in md_files):
                        if topic not in topic_groups:
                            topic_groups[topic] = []
                        topic_groups[topic].append(md_file)
                        print(f"Assigned expert roadmap file '{md_file.name}' to topic '{topic}'")
                        break
                else:
                    if "general" not in topic_groups:
                        topic_groups["general"] = []
                    topic_groups["general"].append(md_file)
                    print(f"Assigned expert roadmap file '{md_file.name}' to 'general' topic")
            else:
                # For any other files that don't match
                if "general" not in topic_groups:
                    topic_groups["general"] = []
                topic_groups["general"].append(md_file)
                print(f"Assigned '{md_file.name}' to 'general' topic (no pattern match)")
    
    print(f"\nIdentified {len(topic_groups)} topic groups:")
    for topic, files in topic_groups.items():
        print(f"- {topic}: {len(files)} files")
    
    if dry_run:
        print("\nDRY RUN: No files will be moved")
        return {
            "status": "dry_run", 
            "message": f"Would organize {sum(len(files) for files in topic_groups.values())} files into {len(topic_groups)} topic folders",
            "topics": list(topic_groups.keys())
        }
    
    # Move files to their respective topic folders
    print("\nMoving files to topic folders:")
    for topic, files in topic_groups.items():
        topic_dir = course_dir / topic
        topic_dir.mkdir(exist_ok=True)
        print(f"Created/verified folder: {topic_dir}")
        
        for file in files:
            # Only move if the file is in the root directory
            if file.parent == course_dir:
                target_path = topic_dir / file.name
                print(f"Moving '{file.name}' to '{topic}/{file.name}'")
                
                # Copy the file to the topic folder
                shutil.copy2(file, target_path)
                
                # Verify the copy was successful before removing the original
                if target_path.exists() and target_path.stat().st_size == file.stat().st_size:
                    # Keep the original file for now (uncomment to remove)
                    # file.unlink()
                    print(f"  ✓ Successfully copied (original preserved)")
                else:
                    print(f"  ✗ Copy failed or incomplete")
    
    print("\nMigration complete. Original files have been preserved in the root directory.")
    print("Once you verify everything is working correctly, you can manually remove the original files.")
    
    return {
        "status": "success", 
        "message": f"Organized {sum(len(files) for files in topic_groups.values())} files into {len(topic_groups)} topic folders",
        "topics": list(topic_groups.keys())
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize course files into topic folders")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()
    
    result = organize_courses_into_folders(dry_run=args.dry_run)
    
    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to perform the actual migration.")