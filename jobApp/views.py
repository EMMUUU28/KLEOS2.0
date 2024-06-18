from django.shortcuts import render
from serpapi import GoogleSearch
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter



def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    prompt_template = """
    You are a tool which finds job using resumes, Identify the top 3 most relevant keywords from the given resume to enhance job matching and optimize the resume for job applications. Focus on the most important and frequently mentioned skills, job titles, and technologies. Strictly Prioritize industry-specific terms and technical skills that are crucial for job matching. \n\n
    Resume:\n {context}?\n

    The Answer should strictly follow this format, Dont number them, give the 3 keywords in a single line saparated by commas :  

    For Example:   
    Web Development, Python, C++, Django, Accounts

    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.1)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    response = chain({"input_documents":docs }, return_only_outputs=True)

    return response

from django.contrib.auth.decorators import login_required

def getjob(request):
    def fetch_jobs(query):
        params = {
            "engine": "google_jobs",
            "q": query,
            "hl": "en",
            "num": "25",
            "api_key": "3fb9e0be680fbc384833423e983140627c494f8d1468c6dc9d1282661ede94e6"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("jobs_results", [])

    skillsession = request.session.get('skill', 'python')
    jobs_results = fetch_jobs(f"{skillsession} Jobs in Mumbai")
    
    if request.method == 'POST' and request.FILES.get('pdf_files'):
        pdf_docs = request.FILES.getlist('pdf_files')
        user_question = "Find Jobs"
        
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        result = user_input(user_question)
        final_result = result.get('output_text', '')
        
        resume_jobs_results = fetch_jobs(final_result)
        if not resume_jobs_results:
            resume_jobs_results = "False"
        
        return render(request, 'jobs/job.html', {
            'response_text': final_result,
            'job_list': jobs_results,
            'resume_jobs': resume_jobs_results
        })
    
    return render(request, 'jobs/job.html', {'job_list': jobs_results})


