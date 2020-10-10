import requests
import re

page = requests.get("https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions")

page.raise_for_status()

x = re.findall(" *\.[^-(\s,\.)]+\s+–", page.text)

for ext in x:
    print(ext[:-2])

