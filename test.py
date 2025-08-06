# import requests
import re
from urllib.request import urlopen

# initate a link 
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
# read a content from link
# with urlopen(link) as response:
#     body = response.read()
# # save it to a file
# with open("example.html", mode="wb") as html_file:
#     html_file.write(body)

with open("example.html", mode="r") as f:
    lst_dirs = f.readlines()
    for i in lst_dirs:
        m = re.search('[0-9]{8}\.n\.[0-9]', i)
        if m != None:
               print(m.group())


# response = requests.get(link)
# response.encoding = "utf-8"
# lst_dirs = response.text
# print(lst_dirs)

