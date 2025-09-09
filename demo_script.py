#!/usr/bin/env python3
"""
Demo script for testing the Twitter Financial Flow without actual API calls.
This creates a mock demonstration of the expected workflow and output.
"""

import json
import time
from datetime import datetime
from loguru import logger

def create_demo_output():
    """Create a demo output file showing expected results"""
    
    demo_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "processing_time_seconds": 45.7,
            "search_keywords": "stocks trading SPY QQQ #StockMarket bullish bearish Bitcoin BTC ETH crypto DeFi forex gold oil USD EUR Fed interest rates earnings technical analysis fundamentals chart NYSE NASDAQ options calls puts",
            "filter_criteria": {
                "min_followers": 5000,
                "min_tweets_2weeks": 5
            },
            "status": "demo_completed"
        },
        "statistics": {
            "total_users_found": 142,
            "total_users_filtered": 24,
            "filter_success_rate": 0.169,
            "search_effectiveness": "high",
            "avg_followers_filtered_users": 16250,
            "avg_posts_per_week_filtered_users": 7.8
        },
        "users": [
            {
                "url": "https://twitter.com/FinancialWizard",
                "username": "FinancialWizard",
                "followers": 15200,
                "avg_posts_per_week": 9.0,
                "verified": True,
                "recent_tweets_count": 18,
                "total_tweets_found": 26
            },
            {
                "url": "https://twitter.com/CryptoTrader_Pro",
                "username": "CryptoTrader_Pro",
                "followers": 8900,
                "avg_posts_per_week": 6.5,
                "verified": False,
                "recent_tweets_count": 13,
                "total_tweets_found": 19
            },
            {
                "url": "https://twitter.com/StockAnalytics",
                "username": "StockAnalytics",
                "followers": 28500,
                "avg_posts_per_week": 11.5,
                "verified": True,
                "recent_tweets_count": 23,
                "total_tweets_found": 38
            },
            {
                "url": "https://twitter.com/MarketMaven",
                "username": "MarketMaven",
                "followers": 12800,
                "avg_posts_per_week": 7.5,
                "verified": False,
                "recent_tweets_count": 15,
                "total_tweets_found": 22
            },
            {
                "url": "https://twitter.com/TradingSignals",
                "username": "TradingSignals",
                "followers": 19600,
                "avg_posts_per_week": 8.5,
                "verified": True,
                "recent_tweets_count": 17,
                "total_tweets_found": 29
            }
        ],
        "processing_details": {
            "keyword_generation_time": 2.8,
            "search_time": 26.3,
            "filtering_time": 11.4,
            "formatting_time": 5.2,
            "api_calls_made": 12,
            "rate_limits_hit": 0
        }
    }
    
    # Save demo output
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_twitter_financial_users_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(demo_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Demo output created: {filename}")
    return filename

def simulate_flow_execution():
    """Simulate the CrewAI flow execution with timing"""
    
    logger.info("🚀 Starting Twitter Financial Flow Demo...")
    start_time = time.time()
    
    # Step 1: Keyword Generation
    logger.info("📝 Step 1: Generating financial market keywords...")
    time.sleep(2)
    keywords = "stocks trading SPY QQQ #StockMarket bullish bearish Bitcoin BTC ETH crypto DeFi"
    logger.info(f"✅ Generated keywords: {keywords[:50]}...")
    
    # Step 2: User Search
    logger.info("🔍 Step 2: Searching Twitter for financial content creators...")
    time.sleep(3)
    logger.info("✅ Found 142 users posting about financial markets")
    
    # Step 3: User Filtering
    logger.info("🔧 Step 3: Filtering users by followers (5000+) and activity (5+ tweets/2weeks)...")
    time.sleep(2)
    logger.info("✅ Filtered to 24 users meeting all criteria")
    
    # Step 4: JSON Formatting
    logger.info("📊 Step 4: Formatting results to structured JSON...")
    time.sleep(1)
    output_file = create_demo_output()
    
    total_time = time.time() - start_time
    logger.success(f"🎉 Demo completed in {total_time:.1f} seconds!")
    logger.success(f"📄 Results saved to: {output_file}")
    
    return output_file

if __name__ == "__main__":
    # Configure logging for demo
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>\n",
        level="INFO"
    )
    
    try:
        output_file = simulate_flow_execution()
        
        print("\n" + "="*60)
        print("📋 DEMO SUMMARY")
        print("="*60)
        print(f"✅ Successfully simulated Twitter Financial Flow")
        print(f"📊 Found 24 qualified financial content creators")
        print(f"📄 Output saved to: {output_file}")
        print(f"🔧 Filter criteria: 5000+ followers, 5+ tweets in 2 weeks")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        exit(1)
