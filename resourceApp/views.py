# # RoadMMap, StudyPlan, Resume Assistant 
# from django.shortcuts import render
# from django.http import HttpResponse, FileResponse
# import requests
# from django.shortcuts import render
# import os
# import google.generativeai as genai
# from PyPDF2 import PdfReader
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.chains.question_answering import load_qa_chain
# from langchain.prompts import PromptTemplate
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from dotenv import load_dotenv

# load_dotenv()
# genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))

# def downloadroadmap(request):

#     test = request.session.get('subject')
#     url = f'https://emmubucket.s3.ap-south-1.amazonaws.com/roadmapimages/{test}.png'
#     response = requests.get(url)
#     print("hello")
#     if response.status_code == 200:
#         # Set the appropriate content type for PDF files
#         file_response = FileResponse(response.content, content_type='image/png')
#         file_response['Content-Disposition'] = f'attachment; filename="{test}.png"'
#         return file_response
#     else:
#         return HttpResponse("Failed to download Roadmap", status=response.status_code)

# import datetime

# def roadmap(request):

#     url = f'https://roadmap.sh/pdfs/roadmaps/python.pdf'
#     imageurl = f'https://emmubucket.s3.ap-south-1.amazonaws.com/roadmapimages/python.png'
#     if request.method == 'POST':
#         selected_roadmap = request.POST.get('roadmap')
#         # Use selected_roadmap as needed
#         url = f'https://roadmap.sh/pdfs/roadmaps/{selected_roadmap}.pdf'
#         imageurl = f'https://emmubucket.s3.ap-south-1.amazonaws.com/roadmapimages/{selected_roadmap}.png'
    
#         request.session['subject'] = selected_roadmap

#     test = request.session.get('subject')
#     print("Test:" , test)
#     imageurl = f'https://emmubucket.s3.ap-south-1.amazonaws.com/roadmapimages/{test}.png'
#     request.session['roadmap'] = url


#     if request.method == 'POST':
#         test = request.session.get('subject')
#         imageurl = f'https://emmubucket.s3.ap-south-1.amazonaws.com/roadmapimages/{test}.png'
#         user_input = request.POST.get('user_question')   
#         genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
#     # Set up the model
#         generation_config = {
#             "temperature": 0.1,
#             "top_p": 1,
#             "top_k": 1,
#             "max_output_tokens": 2048,
#         }

#         safety_settings = [
#             {
#                 "category": "HARM_CATEGORY_HARASSMENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_HATE_SPEECH",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#         ]

#         model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                                     generation_config=generation_config,
#                                     safety_settings=safety_settings)

#         convo = model.start_chat(history=[])
#         context = f"""You are an AI educator which scrapes the pdf from the link given and provides the response to the users question in 500 words with additional links and resources for the users question. If the user asks for a flowchart give a flowchart with explanation."""
#         convo.send_message(f"{context} Link:{url}, User Question : {user_input}")
#         result = convo.last.text
#         return render(request, 'resources/roadmap.html', {'result': result,'url' : imageurl})
#     return render(request, 'resources/roadmap.html', {'url' : imageurl})

# import re

# def extract_info(text):
#   """
#   Extracts day, date, topic, and module from the provided text, handling 
#   both single-day and multi-day formats.

#   Args:
#       text: The text containing the study plan information.

#   Returns:
#       A list of dictionaries containing extracted information for each entry.
#   """
#   all_info = []
#   lines = text.splitlines()  # Split text into lines

#   for line in lines:
#     # Extract day range using a pattern for "Day \d-\d" (or "\d+") for single day)
#     day_range_pattern = r"Day (\d+)-(\d+)|Day (\d+)"
#     day_range_match = re.search(day_range_pattern, line)
    
#     # Extract dates using a pattern for YYYY-MM-DD format
#     date_pattern = r"\d{4}-\d{2}-\d{2}"
#     date_matches = re.findall(date_pattern, line)

