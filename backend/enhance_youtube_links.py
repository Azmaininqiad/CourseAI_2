#!/usr/bin/env python3
"""
Script to enhance YouTube links in course content.
This script processes markdown files and converts YouTube links to a format that can be properly rendered.
"""

import os
import re
from pathlib import Path
import argparse

def get_youtube_id(url):
    """Extract YouTube video ID from URL"""
    pattern = r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def enhance_youtube_links(content):
    """Enhance YouTube links in content"""
    # Process markdown YouTube links
    markdown_youtube_regex = r'\[([^\]]+)\]\((https?:\/\/(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})([^\)]*)|https?:\/\/youtu\.be\/([a-zA-Z0-9_-]{11})([^\)]*))\)'
    
    def markdown_replace(match):
        title = match.group(1)
        url = match.group(2)
        video_id = get_youtube_id(url)
        if video_id:
            return f'<div class="youtube-embed" data-title="{title}" data-video-id="{video_id}"></div>'
        return match.group(0)
    
    content = re.sub(markdown_youtube_regex, markdown_replace, content)
    
    # Process raw YouTube URLs
    raw_youtube_regex = r'(https?:\/\/(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})([^\s]*)|https?:\/\/youtu\.be\/([a-zA-Z0-9_-]{11})([^\s]*))'
    
    # Collect all markdown link ranges to avoid processing URLs inside them
    markdown_link_ranges = []
    markdown_link_regex = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(markdown_link_regex, content):
        markdown_link_ranges.append((match.start(), match.end()))
    
    # Process raw YouTube URLs, skipping those in markdown links
    result = []
    last_pos = 0
    
    for match in re.finditer(raw_youtube_regex, content):
        # Check if this URL is inside a markdown link
        is_in_markdown_link = any(
            start <= match.start() <= end for start, end in markdown_link_ranges
        )
        
        if not is_in_markdown_link:
            video_id = get_youtube_id(match.group(0))
            if video_id:
                result.append(content[last_pos:match.start()])
                result.append(f'<div class="youtube-embed" data-title="YouTube Video" data-video-id="{video_id}"></div>')
                last_pos = match.end()
    
    if result:
        result.append(content[last_pos:])
        return ''.join(result)
    
    return content

def process_file(file_path):
    """Process a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove ```markdown prefix and suffix if present
        if content.startswith('```markdown'):
            content = content.replace('```markdown\n', '', 1)
            if content.endswith('```'):
                content = content[:-3]
        
        # Remove any triple backticks at the beginning or end of the content
        content = re.sub(r'^```\s*\n', '', content)
        content = re.sub(r'\n```\s*$', '', content)
        
        # Enhance YouTube links
        enhanced_content = enhance_youtube_links(content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_content)
        
        print(f"Processed {file_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def process_directory(directory):
    """Process all markdown files in a directory and its subdirectories"""
    directory = Path(directory)
    processed = 0
    failed = 0
    
    # Process files in the root directory
    for md_file in directory.glob("*.md"):
        if process_file(md_file):
            processed += 1
        else:
            failed += 1
    
    # Process files in subdirectories
    for folder in [d for d in directory.iterdir() if d.is_dir()]:
        for md_file in folder.glob("*.md"):
            if process_file(md_file):
                processed += 1
            else:
                failed += 1
    
    return processed, failed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhance YouTube links in markdown files")
    parser.add_argument("--directory", default="course_content", help="Directory containing markdown files")
    args = parser.parse_args()
    
    processed, failed = process_directory(args.directory)
    print(f"Processed {processed} files successfully, {failed} files failed")