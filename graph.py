# from langgrapg import Graph, Node

from langgraph.graph import Graph

from django.contrib.auth.decorators import login_required
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


# Function definitions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain(prompt_template):
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question, prompt_template):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain(prompt_template)
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response


# Create a basic Graph
graph = Graph()

# Add nodes to the graph
graph.add_node("get_pdf_text", get_pdf_text)
graph.add_node("get_text_chunks", get_text_chunks)
graph.add_node("get_vector_store", get_vector_store)
graph.add_node("get_conversational_chain", get_conversational_chain)
graph.add_node("user_input", user_input)

# Define edges to specify dependencies
graph.add_edge("get_pdf_text", "get_text_chunks")
graph.add_edge("get_text_chunks", "get_vector_store")
graph.add_edge("get_vector_store", "get_conversational_chain")  
graph.add_edge("get_conversational_chain", "user_input")

graph.set_entry_point("get_pdf_text")

graph_agent = graph.compile()
# Example of invoking the graph with inputs
# result = graph_agent.invoke({"pdf_docs": pdf_files, "user_question": "What is AI?", "prompt_template": "Your prompt here"})
