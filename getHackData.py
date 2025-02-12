import requests
from bs4 import BeautifulSoup

def scrape_hackathons():
    url = 'https://example.com/hackathons'  # Replace with actual URL of hackathon listings page
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Assuming hackathon details are contained in elements with specific classes or tags
        hackathon_elements = soup.find_all('div', class_='hackathon')
        hackathons = []
        for element in hackathon_elements:
            # Extract relevant information (title, date, description, etc.)
            title = element.find('h2').text.strip()
            date = element.find('span', class_='date').text.strip()
            description = element.find('p', class_='description').text.strip()
            hackathons.append({
                'title': title,
                'date': date,
                'description': description
            })
        return hackathons
    else:
        print(f"Failed to retrieve hackathons. Status code: {response.status_code}")
        return None

# Example usage:
hackathon_data = scrape_hackathons()
if hackathon_data:
    for hackathon in hackathon_data:
        print(f"Title: {hackathon['title']}")
        print(f"Date: {hackathon['date']}")
        print(f"Description: {hackathon['description']}")
        print("=" * 20)
