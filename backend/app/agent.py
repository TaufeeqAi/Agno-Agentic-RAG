from agno.agent import Agent
from agno.models.groq import Groq
from .knowledge import knowledge_base
from agno.tools.reasoning import ReasoningTools
import logging

# Set up logging
logger = logging.getLogger(__name__)

def create_agent():
    # Define the model
    model = Groq(id="llama-3.3-70b-versatile")
    logger.info(f"Model: {model.id}")

    # Define the instructions
    instructions = [
        "Use the following context to answer the question:",
        "{context}",
        "Think step by step and explain your reasoning clearly in your response before providing the final answer. List each reasoning step as a numbered point.",
        "If you don’t know, say you don’t know.",
        "Use markdown to format your answers."
    ]
    logger.info(f"Instructions: {' '.join(instructions)}")

    # Log the knowledge base type
    logger.info(f"Knowledge base: {type(knowledge_base).__name__}")

    # Create ReasoningTools and log its configuration
    reasoning_tools = ReasoningTools(
        think=True,
        analyze=True,
        add_instructions=True,
        add_few_shot=True
    )
    logger.info(f"ReasoningTools: think={reasoning_tools.think}, analyze={reasoning_tools.analyze}, add_instructions={reasoning_tools.add_instructions}")

    # Create the agent with error handling
    try:
        agent = Agent(
            model=model,
            instructions=instructions,
            knowledge=knowledge_base,
            tools=[reasoning_tools],
            show_tool_calls=True,
            markdown=True,
            search_knowledge=True,
        )
        logger.info("Agent created successfully")
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise

    return agent