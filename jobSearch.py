from serpapi import GoogleSearch


def fetch_jobs(query):
        params = {
            "engine": "google_jobs",
            "q": f"{query} Hackathon",
            "hl": "en",
            "num": "25",
            "api_key": "b4c6fa50debf72a9002057d26f1e63edcc77f78644db4b5d650190f60925593b"
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("jobs_results", [])

query = 'AIML'
jobdata = fetch_jobs(query)
print("jobdata: ", jobdata)


'''

'''