#     if day_range_match:
#       # Extract start and end days (handle single day)
#       if len(day_range_match.groups()) == 1:
#         start_day, end_day = day_range_match.group(1), day_range_match.group(1)
#       else:
#         start_day, end_day = day_range_match.group(1), day_range_match.group(2)
      
#       # Extract all dates from matches (consider multiple matches)
#       dates = date_matches

#       # Look for module and topic information on the same line or next line
#       info_pattern = r"Module: (.*) Topic: (.*)"
#       info_match = re.search(info_pattern, line)
#       if info_match:
#         module, topic = info_match.group(1), info_match.group(2)
#       else:
#         next_line_index = lines.index(line) + 1
#         if next_line_index < len(lines):
#           module_match = re.search(r"Module: (.*)", lines[next_line_index])
#           topic_match = re.search(r"Topic: (.*)", lines[next_line_index])
#           if module_match:
#             module = module_match.group(1)
#           else:
#             module = None
#           if topic_match:
#             topic = topic_match.group(1)
#           else:
#             topic = None
#         else:
#           module = None
#           topic = None
        
#       # Create info dictionary for this entry
#       info = {
#           "day": f"Day {start_day}-{end_day}" if len(dates) > 1 else f"Day {start_day}",
#           "date": dates if len(dates) > 1 else dates[0],  # Use list if multiple dates, else single date
#           "module": module,
#           "topic": topic
#       }
#       all_info.append(info)

#   return all_info if all_info else None

# from roadmapper.roadmap import Roadmap
# from roadmapper.timelinemode import TimelineMode

# def studyplan(request):
#     today = datetime.date.today()
#     print(today)
#     selectedroadmap = request.session.get('roadmap','None')
#     subject = request.session.get('subject','None')
#     print(selectedroadmap)
#     url = selectedroadmap
#     if request.method == 'POST':
#         #take days months, how many hours per day ,
#         days_to_study = request.POST.get('days_to_study')
#         hours_per_day = request.POST.get('hours_per_day')

#         print(days_to_study)
#         print(hours_per_day)   

#         genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
#     # Set up the model
#         generation_config = {
#             "temperature": 0.1,
#             "top_p": 1,
#             "top_k": 1,
#             "max_output_tokens": 2048,
#         }

#         safety_settings = [
#             {
#                 "category": "HARM_CATEGORY_HARASSMENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_HATE_SPEECH",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#             {
#                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#                 "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#             },
#         ]

#         model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                                     generation_config=generation_config,
#                                     safety_settings=safety_settings)

#         convo = model.start_chat(history=[])
#         context = f"""You are an AI Study plan maker which scrapes the pdf from the link given and generates a study plan for the respective subject in the roadmap.Create the study plan starting from Today that is {today} and include the actual dates in the response . The date should be in the format of YYYY-MM-DD. 
#         For Example, 
#         Day 1 (2023-05-05)
#         Module: Introduction to Android Development
#         Time: 2 hours     
#         OR    
#         Day 1-3 (2023-05-05 - 2023-05-08)
#         Module: Introduction to Android Development
#         Topic: Setting up your Android development environment
#         Time: 3 hours.      
        
#         Strictly include Module and Topic and follow the example above . Give Short Description at the begninning and Tips at the End """
#         convo.send_message(f"{context} Link:{url}, User Schedule : I have {days_to_study} days to complete the course and can study for {hours_per_day} hours per day  ")
#         result = convo.last.text

#         extracted_info = extract_info(result)



#         roadmap = Roadmap(1700, 1000, colour_theme="BLUEMOUNTAIN")
#         roadmap.set_title(f"Study Timeline for {subject}")
#         roadmap.set_subtitle("Study Planner")
#         roadmap.set_timeline(TimelineMode.WEEKLY, start="2024-04-23", number_of_items=3)
#         group = roadmap.add_group(subject,text_alignment="left")
#         for day_info in extracted_info:
#             print(f"Date: {day_info['date']}")
#             print(f"Module: {day_info['module']}")  
            
