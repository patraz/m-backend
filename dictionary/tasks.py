from celery import shared_task
from requests_html import HTMLSession
import openai
import ast
from django.conf import settings
from .models import Definition

openai.api_key = settings.OPENAI_API
# fuction that outputs list of dictionaries with word, meanin and example

@shared_task
def scrape_words():
    session = HTMLSession()
    scraping_site = 'https://www.miejski.pl/losuj'
    list = []
    print('działam')
    for x in range(5):
        r = session.get(scraping_site)
        try:
            word = r.html.find('article')[0].find('header')[0].text
            meaning = r.html.find('article')[0].find('p')[0].text

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś ekspertem od slangu i języka ulicznego. Przeredaguj ten tekst bez zmieniania slangowego słowa używając synonimów aby brzmiał profesjonalnie"},
                    {"role": "user", "content": f"""
                    meaning: {meaning}
                    Only provide a  Python list compliant response  following this format without deviation.
                    {{
                    "meaning":meaning,
                    }}"""}],
                temperature=0,
                max_tokens=3877,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            dict = response['choices'][0]['message']['content']
            res = ast.literal_eval(dict)
            res['word'] = word
            print(res, type(res))
            list.append(res)
        except:
            pass
    for word in list:
        Definition.objects.create(word=word['word'], meaning=word['meaning'])
    print(list)
    return list
