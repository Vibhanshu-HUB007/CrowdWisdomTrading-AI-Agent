from crewai import Task
from textwrap import dedent


def create_json_formatting_task(agent):
    """Create task for formatting results into JSON"""
    return Task(
        description=dedent("""
            Format the filtered Twitter user results into a structured JSON file with the following requirements:
            
            1. Create a JSON structure containing:
               - Individual user records with:
                 * url to the user profile
                 * username
                 * number of followers
                 * average posts per week
               
            2. Include comprehensive statistics:
               - Processing time
               - Total users found
               - Total users filtered (meeting criteria)
               - Filter criteria used
               - Search keywords used
               - Timestamp of analysis
            
            3. Ensure the JSON is properly formatted and valid
            4. Include metadata about the search process
            
            The output should be ready to save as a .json file.
        """),
        expected_output=dedent("""
            A properly formatted JSON structure containing:
            {
                "metadata": {
                    "timestamp": "ISO datetime",
                    "processing_time_seconds": float,
                    "search_keywords": "string",
                    "filter_criteria": {...}
                },
                "statistics": {
                    "total_users_found": int,
                    "total_users_filtered": int,
                    "filter_success_rate": float
                },
                "users": [
                    {
                        "url": "https://twitter.com/username",
                        "username": "string",
                        "followers": int,
                        "avg_posts_per_week": float
                    }
                ]
            }
        """),
        agent=agent
    )
