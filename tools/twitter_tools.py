import os
import tweepy
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from loguru import logger


class TwitterSearchTool(BaseTool):
    name: str = "Twitter Search Tool"
    description: str = "Search for Twitter users and their tweets based on keywords and criteria"
    
    def __init__(self):
        super().__init__()
        self.setup_twitter_api()
    
    def setup_twitter_api(self):
        """Initialize Twitter API client"""
        try:
            bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
            if not bearer_token:
                raise ValueError("TWITTER_BEARER_TOKEN not found in environment variables")
            
            self.client = tweepy.Client(
                bearer_token=bearer_token,
                wait_on_rate_limit=True
            )
            logger.info("Twitter API client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter API: {e}")
            raise
    
    def _run(self, keywords: str, max_results: int = 100) -> Dict[str, Any]:
        """
        Search for users posting about financial markets
        
        Args:
            keywords: Space-separated keywords to search for
            max_results: Maximum number of results to return
        """
        try:
            # Search for tweets with financial keywords
            query = f"({keywords}) -is:retweet lang:en"
            
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=query,
                tweet_fields=['author_id', 'created_at', 'public_metrics'],
                user_fields=['username', 'name', 'public_metrics', 'verified'],
                expansions=['author_id'],
                max_results=100
            ).flatten(limit=max_results)
            
            # Extract unique users from tweets
            users_data = {}
            tweet_count = {}
            
            for tweet in tweets:
                author_id = tweet.author_id
                if author_id not in users_data:
                    users_data[author_id] = {
                        'tweets': [],
                        'user_info': None
                    }
                    tweet_count[author_id] = 0
                
                users_data[author_id]['tweets'].append({
                    'created_at': tweet.created_at,
                    'text': tweet.text,
                    'public_metrics': tweet.public_metrics
                })
                tweet_count[author_id] += 1
            
            # Get user information
            if hasattr(tweets, 'includes') and 'users' in tweets.includes:
                for user in tweets.includes['users']:
                    if user.id in users_data:
                        users_data[user.id]['user_info'] = {
                            'username': user.username,
                            'name': user.name,
                            'followers_count': user.public_metrics['followers_count'],
                            'verified': user.verified,
                            'profile_url': f"https://twitter.com/{user.username}"
                        }
            
            return {
                'users_data': users_data,
                'total_users_found': len(users_data),
                'search_query': query
            }
            
        except Exception as e:
            logger.error(f"Error searching Twitter: {e}")
            return {'error': str(e), 'users_data': {}, 'total_users_found': 0}


class UserFilterTool(BaseTool):
    name: str = "User Filter Tool"
    description: str = "Filter users based on follower count and posting frequency"
    
    def _run(self, users_data: Dict[str, Any], min_followers: int = 5000, min_tweets_2weeks: int = 5) -> Dict[str, Any]:
        """
        Filter users based on criteria
        
        Args:
            users_data: Raw user data from search
            min_followers: Minimum follower count
            min_tweets_2weeks: Minimum tweets in last 2 weeks
        """
        try:
            filtered_users = []
            two_weeks_ago = datetime.now() - timedelta(days=14)
            
            for user_id, data in users_data.items():
                user_info = data.get('user_info')
                tweets = data.get('tweets', [])
                
                if not user_info:
                    continue
                
                # Filter by follower count
                if user_info['followers_count'] < min_followers:
                    continue
                
                # Count tweets in last 2 weeks
                recent_tweets = [
                    tweet for tweet in tweets 
                    if tweet['created_at'] >= two_weeks_ago
                ]
                
                if len(recent_tweets) < min_tweets_2weeks:
                    continue
                
                # Calculate average posts per week
                avg_posts_per_week = len(recent_tweets) / 2  # 2 weeks
                
                filtered_users.append({
                    'user_id': user_id,
                    'username': user_info['username'],
                    'name': user_info['name'],
                    'followers_count': user_info['followers_count'],
                    'profile_url': user_info['profile_url'],
                    'verified': user_info['verified'],
                    'recent_tweets_count': len(recent_tweets),
                    'avg_posts_per_week': round(avg_posts_per_week, 2),
                    'total_tweets_found': len(tweets)
                })
            
            return {
                'filtered_users': filtered_users,
                'total_filtered': len(filtered_users),
                'filter_criteria': {
                    'min_followers': min_followers,
                    'min_tweets_2weeks': min_tweets_2weeks
                }
            }
            
        except Exception as e:
            logger.error(f"Error filtering users: {e}")
            return {'error': str(e), 'filtered_users': [], 'total_filtered': 0}
