
from requests_html import HTMLSession
import openai
import ast
from django.conf import settings

openai.api_key = settings.OPENAI_API
# fuction that outputs list of dictionaries with word, meanin and example

def scrape_words(times):
    session = HTMLSession()
    scraping_site = 'https://www.miejski.pl/losuj'
    list = []
    for x in range(times):
        r = session.get(scraping_site)
        word = r.html.find('article')[0].find('header')[0].text
        meaning = r.html.find('article')[0].find('p')[0].text
        example = r.html.find('article')[0].find('blockquote')[0].text

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
        print(response['choices'][0]['message']['content'])
        # dict = {
        #     'word': word,
        #     'meaning' : meaning,
        #     'example' : example
        # }
        
        dict = response['choices'][0]['message']['content']
        res = ast.literal_eval(dict)
        res['word'] = word
        print(res, type(res))
        list.append(res)
    return(list)
