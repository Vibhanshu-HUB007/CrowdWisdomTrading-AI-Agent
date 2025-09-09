from crewai import Task
from textwrap import dedent


def create_keyword_generation_task(agent):
    """Create task for generating financial market keywords"""
    return Task(
        description=dedent("""
            Generate a comprehensive list of keywords and phrases for searching Twitter/X users
            who post about US financial markets. The keywords should cover:
            
            1. Stock market terms (SPY, QQQ, stocks, trading, NYSE, NASDAQ)
            2. Cryptocurrency terms (Bitcoin, BTC, ETH, crypto, DeFi)
            3. Forex and commodities (USD, EUR, gold, oil, forex)
            4. Trading terminology (bullish, bearish, calls, puts, options)
            5. Market analysis terms (technical analysis, fundamentals, chart)
            6. Financial news and events (Fed, interest rates, earnings, GDP)
            7. Popular financial hashtags (#StockMarket, #Trading, #Investing)
            
            Focus on terms that active financial content creators would use.
            Return the keywords as a space-separated string optimized for Twitter search.
        """),
        expected_output=dedent("""
            A space-separated string of keywords optimized for Twitter search, including:
            - Core financial terms
            - Popular hashtags
            - Trading terminology
            - Market-specific keywords
            
            Example format: "stocks trading SPY QQQ #StockMarket bullish bearish Bitcoin BTC"
        """),
        agent=agent
    )
