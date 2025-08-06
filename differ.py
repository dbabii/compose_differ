import re
import urllib.request
import os
import json

# assignee a link 
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
metadata = "compose/metadata/"
list_of_packages = "rpms.json"

def search_release(input):
    """Return decimal release"""
    num_release = re.search('[0-9]{8}.n.[0-9]', input)
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
     """Provide a list of releases"""
     for num, release in enumerate(list_of_releases, start=1):
        print(num, release)

def return_value(index):
     """Return a value from the release list"""
     val = list_of_releases[index - 1]
     return val

def url_of_release(release):
     """Creating a direct URL to specific package from the release list"""
     rel = f"Fedora-Rawhide-{release}/"
     url = link + rel + metadata + list_of_packages
     return url


# while True:
#      print_menu()
#      try:
#          first_release = int(input("Select the first release: "))
#      except ValueError:
#           print("Please enter number")
#           continue
     
#      f1 = return_value(first_release)

#      if f1 == "Exit":
#           break
#     #  remove_first = list_of_releases.pop(first_release - 1)
     
#      try:
#         second_release = int(input("Select the second release: "))
#      except ValueError:
#          print("Please enter the number")
#          continue
     
#      f2 = return_value(second_release)

#      if f2 == "Exit":
#           break

#      # create a dir for first release
#      # os.mkdir(f1)
 
#      # create a path where json will be saved
#      file_path_f1 = os.path.join(f1, list_of_packages)
 
#      # download for first release
#      # urllib.request.urlretrieve(url_of_release(f1), file_path_f1)

#      # create a dir for second release
#      # os.mkdir(f2)
     
#      # create a path where json will be saved
#      file_path_f2 = os.path.join(f2, list_of_packages)
     
#      # download for second release
#      # urllib.request.urlretrieve(url_of_release(f2), file_path_f2)
     
#      break

f0 = "rpms.json"
f1 = "20250730.n.0"
f2 = "20250806.n.0"
file_path_f1 = os.path.join(f1, list_of_packages)
file_path_f2 = os.path.join(f2, list_of_packages)
# print(file_path_f1)


def determine_release(release1, release2):
     """Return latest release
     """
     num1 = int(re.sub(r'.n.', '', release1))
     num2 = int(re.sub(r'.n.', '', release2))


     if num1 > num2:
          return num1
     else:
          return num2


determine_release(f1, f2)

file_path = "20250730.n.0/rpms.json"

versions_f1 = []
versions_f2 = []

def load_packages(path, List):
     with open(path, "r") as file:
          out = json.load(file)
          for i in out['payload']['rpms']['Everything']['x86_64']:
               name =  re.split('-[0-9]:', i)[0]
               # version = '-'.join(i.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
               first_num_of_version = re.split(":", i)[0][-1]
               others_nums_of_version = re.split(":", re.split("[.]fc", i)[0])[1]
               version = first_num_of_version + ":" + others_nums_of_version
               human_readable_out = (name, version)
               List.append(human_readable_out)


load_packages(file_path_f1, versions_f1)
load_packages(file_path_f2, versions_f2)     


with open("output.txt", "w") as fil:
     # for i,j in zip(versions_f1, versions_f2):
     #      # print(i[0])
     #      # print(j)
     #      # decompose version to compare between each other
     #      ver1 = re.split(':|[.]|-', i[1])
     #      ver2 = re.split(':|[.]|-', j[1])
          
     #      if i[0] == j[0]:
     #           # compare versions
     #           for k,m in zip(ver1, ver2):
     #               try:
     #                    k = int(k)
     #                    m = int(m)
     #               except ValueError:
     #                    k = str(k)
     #                    m = str(k)
     #               if k < m:
     #                    fil.write(f'{i[0]}\tversion is upgraded: {i[1]} -> {j[1]}\n')
     #                    break
     #               elif k > m:
     #                    fil.write(f'{i[0]}\tversion is downgrade: {i[1]} -> {j[1]}\n')

     names_in_list1 = [name[0] for name in versions_f1]
     names_in_list2 = [name[0] for name in versions_f2]
     removed = [name for name in versions_f1 if name[0] not in names_in_list2]
     # added = [name for name in versions_f2 if name[0] not in names_in_list1]
     print(removed)
     # print(added)