import openai
from openai_config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_description(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

import requests
from requests.structures import CaseInsensitiveDict

def generate_image(description):
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"

    data = """
    {
        """
    data += f'"model": "image-alpha-001",'
    data += f'"prompt": "{description}",'
    data += """
        "num_images":1,
        "size":"1024x1024",
        "response_format":"url"
    }
    """

    url = "https://api.openai.com/v1/images/generations"

    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}")

    return response.json()["data"][0]["url"]

def main():
    while True:
        user_input = input("Enter your query or type 'exit' to quit: ")

        if user_input.lower() == 'exit':
            break

        description = generate_description(user_input)
        print(f"Generated description: {description}")

        image_url = generate_image(description)
        print(f"Generated image URL: {image_url}")
        print()

if __name__ == "__main__":
    main()