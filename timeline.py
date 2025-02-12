import google.generativeai as genai
import os

genai.configure(api_key=(os.getenv("GOOGLE_API_KEY")))  # Set up your API key
# Set up the model
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

mainTopicContext = f"""Act as a career main topic generator, according to career which is given you in that career you are the master and teacher.
the main topics count can be from min=5 to max=10.

career = ML Engineer

# rules to follow while generating output:
- only json list data
- no text except json list data
- be precise and confident 
- give major and main content

# json list format:
- topic
- topics description : in 10 to 20 words
- duration : give minimum time required to learn & complete this topic in (hrs, days, months : only)
"""


subTopicContext = f"""Act as a subtopic generator for the main topic given, according to topic which is given you in that career you are the master and teacher.
the sub topics count can be from min=10 to max=30.

topic = Machine Learning Fundamentals

# rules to follow while generating output:
- only json list data
- no text except json list data
- be precise and confident 
- give major and main content

# json list format:
- subtopic
- subtopic description : in 30 to 60 words
- duration : give minimum time required to learn & complete this topic in (hrs, days, months : only)
"""

# convo.send_message(context)
convo.send_message(subTopicContext)
result = convo.last.text


cleaned_string = result.replace("'", '')
clean_string = cleaned_string.replace('\n', '').replace('\\', '').replace('```', '').replace('json', '')
print("GenOutput: ", clean_string)                                                                                        


topicgentext = """
[
  {
    "topic": "Machine Learning Fundamentals",
    "topic_description": "Introduction to ML, supervised and unsupervised learning, model evaluation",
    "duration": "1 month"
  },
  {
    "topic": "Data Preprocessing and Feature Engineering",
    "topic_description": "Data cleaning, transformation, feature selection, dimensionality reduction",
    "duration": "2 weeks"
  },
  {
    "topic": "Supervised Learning Algorithms",
    "topic_description": "Linear regression, logistic regression, decision trees, support vector machines",
    "duration": "3 weeks"
  },
  {
    "topic": "Unsupervised Learning Algorithms",
    "topic_description": "Clustering, dimensionality reduction, anomaly detection",
    "duration": "2 weeks"
  },
  {
    "topic": "Model Selection and Evaluation",
    "topic_description": "Cross-validation, hyperparameter tuning, model comparison",
    "duration": "1 week"
  },
  {
    "topic": "Deep Learning",
    "topic_description": "Neural networks, convolutional neural networks, recurrent neural networks",
    "duration": "2 months"
  },
  {
    "topic": "Cloud Computing for ML",
    "topic_description": "AWS, Azure, GCP, distributed computing, big data processing",
    "duration": "1 month"
  },
  {
    "topic": "ML Engineering Best Practices",
    "topic_description": "Software engineering principles, version control, documentation, testing",
    "duration": "1 week"
  },
  {
    "topic": "Ethical Considerations in ML",
    "topic_description": "Bias, fairness, privacy, transparency, accountability",
    "duration": "1 week"
  },
  {
    "topic": "Advanced ML Topics",
    "topic_description": "Reinforcement learning, generative models, natural language processing",
    "duration": "2 months"
  }
]
"""

