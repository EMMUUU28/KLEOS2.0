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

# careername = "i am doing electrical enginnering and i am in 2nd year and i have 4 kts, i dont want to continue in this career give me another career path, my other skilles are i am good in commerce, "

careername = '''
You are a career counselor tasked with advising individuals who want to explore new career paths based on their existing skills. Write a comprehensive recommendation for one of your clients, detailing three alternative career options that align with their skill set. Include a brief description of each career path, highlighting how their current skills can be applied effectively in these new roles. Consider the client's strengths, interests, and any additional information that might influence their career choices.
'''
print(recommendCareer(careername))

'''
GenOutput:  [  {    "careertitle": "Financial Analyst",    "careertitle_description": "Financial analysts provide advice to individuals and organizations on investment decisions. They analyze financial data, make recommendations, and develop investment strategies.",    "duration": "12 months"  },  {    "careertitle": "Accountant",    "careertitle_description": "Accountants prepare and examine financial records. They ensure that financial information is accurate and compliant with regulations.",    "duration": "18 months"  },  {    "careertitle": "Business Analyst",    "careertitle_description": "Business analysts identify and solve business problems. They analyze data, develop solutions, and implement changes to improve efficiency and profitability.",    "duration": "12 months"  },  {    "careertitle": "Marketing Manager",    "careertitle_description": "Marketing managers plan and execute marketing campaigns. They develop strategies, create content, and manage budgets to promote products and services.",    "duration": "18 months"  },  {    "careertitle": "Sales Manager",    "careertitle_description": "Sales managers lead and motivate sales teams. They set targets, develop strategies, and provide training to maximize sales performance.",    "duration": "12 months"  }]
[  {    "careertitle": "Financial Analyst",    "careertitle_description": "Financial analysts provide advice to individuals and organizations on investment decisions. They analyze financial data, make recommendations, and develop investment strategies.",    "duration": "12 months"  },  {    "careertitle": "Accountant",    "careertitle_description": "Accountants prepare and examine financial records. They ensure that financial information is accurate and compliant with regulations.",    "duration": "18 months"  },  {    "careertitle": "Business Analyst",    "careertitle_description": "Business analysts identify and solve business problems. They analyze data, develop solutions, and implement changes to improve efficiency and profitability.",    "duration": "12 months"  },  {    "careertitle": "Marketing Manager",    "careertitle_description": "Marketing managers plan and execute marketing campaigns. They develop strategies, create content, and manage budgets to promote products and services.",    "duration": "18 months"  },  {    "careertitle": "Sales Manager",    "careertitle_description": "Sales managers lead and motivate sales teams. They set targets, develop strategies, and provide training to maximize sales performance.",    "duration": "12 months"  }]
'''