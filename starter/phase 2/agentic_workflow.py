# agentic_workflow.py
import logging
from unittest import result

# TODO: 1 - Import the following agents: ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent from the workflow_agents.base_agents module
from workflow_agents.base_agents import ActionPlanningAgent, KnowledgeAugmentedPromptAgent, EvaluationAgent, RoutingAgent
import os
from dotenv import load_dotenv

logging.basicConfig(filename="output.log", level=logging.INFO)

def log_print(*args, **kwargs):
    message = " ".join(str(a) for a in args)
    logging.info(message)

# TODO: 2 - Load the OpenAI key into a variable called openai_api_key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# load the product spec
# TODO: 3 - Load the product spec document Product-Spec-Email-Router.txt into a variable called product_spec
base_dir = os.path.dirname(os.path.abspath(__file__))
spec_path = os.path.join(base_dir, "Product-Spec-Email-Router.txt")

with open(spec_path, "r") as file:
    product_spec = file.read()

# Instantiate all the agents

# Action Planning Agent
knowledge_action_planning = (    
    "Extract exactly 3 high-level workflow steps for Email Router project planning:\n"
    "1- Create user stories - Create comprehensive user stories for the Email Router product. Use the product spec to define the user stories.\n"    
    "2- List product features - Generate list of product features for Email Router product with Feature Name, Description, Key Functionality, and User Benefit\n"    
    "3- Define engineering tasks - Developer tasks for Email Router product with Task ID, Title, Description, Acceptance Criteria, Estimated Effort, and Dependencies\n"    
    "Generate specific plan for the Email Router project. Do NOT generate generic examples."
)

# TODO: 4 - Instantiate an action_planning_agent using the 'knowledge_action_planning'
action_planning_agent = ActionPlanningAgent(openai_api_key, knowledge_action_planning)

# Product Manager - Knowledge Augmented Prompt Agent
persona_product_manager = "You are a Product Manager, you are responsible for defining the user stories for a product."
knowledge_product_manager = (
    "Stories are defined by writing sentences with a persona, an action, and a desired outcome. "
    "The sentences always start with: As a "
    "Write several stories for the product spec below, where the personas are the different users of the product. "
    # TODO: 5 - Complete this knowledge string by appending the product_spec loaded in TODO 3
    f"{product_spec}"
)
# TODO: 6 - Instantiate a product_manager_knowledge_agent using 'persona_product_manager' and the completed 'knowledge_product_manager'
product_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_product_manager, knowledge_product_manager)

# Product Manager - Evaluation Agent
# TODO: 7 - Define the persona and evaluation criteria for a Product Manager evaluation agent and instantiate it as product_manager_evaluation_agent. This agent will evaluate the product_manager_knowledge_agent.
# The evaluation_criteria should specify the expected structure for user stories (e.g., "As a [type of user], I want [an action or feature] so that [benefit/value].").
product_manager_eval_persona = "You are an evaluation agent that checks the answers of other worker agents."
product_manager_evaluation_criteria = f"""
The answer should be stories that follow the following structure: "As a [type of user], I want [an action or feature] so that [benefit/value]."
"""
product_manager_evaluation_agent = EvaluationAgent(openai_api_key, product_manager_eval_persona, product_manager_evaluation_criteria, product_manager_knowledge_agent, 10)


# Program Manager - Knowledge Augmented Prompt Agent
persona_program_manager = "You are a Program Manager, you are responsible for defining the features for a product."
knowledge_program_manager = "Features of a product are defined by organizing similar user stories into cohesive groups."
# Instantiate a program_manager_knowledge_agent using 'persona_program_manager' and 'knowledge_program_manager'
# (This is a necessary step before TODO 8. Students should add the instantiation code here.)
program_manager_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_program_manager, knowledge_program_manager)

# Program Manager - Evaluation Agent
persona_program_manager_eval = "You are an evaluation agent that checks the answers of other worker agents."

