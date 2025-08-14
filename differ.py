#!/usr/bin/env python3
import re
import urllib.request
import os
import json
import sys

# Assignee a link 
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
metadata = "compose/metadata/"
list_of_packages = "rpms.json"

def search_release(input):
    """Return decimal release"""
    num_release = re.search('[0-9]{8}.n.[0-9]', input)
    return num_release

def termination(item):
     if item == "Exit":
          print("Termination...")
          sys.exit(0)

# Read the content dirctly without any temporary file
with urllib.request.urlopen(link) as r:
    body = r.read().decode('utf-8')

list_of_releases = []
for release in body.splitlines():
    m = search_release(release)
    if m != None:
        list_of_releases.append(m.group())

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

#change approach, instead of using a list, the dictionary data structure helps
def load_packages(path):
    # here is I used a path to a package
    init_key = "payload"
    packet_management = "rpms"
    section = "Everything"
    arch="x86_64"
    # Created a dict which fills in by elements and has name and version of each package
    temp_dict = {}
    with open(path, "r") as f:
        out = json.load(f)
        packages_list = out[init_key][packet_management][section][arch]
        for full_package_string in packages_list:
            name = full_package_string.rsplit("-", 2)[0]
            version = '-'.join(full_package_string.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
            temp_dict[name] = version        
    return temp_dict


def what_happend_with_package(old, new, action):
    cats = ('REMOVED', 'ADDED', 'CHANGED')
    width = 9
    lits_of_obj = {}
    match action: # "REMOVED", "ADDED", "CHANGED"
        case "REMOVED":
          for name, version in old.items():
               # print(package[0])
               if name not in new:
                    lits_of_obj[name] = f"{cats[0].ljust(width)} ({name}-{version})"
               
          return lits_of_obj
                    
        case "ADDED":
          for name, version in new.items():
               if name not in old:
                    lits_of_obj[name] = f"{cats[1].ljust(width)} ({name}-{version})"
                    # print(package)
          return lits_of_obj

        case "CHANGED":
          for name, version in new.items():
               if new.get(name) != old.get(name):
                   lits_of_obj[name] = f"{cats[2].ljust(width)} {old.get(name)} -> {new.get(name)}"
               #     print(package)
          return lits_of_obj
        case _:
            termination()

# TODO: need to rewrite: first, asking about how much past X days user want to get a list with releases, second - display exactly the list contains only releases for this past X days, third - provide an option to choose
while True:
     print_menu()
     try:
         first_release = int(input("Select the first release: "))
     except ValueError:
          print("Please enter number")
          continue
     
     f1 = return_value(first_release)

     termination(f1)
     
     try:
          urllib.request.urlopen(url_of_release(f1))
     except urllib.error.HTTPError:
          print("It's minor release, there is no metadata package")  
          list_of_releases.pop(first_release - 1)
          print_menu()
          continue

     remove_first = list_of_releases.pop(first_release - 1)

     print_menu()
     try:
        second_release = int(input("Select the second release: "))
     except ValueError:
         print("Please enter the number")
         continue
     
     f2 = return_value(second_release)

     termination(f2)

     try:
          urllib.request.urlopen(url_of_release(f2))
     except urllib.error.HTTPError:
          print("It's minor release, there is no metadata package")  
          list_of_releases.pop(second_release - 1)
          print_menu()
          continue

     break

# ## f1 is old release, f2 is latest
reorder_releases = determine_release(f1,f2)
f1 = reorder_releases[0]
f2 = reorder_releases[1]

print(f"Selected releases:\n{f1} and {f2}")

## create dirs
os.mkdir(f1)
os.mkdir(f2)

# created pathes where jsons will be saved
file_path_f1 = os.path.join(f1, list_of_packages)
file_path_f2 = os.path.join(f2, list_of_packages)

## Download for first release
urllib.request.urlretrieve(url_of_release(f1), file_path_f1)
print(f"File downloaded: {file_path_f1}")

##  Download for second release
urllib.request.urlretrieve(url_of_release(f2), file_path_f2)
print(f"File downloaded: {file_path_f2}")

old_release = load_packages(file_path_f1)
current_release = load_packages(file_path_f2)

out_file = f"output_{f1}_{f2}.txt"   
# Creating 3 different dicts
removed = what_happend_with_package(old_release, current_release, "REMOVED")
added = what_happend_with_package(old_release, current_release, "ADDED")
changed = what_happend_with_package(old_release, current_release, "CHANGED")
# Making final dictinonary by using unions of created dictinaries 
# added |= removed
# changed |= added

final_dict = changed | added | removed

final_dict = dict(sorted(final_dict.items(), key = lambda i: i[0]))
# Determine max length of name packets for alignment
max_len = max(len(name) for name in list(final_dict.keys())) + 2

with open(out_file, 'w') as file:
     for name, version in final_dict.items():
          file.write(f"{name.ljust(max_len)}\t{version}\n")
          
with open(out_file, "r") as file:     
    file.read()    

## Clean up
os.remove(file_path_f1)
os.remove(file_path_f2)
os.rmdir(determine_release(f1,f2)[0])
os.rmdir(determine_release(f1,f2)[1])