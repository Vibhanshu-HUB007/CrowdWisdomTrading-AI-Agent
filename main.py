#!/usr/bin/env python3
"""
CrowdWisdomTrading AI Agent - Twitter Financial Markets User Finder

This script uses CrewAI to find Twitter/X creators posting about US financial markets.
It filters users with 5000+ followers who posted 5+ tweets in the last 2 weeks.

Usage:
    python main.py [--output filename.json]

Requirements:
    - Twitter API Bearer Token (set in .env file)
    - OpenAI API Key or other LLM provider (set in .env file)
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "logs/twitter_financial_flow_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 day",
    retention="7 days"
)

from flow import TwitterFinancialFlow, validate_environment, validate_api_access


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Find Twitter users posting about US financial markets using CrewAI"
    )
    parser.add_argument(
        "--output", 
        "-o", 
        type=str, 
        help="Output JSON filename (default: auto-generated with timestamp)"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
    
    try:
        # Load environment variables
        load_dotenv()
        logger.info("Environment variables loaded")
        
        # Validate environment and API access
        logger.info("Validating environment and API access...")
        validate_environment()
        
        if not validate_api_access():
            logger.error("API validation failed. Please check your credentials.")
            sys.exit(1)
        
        # Initialize and run the flow
        logger.info("Initializing Twitter Financial Flow...")
        flow = TwitterFinancialFlow()
        
        # Execute the complete workflow
        output_file = flow.run_flow(args.output)
        
        # Success message
        logger.success(f"✅ Flow completed successfully!")
        logger.success(f"📄 Results saved to: {output_file}")
        logger.success(f"🎯 Found Twitter users posting about US financial markets")
        
        return 0
        
    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Flow execution failed: {e}")
        logger.exception("Full error details:")
        return 1


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Run main function
    exit_code = main()
    sys.exit(exit_code)
