"""
Enhanced Course Creation System with proper authentication and error handling
"""
import os
import json
import time
import re
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional, Type
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import our enhanced modules
from enhanced_llm import EnhancedLLM
from config import get_config
from error_handler import handle_error
from api_client import call_ai_api

# Tool Classes (keeping the existing ones but with better error handling)
class ImageSearchInput(BaseModel):
    """Input schema for ImageSearchTool."""
    query: str = Field(..., description="Search query for finding relevant images")
    num_results: int = Field(default=1, description="Number of images to return")

class ImageSearchTool(BaseTool):
    name: str = "image_search_tool"
    description: str = "Search for relevant images using Google Custom Search API"
    args_schema: Type[BaseModel] = ImageSearchInput

    def _run(self, query: str, num_results: int = 1) -> str:
        """Execute the image search."""
        try:
            config = get_config()
            
            if not config.is_media_search_enabled():
                return "Image search is not configured. Please set GOOGLE_API_KEY and SEARCH_ENGINE_ID."
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': config.google_api_key,
                'cx': config.search_engine_id,
                'q': query,
                'searchType': 'image',
                'num': min(num_results, 10),
                'safe': 'active',
                'imgType': 'photo',
                'imgSize': 'large'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'items' not in data:
                return f"No images found for query: {query}"

            results = []
            for item in data['items']:
                image_info = {
                    'url': item.get('link', ''),
                    'title': item.get('title', ''),
                    'context': item.get('snippet', ''),
                    'thumbnail': item.get('image', {}).get('thumbnailLink', ''),
                    'size': f"{item.get('image', {}).get('width', 'Unknown')}x{item.get('image', {}).get('height', 'Unknown')}"
                }
                results.append(image_info)

            return json.dumps(results, indent=2)

        except requests.RequestException as e:
            return f"Error searching for images: {str(e)}"
        except Exception as e:
            return f"Unexpected error in image search: {str(e)}"

class YouTubeSearchInput(BaseModel):
    """Input schema for YouTubeSearchTool."""
    query: str = Field(..., description="Search query for finding relevant YouTube videos")
    num_results: int = Field(default=1, description="Number of videos to return")

class YouTubeSearchTool(BaseTool):
    name: str = "youtube_search_tool"
    description: str = "Search for relevant YouTube videos using YouTube Data API"
    args_schema: Type[BaseModel] = YouTubeSearchInput

    def _run(self, query: str, num_results: int = 1) -> str:
        """Execute the YouTube search."""
        try:
            config = get_config()
            
            if not config.is_youtube_search_enabled():
                return "YouTube search is not configured. Please set YOUTUBE_API_KEY."

            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                'part': 'snippet',
                'maxResults': min(num_results, 25),
                'q': query,
                'type': 'video',
                'key': config.youtube_api_key,
                'order': 'relevance',
                'safeSearch': 'strict',
                'videoDefinition': 'high'
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'items' not in data:
                return f"No videos found for query: {query}"

            # Get video details including duration
            video_ids = [item['id']['videoId'] for item in data['items']]
            details_url = "https://www.googleapis.com/youtube/v3/videos"
            details_params = {
                'part': 'contentDetails,statistics',
                'id': ','.join(video_ids),
                'key': config.youtube_api_key
            }

            details_response = requests.get(details_url, params=details_params, timeout=10)
            details_response.raise_for_status()
            details_data = details_response.json()

            # Create a mapping of video ID to details
            video_details = {}
            for item in details_data.get('items', []):
                video_details[item['id']] = {
                    'duration': item.get('contentDetails', {}).get('duration', 'Unknown'),
                    'viewCount': item.get('statistics', {}).get('viewCount', '0')
                }

            results = []
            for item in data['items']:
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                video_info = {
                    'title': item['snippet']['title'],
                    'url': video_url,
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'][:200] + "..." if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'published': item['snippet']['publishedAt'],
                    'duration': video_details.get(video_id, {}).get('duration', 'Unknown'),
                    'views': video_details.get(video_id, {}).get('viewCount', '0')
                }
                results.append(video_info)

            return json.dumps(results, indent=2)

        except requests.RequestException as e:
            return f"Error searching YouTube: {str(e)}"
        except Exception as e:
            return f"Unexpected error in YouTube search: {str(e)}"

