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
url = "https://pcccreative.org/wp-content/uploads/2012/07/geology-roadmap1.jpg"
# url = image_urls[0]
# imgbase64Var = image_to_base64(url)


# import requests
# import base64

def getGenText(img_base64):
    url = 'https://2f16-34-105-55-3.ngrok-free.app/process_image'
    data = {'imgbase64': img_base64}
    response = requests.post(url, json=data)
    print(response.json())

    # Parse JSON response and print only the 'message' value
    message_value = response.json().get('message', None)
    if message_value:
        print(message_value)
        return message_value
    else:
        print("No 'message' key found in the response.")
        return "No 'message' key found in the response."

print("url: ", url)
roadmapKeywords = getGenText(url)

print("roadmapKeywords: ", roadmapKeywords)