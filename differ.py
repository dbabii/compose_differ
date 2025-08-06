import re
import urllib.request
import os

# assignee a link 
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
metadata = "compose/metadata/"
list_of_packages = "rpms.json"

def search_release(input):
    num_release = re.search('[0-9]{8}\.n\.[0-9]', input)
    return num_release


# read a content from link
# with urllib.request.urlopen(link) as response:
#     body = response.read()
# # save it to a file
# with open("example.html", mode="wb") as html_file:
#     html_file.write(body)

list_of_releases = []

with open("example.html", mode="r") as f:
    releases = f.readlines()
    for i in releases:
        m = search_release(i)
        if m != None:
               list_of_releases.append(m.group())

list_of_releases.append("Repeat")
list_of_releases.append("Exit")

def print_menu():
     for num, release in enumerate(list_of_releases, start=1):
        print(num, release)

def return_value(index):
     val = list_of_releases[index - 1]
     return val

def url_of_release(release):
     rel = f"Fedora-Rawhide-{release}/"
     url = link + rel + metadata + list_of_packages
     return url
     

while True:
     print_menu()
     try:
         first_release = int(input("Select the first release: "))
     except ValueError:
          print("Please enter number")
          continue
     
     f1 = return_value(first_release)
     # create a dir
     os.mkdir(return_value(first_release))
     # create a path where json will be saved
     file_path_f1 = os.path.join(return_value(first_release), list_of_packages)
     # download for first release
     urllib.request.urlretrieve(url_of_release(f1), file_path_f1)

     if return_value(first_release) == "Exit":
          break
    #  remove_first = list_of_releases.pop(first_release - 1)
     
     try:
        second_release = int(input("Select the second release: "))
     except ValueError:
         print("Please enter the number")
         continue
     
     f2 = return_value(second_release)
          
     # create a second dir
     os.mkdir(return_value(second_release))
     
     # create a path where json will be saved
     file_path_f2 = os.path.join(return_value(first_release), list_of_packages)
     
     # download for second release
     urllib.request.urlretrieve(url_of_release(f1), file_path_f2)
     
     if return_value(second_release) == "Exit":
          break
     
     break