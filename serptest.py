from serpapi import GoogleSearch


# params = {
#             "engine": "youtube",
#             "search_query": "Introduction to Machine Learning" + "Tutorial Playlist",
#             "api_key": "3fb9e0be680fbc384833423e983140627c494f8d1468c6dc9d1282661ede94e6"
#         }

# search = GoogleSearch(params)
# results = search.get_dict()

# print("results: ", results)




textVar = """
results:  {'search_metadata': {'id': '6675e726c9de45bb747e912c', 'status': 'Success', 'json_endpoint': 'https://serpapi.com/searches/f933f8d3a9843322/6675e726c9de45bb747e912c.json', 'created_at': '2024-06-21 20:48:38 UTC', 'processed_at': '2024-06-21 20:48:38 UTC', 'youtube_url': 'https://www.youtube.com/results?search_query=Introduction+to+Machine+LearningTutorial+Playlist', 'raw_html_file': 'https://serpapi.com/searches/f933f8d3a9843322/6675e726c9de45bb747e912c.html', 'total_time_taken': 2.4}, 'search_parameters': {'engine': 'youtube', 'search_query': 'Introduction to Machine LearningTutorial Playlist'}, 'search_information': {'total_results': 15829102, 'video_results_state': 'Some results for exact spelling but showing fixed spelling', 'query_displayed': 'Introduction to Machine LearningTutorial Playlist', 'spelling_fix': 'Introduction to Machine ', 'showing_results_for': 'Introduction to Machine '}, 'playlist_results': [{'position_on_page': 1, 'title': 'Machine Learning Tutorial Python | Machine Learning For Beginners', 'link': 'https://www.youtube.com/watch?v=gmvvaobm7eQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw', 'channel': {'name': 'codebasics', 'link': 'https://www.youtube.com/@codebasics', 'verified': True}, 'video_count': 42, 'videos': [{'title': 'Machine Learning Tutorial Python -1: What is Machine Learning?', 'link': 'https://www.youtube.com/watch?v=gmvvaobm7eQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw', 'length': '6:51'}, {'title': 'Machine Learning Tutorial Python - 2: Linear Regression Single Variable', 'link': 'https://www.youtube.com/watch?v=8jazNUpO3lQ&list=PLeo1K3hjS3uvCeTYTeyfe0-rN5r8zn9rw', 'length': '15:14'}], 'thumbnail': 'https://i.ytimg.com/vi/gmvvaobm7eQ/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDo3DK0bXB5WaiRsCKB87xGbWIDEw'}, {'position_on_page': 2, 'title': '🔥Machine Learning | Machine Learning Tutorial For Beginners | Machine Learning Projects | Simplilearn | Updated Machine Learning Playlist 2024', 'link': 'https://www.youtube.com/watch?v=ukzFI9rgwfU&list=PLEiEAq2VkUULYYgj13YHUWmRePqiu8Ddy', 'channel': {'name': 'Simplilearn', 'link': 'https://www.youtube.com/@SimplilearnOfficial', 'verified': True}, 'video_count': 174, 'videos': [{'title': 'Machine Learning | What Is Machine Learning? | Introduction To Machine Learning | 2024 | Simplilearn', 'link': 'https://www.youtube.com/watch?v=ukzFI9rgwfU&list=PLEiEAq2VkUULYYgj13YHUWmRePqiu8Ddy', 'length': '7:52'}, {'title': 'Machine Learning | What Is Machine Learning? | Machine Learning Basics | 2023 | Simplilearn', 'link': 'https://www.youtube.com/watch?v=cfSDvPlFFVQ&list=PLEiEAq2VkUULYYgj13YHUWmRePqiu8Ddy', 'length': '1:56'}], 'thumbnail': 'https://i.ytimg.com/vi/ukzFI9rgwfU/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLBoILWHb0JbXYApNdmO-TK3Rou5Tg'}, {'position_on_page': 3, 'title': 'Introduction to Machine Learning', 'link': 'https://www.youtube.com/watch?v=T3PsRW6wZSY&list=PLIg1dOXc_acbdJo-AE5RXpIM_rvwrerwR', 'channel': {'name': 'Machine Learning- Sudeshna Sarkar', 'link': 'https://www.youtube.com/@machinelearning-sudeshnasa3607'}, 'video_count': 44, 'videos': [{'title': 'Introduction', 'link': 'https://www.youtube.com/watch?v=T3PsRW6wZSY&list=PLIg1dOXc_acbdJo-AE5RXpIM_rvwrerwR', 'length': '28:44'}, {'title': 'Different Types of Learning', 'link': 'https://www.youtube.com/watch?v=EWmCkVfPnJ8&list=PLIg1dOXc_acbdJo-AE5RXpIM_rvwrerwR', 'length': '24:55'}], 'thumbnail': 'https://i.ytimg.com/vi/T3PsRW6wZSY/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDZV8J09JpUoocWgubDje4EIwUOYQ'}, {'position_on_page': 4, 'title': 'MIT 6.S191: Introduction to Deep Learning', 'link': 'https://www.youtube.com/watch?v=ErnWZxJovaM&list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI', 'channel': {'name': 'Alexander Amini', 'link': 'https://www.youtube.com/@AAmini'}, 'video_count': 71, 'videos': [{'title': 'MIT Introduction to Deep Learning | 6.S191', 'link': 'https://www.youtube.com/watch?v=ErnWZxJovaM&list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI', 'length': '1:09:58'}, {'title': 'MIT 6.S191: Recurrent Neural Networks, Transformers, and Attention', 'link': 'https://www.youtube.com/watch?v=dqoEU9Ac3ek&list=PLtBw6njQRU-rwp5__7C0oIVt26ZgjG9NI', 'length': '1:01:31'}], 'thumbnail': 'https://i.ytimg.com/vi/ErnWZxJovaM/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLD26bJRtpZevB5d8t50X8bRbEcr3A'}, {'position_on_page': 6, 'title': 'Stanford CS229: Machine Learning Full Course taught by Andrew Ng | Autumn 2018', 'link': 'https://www.youtube.com/watch?v=jGwO_UgTS7I&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU', 'channel': {'name': 'Stanford Online', 'link': 'https://www.youtube.com/@stanfordonline', 'verified': True}, 'video_count': 20, 'videos': [{'title': 'Stanford CS229: Machine Learning Course, Lecture 1 - Andrew Ng (Autumn 2018)', 'link': 'https://www.youtube.com/watch?v=jGwO_UgTS7I&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU', 'length': '1:15:20'}, {'title': 'Stanford CS229: Machine Learning - Linear Regression and Gradient Descent |  Lecture 2 (Autumn 2018)', 'link': 'https://www.youtube.com/watch?v=4b4MUYve_U8&list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU', 'length': '1:18:17'}], 'thumbnail': 'https://i.ytimg.com/vi/jGwO_UgTS7I/hqdefault.jpg?sqp=-oaymwEwCKgBEF5IWvKriqkDIwgBFQAAiEIYAfABAfgB_gmAAtAFigIMCAAQARhlIGUoZTAP&rs=AOn4CLAP_TcODah-q53YXGH4G6ZReougNg'}, {'position_on_page': 7, 'title': 'Machine Learning with Python', 'link': 'https://www.youtube.com/watch?v=OGxgnH8y2NM&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v', 'channel': {'name': 'sentdex', 'link': 'https://www.youtube.com/@sentdex', 'verified': True}, 'video_count': 72, 'videos': [{'title': 'Practical Machine Learning Tutorial with Python Intro p.1', 'link': 'https://www.youtube.com/watch?v=OGxgnH8y2NM&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v', 'length': '5:55'}, {'title': 'Regression Intro - Practical Machine Learning Tutorial with Python p.2', 'link': 'https://www.youtube.com/watch?v=JcI5Vnw0b2c&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v', 'length': '10:58'}], 'thumbnail': 'https://i.ytimg.com/vi/OGxgnH8y2NM/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLBJ-Kxm4AJEhfcghsBbG09KTJ3GRQ'}, {'position_on_page': 10, 'title': 'Machine Learning Specialization by Andrew Ng', 'link': 'https://www.youtube.com/watch?v=vStJoetOxJg&list=PLkDaE6sCZn6FNC6YRfRQc_FbeQrF8BwGI', 'channel': {'name': 'DeepLearningAI', 'link': 'https://www.youtube.com/@Deeplearningai'}, 'video_count': 41, 'videos': [{'title': '#1 Machine Learning Specialization [Course 1, Week 1, Lesson 1]', 'link': 'https://www.youtube.com/watch?v=vStJoetOxJg&list=PLkDaE6sCZn6FNC6YRfRQc_FbeQrF8BwGI', 'length': '2:45'}, {'title': '#2 Machine Learning Specialization [Course 1, Week 1, Lesson 1]', 'link': 'https://www.youtube.com/watch?v=wiNXzydta4c&list=PLkDaE6sCZn6FNC6YRfRQc_FbeQrF8BwGI', 'length': '4:29'}], 'thumbnail': 'https://i.ytimg.com/vi/vStJoetOxJg/hqdefault.jpg?sqp=-oaymwEwCKgBEF5IWvKriqkDIwgBFQAAiEIYAfABAfgB_gmAAtAFigIMCAAQARhlIGUoZTAP&rs=AOn4CLBKMALZc05L4CjgBroHudhzvUsjCA'}, {'position_on_page': 11, 'title': 'Machine Learning', 'link': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF', 'channel': {'name': 'StatQuest with Josh Starmer', 'link': 'https://www.youtube.com/@statquest', 'verified': True}, 'video_count': 98, 'videos': [{'title': 'A Gentle Introduction to Machine Learning', 'link': 'https://www.youtube.com/watch?v=Gv9_4yMHFhI&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF', 'length': '12:45'}, {'title': 'Machine Learning Fundamentals: Cross Validation', 'link': 'https://www.youtube.com/watch?v=fSytzGwwBVw&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF', 'length': '6:05'}], 'thumbnail': 'https://i.ytimg.com/vi/Gv9_4yMHFhI/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDVMMcBDYFDMXFzBS6fWQScIc2l6g'}, {'position_on_page': 14, 'title': 'Complete Machine Learning playlist', 'link': 'https://www.youtube.com/watch?v=bPrmA1SEN2k&list=PLZoTAELRMXVPBTrWtJkn3wWQxZkmTXGwe', 'channel': {'name': 'Krish Naik', 'link': 'https://www.youtube.com/@krishnaik06', 'verified': True}, 'video_count': 153, 'videos': [{'title': 'Complete Road Map To Be Expert In Python- Follow My Way', 'link': 'https://www.youtube.com/watch?v=bPrmA1SEN2k&list=PLZoTAELRMXVPBTrWtJkn3wWQxZkmTXGwe', 'length': '29:11'}, {'title': 'Complete Roadmap To Follow To  Prepare Machine Learning With All Videos And Materials', 'link': 'https://www.youtube.com/watch?v=VOpETRQGXy0&list=PLZoTAELRMXVPBTrWtJkn3wWQxZkmTXGwe', 'length': '18:56'}], 'thumbnail': 'https://i.ytimg.com/vi/bPrmA1SEN2k/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLAehZrTbox7ty15yIX9r3Wg4OSpZg'}, {'position_on_page': 15, 'title': 'Machine Learning Tutorial in Python | Edureka', 'link': 'https://www.youtube.com/watch?v=GwIo3gDZCVQ&list=PL9ooVrP1hQOHUfd-g8GUpKI3hHOwM_9Dn', 'channel': {'name': 'edureka!', 'link': 'https://www.youtube.com/@edurekaIN', 'verified': True}, 'video_count': 106, 'videos': [{'title': 'Machine Learning Full Course - Learn Machine Learning 10 Hours | Machine Learning Tutorial | Ed

"""


