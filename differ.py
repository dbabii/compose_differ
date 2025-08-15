#!/usr/bin/env python3
import re
from urllib import error
from urllib import request
import os
import json
import sys

# Assignee a link
link = "https://kojipkgs.fedoraproject.org/compose/rawhide/"
metadata = "compose/metadata/"
list_of_packages = "rpms.json"
width = 2

def search_release(input):
    """Return decimal release"""
    num_release = re.search('[0-9]{8}[.]n[.][0-9]+', input)
    return num_release

def termination(item):
    if item == "Exit":
        print("Termination...")
        sys.exit(0)

def url_of_release(release):
    """Creating a direct URL to specific package from the release list"""
    rel = f"Fedora-Rawhide-{release}/"
    url = link + rel + metadata + list_of_packages
    return url

# Read the content directly without any temporary file
try:
    with request.urlopen(link) as r:
        body = r.read().decode('utf-8')
except error.HTTPError as e:
    print(f"Unable to connect to {link}\nError: {e}")
    sys.exit(1)

list_of_releases = []
list_of_unavailable_releases = []

for release in body.splitlines():
    m = search_release(release)
    if m != None:
        list_of_releases.append(m.group())

# Here, the list with releases is checked and return the updated list
for release in list_of_releases:
     try:
          request.urlopen(url_of_release(release))
     except error.HTTPError:
          list_of_releases.remove(release)
          list_of_unavailable_releases.append(release)

list_of_releases.append("Exit")


def print_menu():
     """Provide a list of releases"""
     for num, release in enumerate(list_of_releases, start=1):
        print(num, release)

def select_release(order):
     is_valid_input = False
     while not is_valid_input:
          try:
               num = int(input(f"Select the {order} release: "))
               if 1 <= num <= len(list_of_releases):
                   is_valid_input = True
                   return num
               else:
                   print(f"Select number between 1 and last release {len(list_of_releases) - 1}. Or choose {list_of_releases[-1]} by typing {len(list_of_releases)}")
          except ValueError:
               print("Invalid input, please choose a number")


def return_value(index):
     """Return a value from the release list"""
     val = list_of_releases[index - 1]
     return val


def determine_release(release1, release2):
     """Return latest release"""
     num1 = int(re.sub(r'.n.', '', release1))
     num2 = int(re.sub(r'.n.', '', release2))

     if num1 > num2:
          old = release2
          new = release1
     else:
          old = release1
          new = release2
     return old, new

def load_packages(url):
    # here is I used a path to a package
    init_key = "payload"
    packet_management = "rpms"
    section = "Everything"
    arch = "x86_64"
    # Created a dict which fills in by elements and has name and version of each package
    temp_dict = {}
    with request.urlopen(url) as f:
        json_data = f.read().decode('utf-8')
        out = json.loads(json_data)
        packages_list = out[init_key][packet_management][section][arch]
        for full_package_string in packages_list:
            name = full_package_string.rsplit("-", 2)[0]
            version = '-'.join(full_package_string.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
            temp_dict[name] = version        
    return temp_dict


def what_happend_with_package(old, new, action):
    cats = ('REMOVED', 'ADDED', 'CHANGED')
    len_status = len(max(cats)) + width
    lits_of_obj = {}
    match action: # "REMOVED", "ADDED", "CHANGED"
        case "REMOVED":
          for name, version in old.items():
               # print(package[0])
               if name not in new:
                    lits_of_obj[name] = f"{cats[0].ljust(len_status)} ({name}-{version})"
               
          return lits_of_obj
                    
        case "ADDED":
          for name, version in new.items():
               if name not in old:
                    lits_of_obj[name] = f"{cats[1].ljust(len_status)} ({name}-{version})"
                    # print(package)
          return lits_of_obj

        case "CHANGED":
          for name, version in new.items():
               if new.get(name) != old.get(name):
                   lits_of_obj[name] = f"{cats[2].ljust(len_status)} {old.get(name)} -> {new.get(name)}"
               #     print(package)
          return lits_of_obj
        case _:
            termination()

# TODO: need to rewrite: first, asking about how much past X days user want to get a list with releases, second - display exactly the list contains only releases for this past X days, third - provide an option to choose
if list_of_unavailable_releases:
    print("Not available releases: ")
    for i in list_of_unavailable_releases:
          print('i', end=width)

print_menu()

first_release = select_release("first")
f1 = return_value(first_release)
termination(f1)
list_of_releases.pop(first_release - 1)

print_menu()

second_release = select_release("second")
f2 = return_value(second_release)
termination(f2)

## f1 is old release, f2 is latest
reorder_releases = determine_release(f1,f2)
old_release, new_release = reorder_releases[0], reorder_releases[1]

for i in list_of_releases:
    print(i, end=" " * width)

print(f"\nSelected releases:\n\t{old_release} and {new_release}\n")

old_packages = load_packages(url_of_release(old_release))
new_packages = load_packages(url_of_release(new_release))

out_file = f"output_{f1}_{f2}.txt"   
# Creating 3 different dicts
removed = what_happend_with_package(old_packages, new_packages, "REMOVED")
added = what_happend_with_package(old_packages, new_packages, "ADDED")
changed = what_happend_with_package(old_packages, new_packages, "CHANGED")
# Making final dictinonary by using unions of created dictinaries and sort it
final_dict = changed | added | removed

final_dict = dict(sorted(final_dict.items(), key = lambda i: i[0]))
# Determine max length of name packets for alignment
max_len = max(len(name) for name in list(final_dict.keys())) + 2

with open(out_file, 'w') as file:
     for name, version in final_dict.items():
          file.write(f"{name.ljust(max_len)}\t{version}\n")
          
# with open(out_file, "r") as file:     
#     print(file.read())
