from crewai import Task
from textwrap import dedent


def create_user_search_task(agent, tools):
    """Create task for searching Twitter users"""
    return Task(
        description=dedent("""
            Use the generated keywords to search for Twitter/X users who actively post about
            US financial markets. Your task is to:
            
            1. Take the keywords from the previous task
            2. Use the Twitter Search Tool to find users posting financial content
            3. Collect comprehensive data about each user including:
               - Username and profile information
               - Follower count
               - Recent tweets and posting frequency
               - Verification status
            
            Focus on finding users who regularly engage with financial market topics,
            not just occasional mentions. Look for patterns of consistent financial content.
        """),
        expected_output=dedent("""
            Raw user data containing:
            - User profiles and metadata
            - Tweet history and frequency data
            - Follower counts and engagement metrics
            - Search query used and total users found
        """),
        agent=agent,
        tools=tools
    )


def create_user_filtering_task(agent, tools):
    """Create task for filtering users based on criteria"""
    return Task(
        description=dedent("""
            Filter the discovered users based on the specified criteria:
            
            1. Minimum 5,000 followers
            2. Posted at least 5 tweets in the last 2 weeks
            3. Calculate average posts per week for each user
            
            Apply these filters to identify high-quality financial content creators
            who have both reach (followers) and activity (recent posts).
        """),
        expected_output=dedent("""
            Filtered user data containing:
            - Users meeting all criteria
            - Calculated metrics (avg posts per week)
            - Filter statistics (how many users passed/failed each filter)
        """),
        agent=agent,
        tools=tools
    )
