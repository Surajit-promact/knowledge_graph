import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, create_tool_calling_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import StructuredTool
from langchain_core.prompts import PromptTemplate
from langchain_community.graphs import Neo4jGraph

from qna import get_cypher_query, run_cypher_query


load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
neo4j_url = os.getenv('NEO4J_URI_0')
database = 'newdb'

run_cypher = StructuredTool.from_function(
    func=run_cypher_query,
    name="run_cypher",
    description="useful for when you need to run cypher query to retrieve information",
)

tools = [run_cypher]

graph = Neo4jGraph(url=url, username=username, password=password, database=database)

template = '''You are an assistant bot, help to answer the following question related to law as best you can. For answering you need to retrieve information from a graph database. Here is the graph schema:

{graph_schema}

You have also access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: extract if any of the properties of the graph nodes are present in the user question. if present then get those property and value
Action Input: question
Action:  write a cypher query to retrieve the answer. Follow the graph node name, relationship name, property name properly according to schema.
Action Input: question and retrieved keywords, values.
Action: run the cypher query, should use [{tool_names}]
Action Input: cypher query
Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke(
    {
        "input": "all case names related to Patna high court",
        "graph_schema": graph.schema,
    }
)