# import re

# def extract_youtube_urls(inText):
#     # Define the regex pattern for YouTube URLs
#     youtube_url_pattern = re.compile(r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)')
    
#     # Find all matches in the input text
#     urls = youtube_url_pattern.findall(inText)
    
#     return urls


# # Extract and print the URLs
# youtube_urls = extract_youtube_urls(textVar)
# for url in youtube_urls:
#     print(url)

from pytube import YouTube

# List of YouTube video URLs
ytvideolist = [
    "https://www.youtube.com/watch?v=vStJoetOxJg",
    "https://www.youtube.com/watch?v=wiNXzydta4c",
    "https://www.youtube.com/watch?v=Gv9_4yMHFhI",
]

def get_video_details(url):
    try:
        yt = YouTube(url)
        video_details = {
            'title': yt.title,
            'description': yt.description,
            'duration': yt.length,
            'views': yt.views,
            'rating': yt.rating
        }
        return video_details
    except Exception as e:
        print(f"Error fetching details for {url}: {e}")
        return None

# Extracting details for each video
video_details_list = [get_video_details(url) for url in ytvideolist]

# Printing the details
for index, details in enumerate(video_details_list):
    if details:
        print(f"Video {index + 1}:")
        print(f"Title: {details['title']}")
        print(f"Description: {details['description']}")
        print(f"Duration: {details['duration']} seconds")
        print(f"Views: {details['views']}")
        print(f"Rating: {details['rating']}")
        print("\n" + "-"*40 + "\n")

# If you want to see all the details at once
import json
print(json.dumps(video_details_list, indent=4))

'''
    {
        "title": "A Gentle Introduction to Machine Learning",
        "description": null,
        "duration": 765,
        "views": 988378,
        "rating": null
    }
'''