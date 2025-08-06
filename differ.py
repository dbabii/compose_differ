#!/usr/bin/env python3
import re
import urllib.request
import os
import json
import sys

# assignee a link 
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
metadata = "compose/metadata/"
list_of_packages = "rpms.json"
file_name = "example.html"

def search_release(input):
    """Return decimal release"""
    num_release = re.search('[0-9]{8}.n.[0-9]', input)
    return num_release


# read a content from link
with urllib.request.urlopen(link) as response:
    body = response.read()

# save it to a file
with open(file_name, mode="wb") as html_file:
    html_file.write(body)

list_of_releases = []

with open(file_name, mode="r") as f:
    releases = f.readlines()
    for i in releases:
        m = search_release(i)
        if m != None:
               list_of_releases.append(m.group())

list_of_releases.append("Exit")

def termination(item):
     if item == "Exit":
          print("Termination...")
          os.remove(file_name)
          sys.exit(0)


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

def determine_release(release1, release2):
     """Return latest release
     """
     num1 = int(re.sub(r'.n.', '', release1))
     num2 = int(re.sub(r'.n.', '', release2))


     if num1 > num2:
          old = release2
          new = release1
     else:
          old = release1
          new = release2
     
     return old, new

def load_packages(path, List):
     with open(path, "r") as f:
          out = json.load(f)
          for i in out['payload']['rpms']['Everything']['x86_64']:
               name =  re.split('-[0-9]:', i)[0]
               # version = '-'.join(i.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
               first_num_of_version = re.split(":", i)[0][-1]
               others_nums_of_version = re.split(":", re.split("[.]fc", i)[0])[1]
               version = first_num_of_version + ":" + others_nums_of_version
               human_readable_out = (name, version)
               List.append(human_readable_out)


while True:
     print_menu()
     try:
         first_release = int(input("Select the first release: "))
     except ValueError:
          print("Please enter number")
          continue
     
     f1 = return_value(first_release)

     termination(f1)
     
     remove_first = list_of_releases.pop(first_release - 1)
     print_menu()
     try:
        second_release = int(input("Select the second release: "))
     except ValueError:
         print("Please enter the number")
         continue
     
     f2 = return_value(second_release)

     termination(f2)

     print(f"Selected releases:\n{f1} and {f2}")
     # f1 is old release, f2 is latest
     reorder_releases = determine_release(f1,f2)
     f1 = reorder_releases[0]
     f2 = reorder_releases[1]
     

     # create dirs
     os.mkdir(f1)
     os.mkdir(f2)

     # created pathes where jsons will be saved
     file_path_f1 = os.path.join(f1, list_of_packages)
     file_path_f2 = os.path.join(f2, list_of_packages)
     
     
     # download for first release
     urllib.request.urlretrieve(url_of_release(f1), file_path_f1)
     print(f"File downloaded: {file_path_f1}")
          
     # download for second release
     urllib.request.urlretrieve(url_of_release(f2), file_path_f2)
     print(f"File downloaded: {file_path_f2}")
     
     versions_f1 = []
     versions_f2 = []

     load_packages(file_path_f1, versions_f1)
     load_packages(file_path_f2, versions_f2)  

     out_file = f"output_{f1}_{f2}.txt"   

     with open(out_file, "w") as f:
          names_in_list1 = [name[0] for name in versions_f1]
          names_in_list2 = [name[0] for name in versions_f2]
          removed = [name for name in versions_f1 if name[0] not in names_in_list2]
          added = [name for name in versions_f2 if name[0] not in names_in_list1]
          for i in added:
               f.write(f"{i[0]}\tAdded\t({i[0]}{i[1]})\n")
          
          for i in removed:
               f.write(f"{i[0]}\tRemoved\t({i[0]}{i[1]})\n")


          for i,j in zip(versions_f1, versions_f2):
               # decompose version to compare between each other
               ver1 = re.split(':|[.]|-', i[1])
               ver2 = re.split(':|[.]|-', j[1])
               
               if i[0] == j[0]:
                    # compare versions
                    for k,m in zip(ver1, ver2):
                         try:
                              k = int(k)
                              m = int(m)
                         except ValueError:
                              k = str(k)
                              m = str(k)
                         if k < m:
                              f.write(f'{i[0]}\tversion is upgraded: {i[1]} -> {j[1]}\n')
                              break
                         elif k > m:
                              f.write(f'{i[0]}\tversion is downgrade: {i[1]} -> {j[1]}\n')
     
     with open(out_file, "r") as f:
          print(f.read())

     # clean up
     os.remove(file_name)
     os.remove(file_path_f1)
     os.remove(file_path_f2)
     os.rmdir(determine_release(f1,f2)[0])
     os.rmdir(determine_release(f1,f2)[1])
     
     
     break