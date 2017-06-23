import platform

"""
[Note for Windows]
- Install 'Git for Windows'.

[Note for POSIX]
- Use '/' for path.
Ex) gitStoragePath = "/home/ubuntu/gitrepos"
"""

gitStoragePath = r"/home/squizz/gitrepos"
version = "3.0.3" # for use in IoTcube.

pf = platform.platform()
if "Windows" in pf:  # Windows
    gitBinary = r"C:\Program Files\Git\bin\git.exe"
    diffBinary = r"C:\Program Files\Git\usr\bin\diff.exe"
else:  # POSIX
    gitBinary = "git"
    diffBinary = "diff"
    javaBinary = "java"
