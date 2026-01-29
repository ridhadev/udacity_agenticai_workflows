# TODO: 1 - Import the AugmentedPromptAgent class
import os
from dotenv import load_dotenv
import workflow_agents.base_agents as base_agents

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

prompt = "What is the capital of France?"
persona = "You are a college professor; your answers always start with: 'Dear students,'"

# TODO: 2 - Instantiate an object of AugmentedPromptAgent with the required parameters
augmented_prompt_agent = base_agents.AugmentedPromptAgent(openai_api_key, persona)

# TODO: 3 - Send the 'prompt' to the agent and store the response in a variable named 'augmented_agent_response'
augmented_agent_response = augmented_prompt_agent.respond(prompt)

# Print the agent's response
print(augmented_agent_response)

# TODO: 4 - Add a comment explaining:

# - What knowledge the agent likely used to answer the prompt.
# >> The agent used its own knowledge to answer the prompt because no specifc information was provided to help it find the answser.

# - How the system prompt specifying the persona affected the agent's response.
# >> The prompt response starts with "Dear students," which was specified in the persona details provided.