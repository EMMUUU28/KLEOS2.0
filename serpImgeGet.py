from serpapi import GoogleSearch

def getImgLink(userQuery):
    params = {
        "engine": "google_images",
        "q": f"roadmap for {userQuery}",
        "location": "Mumbai, Maharashtra, India",
        "api_key": "3fb9e0be680fbc384833423e983140627c494f8d1468c6dc9d1282661ede94e6"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results

def extract_image_urls(results, max_images=4):
    # Extract image URLs from the results
    image_urls = []
    for image_result in results.get("images_results", []):
        image_urls.append(image_result.get("original"))
        if len(image_urls) >= max_images:
            break
    return image_urls

userQuery = 'geology'
gotresult = getImgLink(userQuery)

# Extract the image URLs
image_urls = extract_image_urls(gotresult)

# Print the image URLs
for url in image_urls:
    print(url)

import requests
import base64

def image_to_base64(url):
    try:
        # Fetching the image from URL
        response = requests.get(url)
        if response.status_code == 200:
            # Encoding the image content to base64
            base64_data = base64.b64encode(response.content)
            # Decoding to a string (if using Python 3, base64_data is already a bytes-like object)
            base64_string = base64_data.decode('utf-8')
            # Print the base64 encoded string
            print(base64_string)
        else:
            print(f"Failed to retrieve image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage
# url = "https://pcccreative.org/wp-content/uploads/2012/07/geology-roadmap1.jpg"
url = image_urls[0]
imgbase64Var = image_to_base64(url)


import requests
import base64

def getGenText(img_base64):
    url = 'https://b553-34-105-55-3.ngrok-free.app/process_image'
    data = {'imgbase64': img_base64}
    response = requests.post(url, json=data)
    # print(response.json())

    # Parse JSON response and print only the 'message' value
    message_value = response.json().get('message', None)
    if message_value:
        print(message_value)
        return message_value
    else:
        print("No 'message' key found in the response.")
        return "No 'message' key found in the response."


roadmapKeywords = getGenText(imgbase64Var)

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

geminiPrompt = f"""below are the keywords of the career, give me the summary of the roadmap keywords, dont mention "keyoword" in summary
the summary should be in detailed around 80 to 150 words, be precise and help the human to build his career and have a grate future {roadmapKeywords} """




'''
https://pcccreative.org/wp-content/uploads/2012/07/geology-roadmap1.jpg
https://www.researchgate.net/publication/355137324/figure/fig1/AS:1076880224591872@1633759661078/Roadmap-of-3D-geological-modeling-technology.png
https://www.researchgate.net/profile/Gye-Chun-Cho/publication/263467683/figure/fig4/AS:614062375333890@1523415287357/Korean-geologic-CO-2-storage-technology-roadmap-Presidential-Committee-on-Green-Growth.png
https://www.visualcapitalist.com/wp-content/uploads/2018/03/mineral-exploration-roadmap-share.jpg
'''