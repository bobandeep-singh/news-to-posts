from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import find_dotenv, load_dotenv
import os

from custom_tools import scrape_top_news

load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def create_agent_executor():
    try:
        prompt_template = """
        Given the {input} understand what the user wants. If the user first question or the followup questions
        is related so give him the news, identify the category he wants the news from. The category should be one of these 'business', 
        'entertainment', 'general', 'health', 'science', 'sports', 'technology', otherwise respond him with 'Invalid Input'. Your answer 
        should contain only the News Title and the URL of the content in simple readable format without any special characters. 
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template("You are a helpful assistant."),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                HumanMessagePromptTemplate.from_template(prompt_template),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

        agent_tools = [scrape_top_news]
        langchain_agent = create_openai_tools_agent(llm, agent_tools, prompt)
        agent_executor = AgentExecutor(agent=langchain_agent,
                                       tools=agent_tools,
                                       verbose=True,
                                       return_intermediate_steps=False)
        return agent_executor
    except Exception as e:
        print(e)



