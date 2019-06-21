import urllib.request
import pprint
import json
from bs4 import BeautifulSoup

# run pip install beautifulsoup4 before running this file

pp = pprint.PrettyPrinter()

def build_site_map(starting_url, max_depth: int = 10):
  json_site_map = []
  curr_depth = 0
  visited_set = set()
  curr_urls = [starting_url]
  while curr_depth < max_depth:
    next_urls = []
    print(len(curr_urls))
    for url in curr_urls: 
      ## TODO: check the json_site_map to see if we visited this site already ##
      curr = {
        'page_url': url,
        'links': [],
        'images': [],
      }

      html = urllib.request.urlopen(url)
      soup = BeautifulSoup(html, 'html.parser')

      links = soup.find_all("a") # find all links  
      for link in links:
        next_link = link.get('href')
        if (next_link[:4] != "http") and (next_link[:3] != "www"): # if next_link is a relative link i.e. /en-US/firefox/, add it to the starting url
          next_link = starting_url + next_link
        curr['links'].append(next_link)
        if url == next_link[:len(url)] and next_link not in visited_set:
           # if the link has the same domain as the current link and has not been visited, add it to the visited set and the next depth 
          visited_set.add(next_link)
          next_urls.append(next_link)

      images = soup.find_all("img") # find all images
      for img in images:
        curr['images'].append(img.get('src'))

      json_site_map.append(curr)
    curr_urls = next_urls
    curr_depth += 1


    
  
  with open('result.json', 'w') as fp:
    json.dump(json_site_map, fp)



  
  # print(len(images))






build_site_map('https://mozilla.org')
# build_site_map('https://www.w3schools.com')
# print(len(links))

# print(f.read(100))