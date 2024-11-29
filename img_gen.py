from fileinput import lineno

import requests
import time


url_gen = 'https://api.prodia.com/v1/sd/generate'
url_img = 'https://api.prodia.com/v1/job/'


def generate(promt):
    headers = {'X-Prodia-Key': '06b2ac41-5dc0-461e-85d8-abbac08c5491', 'accept': 'application/json'}

    payload = {'prompt': promt}

    response = requests.post(url_gen, headers=headers, json=payload)
    return response.json()['job']


def retrieve(job):
    headers = {'X-Prodia-Key': '06b2ac41-5dc0-461e-85d8-abbac08c5491', 'accept': 'application/json'}

    response = requests.get(url_img+job, headers=headers).json()
    link = response.get('imageUrl')
    status = response.get('status')
    return link, status

def get_link(prompt):
    a = generate(prompt)
    status = 'generating'
    while status == 'generating':
        link, status = retrieve(a)
        time.sleep(3)

    return link

