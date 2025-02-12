from pytube import YouTube
import os
import speech_recognition as sr
from moviepy.editor import VideoFileClip

# Function to download YouTube video
def download_video(video_url, output_filename='video.mp4', output_path='./'):
    try:
        # Create a YouTube object with the video URL
        yt = YouTube(video_url)

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video to the specified output path with the specified filename
        print(f"Downloading '{yt.title}'...")
        stream.download(output_path, filename=output_filename)
        print('Download complete!')

    except Exception as e:
        print(f"Error downloading video: {e}")

# Function to perform speech recognition on video's audio
def recognize_speech(video_file):
    try:
        # Load the video file
        video = VideoFileClip(video_file)

        # Extract audio from the video
        audio = video.audio

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Convert audio to text
        with sr.AudioFile(audio.filename) as source:
            audio_data = recognizer.record(source)

        # Perform speech recognition
        recognized_text = recognizer.recognize_google(audio_data)
        return recognized_text

    except Exception as e:
        return f"Error recognizing speech: {e}"

# Main function
if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=x7X9w_GIm1s'
    download_video(video_url)

    video_file = "video.mp4"
    
    # Perform speech recognition on the video file
    recognized_text = recognize_speech(video_file)
    
    # Print the recognized text
    print("Recognized text:")
    print(recognized_text)
