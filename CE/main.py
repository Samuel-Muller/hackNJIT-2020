# -*- coding: utf-8 -*-

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import os, requests, uuid, json
from dotenv import load_dotenv
load_dotenv()

'''key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'''''
'''if not key_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(key_var_name))'''
subscription_key = os.getenv("VAR")

'''endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'''
'''if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))'''
endpoint = os.getenv("VAR2")
location = 'eastus'

lang = {
    'afrikaans': 'af',
    'arabic': 'ar',
    'bulgarian': 'bg',
    'catalan': 'ca',
    "chinese simplified": 'zh-Hans',
    "chinese tradional": 'zh-Hant',
    'croatian': 'hr',
    'czech': 'cs',
    'danish': 'da',
    'dutch': 'nl',
    'english': 'en',
    'estonian': 'et',
    'finnish': 'fi',
    'french': 'fr',
    'german': 'de',
    'greek': 'el',
    'gujarati': 'gu',
    "haitian creole": 'ht',
    'hebrew': 'he',
    'hindi': 'hi',
    'hungarian': 'hu',
    'icelandic': 'is',
    'indonesian': 'id',
    'irish': 'ga',
    'italian': 'it',
    'japanese': 'ja',
    'klingon': 'tlh-Latn',
    'korean': 'ko',
    "kurdish central": 'ku',
    'latvian': 'lv',
    'lithuanian': 'lt',
    'malay': 'ms',
    'maltese': 'mt',
    'norwegian': 'nb',
    'pashto': 'ps',
    'persian': 'fa',
    'polish': 'pl',
    "portuguese brazil": 'pt-br',
    "portuguese portugal": 'pt-pt',
    'punjabi': 'pa',
    "queretaro otomi": 'otq',
    'romanian': 'ro',
    'russian': 'ru',
    "serbian cyrillic": 'sr-Cyrl',
    "serbian latin": 'sr-Latn',
    'slovak': 'sk',
    'slovenian': 'sl',
    'spanish': 'es',
    'swahili': 'sw',
    'swedish': 'sv',
    'tahitian': 'ty',
    'thai': 'th',
    'turkish': 'tr',
    'ukrainian': 'uk',
    'urdu': 'ur',
    'vietnamese': 'vi',
    'welsh': 'cy',
    "yucatec maya": 'yua'
}
print('Enter desired text to be translated: ')
txt = input()

# If you encounter any issues with the base_url or path, make sure
# that you are using the latest endpoint: https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate
path = '/translate?api-version=3.0'
print('Enter desired language in all lowercase: ')
newLang = input()

if newLang in lang:
    translateLang = lang[newLang]

params = '&to=de&to=it&to=' + translateLang
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
# You can pass more than one object in body.
body = [{
    'text' : txt
}]
request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))