subTopicGenText = """
[
  {
    "subtopic": "Introduction to Machine Learning",
    "subtopic description": "Overview of machine learning, its types, and applications in various domains.",
    "duration": "1 day"
  },
  {
    "subtopic": "Supervised Learning",
    "subtopic description": "Understanding supervised learning algorithms, such as linear regression, logistic regression, and decision trees.",
    "duration": "2 days"
  },
  {
    "subtopic": "Unsupervised Learning",
    "subtopic description": "Exploring unsupervised learning algorithms, such as clustering, dimensionality reduction, and anomaly detection.",
    "duration": "2 days"
  },
  {
    "subtopic": "Model Evaluation and Selection",
    "subtopic description": "Techniques for evaluating machine learning models, including metrics, cross-validation, and hyperparameter tuning.",
    "duration": "1 day"
  },
  {
    "subtopic": "Feature Engineering",
    "subtopic description": "Importance of feature engineering, techniques for feature selection, transformation, and creation.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Libraries",
    "subtopic description": "Overview of popular machine learning libraries, such as scikit-learn, TensorFlow, and PyTorch.",
    "duration": "1 day"
  },
  {
    "subtopic": "Natural Language Processing (NLP)",
    "subtopic description": "Introduction to NLP, text preprocessing, feature extraction, and NLP applications.",
    "duration": "2 days"
  },
  {
    "subtopic": "Computer Vision",
    "subtopic description": "Fundamentals of computer vision, image processing, object detection, and image classification.",
    "duration": "2 days"
  },
  {
    "subtopic": "Time Series Analysis",
    "subtopic description": "Understanding time series data, forecasting techniques, and applications in various domains.",
    "duration": "1 day"
  },
  {
    "subtopic": "Reinforcement Learning",
    "subtopic description": "Introduction to reinforcement learning, reward functions, and applications in robotics and game playing.",
    "duration": "1 day"
  },
  {
    "subtopic": "Deep Learning",
    "subtopic description": "Overview of deep learning, neural networks, convolutional neural networks, and recurrent neural networks.",
    "duration": "2 days"
  },
  {
    "subtopic": "Machine Learning Ethics",
    "subtopic description": "Ethical considerations in machine learning, such as bias, fairness, and privacy.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Healthcare",
    "subtopic description": "Applications of machine learning in healthcare, including disease diagnosis, drug discovery, and personalized medicine.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Finance",
    "subtopic description": "Applications of machine learning in finance, including fraud detection, risk assessment, and algorithmic trading.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Manufacturing",
    "subtopic description": "Applications of machine learning in manufacturing, including predictive maintenance, quality control, and process optimization.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Transportation",
    "subtopic description": "Applications of machine learning in transportation, including traffic prediction, route optimization, and autonomous vehicles.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Retail",
    "subtopic description": "Applications of machine learning in retail, including customer segmentation, personalized recommendations, and inventory optimization.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Energy",
    "subtopic description": "Applications of machine learning in energy, including renewable energy forecasting, energy efficiency, and smart grid management.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Agriculture",
    "subtopic description": "Applications of machine learning in agriculture, including crop yield prediction, disease detection, and precision farming.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Education",
    "subtopic description": "Applications of machine learning in education, including personalized learning, student assessment, and educational data mining.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Government",
    "subtopic description": "Applications of machine learning in government, including fraud detection, policy analysis, and public service optimization.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Cybersecurity",
    "subtopic description": "Applications of machine learning in cybersecurity, including intrusion detection, malware analysis, and threat intelligence.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Social Media",
    "subtopic description": "Applications of machine learning in social media, including sentiment analysis, community detection, and content recommendation.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Gaming",
    "subtopic description": "Applications of machine learning in gaming, including AI-powered opponents, game design optimization, and player behavior analysis.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Robotics",
    "subtopic description": "Applications of machine learning in robotics, including navigation, object manipulation, and human-robot interaction.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Space Exploration",
    "subtopic description": "Applications of machine learning in space exploration, including data analysis, anomaly detection, and autonomous navigation.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Climate Science",
    "subtopic description": "Applications of machine learning in climate science, including climate modeling, weather forecasting, and climate change analysis.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Drug Discovery",
    "subtopic description": "Applications of machine learning in drug discovery, including target identification, lead optimization, and clinical trial design.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Materials Science",
    "subtopic description": "Applications of machine learning in materials science, including materials design, property prediction, and materials discovery.",
    "duration": "1 day"
  },
  {
    "subtopic": "Machine Learning Applications in Financial Services",
    "subtopic description": "Applications of machine learning in financial services, including risk management, fraud detection, and algorithmic trading.",
    "duration": "1 day"
  }
]
"""


import json

# Convert the string to JSON data
json_data = json.loads(clean_string)

# Print the JSON data
print(json.dumps(json_data, indent=2))



'''

You are an AI assistant tasked with helping users identify all the skills required for their dream job. Given a specific dream role, generate a detailed list of technical and soft skills necessary for excelling in that role. Your response should include only the names of the skills, presented in a JSON format.
    if it includes any programming language mention it in the Technical Skills itself.
Example:

    "dream_role": "Data Scientist",
    "skills": 
        "technical_skills": [
        "Python",
        "R",
        "Statistical Analysis",
        "Data Visualization",
        "Machine Learning Algorithms",
        "Big Data Technologies"
        ],
        "soft_skills": [
        "Problem-Solving",
        "Communication",
        "Critical Thinking"
        ]
'''