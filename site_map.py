import urllib.request
import json
import time

from bs4 import BeautifulSoup

# run pip install beautifulsoup4 before running this file

def build_site_map(starting_url, max_depth: int = 10):
  json_site_map = []
  curr_depth = 0
  visited_set = set()
  curr_urls = [starting_url]
  while curr_depth < max_depth and len(curr_urls) > 0:
    next_urls = []
    print("Curr Depth: " + str(curr_depth) + " | Number of URLs "+ str(len(curr_urls)))
    for url in curr_urls:  # loop through every url of the current depth
      try:
        html = urllib.request.urlopen(url)
      except Exception: # any other weird exception happens when trying to access one of the links (i.e. 403: Forbidden)
        continue
      new_url = html.geturl() # checks for redirects  
      visited_set.add(new_url) # adds the redirect url to the set
      soup = BeautifulSoup(html, 'html.parser')
      curr = {
        'page_url': new_url,
        'links': [],
        'images': [],
      }

      links = soup.find_all("a") # find all links  
      for link in links:
        next_link = link.get('href')
        if next_link is None: # some 'a' tags don't have hrefs
          continue 
        if (next_link[:4] != "http") and (next_link[:3] != "www"): # if next_link is a relative link i.e. /en-US/firefox/, add it to the starting url
          next_link = starting_url + next_link
        curr['links'].append(next_link)
        if url == next_link[:len(url)] and next_link not in visited_set: # if the link has the same domain as the current link and has not been visited, add it to the visited set and the next depth 
          visited_set.add(next_link)
          next_urls.append(next_link)

      images = soup.find_all("img") # find all images
      for img in images:
        next_img = img.get('src')
        if img is None:
          continue 
        curr['images'].append(next_img)

      json_site_map.append(curr) 
    curr_urls = next_urls
    curr_depth += 1

  # print to json file
  with open('result.json', 'w') as fp:
    json.dump(json_site_map, fp)
### main section ###
user_website = ""
while not user_website:
  user_website = input("Enter a website in the form, https://mozilla.org: ").strip()
  try:
    html = urllib.request.urlopen(user_website)
  except (ValueError, urllib.error.URLError) as e:
    if type(e) == ValueError:
      print("Invalid Format.")
      user_website = ""
    elif type(e) == urllib.error.URLError:
      print("This site cannot be reached.")
      user_website = ""
max_depth = ""
while not max_depth:
  max_depth = int(input("Enter a max depth (max 10):"))
  if max_depth > 10 or max_depth < 0:
    max_depth = 10
t0 = time.time()
build_site_map(user_website, max_depth)
t1 = time.time()

print("Time:" + str(t1-t0) + "s")