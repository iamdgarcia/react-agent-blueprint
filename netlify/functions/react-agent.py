import json
import os
from fastapi import FastAPI, HTTPException
from mangum import Mangum
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI()

# Request/Response models
class ChatMessage(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    reasoning_steps: List[Dict[str, Any]]
    history: List[Dict[str, str]]

# Mock tools (in a real implementation, these would call actual APIs)
def search_tool(query: str) -> str:
    """Mock search tool"""
    return f"Search results for: {query}. This is a mock response showing information about {query}."

def calculator_tool(expression: str) -> str:
    """Mock calculator tool"""
    try:
        # Simple eval for demo - in production use a safe eval
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

def weather_tool(location: str) -> str:
    """Mock weather tool"""
    return f"Weather in {location}: Sunny, 72°F (mock data)"

# Available tools
TOOLS = {
    "search": search_tool,
    "calculator": calculator_tool,
    "weather": weather_tool
}

def get_tool_description(tool_name: str, tool_func) -> str:
    """Get description of a tool for the agent"""
    descriptions = {
        "search": "Useful for searching information about current events, topics, or general knowledge.",
        "calculator": "Useful for performing mathematical calculations.",
        "weather": "Useful for getting weather information for a specific location."
    }
    return descriptions.get(tool_name, f"A tool named {tool_name}")

def react_agent_reasoning(user_message: str, history: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Simple ReAct agent implementation
    In a real implementation, this would use an LLM to reason
    For this blueprint, we'll use a rule-based approach to demonstrate the pattern
    """
    reasoning_steps = []
    
    # Step 1: Reason about what we need to do
    reasoning_steps.append({
        "type": "reason",
        "content": f"I need to understand the user's request: '{user_message}'. Let me break this down to see what tools might be helpful."
    })
    
    # Simple keyword-based tool selection (in practice, an LLM would do this)
    user_lower = user_message.lower()
    selected_tools = []
    
    if any(word in user_lower for word in ["search", "find", "look up", "what is", "who is", "tell me about"]):
        selected_tools.append("search")
        reasoning_steps.append({
            "type": "reason",
            "content": "The user seems to be asking for information, so I should use the search tool."
        })
    
    if any(word in user_lower for word in ["calculate", "compute", "math", "+", "-", "*", "/", "="]):
        selected_tools.append("calculator")
        reasoning_steps.append({
            "type": "reason",
            "content": "The user seems to be asking for a calculation, so I should use the calculator tool."
        })
    
    if any(word in user_lower for word in ["weather", "temperature", "forecast", "rain", "sun"]):
        selected_tools.append("weather")
        reasoning_steps.append({
            "type": "reason",
            "content": "The user seems to be asking about weather, so I should use the weather tool."
        })
    
    # If no specific tools detected, default to search for general questions
    if not selected_tools and "?" in user_message:
        selected_tools.append("search")
        reasoning_steps.append({
            "type": "reason",
            "content": "The user asked a question, so I'll use search to find information."
        })
    
    # Step 2: Act using the selected tools
    observations = []
    for tool_name in selected_tools:
        if tool_name in TOOLS:
            tool_func = TOOLS[tool_name]
            reasoning_steps.append({
                "type": "act",
                "content": f"I will use the {tool_name} tool."
            })
            
            # Extract parameters (simplified for demo)
            if tool_name == "search":
                # Extract likely search terms
                search_query = user_message.replace("?", "").strip()
                observation = tool_func(search_query)
            elif tool_name == "calculator":
                # Try to extract a mathematical expression
                import re
                # Look for patterns like "2+2", "calculate 5*3", etc.
                calc_pattern = r'[\d+\-*/().\s]+'
                matches = re.findall(calc_pattern, user_message)
                expression = matches[0].strip() if matches else "2+2"  # default
                observation = tool_func(expression)
            elif tool_name == "weather":
                # Extract location (simplified)
                location = "New York"  # default
                # In reality, we'd parse the location from the message
                observation = tool_func(location)
            
            observations.append({
                "tool": tool_name,
                "result": observation
            })
            
            reasoning_steps.append({
                "type": "observe",
                "content": f"The {tool_name} tool returned: {observation}"
            })
    
    # Step 3: Reason again to formulate final response
    reasoning_steps.append({
        "type": "reason",
        "content": "Now I have enough information to formulate a response to the user."
    })
    
    # Generate final response based on observations
    if not observations:
        final_response = f"I understand you're asking about: '{user_message}'. However, I'm not sure which tools to use for this query. Could you clarify or provide more details?"
    else:
        response_parts = []
        for obs in observations:
            if obs["tool"] == "search":
                response_parts.append(f"Based on my search: {obs['result']}")
            elif obs["tool"] == "calculator":
                response_parts.append(f"The calculation result is: {obs['result']}")
            elif obs["tool"] == "weather":
                response_parts.append(f"The weather information is: {obs['result']}")
        
        final_response = " ".join(response_parts)
        
        # Add a conversational touch
        if len(observations) == 1:
            final_response += " Is there anything else you'd like to know?"
        else:
            final_response += " Let me know if you need more details on any of this."
    
    # Update history
    updated_history = history.copy()
    updated_history.append({"role": "user", "content": user_message})
    updated_history.append({"role": "assistant", "content": final_response})
    
    return {
        "response": final_response,
        "reasoning_steps": reasoning_steps,
        "history": updated_history
    }

@app.get("/")
async def root():
    return {"message": "ReAct Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    try:
        result = react_agent_reasoning(
            user_message=chat_message.message,
            history=chat_message.history or []
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Handler for Netlify Functions
handler = Mangum(app)