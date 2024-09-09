import os
from dotenv import load_dotenv
from langchain.vectorstores import Neo4jVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
neo4j_url = os.getenv('NEO4J_URI_0')
database = 'htmldb2'

vector_index = Neo4jVector.from_existing_graph(
    GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
    url=url,
    username=username,
    password=password,
    database=database,
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)


