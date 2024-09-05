import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import GraphCypherQAChain


load_dotenv()
url_0 = os.getenv('NEO4J_URI_0')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
google_api_key = os.getenv('GOOGLE_API_KEY')


graph = Neo4jGraph(url=url, username=username, password=password)
graph.refresh_schema()
#print(graph.schema)

# setup llm model
llm = GoogleGenerativeAI(model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)

chain = GraphCypherQAChain.from_llm(graph=graph, llm=llm, verbose=True)
response = chain.invoke({"query": "cases associated with Rajasthan High Court (RAJ) court"})
print(response.result)
