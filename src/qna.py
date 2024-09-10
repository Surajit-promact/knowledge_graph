import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from neomodel import db, config


load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
neo4j_url = os.getenv('NEO4J_URI_0')
database = 'newvectordb2'


prompt_template = """A user asked a question related to a legal case.
Now to answer the question we need to search through graph database.
here is the graph schema:
graph_schema: {graph_schema}

Atfirst, you need to extract if any of these properties are present \
in the user question. if present then get those property and value.
Then, write a cypher query to retrieve all information, all nodes,\
all relations, all properties related to all the keywords from the graph \
database. Follow the graph node name, relationship name, property name \
properly according to schema. Also look for partial matches by using contains,\
lower, regex, starts_with etc.

eg.
question: "give me case names related to 'Dowry Harassment'"

cypher query:
MATCH (c:Case)-[:Has_data]->(cd:CitationsData),
      (c)-[:Has_data]->(sd:SummaryData),
      (c)-[:Has_data]->(ctd:CourtData),
      (court:Court)-[:Is_case]->(c)
WHERE c.case_name CONTAINS 'Dowry Harassment' OR
      cd.cited CONTAINS 'Dowry Harassment' OR
      cd.keywords CONTAINS 'Dowry Harassment' OR
      sd.summary CONTAINS 'Dowry Harassment' OR
      sd.facts CONTAINS 'Dowry Harassment' OR
      ctd.act CONTAINS 'Dowry Harassment'
RETURN c, cd, sd, ctd, court


Only return the cypher query.

you have retrieved the following information from user question for writing \
the query,
question_information:{question}
cypher query:
"""


def get_cypher_query(question):
    llm = GoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)
    # graph = Neo4jGraph(url=url, username=username, password=password)
    graph = Neo4jGraph(
        url=url, username=username, password=password, database=database)

    # Create a prompt template
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["graph_schema", "question"],
    )

    # Create the LLM chain
    chain = prompt | llm

    cypher_query = chain.invoke(
        {"graph_schema": graph.schema, "question": question})
    print(cypher_query)
    return cypher_query[10:-4]


def run_cypher_query(cypher_query):
    config.DATABASE_URL = neo4j_url
    results, meta = db.cypher_query(cypher_query)
    # print('result: ', results)
    return results


def get_answer(context, question):
    llm = GoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest", google_api_key=google_api_key)
    response = llm.invoke(f"answer the following question based on context.\
    \nContext: {context} \nQuestion: {question}")
    # print(response)
    return response