#             if isinstance(day_info['date'], list):
#                 start_date, end_date = day_info['date'][0], day_info['date'][1]
#             else:
#                 start_date = end_date = day_info['date']
#             if day_info['module']:
#                 task = group.add_task(day_info['module'], start_date, end_date,font_size=15)
#             else:
#                task = group.add_task("Refresh", start_date, end_date,font_size=15)
        
#         parellel_task = task.add_parallel_task("Enhancements", "2024-11-15", "2025-03-31")
#         parellel_task.add_milestone("v.2.0", "2025-03-30")

#         task.add_parallel_task("Showcase #2", "2024-06-01", "2024-08-07")
        

           
#         roadmap.draw()
#         roadmap.save("static/roadmap.png")

#         if extracted_info:
#             for day_info in extracted_info:
                
#                 print(f"Day: {day_info['day']}")
#                 print(f"Date: {day_info['date']}")
#                 print(f"Module: {day_info['module']}")  # Will be None for this format
#                 print(f"Topic: {day_info['topic']}")
#                 print("-" * 20)  # Separator between entries
#             else:
#                 print("No information found in the provided text.")
    
   
        
        

#         # roadmap.set_footer("Generated by Roadmapper")
        
            
#         return render(request, 'studyplan/studyplan.html', {'result': result,'url' : url,'subject':subject})
#     return render(request, 'studyplan/studyplan.html', {'url' : url,'subject':subject})


# #resumeAssistant

# def get_pdf_text(pdf_docs):
#     text=""
#     for pdf in pdf_docs:
#         pdf_reader= PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text+= page.extract_text()
#     return  text

# def get_vector_store(text_chunks):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
#     vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
#     vector_store.save_local("faiss_index")

# def get_conversational_chain():

#     prompt_template = """
#     You are a Resume Analyzer and Chatbot. Your task is to analyze the provided resume and return a  JSON response strictly that includes the following details:

#     Keywords: Extract and list key skills, technologies, and relevant terms found in the resume.
#     Sections: Identify and list the main sections of the resume (e.g., Education, Work Experience, Skills, Projects).
#     Score: Assign a score out of 100 based on the overall quality and relevance of the resume.
#     Improvements: Suggest areas for improvement to enhance the resume.
#     Answer: Provide a direct answer to any specific question asked by the user related to their resume. \n\n
#     Resume:\n {context}?\n
#     Question: \n{question}\n

#     Answer:
#     """

#     model = ChatGoogleGenerativeAI(model="gemini-pro",
#                              temperature=0.1)

#     prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
#     chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
#     return chain

# def user_input(user_question):
#     embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
#     new_db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
#     docs = new_db.similarity_search(user_question)

#     chain = get_conversational_chain()

    
#     response = chain(
#         {"input_documents":docs, "question": user_question}
#         , return_only_outputs=True)

#     return response

# def get_text_chunks(text):
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
#     chunks = text_splitter.split_text(text)
#     return chunks


# from django.contrib.auth.decorators import login_required
# import json
# from graph import graph_agent

    
# @login_required
# def resumeassistant(request):
#     if request.method == 'POST' and request.FILES.get('pdf_files'):
#         pdf_docs = request.FILES.getlist('pdf_files')
#         user_question = request.POST.get('user_question')

#         raw_text = get_pdf_text(pdf_docs)
#         text_chunks = get_text_chunks(raw_text)
#         get_vector_store(text_chunks)
#         result = user_input(user_question)
#         print(result)
#         print("--------------------------------------------")
#         final_result = result['output_text']

#         cleaned_string = final_result.replace("'", '')
#         clean_string = cleaned_string.replace('\n', '').replace('\\', '').replace('```', '').replace('json', '')
        
#         final_data = json.loads(clean_string) 
#         # print(json.dumps(final_data, indent=4))


#         return render(request,'resources/resume.html',{'response_text':final_data})
#     return render(request,'resources/resume.html')
