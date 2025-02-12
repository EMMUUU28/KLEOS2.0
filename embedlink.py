import re

def get_youtube_embed_link(url):
    # Define the regex pattern to extract the video ID
    youtube_id_pattern = re.compile(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*')
    match = youtube_id_pattern.search(url)
    
    if match:
        video_id = match.group(1)
        embed_link = f"https://www.youtube.com/embed/{video_id}"
        return embed_link
    else:
        return None

# Example usage
url = "https://www.youtube.com/watch?v=z18nw4adsx4"
embed_link = get_youtube_embed_link(url)
print(embed_link)  # Output: https://www.youtube.com/embed/z18nw4adsx4
