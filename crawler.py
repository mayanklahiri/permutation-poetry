#!/usr/bin/env python
import json
import requests
import random
import re
from urllib import urlencode
from subprocess import check_output

POET_COUPLETS = 200
POET_SYLLABLES_PER_LINE = 5
POET_RHYMING = 2

API_KEY = '8f16841b2da951203cb2a11c87726501'
API_ENDPOINT = 'https://api.flickr.com/services/rest/?api_key=' + API_KEY

def clean(sentence):
  return re.sub(r'^[\-\s:]+', '', re.sub(r'\-\-', '- ', re.sub(r'[\d{}\[\]]+', '', sentence).strip()))

def search(query):
  url = API_ENDPOINT + '&' + urlencode({
        'method': 'flickr.photos.search',
        'text': query,
        'format': 'json',
        'sort': 'interestingness-desc',
        'nojsoncallback': 1
    })
  r = requests.get(url)
  if r.json():
    results = r.json()['photos']['photo']
    if len(results):
      chosen = random.choice(results[:5])
      return chosen
  return None

def main():
  poetry = check_output('./poet.py %d %d %d' % (
      POET_COUPLETS, POET_SYLLABLES_PER_LINE, POET_RHYMING), shell=True)
  lines = poetry.split('\n')

  output = json.loads(open('poetry.json').read()) or []

  for i in range(0, len(lines)-1, 2):
    couplet = clean(lines[i]), clean(lines[i+1])
    print 'COUPLET: ' + ' | '.join(couplet)
    result = search(couplet[0])
    if result:
      print 'RESULT', result
      output.append({
          'sentences': couplet,
          'image': result,
        })
      open('poetry.json', 'w+').write(json.dumps(output))
    else:
      print 'NO RESULT'

if __name__ == '__main__': main()
