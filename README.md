# CrowdWisdomTrading AI Agent - Twitter Financial Markets User Finder

A CrewAI-powered backend Python script that searches for Twitter/X creators posting about US financial markets, filtering for users with 5000+ followers who have posted 5+ tweets in the last 2 weeks.

## 🎯 Project Overview

This project implements a multi-agent CrewAI Flow that:
1. **Generates keywords** for US financial market searches
2. **Searches Twitter/X** for users posting financial content
3. **Filters users** based on follower count and posting frequency
4. **Formats results** into structured JSON with comprehensive statistics

## 🏗️ Architecture

### CrewAI Flow Structure
- **Keyword Agent**: Generates financial market search terms
- **Search Agent**: Finds Twitter users posting about financial markets
- **Formatter Agent**: Structures results into JSON format

### Flow Steps
1. `generate_keywords()` - Creates optimized search keywords
2. `search_users()` - Searches Twitter using generated keywords
3. `filter_users()` - Applies follower and activity filters
4. `format_to_json()` - Creates structured JSON output with statistics

## 📋 Requirements

### API Access
- **Twitter API v2** Bearer Token (required)
- **LLM Provider** API Key (OpenAI, Anthropic, or Google)

### Python Dependencies
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env
```

### 2. Configure API Keys
Add your credentials to `.env`:
```bash
# Twitter/X API Configuration
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# LiteLLM Configuration  
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Application
```bash
# Basic usage
python main.py

# With custom output filename
python main.py --output my_results.json

# With verbose logging
python main.py --verbose
```

## 📊 Output Format

The script generates a JSON file with the following structure:

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "processing_time_seconds": 45.2,
    "search_keywords": "stocks trading SPY QQQ #StockMarket bullish bearish Bitcoin BTC",
    "filter_criteria": {
      "min_followers": 5000,
      "min_tweets_2weeks": 5
    }
  },
  "statistics": {
    "total_users_found": 150,
    "total_users_filtered": 23,
    "filter_success_rate": 0.153
  },
  "users": [
    {
      "url": "https://twitter.com/financialtrader",
      "username": "financialtrader",
      "followers": 12500,
      "avg_posts_per_week": 8.5
    }
  ]
}
```

## 🔧 Configuration

### Filter Criteria
- **Minimum Followers**: 5,000 (configurable in code)
- **Minimum Posts**: 5 tweets in last 2 weeks (configurable in code)

### LLM Models
Supports any LiteLLM-compatible model:
- OpenAI GPT-4/GPT-3.5
- Anthropic Claude
- Google Gemini
- Local models via Ollama

## 📁 Project Structure

```
CrewaAI/
├── agents/                 # CrewAI agent definitions
│   ├── __init__.py
│   ├── keyword_agent.py
│   ├── search_agent.py
│   └── formatter_agent.py
├── tasks/                  # CrewAI task definitions
│   ├── __init__.py
│   ├── keyword_tasks.py
│   ├── search_tasks.py
│   └── formatting_tasks.py
├── tools/                  # Custom Twitter tools
│   ├── __init__.py
│   └── twitter_tools.py
├── flow/                   # CrewAI Flow implementation
│   ├── __init__.py
│   └── twitter_financial_flow.py
├── logs/                   # Application logs
├── main.py                 # Main execution script
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

## 🛡️ Guardrails & Error Handling

### Environment Validation
- Checks for required API keys before execution
- Validates Twitter API access

### Error Recovery
- Comprehensive logging with file rotation
- Graceful error handling at each flow step
- Structured error output in JSON format

### Rate Limiting
- Built-in Twitter API rate limit handling
- Automatic retry with exponential backoff

## 🔍 Features

### Core Functionality
- ✅ Multi-agent CrewAI Flow architecture
- ✅ Twitter API v2 integration
- ✅ LiteLLM support for multiple LLM providers
- ✅ Comprehensive filtering (followers + activity)
- ✅ Structured JSON output with statistics

### Advanced Features
- ✅ Processing time tracking
- ✅ Comprehensive logging system
- ✅ Command-line interface
- ✅ Environment validation
- ✅ Error handling and recovery

## 📈 Usage Examples

### Finding Crypto Influencers
The system automatically generates keywords covering:
- Stock market terms (SPY, QQQ, NYSE, NASDAQ)
- Cryptocurrency (Bitcoin, BTC, ETH, DeFi)
- Trading terminology (bullish, bearish, options)
- Market analysis (technical analysis, charts)

### Output Statistics
Each run provides detailed metrics:
- Total processing time
- Users found vs. filtered
- Filter success rates
- Search effectiveness

## 🐛 Troubleshooting

### Common Issues

**Twitter API Errors**
```bash
# Check your bearer token
export TWITTER_BEARER_TOKEN="your_token_here"
python -c "import os; print(os.getenv('TWITTER_BEARER_TOKEN'))"
```

**LLM API Errors**
```bash
# Verify OpenAI API key
export OPENAI_API_KEY="your_key_here"
python -c "import openai; print('API key configured')"
```

**Rate Limiting**
- The system handles Twitter API rate limits automatically
- For heavy usage, consider Twitter API Pro plan

## 📝 Development

### Adding New Agents
1. Create agent in `agents/` directory
2. Define corresponding tasks in `tasks/`
3. Update the flow in `flow/twitter_financial_flow.py`

### Custom Tools
1. Extend `BaseTool` in `tools/` directory
2. Add tool to agent initialization
3. Update task definitions to use new tools

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Submit a pull request

## 📄 License

This project is created for the CrowdWisdomTrading internship assessment.

## 🙋‍♂️ Support

For questions or issues:
- Check the logs in `logs/` directory
- Review error messages in console output
- Verify API credentials and rate limits

---

**Built with CrewAI, LiteLLM, and Twitter API v2**
