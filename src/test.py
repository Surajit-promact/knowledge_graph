from pathlib import Path
import os
from dotenv import load_dotenv
from langchain.vectorstores import Neo4jVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from load_html import load_html_files

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')
url = os.getenv('NEO4J_URI')
username = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
neo4j_url = os.getenv('NEO4J_URI_0')
database = 'newvectordb'


def load_data(file_dir_path):
    html_files = Path(file_dir_path).glob('*.htm')

    vector_index = None
    for file in html_files:
        try:
            html_data = load_html_files(file)
            vector_index = Neo4jVector.from_documents(
                html_data,
                GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
                url=url,
                username=username,
                password=password,
                database=database,
                search_type="hybrid",
                node_label=[
                    "Court", "Case", "AppealedCase", "CourtData", "SummaryData", "CitationsData"
                ],
                text_node_properties=[
                    "court_name",
                    "court_abbreviation",
                    "case_name",
                    "result",
                    "case_no",
                    "overruled",
                    "overruled_by",
                    "reportable",
                    "petitioner",
                    "case_type",
                    "respondent",
                    "bench",
                    "coram",
                    "dated",
                    "case_no",
                    "petitioner_counsel",
                    "respondent_counsel",
                    "act",
                    "petitioners_arguments",
                    "courts_reasoning",
                    "summary",
                    "evidence",
                    "respondents_arguments",
                    "issues",
                    "facts",
                    "conclusion",
                    "legal_analysis",
                    "precedent_analysis",
                    "cited",
                    "citations",
                    "case_referred",
                    "keywords",
                    "headnotes"
                ],
                embedding_node_property="embedding"
            )
            print(vector_index)
        except Exception as e:
            print(f'Error occurred while processing {file}: {e}')
    return vector_index


def get_answer(vector_index, question):
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True
    )
    qa = ConversationalRetrievalChain.from_llm(
        ChatGoogleGenerativeAI(
            temperature=0,
            api_key=google_api_key,
            model='models/gemini-1.5-flash-latest'
        ),
        vector_index.as_retriever(),
        memory=memory
    )
    return qa


if __name__ == '__main__':
    # load data into graph
    file_dir_path = './html_data'
    vector_index = load_data(file_dir_path)
    print(vector_index)

    # perform Q&A using Cypher query
    # question = input('Enter a question: ')
    # answer = get_answer(vector_index, question)
    # print("answer: ", answer)
