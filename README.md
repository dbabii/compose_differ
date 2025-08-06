Differ Compose

Python CLI tool that helps to identify what packages have changed between two releases


Task:
1. Outputs a list of Rawhide composes built in the past X days (the “latest” folder can be ignored)
2. Outputs a change-set of packages for the x86_64 architecture between two specified Rawhide composes (in human readable or machine-parsable format), sorted into three categories
    - Packages added to the later compose
    - Packages removed from the later compose
    - Packages which changed version between the composes

Execution:
1. Get a list of directories from the URL: https://kojipkgs.fedoraproject.org/compose/rawhide/
    - Ignore the "latest" dir
    - Making the list of dirs by using RegEx
2. Rename the original name of each entity to the day only:
    - 20250215.n.0
    - 20250216.n.0
    - 20250217.n.0
3. Asking about selecting 2 Rawhide composes that should be made a difference
    - There shouldn't be selected the same compose twice (it can be implemented by using step-by-step selecting, and after first selection, that compose will be removed from the list)
4. Creating 2 selected composes dirs with renaming
5. Download rpms.json
    - perhaps, it would be nice if there will be a progress bar of downloading
6. Making a comparison file in the above level of downloaded dirs 
7. Removing created dirs and files and remaining only comparing file