import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('api_key')
end_point = os.getenv('end_point')

print(f"API Key: {api_key}")
print(f"Database URL: {end_point}")


def generate(
        model: str,
        system: str,
        query: str,
        temperature: float | None = None,
        lastk: int | None = None,
        session_id: str | None = None,
        rag_threshold: float | None = 0.5,
        rag_usage: bool | None = False,
        rag_k: int | None = 0
):
    headers = {
        'x-api-key': api_key
    }

    request = {
        'model': model,
        'system': system,
        'query': query,
        'temperature': temperature,
        'lastk': lastk,
        'session_id': session_id,
        'rag_threshold': rag_threshold,
        'rag_usage': rag_usage,
        'rag_k': rag_k
    }

    print(f"request: {request}")

    msg = None

    try:
        response = requests.post(end_point, headers=headers, json=request)

        if response.status_code == 200:
            res = json.loads(response.text)
            msg = {'response': res['result'], 'rag_context': res['rag_context']}
        else:
            msg = f"Error: Received response code {response.status_code}"
    except requests.exceptions.RequestException as e:
        msg = f"An error occurred: {e}"
    return msg


def upload(multipart_form_data):
    headers = {
        'x-api-key': api_key
    }

    msg = None
    try:
        response = requests.post(end_point, headers=headers, files=multipart_form_data)

        if response.status_code == 200:
            msg = "Successfully uploaded. It may take a short while for the document to be added to your context"
        else:
            msg = f"Error: Received response code {response.status_code}"
    except requests.exceptions.RequestException as e:
        msg = f"An error occurred: {e}"

    return msg


def pdf_upload(
        path: str,
        strategy: str | None = None,
        description: str | None = None,
        session_id: str | None = None
):
    params = {
        'description': description,
        'session_id': session_id,
        'strategy': strategy
    }

    multipart_form_data = {
        'params': (None, json.dumps(params), 'application/json'),
        'file': (None, open(path, 'rb'), "application/pdf")
    }

    response = upload(multipart_form_data)
    return response


def text_upload(
        text: str,
        strategy: str | None = None,
        description: str | None = None,
        session_id: str | None = None
):
    params = {
        'description': description,
        'session_id': session_id,
        'strategy': strategy
    }

    multipart_form_data = {
        'params': (None, json.dumps(params), 'application/json'),
        'text': (None, text, "application/text")
    }

    response = upload(multipart_form_data)
    return response
