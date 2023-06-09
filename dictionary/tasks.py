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
                    {"role": "user", "content": f"""{meaning}"""}],
                temperature=0,
                max_tokens=3877,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            word_dict = dict()
            meaning = response['choices'][0]['message']['content']
            # res = ast.literal_eval(dict)
            word_dict['meaning'] = meaning
            word_dict['word'] = word
            list.append(word_dict)
        except:
            pass
    for word in list:
        if not Definition.objects.filter(word=word['word']).exists():
            Definition.objects.create(word=word['word'], meaning=word['meaning'])
    print(list)
    return list
