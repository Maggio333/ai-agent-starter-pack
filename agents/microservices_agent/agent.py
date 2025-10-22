import os
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import function_tool

# Importujemy Container bezpośrednio - bez DIService
from application.container import Container

# Inicjalizujemy Container
container = Container()

# Konfiguracja LiteLlm dla LM Studio - bez API key
lm_studio_model = LiteLlm(
    model="lm_studio/model:1",
    api_base="http://127.0.0.1:8123/v1"  # Twój proxy na porcie 8123!
)

# Pobieramy ChatAgentService przez Container - bezpośrednio
chat_agent_service = container.chat_agent_service()

# Nasz agent używający LM Studio przez LiteLlm z narzędziami
root_agent = Agent(
    name="microservices_chat_agent",
    model=lm_studio_model,
    description="Advanced AI agent with Microservices Architecture, sophisticated ROP patterns, DI, Clean Architecture, and comprehensive city data services.",
    instruction="""
    You are an advanced microservices-based agent who can answer complex questions about cities using sophisticated ROP patterns, multiple specialized services, and Clean Architecture principles. You have access to weather, time, city information, knowledge base, and conversation management services.
    
    Always respond in Polish unless asked otherwise.
    Be helpful, accurate, and provide detailed information when requested.
    """,
    tools=[
        # Weather Service Tools
        function_tool.FunctionTool(chat_agent_service.get_weather),
        function_tool.FunctionTool(chat_agent_service.get_weather_forecast),
        function_tool.FunctionTool(chat_agent_service.get_weather_alerts),
        
        # Time Service Tools
        function_tool.FunctionTool(chat_agent_service.get_current_time),
        function_tool.FunctionTool(chat_agent_service.get_timezone_info),
        function_tool.FunctionTool(chat_agent_service.get_world_clock),
        
        # City Service Tools
        function_tool.FunctionTool(chat_agent_service.get_city_info),
        function_tool.FunctionTool(chat_agent_service.search_cities),
        function_tool.FunctionTool(chat_agent_service.get_city_attractions),
        function_tool.FunctionTool(chat_agent_service.compare_cities),
        
        # Knowledge Service Tools
        function_tool.FunctionTool(chat_agent_service.search_knowledge_base),
        function_tool.FunctionTool(chat_agent_service.add_knowledge),
        function_tool.FunctionTool(chat_agent_service.get_knowledge_stats),
        
        # Conversation Service Tools
        function_tool.FunctionTool(chat_agent_service.start_conversation),
        function_tool.FunctionTool(chat_agent_service.get_conversation_history),
        function_tool.FunctionTool(chat_agent_service.end_conversation),
        function_tool.FunctionTool(chat_agent_service.get_conversation_stats),
        
        # Orchestration Tools
        function_tool.FunctionTool(chat_agent_service.process_city_request),
        function_tool.FunctionTool(chat_agent_service.get_service_health),
        function_tool.FunctionTool(chat_agent_service.get_service_capabilities),
    ],
)
