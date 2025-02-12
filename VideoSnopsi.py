from pytube import YouTube
import os
import re

import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment

import requests



def video_2_text():
    # clip = mp.VideoFileClip(r"Obama_1.mp4")

    clip = mp.VideoFileClip(r"video.mp4")
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


# speechText = video_2_text()
# print("speechText: ", speechText)


speechText = '''
Python a high level interpreted programming language famous for its Zen like code it's arguably the most popular language in the world because it's easy to learn and released in 1991 who named is commonly used to build server side applications like web apps with machine learning many students because of its emphasis on readability as out Temptation to Sprinkle and magic that causes MCQ individual cells can be executed then documented in the same place for current and you can get started equal to a value its strongly typed which means value is more unexpected ways but dynamics are not required the syntax is highly efficient allowing you to clear multiple variables on a single line and define two poles list will say that your code is not pythonic instead of semicolons python indentation to terminate or determine the scope of a line of code define a function with the duck keyword then intent the next line usually by four spaces to define the function body found in many other languages Python is a multi paradigm language five functional programming patterns with things like anonymous functions using Lambda it also uses objects as an abstraction for data allowing you to implement object oriented patterns but things it also has a huge ecosystem of third party libraries such as deep learning frameworks like tensorflow and wrappers for many high performance low level packages open computer vision which are most often installed without package manager this is the Python programming language in 100 seconds hit the like button if you want to see more short videos like this for watching and I will see you in the next one
'''

# print(recommendCareerKeywords(speechText))

QuizData = [  
    {    "question": "When was Python programming language released?",    "options": [      "1989",      "1991",      "1993",      "1995"    ],    "correct_answer": "1991"  },  
    
    
    {    "question": "What is Python commonly used for?",    "options": [      "Web applications",      "Machine learning",      "Desktop applications",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a key feature of Pythons syntax?",    "options": [      "Indentation",      "Semicolons",      "Curly braces",      "Angle brackets"    ],    "correct_answer": "Indentation"  },  {    "question": "What is a unique characteristic of Pythons type system?",    "options": [      "Strongly typed",      "Dynamically typed",      "Statically typed",      "Weakly typed"    ],    "correct_answer": "Strongly typed"  },  {    "question": "What is a benefit of Pythons multi-paradigm nature?",    "options": [      "Allows for different programming styles",      "Improves code readability",      "Reduces development time",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a popular third-party library for deep learning in Python?",    "options": [      "TensorFlow",      "PyTorch",      "Keras",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is the purpose of the duck keyword in Python?",    "options": [      "To define a function",      "To create a class",      "To import a module",      "To terminate a line of code"    ],    "correct_answer": "To define a function"  },  {    "question": "What is a key advantage of Pythons ecosystem?",    "options": [      "Large number of third-party libraries",      "Easy installation of packages",      "Support for high-performance computing",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a common criticism of Pythons syntax?",    "options": [      "Too verbose",      "Difficult to read",      "Inconsistent",      "All of the above"    ],    "correct_answer": "Too verbose"  },  {    "question": "What is a unique feature of Pythons object-oriented programming capabilities?",    "options": [      "Use of objects as abstractions for data",      "Support for multiple inheritance",      "Dynamic binding",      "All of the above"    ],    "correct_answer": "Use of objects as abstractions for data"  },  {    "question": "What is a key benefit of Pythons emphasis on readability?",    "options": [      "Reduced development time",      "Improved code maintainability",      "Increased code efficiency",      "All of the above"    ],    "correct_answer": "Improved code maintainability"  },  {    "question": "What is a common use case for Pythons lambda functions?",    "options": [      "Creating anonymous functions",      "Implementing functional programming patterns",      "Defining event handlers",      "All of the above"    ],    "correct_answer": "All of the above"  }]
[  {    "question": "When was Python programming language released?",    "options": [      "1989",      "1991",      "1993",      "1995"    ],    "correct_answer": "1991"  },  {    "question": "What is Python commonly used for?",    "options": [      "Web applications",      "Machine learning",      "Desktop applications",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a key feature of Pythons syntax?",    "options": [      "Indentation",      "Semicolons",      "Curly braces",      "Angle brackets"    ],    "correct_answer": "Indentation"  },  {    "question": "What is a unique characteristic of Pythons type system?",    "options": [      "Strongly typed",      "Dynamically typed",      "Statically typed",      "Weakly typed"    ],    "correct_answer": "Strongly typed"  },  {    "question": "What is a benefit of Pythons multi-paradigm nature?",    "options": [      "Allows for different programming styles",      "Improves code readability",      "Reduces development time",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a popular third-party library for deep learning in Python?",    "options": [      "TensorFlow",      "PyTorch",      "Keras",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is the purpose of the duck keyword in Python?",    "options": [      "To define a function",      "To create a class",      "To import a module",      "To terminate a line of code"    ],    "correct_answer": "To define a function"  },  {    "question": "What is a key advantage of Pythons ecosystem?",    "options": [      "Large number of third-party libraries",      "Easy installation of packages",      "Support for high-performance computing",      "All of the above"    ],    "correct_answer": "All of the above"  },  {    "question": "What is a common criticism of Pythons syntax?",    "options": [      "Too verbose",      "Difficult to read",      "Inconsistent",      "All of the above"    ],    "correct_answer": "Too verbose"  },  {    "question": "What is a unique feature of Pythons object-oriented programming capabilities?",    "options": [      "Use of objects as abstractions for data",      "Support for multiple inheritance",      "Dynamic binding",      "All of the above"    ],    "correct_answer": "Use of objects as abstractions for data"  },  {    "question": "What is a key benefit of Pythons emphasis on readability?",    "options": [      "Reduced development time",      "Improved code maintainability",      "Increased code efficiency",      "All of the above"    ],    "correct_answer": "Improved code maintainability"  },  {    "question": "What is a common use case for Pythons lambda functions?",    "options": [      "Creating anonymous functions",      "Implementing functional programming patterns",      "Defining event handlers",      "All of the above"    ],    "correct_answer": "All of the above"  }]