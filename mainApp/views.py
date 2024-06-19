from django.shortcuts import render,HttpResponse
from .models import Skill,WorkExperience,Education,CareerInfo
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'home/index.html')

def calendar(request):
    return render(request,'calendar/calendar.html')

@login_required
def profile(request):
    user = request.user
    education = Education.objects.filter(user=user)
    workexp = WorkExperience.objects.filter(user=user)
    skill_info = Skill.objects.filter(user=user)
    career_info = CareerInfo.objects.filter(user=user).last()
    
    print(education)
    print(workexp)
    print(skill_info)
    params = {
        'education':education,
        'workexp':workexp,
        'skill':skill_info,
        'current_year': career_info.current_year,
        'dream_role': career_info.dream_role,
        'linkedin_link': career_info.linkedin_link,
        'github_link': career_info.github_link
        
    } 
    return render(request,'profile/profile.html', params)

@login_required
def updateprofile(request):
    return render(request,'profile/updateprofile.html')

@login_required
def updateworkexp(request):
    if request.method == 'POST':
        
        company = request.POST.get('company')
        position = request.POST.get('position')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        brief = request.POST.get('brief')
        
        # Print form data
        print(f"Company: {company}")
        print(f"Position: {position}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        print(f"Brief: {brief}")
        user = request.user

        WorkExperience.objects.create(
            user=user,
            company=company,
            position=position,
            start_date=start_date,
            end_date=end_date,
            description=brief,
        )
        
        # Do something with the form data, such as saving to a database
        return render(request,'profile/updateprofile.html')
    return render(request,'profile/updateprofile.html')

@login_required
def updateeducation(request):
    if request.method == 'POST':
        institution = request.POST.get('institution')
        degree = request.POST.get('degree')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        user = request.user
       
        # Print form data
        print(f"Institution: {institution}")
        print(f"Degree: {degree}")
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")

        Education.objects.create(
            user=user,
            institution=institution,
            degree=degree,
            start_date=start_date,
            end_date=end_date,
        )
        
        # Do something with the form data, such as saving to a database
        return render(request,'profile/updateprofile.html')
    return render(request,'profile/updateprofile.html')

@login_required
def updateskills(request):
    if request.method == 'POST':
        user = request.user

        skills = request.POST.get('skills')
        
        skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]  # Split skills by comma and remove any empty or whitespace-only skills
        
        # Print individual skills
        for skill in skills_list:
            print(f"Skill: {skill}")

        for skill_name in skills_list:
                Skill.objects.create(user=user, skill_name=skill_name)

        
        # Do something with the form data, such as saving to a database
        return render(request,'profile/updateprofile.html')
    return render(request,'profile/updateprofile.html')


import requests
from django.shortcuts import render
from serpapi import GoogleSearch

@login_required
def studymaterials(request):
    user = request.user
    skills = Skill.objects.filter(user=user)
    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        user = request.user
        skill = Skill.objects.get(id=skill_id,user=user)
        print(skill.skill_name)
        request.session['skill'] = skill.skill_name


        params = {
            "engine": "youtube",
            "search_query": skill.skill_name + "Tutorial Playlist",
            "api_key": "3fb9e0be680fbc384833423e983140627c494f8d1468c6dc9d1282661ede94e6"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Print out the results for debugging
        # print(results['playlist_results'])
            
        
        # Print individual skills
        


        return render(request,'resources/studymaterial.html',{'skills':skills,'videos':results['playlist_results']})
    return render(request,'resources/studymaterial.html',{'skills':skills})



# Update Profile Using Resume 


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

    Given a resume, extract and structure the information into a JSON format. The JSON should include the following sections:

    Education:

    User: The name of the person
    Institution: The educational institution attended
    Degree: The degree obtained
    Start Date: The start date of the education
    End Date: The end date of the education


    Work Experience:

    Company: The name of the company where the user worked
    Position: The job title or position held
    Start Date: The start date of the job
    End Date: The end date of the job
    Description: A brief description of the user's responsibilities or achievements
    Skills:

    Skill Name: The name of the skill

    Resume:\n {context}?\n


    For Example:   
    
  "education":   

      "institution": "University of Example",
      "degree": "Bachelor of Science in Computer Science",
      "start_date": "2015-09-01",
      "end_date": "2019-06-01"
    
  
  "work_experience": 
    
      "company": "Tech Solutions Inc.",
      "position": "Software Engineer",
      "start_date": "2019-07-01",
      "end_date": "2022-08-01",
      "description": "Developed and maintained web applications using JavaScript and Python."
    
    
      "company": "Innovative Tech",
      "position": "Senior Developer",
      "start_date": "2022-09-01",
      "end_date": "Present",
      "description": "Led a team of developers in creating cutting-edge AI solutions."
    
  "skills": 

      "skill_name": "JavaScript"
      "skill_name": "Python"
      "skill_name": "AI Development"

    """

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.1)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    response = chain({"input_documents":docs }, return_only_outputs=True)

    return response

from django.contrib.auth.decorators import login_required
import json 
from datetime import datetime


def updateprofile_resume(request):
  
    if request.method == 'POST' and request.FILES.get('pdf_files'):
        pdf_docs = request.FILES.getlist('pdf_files')
        user_question = "Find Jobs"
        
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        result = user_input(user_question)
        final_result = result.get('output_text', '')
        
        cleaned_string = final_result.replace("'", '')
        clean_string = cleaned_string.replace('\n', '').replace('\\', '').replace('```', '').replace('json', '')
        
        data = json.loads(clean_string)
        print(final_result)

        user=request.user

        # Save Education Data
        for edu in data['education']:
            Education.objects.create(
                user=user,
                institution=edu['institution'],
                degree=edu['degree'],
                start_date=edu.get('start_date', ''),
                end_date=edu.get('end_date', '')
            )
        
        # Save Work Experience Data
        for work in data['work_experience']:
            WorkExperience.objects.create(
                user=user,
                company=work['company'],
                position=work['position'],
                start_date=datetime.strptime(work['start_date'], '%B %Y').date(),
                end_date=datetime.strptime(work['end_date'], '%B %Y').date(),
                description=work['description']
            )
        
        # Save Skills Data
        for skill in data['skills']:
            Skill.objects.create(
                user=user,
                skill_name=skill['skill_name']
            )
        
        return render(request, 'profile/updateprofile.html')
    
    return render(request, 'profile/updateprofile.html')

def updatecareerinfo(request):
    if request.method == 'POST':
        current_year = request.POST.get('current_year')
        dream_role = request.POST.get('dream_role')
        linkedin_link = request.POST.get('linkedin')
        github_link = request.POST.get('github')
        user=request.user
        # Create a new CareerInfo object and save the form data
        career_info = CareerInfo(
            user=user,
            current_year=current_year,
            dream_role=dream_role,
            linkedin_link=linkedin_link,
            github_link=github_link
        )
        career_info.save()
        return render(request, 'profile/updateprofile.html')
    return render(request, 'profile/updateprofile.html')