# TODO: 8 - Instantiate a program_manager_evaluation_agent using 'persona_program_manager_eval' and the evaluation criteria below.
#                      "The answer should be product features that follow the following structure: " \
#                      "Feature Name: A clear, concise title that identifies the capability\n" \
#                      "Description: A brief explanation of what the feature does and its purpose\n" \
#                      "Key Functionality: The specific capabilities or actions the feature provides\n" \
#                      "User Benefit: How this feature creates value for the user"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
program_manager_evaluation_criteria = f"""
The answer should be product features that follow the following structure:
- Feature Name: A clear, concise title that identifies the capability"
- Description: A brief explanation of what the feature does and its purpose"
- Key Functionality: The specific capabilities or actions the feature provides"
- User Benefit: How this feature creates value for the user"
"""
program_manager_evaluation_agent = EvaluationAgent(openai_api_key, persona_program_manager_eval, program_manager_evaluation_criteria, program_manager_knowledge_agent, 10)

# Development Engineer - Knowledge Augmented Prompt Agent
persona_dev_engineer = "You are a Development Engineer, you are responsible for defining the development tasks for a product."
knowledge_dev_engineer = "Development tasks are defined by identifying what needs to be built to implement each user story."
# Instantiate a development_engineer_knowledge_agent using 'persona_dev_engineer' and 'knowledge_dev_engineer'
# (This is a necessary step before TODO 9. Students should add the instantiation code here.)
development_engineer_knowledge_agent = KnowledgeAugmentedPromptAgent(openai_api_key, persona_dev_engineer, knowledge_dev_engineer)

# Development Engineer - Evaluation Agent
persona_dev_engineer_eval = "You are an evaluation agent that checks the answers of other worker agents."
# TODO: 9 - Instantiate a development_engineer_evaluation_agent using 'persona_dev_engineer_eval' and the evaluation criteria below.
#                      "The answer should be tasks following this exact structure: " \
#                      "Task ID: A unique identifier for tracking purposes\n" \
#                      "Task Title: Brief description of the specific development work\n" \
#                      "Related User Story: Reference to the parent user story\n" \
#                      "Description: Detailed explanation of the technical work required\n" \
#                      "Acceptance Criteria: Specific requirements that must be met for completion\n" \
#                      "Estimated Effort: Time or complexity estimation\n" \
#                      "Dependencies: Any tasks that must be completed first"
# For the 'agent_to_evaluate' parameter, refer to the provided solution code's pattern.
development_engineer_evaluation_criteria = f"""
The answer should be tasks that follow the following structure:
- Task ID: A unique identifier for tracking purposes"
- Task Title: Brief description of the specific development work"
- Related User Story: Reference to the parent user story"
- Description: Detailed explanation of the technical work required"
- Acceptance Criteria: Specific requirements that must be met for completion"
- Estimated Effort: Time or complexity estimation"
- Dependencies: Any tasks that must be completed first"
"""
development_engineer_evaluation_agent = EvaluationAgent(openai_api_key, persona_dev_engineer_eval, development_engineer_evaluation_criteria, development_engineer_knowledge_agent, 10)
    
# Routing Agent
# TODO: 10 - Instantiate a routing_agent. You will need to define a list of agent dictionaries (routes) for Product Manager, Program Manager, and Development Engineer. Each dictionary should contain 'name', 'description', and 'func' (linking to a support function). Assign this list to the routing_agent's 'agents' attribute.

# Job function persona support functions
# TODO: 11 - Define the support functions for the routes of the routing agent (e.g., product_manager_support_function, program_manager_support_function, development_engineer_support_function).
# Each support function should:
#   1. Take the input query (e.g., a step from the action plan).
#   2. Get a response from the respective Knowledge Augmented Prompt Agent.
#   3. Have the response evaluated by the corresponding Evaluation Agent.
#   4. Return the final validated response.
def program_manager_support_function(input_query):
    knowledge_result = program_manager_knowledge_agent.respond(input_query)
    eval_result = program_manager_evaluation_agent.evaluate(knowledge_result)
    return eval_result["final_response"]