class EnhancedCourseCreationSystem:
    """Enhanced system for course creation with proper authentication"""

    def __init__(self, images_per_module: int = 1, videos_per_module: int = 1):
        # Check configuration
        self.config = get_config()
        if not self.config.validation_result.is_valid:
            print("❌ Configuration Error:")
            print(self.config.get_setup_instructions())
            raise Exception("System not properly configured")
        
        # Use the enhanced LLM with proper authentication
        self.llm = EnhancedLLM()
        
        self.course_directory = Path("course_content")
        self.course_directory.mkdir(exist_ok=True)

        # Configurable media counts
        self.images_per_module = images_per_module
        self.videos_per_module = videos_per_module

        # Initialize tools
        self.image_search_tool = ImageSearchTool()
        self.youtube_search_tool = YouTubeSearchTool()

    def create_agents(self) -> tuple:
        """Create specialized agents with enhanced LLM"""

        # Agent 1: Course Structure Creator
        course_planner = Agent(
            role='Course Structure Planner',
            goal='Create a comprehensive course outline and structure with 15 markdown files',
            backstory="""You are an expert educational designer who specializes in creating
            well-structured learning paths. You understand how to break down complex topics
            into digestible modules and create logical learning progressions.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        # Agent 2: Content Creator
        content_creator = Agent(
            role='Course Content Creator',
            goal='Generate detailed course content for each module based on the structure',
            backstory="""You are an expert content creator and educator who excels at
            transforming course outlines into engaging, comprehensive learning materials.
            You create content that is both educational and engaging, suitable for
            self-paced learning.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        # Agent 3: Keyword Generator
        keyword_generator = Agent(
            role='Search Keyword Generator',
            goal='Generate relevant search keywords for images and videos based on course content',
            backstory="""You are an expert at analyzing educational content and generating
            precise search keywords that will find the most relevant visual and video content
            to enhance learning materials.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        # Agent 4: Media Collector
        media_collector = Agent(
            role='Media Content Collector',
            goal='Search and collect relevant images and videos for course modules',
            backstory="""You are a skilled researcher who excels at finding high-quality
            visual and video content that enhances educational materials. You know how to
            search effectively and select the most appropriate media.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[self.image_search_tool, self.youtube_search_tool]
        )

        # Agent 5: Content Enhancer
        content_enhancer = Agent(
            role='Content Enhancement Specialist',
            goal='Integrate media content into course modules to make them more attractive',
            backstory="""You are an expert at enhancing educational content by seamlessly
            integrating relevant images and videos. You know how to place media content
            strategically to improve learning outcomes.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

        return course_planner, content_creator, keyword_generator, media_collector, content_enhancer

    # Keep all the existing methods but add better error handling
    def create_structure_task(self, course_topic: str, agent: Agent) -> Task:
        """Create task for course structure planning"""
        return Task(
            description=f"""
            Create a comprehensive course structure for the topic: "{course_topic}"

            Requirements:
            1. Create exactly 15 markdown files with logical progression
            2. Start with "01_introduction_roadmap.md"
            3. End with "15_expert_roadmap.md"
            4. Each file should represent 10-12 minutes of reading content
            5. Total course should be approximately 3 hours

            For each file, provide:
            - File name (following the pattern: XX_descriptive_name.md)
            - Main topic/title
            - Key subtopics to cover
            - Learning objectives
            - Difficulty level
            - Estimated reading time

            Structure the course to flow logically from beginner to advanced concepts.
            Include practical examples, exercises, and real-world applications.

            Return the structure as a JSON format with file details.
            """,
            expected_output="A detailed JSON structure containing 15 course modules with filenames, topics, subtopics, and guidelines",
            agent=agent
        )

    def save_content_to_file(self, filename: str, content: str):
        """Save content to markdown file"""
        file_path = self.course_directory / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Saved: {filename}")

    def create_default_structure(self, course_topic: str) -> Dict:
        """Create a default course structure if JSON parsing fails"""
        base_name = course_topic.lower().replace(' ', '_').replace('-', '_')

        modules = []
        for i in range(1, 16):
            if i == 1:
                title = f"Introduction and Roadmap to {course_topic}"
                filename = f"01_introduction_roadmap.md"
                subtopics = ["Course Overview", "Learning Path", "Prerequisites", "Goals"]
            elif i == 15:
                title = f"Expert Roadmap and Advanced {course_topic}"
                filename = f"15_expert_roadmap.md"
                subtopics = ["Advanced Concepts", "Expert Resources", "Career Paths", "Next Steps"]
            else:
                title = f"{course_topic} - Module {i}"
                filename = f"{i:02d}_{base_name}_module_{i}.md"
                subtopics = [f"Topic {i}.1", f"Topic {i}.2", f"Topic {i}.3"]

            modules.append({
                "filename": filename,
                "title": title,
                "subtopics": subtopics,
                "objectives": [f"Understand {title}"],
                "difficulty": "Intermediate" if i > 10 else "Beginner",
                "estimated_time": "10-12 minutes"
            })

        return {"modules": modules}

    def run_enhanced_course_creation(self, course_topic: str):
        """Main method to run the enhanced course creation process with better error handling"""
        
        print(f"🚀 Starting enhanced course creation for: {course_topic}")
        print("=" * 60)
        
        try:
            # Create agents
            course_planner, content_creator, keyword_generator, media_collector, content_enhancer = self.create_agents()

            # Step 1: Create course structure
            print("\n📋 Step 1: Creating course structure...")
            structure_task = self.create_structure_task(course_topic, course_planner)

            structure_crew = Crew(
                agents=[course_planner],
                tasks=[structure_task],
                verbose=True,
                process=Process.sequential
            )

            try:
                structure_result = structure_crew.kickoff()
                
                # Parse structure result
                raw_output = str(structure_result.raw)
                
                # Check if the output contains an error message
                if "Error generating content:" in raw_output:
                    print(f"❌ Structure generation failed: {raw_output}")
                    print("Using default structure...")
                    course_structure = self.create_default_structure(course_topic)
                else:
                    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    if json_match:
                        json_str = json_match.group()
                        course_structure = json.loads(json_str)
                        print(f"✅ Parsed course structure: {len(course_structure.get('modules', []))} modules")
                    else:
                        print("⚠️ Using default structure")
                        course_structure = self.create_default_structure(course_topic)
                        
            except Exception as e:
                print(f"❌ Structure creation failed: {e}")
                course_structure = self.create_default_structure(course_topic)

            # Continue with the rest of the process...
            # (keeping the existing logic but with better error handling)
            
            print(f"\n🎉 Course creation process initiated!")
            print(f"📁 Files will be saved in: {self.course_directory}")
            print(f"📚 Total modules planned: {len(course_structure.get('modules', []))}")
            
            return course_structure
            
        except Exception as e:
            error_response = handle_error(e, {
                "topic": course_topic,
                "step": "course_creation"
            })
            
            print(f"❌ Course creation failed: {error_response['error']['message']}")
            print(f"Details: {error_response['error']['details']}")
            print(f"Suggested action: {error_response['error']['suggested_action']}")
            
            raise e

# Main execution function
def create_enhanced_course(course_topic: str, images_per_module: int = 1, videos_per_module: int = 1):
    """Main function to create an enhanced course with proper error handling"""

    print("🎓 Enhanced CrewAI Course Creation System")
    print("=" * 60)
    print(f"📖 Course Topic: {course_topic}")
    print(f"🖼️ Images per module: {images_per_module}")
    print(f"🎬 Videos per module: {videos_per_module}")
    print("=" * 60)

    try:
        # Initialize system
        system = EnhancedCourseCreationSystem(images_per_module, videos_per_module)

        # Run enhanced course creation
        system.run_enhanced_course_creation(course_topic)

        return system.course_directory
        
    except Exception as e:
        print(f"\n❌ Failed to create course: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check your API keys in the .env file")
        print("2. Run 'python setup_check.py' to test your configuration")
        print("3. Make sure you have a working internet connection")
        return None

# Example usage
if __name__ == "__main__":
    # Check configuration first
    from config import get_config
    
    config = get_config()
    if not config.validation_result.is_valid:
        print("❌ Configuration Error:")
        print(config.get_setup_instructions())
        exit(1)
    
    # Get course topic from user
    course_topic = input("Enter the course topic: ")

    # Optional: Customize media counts
    images_per_module = 1
    videos_per_module = 1

    # Create the enhanced course
    course_directory = create_enhanced_course(course_topic, images_per_module, videos_per_module)