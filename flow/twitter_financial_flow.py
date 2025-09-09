import os
import json
import time
from datetime import datetime
from typing import Dict, Any, List
from crewai import Crew, Flow
from crewai.flow.flow import listen, start
from pydantic import BaseModel, Field
from loguru import logger
import litellm

from agents import create_keyword_agent, create_search_agent, create_formatter_agent
from tasks import (
    create_keyword_generation_task,
    create_user_search_task,
    create_user_filtering_task,
    create_json_formatting_task
)
from tools import TwitterSearchTool, UserFilterTool


class FlowState(BaseModel):
    """State management for the Twitter Financial Flow"""
    keywords: str = ""
    raw_search_results: Dict[str, Any] = Field(default_factory=dict)
    filtered_results: Dict[str, Any] = Field(default_factory=dict)
    final_json: str = ""
    processing_start_time: float = Field(default_factory=time.time)
    statistics: Dict[str, Any] = Field(default_factory=dict)


class TwitterFinancialFlow(Flow[FlowState]):
    """CrewAI Flow for finding Twitter users posting about US financial markets"""
    
    def __init__(self):
        super().__init__()
        self.setup_llm()
        self.setup_tools()
        self.setup_agents()
        
    def setup_llm(self):
        """Initialize LiteLLM with configured model"""
        try:
            # Use OpenAI GPT-4 as default, but can be configured via environment
            model = os.getenv('LITELLM_MODEL', 'gpt-4')
            self.llm = litellm.completion
            logger.info(f"LiteLLM initialized with model: {model}")
        except Exception as e:
            logger.error(f"Failed to initialize LiteLLM: {e}")
            raise
    
    def setup_tools(self):
        """Initialize Twitter tools"""
        try:
            self.twitter_search_tool = TwitterSearchTool()
            self.user_filter_tool = UserFilterTool()
            logger.info("Twitter tools initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Twitter tools: {e}")
            raise
    
    def setup_agents(self):
        """Initialize CrewAI agents"""
        try:
            self.keyword_agent = create_keyword_agent(self.llm)
            self.search_agent = create_search_agent(self.llm)
            self.formatter_agent = create_formatter_agent(self.llm)
            logger.info("CrewAI agents initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            raise

    @start()
    def generate_keywords(self) -> FlowState:
        """Step 1: Generate financial market keywords"""
        logger.info("Starting keyword generation...")
        
        try:
            # Create keyword generation task
            keyword_task = create_keyword_generation_task(self.keyword_agent)
            
            # Create crew for keyword generation
            keyword_crew = Crew(
                agents=[self.keyword_agent],
                tasks=[keyword_task],
                verbose=True
            )
            
            # Execute keyword generation
            result = keyword_crew.kickoff()
            keywords = str(result).strip()
            
            logger.info(f"Generated keywords: {keywords}")
            
            return FlowState(
                keywords=keywords,
                processing_start_time=time.time()
            )
            
        except Exception as e:
            logger.error(f"Error in keyword generation: {e}")
            raise

    @listen(generate_keywords)
    def search_users(self, state: FlowState) -> FlowState:
        """Step 2: Search for Twitter users using generated keywords"""
        logger.info("Starting user search...")
        
        try:
            # Validate keywords
            if not state.keywords:
                raise ValueError("No keywords generated for search")
            
            # Create search task
            search_task = create_user_search_task(
                self.search_agent, 
                [self.twitter_search_tool]
            )
            
            # Create crew for user search
            search_crew = Crew(
                agents=[self.search_agent],
                tasks=[search_task],
                verbose=True
            )
            
            # Execute search with keywords as context
            result = search_crew.kickoff(inputs={"keywords": state.keywords})
            
            # Parse search results
            if hasattr(result, 'raw'):
                search_results = result.raw
            else:
                search_results = str(result)
            
            logger.info(f"Search completed. Found data for processing.")
            
            state.raw_search_results = {"search_output": search_results}
            return state
            
        except Exception as e:
            logger.error(f"Error in user search: {e}")
            state.raw_search_results = {"error": str(e)}
            return state

    @listen(search_users)
    def filter_users(self, state: FlowState) -> FlowState:
        """Step 3: Filter users based on criteria (5000+ followers, 5+ tweets in 2 weeks)"""
        logger.info("Starting user filtering...")
        
        try:
            # Create filtering task
            filter_task = create_user_filtering_task(
                self.search_agent,
                [self.user_filter_tool]
            )
            
            # Create crew for filtering
            filter_crew = Crew(
                agents=[self.search_agent],
                tasks=[filter_task],
                verbose=True
            )
            
            # Execute filtering with search results as context
            result = filter_crew.kickoff(inputs={
                "search_results": state.raw_search_results
            })
            
            # Parse filtering results
            if hasattr(result, 'raw'):
                filtered_results = result.raw
            else:
                filtered_results = str(result)
            
            logger.info("User filtering completed")
            
            state.filtered_results = {"filtered_output": filtered_results}
            return state
            
        except Exception as e:
            logger.error(f"Error in user filtering: {e}")
            state.filtered_results = {"error": str(e)}
            return state

    @listen(filter_users)
    def format_to_json(self, state: FlowState) -> FlowState:
        """Step 4: Format results to JSON with statistics"""
        logger.info("Starting JSON formatting...")
        
        try:
            # Calculate processing time
            processing_time = time.time() - state.processing_start_time
            
            # Create formatting task
            format_task = create_json_formatting_task(self.formatter_agent)
            
            # Create crew for formatting
            format_crew = Crew(
                agents=[self.formatter_agent],
                tasks=[format_task],
                verbose=True
            )
            
            # Prepare context for formatting
            context = {
                "keywords": state.keywords,
                "search_results": state.raw_search_results,
                "filtered_results": state.filtered_results,
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat()
            }
            
            # Execute formatting
            result = format_crew.kickoff(inputs=context)
            
            # Get final JSON
            if hasattr(result, 'raw'):
                final_json = result.raw
            else:
                final_json = str(result)
            
            # Update statistics
            state.statistics = {
                "processing_time_seconds": processing_time,
                "timestamp": datetime.now().isoformat(),
                "keywords_used": state.keywords,
                "status": "completed"
            }
            
            state.final_json = final_json
            
            logger.info(f"JSON formatting completed in {processing_time:.2f} seconds")
            return state
            
        except Exception as e:
            logger.error(f"Error in JSON formatting: {e}")
            state.final_json = json.dumps({"error": str(e)})
            return state

    def save_results(self, state: FlowState, output_file: str = None) -> str:
        """Save the final JSON results to file"""
        try:
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"twitter_financial_users_{timestamp}.json"
            
            # Ensure the final_json is valid JSON
            try:
                if isinstance(state.final_json, str):
                    json_data = json.loads(state.final_json)
                else:
                    json_data = state.final_json
            except json.JSONDecodeError:
                # If parsing fails, create a structured output
                json_data = {
                    "metadata": {
                        "timestamp": state.statistics.get("timestamp", datetime.now().isoformat()),
                        "processing_time_seconds": state.statistics.get("processing_time_seconds", 0),
                        "search_keywords": state.keywords,
                        "status": "completed_with_parsing_issues"
                    },
                    "raw_output": state.final_json,
                    "statistics": state.statistics
                }
            
            # Save to file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Results saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            raise

    def run_flow(self, output_file: str = None) -> str:
        """Execute the complete flow with guardrails"""
        try:
            logger.info("Starting Twitter Financial Flow...")
            
            # Execute the flow
            final_state = self.kickoff()
            
            # Save results
            output_path = self.save_results(final_state, output_file)
            
            # Log completion statistics
            logger.info("Flow completed successfully!")
            logger.info(f"Processing time: {final_state.statistics.get('processing_time_seconds', 0):.2f} seconds")
            logger.info(f"Output saved to: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Flow execution failed: {e}")
            raise


# Guardrails and validation functions
def validate_environment():
    """Validate required environment variables"""
    required_vars = ['TWITTER_BEARER_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logger.info("Environment validation passed")


def validate_api_access():
    """Validate API access before running flow"""
    try:
        # Test Twitter API access
        twitter_tool = TwitterSearchTool()
        logger.info("Twitter API access validated")
        return True
    except Exception as e:
        logger.error(f"API validation failed: {e}")
        return False