def development_engineer_support_function(input_query):
    knowledge_result = development_engineer_knowledge_agent.respond(input_query)
    eval_result = development_engineer_evaluation_agent.evaluate(knowledge_result)
    return eval_result['final_response']

def product_manager_support_function(input_query):
    knowledge_result = product_manager_knowledge_agent.respond(input_query)
    eval_result = product_manager_evaluation_agent.evaluate(knowledge_result)
    return eval_result["final_response"]

routes = [
    {
        "name": "Product Manager",
        "description": "Responsible for defining product personas and user stories only. Does not define features or tasks. Does not group stories",
        "func": product_manager_support_function
    },
    {
        "name": "Program Manager",
        "description": "Responsible for defining product features only. Does not define user stories or tasks. Does not group stories",
        "func": program_manager_support_function
    },
    {
        "name": "Development Engineer",
        "description": "Responsible for defining development tasks only. Does not define user stories or features. Does not group stories",
        "func": development_engineer_support_function
    }
]

routing_agent = RoutingAgent(openai_api_key, routes)

# Run the workflow
if __name__ == "__main__":
    print("\n*** Workflow execution started ***\n")
    pass
    # Workflow Prompt
    # ****
    # workflow_prompt = "What would the development tasks for this product be?"
    workflow_prompt = "Create a clear and structured full project plan to develop an Email Router product."
    print(f"Task to complete in this workflow, workflow prompt = {workflow_prompt}")

    print("\nDefining workflow steps from the workflow prompt")
    # TODO: 12 - Implement the workflow.
    #   1. Use the 'action_planning_agent' to extract steps from the 'workflow_prompt'.
    steps = action_planning_agent.extract_steps_from_prompt(workflow_prompt)
    print(f"Extracted steps ({len(steps)}): {steps}")

    #   2. Initialize an empty list to store 'completed_steps'.
    completed_steps = []

    user_stories= ""
    product_features = ""
    engineering_tasks = ""

    #   3. Loop through the extracted workflow steps:
        #      a. For each step, use the 'routing_agent' to route the step to the appropriate support function.
        #      b. Append the result to 'completed_steps'.
        #      c. Print information about the step being executed and its result.
    istep = 0
    for step in steps:
        
        istep += 1
        print(f">> Processing step ({istep}): {step}")
        print("-"*55)
        routing_result = routing_agent.route(step)
        
        print(f"<< Routing result:\n {routing_result}")
        print("-"*55)

        # Assign the routing result based on the max occurance for each of the keyword "story", "feature" and "task"
        word_counts = { 
            "as a": routing_result.lower().count("as a"),
            "story": routing_result.lower().count("story"), 
            "feature": routing_result.lower().count("feature"), 
            "task": routing_result.lower().count("task") 
        }

        # Assign the output to the appropriate section based on the max occurance
        max_word_count = max(word_counts.values())
        for keyword, count in word_counts.items():
            if not user_stories and (word_counts["story"] == max_word_count or word_counts["as a"] == max_word_count):
                user_stories = routing_result
                break
            elif not product_features and word_counts["feature"] == max_word_count:
                product_features = routing_result
                break
            elif not engineering_tasks and word_counts["task"] == max_word_count:
                engineering_tasks = routing_result
                break 
        completed_steps.append(routing_result)


    #   4. After the loop, print the final output of the workflow (the last completed step).
    print("\n*******************************************************\n")
    print(f"Final output of the workflow:\n {completed_steps[-1]}")
   

    print("\n=================================================================\n")
    print(f">> STRUCTURED OUTPUT:\n")
    
    print(f"\n**USER STORIES**:\n\n{user_stories}")
    print(f"\n**PRODUCT FEATURES**:\n\n{product_features}")
    print(f"\n**ENGINEERING TASKS**:\n\n{engineering_tasks}")
