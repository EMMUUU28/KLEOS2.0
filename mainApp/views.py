from django.shortcuts import render,HttpResponse, get_object_or_404, redirect
from .models import Skill,WorkExperience,Education,CareerInfo, NotificationData, UserGitRepos, MyCareerDisplay, MyCareerDetailed, MyCareerTaskDetailed, MyRecCareer, CraeerSearch, QuizDetails
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse



import requests


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
    print(education)
    print(workexp)
    print(skill_info)
    params = {
        'education':education,
        'workexp':workexp,
        'skill':skill_info
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
            "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Print out the results for debugging
        # print(results['playlist_results'])
            
        
        # Print individual skills
        


        return render(request,'resources/studymaterial.html',{'skills':skills,'videos':results['playlist_results']})
    return render(request,'resources/studymaterial.html',{'skills':skills})



#Update Profile Using Resume 


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




def get_github_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Accept': 'application/vnd.github.v3+json'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses
        repos = response.json()

        # Extracting repository details (title, description, link)
        repo_details = []
        for repo in repos:
            title = repo['name']
            description = repo['description'] if repo['description'] else 'No description'
            link = repo['html_url']

            repo_details.append({
                'title': title,
                'description': description,
                'link': link
            })

        return repo_details

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories for {username}: {e}")
        return None




# username = 'AtharvaPawar456'
# repos = get_github_repos(username)

# if repos:
#     print(f"Repositories for {username}:")
#     for repo in repos:
#         print(f"Title: {repo['title']}")
#         print(f"Description: {repo['description']}")
#         print(f"Link: {repo['link']}")
#         print()  # Empty line for readability
# else:
#     print(f"No repositories found for {username}.")


def updatecareerinfo(request):
    if request.method == 'POST':
        current_year = request.POST.get('current_year')
        dream_role = request.POST.get('dream_role')
        linkedin_link = request.POST.get('linkedin')
        github_link = request.POST.get('github')
        # github_link = "https://github.com/AtharvaPawar456"
        gitusername = github_link.split('/')[-1]

        print("gitusername: \n\n", gitusername)
        repos = get_github_repos(gitusername)
        print("repos: \n\n", repos)

        if repos:
            # print(f"Repositories for {gitusername}:")
            for repo in repos:
                # print(f"Title: {repo['title']}")
                # print(f"Description: {repo['description']}")
                # print(f"Link: {repo['link']}")
                # print()  # Empty line for readability
                if not UserGitRepos.objects.filter(github_link=repo['link']).exists():
                    git_info = UserGitRepos(
                            user_name = request.user,

                            title=repo['title'],
                            description=repo['description'],
                            github_link=repo['link'],
                        )
                    git_info.save()
        
        # Create a new CareerInfo object and save the form data
        username = request.user
        try:
            career_info = CareerInfo.objects.get(user_name=username)
            career_info.current_year = current_year
            career_info.dream_role = dream_role
            career_info.linkedin_link = linkedin_link
            career_info.github_link = github_link
            career_info.save()
        except CareerInfo.DoesNotExist:
            career_info = CareerInfo(
                user_name=username,
                current_year=current_year,
                dream_role=dream_role,
                linkedin_link=linkedin_link,
                github_link=github_link
            )
            career_info.save()
        return render(request, 'profile/updateprofile.html')
    return render(request, 'profile/updateprofile.html')










def filter_by_username(request, username):
    # Filter by user_name and sort by timestamp (latest to oldest)
    emails = NotificationData.objects.filter(user_name=username).order_by('-timestamp')
    return render(request, 'filter_by_username.html', {'emails': emails, 'username': username})

# def filter_by_emailid(request, emailid):
#     # Filter by emailid and sort by timestamp (latest to oldest)
#     emails = NotificationData.objects.filter(emailid=emailid).order_by('-timestamp')
#     return render(request, 'filter_by_emailid.html', {'emails': emails, 'emailid': emailid})

def notificationfav(request, notificationid):
    if request.method == 'GET':
        email = get_object_or_404(NotificationData, eid=notificationid)

        if email.fav == "1":
            email.fav = "0"
        else:
            email.fav = "1"
        email.save()  # Save the changes to the database

        return JsonResponse({'status': 'success', 'fav': email.fav})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    


@login_required
def notification(request, myfilter):
    username = request.user

    emails = NotificationData.objects.filter(user_name=username).order_by('-timestamp')

    if not emails:
        gotuserData = NotificationData.objects.create(
                                    user_name=username,
                                    emailid="pixel@gmail.com",
                                    title="Welcome to PixelMap",
                                    content="Welcome! We're thrilled to have you here. Dive in and explore the amazing opportunities awaiting you.",
                                    )

    # Apply filters
    if emails:
        if 'recent20' in myfilter:
            emails = emails[:20]

        if 'fav' in myfilter:
            emails = emails.filter(fav='1')

    else:
        emails = "no emails"

    emailsContent = ""

    if "_" in myfilter:
        emailindex = myfilter.split('_')

        if len(emailindex) > 1:
            eid = emailindex[-1]

            emailsContent = NotificationData.objects.get(eid=eid)
            if emailsContent:
                email_ = get_object_or_404(NotificationData, eid = eid)

                if email_.seen == "0":
                    email_.seen = "1"
                    email_.save()
                
        
        else:
            emailsContent = "None"


    return render(request, 'profile/notification.html', {'emails': emails, 'username': username, 'emailsContent' : emailsContent})



@login_required
def myproject(request):
    username = request.user

    myrepos = UserGitRepos.objects.filter(user_name=username)

    
    if not myrepos:
        myrepos = 'none'

    print("myrepos : ", myrepos)

    return render(request, 'profile/myprojectsview.html', {'myrepos': myrepos, 'username': username})
    



@login_required
def mycourses(request, myfilter):
    username = request.user

    # if myfilter == 'all':


    # myrepos = UserGitRepos.objects.filter(user_name=username)

    
    # if not myrepos:
    #     myrepos = 'none'

    # print("myrepos : ", myrepos)

    return render(request, 'profile/mycourses.html', {'myrepos': "myrepos", 'username': username})













    
import google.generativeai as genai
import os

def geminiApiCode(prompt):
    genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
    generation_config = {
        "temperature": 0.1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]
    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    convo.send_message(prompt)
    result = convo.last.text
    cleaned_string = result.replace("'", '')
    clean_string = cleaned_string.replace('\n', '').replace('\\', '').replace('```', '').replace('json', '')
    print("GenOutput: ", clean_string) 
    return clean_string


def recommendCareer(careername, min=2, max=5):
    mainTopicContext = f"""Act as a career recommender, according to give conditions which is given to you, you are the master of the in career recommmendation system.
    recommended career count can be from min={min} to max={max}.

    conditions = {careername}

    # rules to follow while generating output:
    - only json list data
    - no text except json list data
    - be precise and confident 
    - give major and main content

    # json list format:
    - careertitle
    - careertitle_description : in 60 to 100 words
    - duration : give minimum time required to learn & complete this topic in (hrs, days, months : only)
    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics


def getMainTopic(careername, min=2, max=5):
    mainTopicContext = f"""Act as a career main topic generator, according to career which is given you in that career you are the master and teacher.
    the main topics count can be from min={min} to max={max}.

    career = {careername}

    # rules to follow while generating output:
    - only json list data
    - no text except json list data
    - be precise and confident 
    - give major and main content

    # json list format:
    - topic
    - topics_description : in 10 to 20 words
    - duration : give minimum time required to learn & complete this topic in (hrs, days, months : only)
    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics


def getSubTopic(maintopicname, duration, min=2, max=5):
    subTopicContext = f"""Act as a subtopic generator for the main topic given, according to topic which is given you in that career you are the master and teacher.
    the sub topics count can be from min={min} to max={max}.


    topic = {maintopicname}
    duration = {duration}

    # rules to follow while generating output:
    - only json list data
    - no text except json list data
    - be precise and confident 
    - give major and main content
    - all the subtopics should be coverd in mentioned duration only stricly...

    # json list format:
    - subtopic
    - subtopic_description : in 30 to 60 words
    - duration : give minimum time required to learn & complete this topic in (hrs, days, months : only) 
    """

    got_subtopics = geminiApiCode(subTopicContext)
    return got_subtopics


# def print_topics_from_json(topic_text):
#     try:
#         # Convert the string to a JSON object
#         topics = json.loads(topic_text)
        
#         # Loop through each topic and print details
#         for topic in topics:
#             print(f"Topic: {topic['topic']}")
#             print(f"Description: {topic['topic_description']}")
#             print(f"Duration: {topic['duration']}\n")
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON: {e}")

# Call the function with the provided topicgentext
# print_topics_from_json(topicgentext)


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_future_date(current_date, interval):
    # Ensure the current_date is a date object
    if isinstance(current_date, datetime):
        current_date = current_date.date()
    
    # Split the interval to get the number and the unit
    amount, unit = interval.split()
    amount = int(amount)
    
    if unit.endswith('s'):  # Make unit singular if it's plural
        unit = unit[:-1]
    
    # Calculate the future date based on the unit
    if unit == 'day':
        future_date = current_date + timedelta(days=amount)
    elif unit == 'week':
        future_date = current_date + timedelta(weeks=amount)
    elif unit == 'month':
        future_date = current_date + relativedelta(months=amount)
    else:
        raise ValueError("Invalid time interval unit. Use 'day', 'week', or 'month'.")
    
    # Return the future date object
    return future_date


    # return future_date.strftime("%d-%m-%Y")
    # return future_date.date()  # Return only the date part
    # return (future_date.strftime("%d-%m-%Y"), future_date.date())



from serpapi import GoogleSearch
import re
from pytube import YouTube

def get_video_details(url):
    try:
        yt = YouTube(url)
        video_details = {
            'title': yt.title,
            'duration': yt.length,
        }
        return video_details
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        return None
    
def extract_youtube_id(url):
    # Define the regex pattern for YouTube video ID
    youtube_id_pattern = re.compile(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    match = youtube_id_pattern.search(url)
    
    # Check if the regex found a match
    if match:
        return match.group(1)
    else:
        return None

def getYTLinks(Query):
    params = {
                "engine": "youtube",
                "search_query": Query + " Tutorial Playlist",
                "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
            }

    search = GoogleSearch(params)
    results = search.get_dict()

    # print("results: ", results)

    # Extract video results from the dictionary
    video_results = results.get('video_results', [])

    # Define the regex pattern for YouTube URLs
    youtube_url_pattern = re.compile(r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)')
    
    # Extract URLs from video results
    urls = []
    for video in video_results:
        link = video.get('link')
        if link and youtube_url_pattern.match(link):
            urls.append(link)

    if len(urls) >=2:
        mycount = 2
    else:
        mycount = 1

    myretvideo_details = '<div class="row row-cols-1 row-cols-md-3 g-4 mb-5"> '
    print("mycount: ", urls)
    for item in range(mycount):
        print("---- urls: ", len(urls), urls)
        try:
            retvideo_details = get_video_details(urls[item])
            video_id = extract_youtube_id(urls[item])

            text = f"""
            <div class="col">
                <div class="card h-100">
                    <iframe class="embed-responsive-item" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    <div class="card-body">
                    <h5 class="card-title">{retvideo_details['title']}</h5>
                    <i class="menu-icon tf-icons bx bx-timer ml-4"></i>{retvideo_details['duration']}
                    </div>
                </div>
                </div>
            """
            myretvideo_details += text

        except Exception as e:
            print(f"Error processing video at index {item}: {str(e)}")
            # Optionally, you can handle the error gracefully or skip this video


    return myretvideo_details + ' </div>'

'''
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h1 class="text-2xl font-bold mb-4">{retvideo_details['title']}</h1>
            <h1 class="text-md font-bold mb-4"><i class="menu-icon tf-icons bx bx-timer ml-4"></i>{retvideo_details['duration']}</h1>
            <div class="h-[550px] w-10/12 mx-auto p-1 border border-2 rounded-md shadow-md">
                
                <iframe class="w-full h-full" src="https://www.youtube.com/embed/{video_id}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


            </div>
        </div>
        <div class="py-4"></div>
'''

def recommendCareer(careername, min=3, max=5):
    mainTopicContext = f"""Act as a career recommender, according to give conditions which is given to you, you are the master of the in career recommmendation system.
    recommended career count can be from min={min} to max={max}.

    conditions = {careername}

    # rules to follow while generating output:
    - only json list data
    - no text except json list data
    - be precise and confident 
    - give major and main content

    # json list format:
    - careertitle
    - careertitle_description : in 60 to 100 words
    - duration : give minimum time required to learn & complete this topic in (hrs, days, months : only)
    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics

def check_at_symbol(val):
    if '@' in val:
        return True
    else:
        return False

@login_required
def mycareer(request, myfilter):
    username = request.user
    print("------------------------------------my career")

    if request.method == 'POST':
        careername = request.POST['entercareer']
        # recommmendcareer = request.POST['recommmendcareer']

        

        if check_at_symbol(careername) :
            careername = '''
            You are a career counselor tasked with advising individuals who want to explore new career paths based on their existing skills. Write a comprehensive recommendation for one of your clients, detailing three alternative career options that align with their skill set. Include a brief description of each career path, highlighting how their current skills can be applied effectively in these new roles. Consider the client's strengths, interests, and any additional information that might influence their career choices.
            '''
            gotRecommendJson = recommendCareer(careername)

            try:
                # Convert the string to a JSON object
                rectopics = json.loads(gotRecommendJson)
                for item in rectopics:
                    # recCareer = MyRecCareer.objects.create(user_name=username,careername=careername)
                    recCareer = MyRecCareer.objects.create(
                                    user_name=username,
                                    careername=item['careertitle'],

                                    description=item['careertitle_description'],
                                    duration=item['duration'],
                                    )
                    

                returnfilter = 'all'
                mycareer = MyCareerDisplay.objects.filter(user_name=username)
                renderMyRecCareer = MyRecCareer.objects.filter(user_name=username)
                print("renderMyRecCareer: ", renderMyRecCareer)

                content = {'mycareer':mycareer, 'filter':returnfilter, 'course': myfilter, 'renderMyRecCareer': renderMyRecCareer}

                return render(request, 'profile/mycareer.html', content)


            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

        else:
            gotMainTopicsJson = getMainTopic(careername, min=2, max=3)

            try:
                # Convert the string to a JSON object
                topics = json.loads(gotMainTopicsJson)
                savedCareer = MyCareerDisplay.objects.create(user_name=username,careername=careername)

                topiclatestDate = []
                topiclatestDate.append(datetime.now())


                # Loop through each topic and print details
                for topic in topics:
                    print(f"Topic: {topic['topic']}")
                    print(f"Description: {topic['topics_description']}")
                    print(f"Duration: {topic['duration']}\n")

                    # Example usage
                    current_date = topiclatestDate[-1]
                    interval = topic['duration']

                    future_date = calculate_future_date(current_date, interval)
                    topiclatestDate.append(future_date)
                    print(f"Current Date: {current_date} --- Future Date: {future_date}")

                    topicval = topic['topic']

                    savedTopics = MyCareerDetailed.objects.create(
                                user_name=username,
                                careername=careername,
                                topic=topic['topic'],
                                content=topic['topics_description'],
                                duration=topic['duration'],
                                slug=topicval.strip(),

                                date=future_date,
                                )

                    gotSubTopicsJson = getSubTopic(topic['topic'], topic['duration'], min=2, max=3)

                    try:
                        # Convert the string to a JSON object
                        subtopics = json.loads(gotSubTopicsJson)

                        subtopiclatestDate = []
                        subtopiclatestDate.append(current_date)

                        
                        # Loop through each topic and print details
                        for subtopic in subtopics:
                            print(f"SubTopic: {subtopic['subtopic']}")
                            print(f"Description: {subtopic['subtopic_description']}")
                            print(f"Duration: {subtopic['duration']}\n")

                            subcurrent_date = subtopiclatestDate[-1]

                            subfuture_date = calculate_future_date(subcurrent_date, interval)
                            subtopiclatestDate.append(subfuture_date)
                            print(f"Current Date: {current_date} --- Future Date: {subfuture_date}")

                            subtopicval = topic['topic'] + subtopic['subtopic']

                            getSubtopicContent = getYTLinks(str(subtopic['subtopic']))

                            topcontent = f"""
                                <div class="text-4xl font-bold text-center mb-4">{subtopic['subtopic']}</div>
                                <div class="text-md font-bold mb-4 px-4">{subtopic['subtopic_description']}</div>
                            """

                            final_content = topcontent + getSubtopicContent

                            savedSubTopics = MyCareerTaskDetailed.objects.create(
                                user_name=username,
                                careername=careername,
                                topic=topic['topic'],
                                subtopic=subtopic['subtopic'],
                                content=final_content,
                                duration=subtopic['duration'],
                                slug=subtopicval.strip(),

                                date=subfuture_date,
                                )

                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")


            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

            mycareer = MyCareerDisplay.objects.filter(user_name=username)
            if not mycareer:
                mycareer = 'none'
            return render(request, 'profile/mycareer.html', {'mycareer': mycareer, 'filter':'all'})




    if myfilter == 'all':
        mycareer = MyCareerDisplay.objects.filter(user_name=username)
        renderMyRecCareer = MyRecCareer.objects.filter(user_name=username)
        print("renderMyRecCareer: ", renderMyRecCareer)
        # renderMyRecCareer = MyRecCareer.objects.filter(user_name=username)
        # taskDoneStatusCount = []
        # for task_instance in mycareer:
        #     allsubtopicAll  = MyCareerTaskDetailed.objects.filter(user_name=username, careername=task_instance.careername)
        #     allsubtopicDone = MyCareerTaskDetailed.objects.filter(user_name=username, careername=task_instance.careername, done='1')
            
        #     remainingSubtopics = allsubtopicAll.count() - allsubtopicDone.count()

        #     donData = f'{allsubtopicDone.count()}/{allsubtopicAll.count()}'
        #     print(f"----------  subtopics: {allsubtopicDone.count()}/{allsubtopicAll.count()}")
            
        #     taskDoneStatusCount.append(donData)

        # # mycareer = [career for career in mycareer if career.status == f"hello"]

        # for item in mycareer:
        #     print("hello: ", item)

        # print("taskDoneStatusCountList: ", taskDoneStatusCount)

        # taskDoneStatusCount = ['1']
        returnfilter = 'all'

        content = {'mycareer':mycareer, 'filter':returnfilter, 'course': myfilter, 'renderMyRecCareer': renderMyRecCareer}
    
        return render(request, 'profile/mycareer.html', content)



    else:
        mycareerval = MyCareerTaskDetailed.objects.filter(user_name=username, careername=myfilter.replace("%20", " "))  # myfilter has topic
        # print("mycareerval:", mycareerval)
        data = {}

        # Iterate through each record in mycareer queryset
        for record in mycareerval:
            # Check if the topic already exists in data dictionary
            if record.topic in data:
                # Append the full record to the existing list for this topic
                data[record.topic].append({
                    'subtopic': record.subtopic,
                    'content': record.content,
                    'duration': record.duration,
                    'date': record.date,
                    'slug': record.slug,
                    'done': record.done
                })
            else:
                # Create a new entry for this topic with its full record list
                data[record.topic] = [{
                    'subtopic': record.subtopic,
                    'content': record.content,
                    'duration': record.duration,
                    'date': record.date,
                    'slug': record.slug,
                    'done': record.done
                }]

        mycareer = data
        returnfilter = 'subtopic'


    
    # if not myrepos:
    #     myrepos = 'none'

    # print("myrepos : ", myrepos)
    # if taskDoneStatusCount == '':
    #     taskDoneStatusCount = 'none'
    # print(taskDoneStatusCount)

    content = {'mycareer':mycareer, 'filter':returnfilter, 'course': myfilter}

    return render(request, 'profile/mycareer.html', content)
    




@login_required
def mycareerview(request, myslug):
    username = request.user

    mysubtopic = MyCareerTaskDetailed.objects.filter(user_name=username, slug=myslug)
    # print("mysubtopic : ", mysubtopic)
    
    if not mysubtopic:
        mysubtopic = 'none'

    print("mysubtopic : ", mysubtopic)

    return render(request, 'profile/mycareer.html', {'mycareer': mysubtopic, 'filter':"subtask"})




def mycareerdone(request, task_slug):
    username = request.user

    # Fetch the task instance
    task_instance   = MyCareerTaskDetailed.objects.get(user_name=username, slug=task_slug)
    allsubtopicAll  = MyCareerTaskDetailed.objects.filter(user_name=username, careername=task_instance.careername)
    allsubtopicDone = MyCareerTaskDetailed.objects.filter(user_name=username, careername=task_instance.careername, done='1')

    print("allsubtopicAll: ", len(allsubtopicAll))
    print("allsubtopicDone: ", len(allsubtopicDone))
    
    # Toggle the 'done' field
    if task_instance.done == '0':
        task_instance.done = '1'
        gotuserData = NotificationData.objects.create(
                            user_name=username,
                            emailid="pixel@gmail.com",
                            title= f"Congratulation you have completed the subtopic : {task_instance.subtopic} of {task_instance.topic}",
                            content=f"""
Congratulations on completing your course tasks {task_instance.subtopic}! 
Your dedication and hard work have paid off. 
Keep up the excellent work and continue to strive for excellence in your learning journey.

Best wishes for your future endeavors!

<a href="/mycareer/{task_instance.careername}/">visit</a>

""",
                            )
    # else:
    #     task_instance.done = '0'
    
    # Save the instance to update the database
    task_instance.save()

    redirect_url = f'/mycareer/{task_instance.careername}/'  # Note the URL encoding for space (%20)

    return redirect(redirect_url)




from serpapi import GoogleSearch


def getImgLink(userQuery):
    params = {
        "engine": "google_images",
        "q": f"roadmap for {userQuery}",
        "location": "Mumbai, Maharashtra, India",
        "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
    }
    search = GoogleSearch(params)
    return search.get_dict()

def extract_image_urls(results, max_images=4):
    # Extract image URLs from the results
    image_urls = []
    for image_result in results.get("images_results", []):
        image_urls.append(image_result.get("original"))
        if len(image_urls) >= max_images:
            break
    return image_urls


def recommendCareerKeywords(careername, min=10, max=20):
    mainTopicContext = f"""Act as a career skills generator, according to give career which is given to you, and you are master of career skills generation system.
    Career skills count can be from min={min} to max={max}.

    career = {careername}

    # Rules to follow while generating output:
    - only python list data like ['skill1', 'skill2', 'skill3']
    - no text except python plain string list data
    - be precise and confident 
    - give major and main content

    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics


def CareerKeywordsSummarizer(skilllist, min=10, max=20):
    mainTopicContext = f"""Act as a career summary generator, according to give conditions which is given to you, and you are master of career summary generator.
    career summary generator word count can be from min={min} to max={max}.

    skills list = {skilllist}

    # Rules to follow while generating output:
    - in plain text 
    - but where "." then after that put "<br>"
    - no code at all
    - be precise and confident 
    - give major and main content

    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics

def serpYTextractor(topic):
    params = {
                "engine": "youtube",
                "search_query": topic + " Tutorial Playlist",
                "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
            }
    search = GoogleSearch(params)
    results = search.get_dict()
    print('def results: ', results)
    return f""" {results['playlist_results']} """

def fetch_jobs(query):
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "num": "25",
        "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("jobs_results", [])

import ast
@login_required
def careersearch(request, myslug):
    print("------------------------------------ career search")
    username = request.user

    if myslug == 'all':

        if request.method == 'POST':
            careername = request.POST['entercareer']
            print("careername: ", careername)

            gotresult = getImgLink(careername)
            image_urls = extract_image_urls(gotresult)


            roadMapUrl = image_urls[0]
            print("roadMapUrl: ", roadMapUrl)

            jobdata = fetch_jobs(careername)
            print("jobdata: ", jobdata)

            skilllist = recommendCareerKeywords(careername)
            print("skilllist: ", skilllist)

            skillSummary = CareerKeywordsSummarizer(skilllist)
            ytJson = serpYTextractor(careername)
            youtube_url_pattern = re.compile(r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)')
            allyturls = youtube_url_pattern.findall(ytJson)

            print("\n\nallyturls: ", type(allyturls), "\n\n")

            # for item in ytJson:
            #     print(item)

            gotuserData = CraeerSearch.objects.create(
                        user_name=username,
                        careername=careername,
                        skills=skilllist,
                        roadmapURL=roadMapUrl,
                        content=ytJson[2:-2],
                        jobcontent=jobdata,
                        summary=skillSummary,
                    )

        # if myfilter == 'all':
        allcareerssearch = CraeerSearch.objects.filter(user_name=username)
        # if not myrepos:
        #     myrepos = 'none'
        # print("myrepos : ", myrepos)

        content =  {
            'allcareerssearch'  : allcareerssearch, 
            'filter'    : myslug
                    }
        return render(request, 'profile/careerSearch.html', content)
    
    
    else:
        mycareers = CraeerSearch.objects.get(user_name=username, careername=myslug)
        if not mycareers:
            mycareers = 'none'
        print("mycareers : ", mycareers)
        myjsonData = mycareers.content
        print(type(myjsonData))
        # gotdata = json.loads(myjsonData)

        data_list = mycareers.skills
        datalaist = data_list.strip("[]")
        data_list = [item.strip() for item in datalaist.split(",")]

        mainContent = ast.literal_eval(mycareers.content)
        mainjobcontent = ast.literal_eval(mycareers.jobcontent)
        content =  {
            'mycareer'  : mycareers, 
            'filter'    : myslug,
            'contentdata'   : mainContent,
            'mainjobcontent': mainjobcontent,
            'skill_list'   : data_list,
                    }
        return render(request, 'profile/careerSearch.html', content)






# QUIZ Maker -------------------------------------------------------------

from pytube import YouTube
import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip

import re

import moviepy.editor as mp
from pydub import AudioSegment

from django.conf import settings
from django.core.files.storage import FileSystemStorage


# media_full_path = settings.MEDIA_ROOT + "\playapp_data"
# upload_file_full_path = settings.STATIC_MEDIA_ROOT + "\\static\\fitnessapp\\uploaded_files"
upload_file_full_path = settings.STATIC_MEDIA_ROOT + "\\assets\\quiz"


def extract_youtube_id(url):
    """
    Extracts the YouTube video ID from a URL.
    
    Args:
    - url (str): The YouTube video URL
    
    Returns:
    - str: The YouTube video ID
    - None: If the URL is invalid or no video ID found
    """
    # Regular expression pattern to match YouTube video URLs
    youtube_pattern = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

    # Try to match the pattern in the given URL
    match = re.match(youtube_pattern, url)
    if match:
        return match.group(6)  # Return the extracted video ID
    else:
        return None  # Return None if no match found


# Function to download YouTube video
def download_video(video_url, output_filename='video.mp4', output_path='./'):
    try:
        # Create a YouTube object with the video URL
        yt = YouTube(video_url)

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video to a temporary location
        temp_file_path = os.path.join(output_path, output_filename)
        print(f"Downloading '{yt.title}' to {temp_file_path}...")
        stream.download(output_path, filename=output_filename)
        print('Download complete!')

        # Save the video file to Django's media folder, overwriting if exists
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        if fs.exists(output_filename):
            fs.delete(output_filename)  # Delete the existing file if it exists
        with open(temp_file_path, 'rb') as video_file:
            fs.save(output_filename, video_file)
            print("output_filename: ", output_filename)

        # Optionally, remove the temporary download file
        os.remove(temp_file_path)

    except Exception as e:
        print(f"Error downloading or saving video: {e}")


# Function to perform speech recognition on video's audio
def video_2_text():
    # clip = mp.VideoFileClip(r"Obama_1.mp4")

    clip = mp.VideoFileClip(r"C:\\Users\\Atharva Pawar\\Documents\\GitHub\\KLEOS2.0\\media\\video.mp4")
    clip.audio.write_audiofile(r"converted.wav")

    # Split the audio file into smaller chunks to avoid memory issues
    audio_file = AudioSegment.from_file(r"converted.wav", format="wav")
    chunk_size = 10 * 1000  # 10 seconds
    chunks = []
    for i in range(0, len(audio_file), chunk_size):
        chunks.append(audio_file[i:i + chunk_size])

    # Initialize variables for result text and summarized text
    result_text = ""

    # Create a Recognizer instance and transcribe each chunk
    r = sr.Recognizer()
    for chunk in chunks:
        try:
            with sr.AudioFile(chunk.export(format="wav")) as audio:
                audio_data = r.record(audio)
                text = r.recognize_google(audio_data)
                result_text += text + " "
        except sr.UnknownValueError:
            # Handle the case when no speech is recognized in the chunk
            print("No speech detected in a chunk.")
            continue
    # print(result_text)


    # # Write the data to the file
    # file_path = 'static/videotext.txt'
    # with open(file_path, 'w') as file:
    #     file.write(result_text)
    # print(f"Data saved to {file_path}")

    return result_text


def recommendCareerKeywords(content, min=5, max=12):
    mainTopicContext = f"""Act as a quiz generator, according to given content which is given to you, and you are master of quiz generation system.
    Quiz question count can be from min={min} to max={max}.

    content = {content}

    # rules to follow while generating output:
    - only json list data
    - no text except json list data
    - be precise and confident 
    - give major and main content

    # json list format:
    - question : min 6 words to max 20 words 
    - options : 4 options, it should be in list
    - correct_answer : 

    """

    got_topics = geminiApiCode(mainTopicContext)
    return got_topics

@login_required
def quiz(request, myslug):
    print("------------------------------------ quiz time")
    username = request.user

    if myslug == 'all':

        if request.method == 'POST':
            video_url = request.POST['ytlink']
            print("ytlink: ", video_url)

            # video_url = 'https://www.youtube.com/watch?v=x7X9w_GIm1s'
            # download_video(video_url)
            fileName = extract_youtube_id(video_url)
            fullPath = upload_file_full_path + f"\\{fileName}mp4"
            print("upload_file_full_path: ", fullPath)

            # static\assets\quiz\video.mp4
            # C:\Users\Atharva Pawar\Documents\GitHub\KLEOS2.0\static\assets\quiz
            download_video(video_url, output_path=fullPath)

            videomediapath = r"C:\\Users\\Atharva Pawar\\Documents\\GitHub\\KLEOS2.0\\media\\video.mp4"

            speechData = video_2_text()
            print("speechData: ", speechData)

            quizJson = recommendCareerKeywords(speechData)

            quiz_data = ast.literal_eval(quizJson)

            for items in quiz_data:
                gotuserData = QuizDetails.objects.create(
                    user_name=username,
                    ytlink=video_url,
                    content=speechData,
                    
                    question=items["question"],
                    options=items["options"],
                    correctanswer=items["correct_answer"],
                )


        # allQuizes = QuizDetails.objects.filter(user_name=username)
        # allQuizes = QuizDetails.objects.filter(user_name=username).values('ytlink').distinct()
        # allQuizes = QuizDetails.objects.filter(user_name=username).distinct('ytlink')

        all_quizes = QuizDetails.objects.filter(user_name=username)

        unique_ytlinks = set()
        unique_quizes = []

        for quiz in all_quizes:
            if quiz.ytlink not in unique_ytlinks:
                unique_ytlinks.add(quiz.ytlink)
                unique_quizes.append(quiz)
            # if not myrepos:
            #     myrepos = 'none'
            # print("myrepos : ", myrepos)

            # Add an index to each quiz
            indexed_quizes = [{'index': i, 'quiz': quiz} for i, quiz in enumerate(unique_quizes)]

        print("indexed_quizes: ", indexed_quizes)

        content =  {
            'allQuizes'  : indexed_quizes, 
            'filter'    : myslug
                    }
        return render(request, 'profile/quiz.html', content)

    else:
        selectedQuiz = QuizDetails.objects.get(user_name=username, id=myslug)
        fullQuiz = QuizDetails.objects.filter(user_name=username, ytlink=selectedQuiz.ytlink)

        print("fullQuiz: ",fullQuiz)

        if not fullQuiz:
            fullQuiz = 'none'

        for item in fullQuiz:
            item.options = ast.literal_eval(item.options)
        
        fullQuizoptions = fullQuiz

        content =  {
            'fullQuiz'  : fullQuiz, 
            # 'fullQuizoptions'  : fullQuizoptions, 
            'filter'    : myslug,
                    }
        return render(request, 'profile/quiz.html', content)
    

@login_required
def quizdone(request, myid, myoption):
    print("------------------------------------ quiz marking")
    username = request.user

    try:
        # Fetch the quiz object by id
        quiz = get_object_or_404(QuizDetails, id=myid)
        
        # Update useranswer field
        quiz.useranswer = myoption
        
        # Check if user answer matches correct answer
        if quiz.useranswer == quiz.correctanswer:
            quiz.iscorrect = '1'
        else:
            quiz.iscorrect = '0'
        
        # Save the updated quiz object
        quiz.save()
        
        # Optionally, return a success message or redirect
        # return HttpResponse("Quiz marked successfully.")
        return redirect('quiz', myslug=quiz.id)


    except QuizDetails.DoesNotExist:
        return HttpResponse("Quiz not found.")