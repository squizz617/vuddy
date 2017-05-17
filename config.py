import platform

"""
[Note for Windows]
- Use '\\' or '/' in path
Ex) gitStoragePath = "D:\\Source\\gitrepos"
- Install 'Git for Windows'
- Windows version of VUDDY use its own JRE

[Note for POSIX]
- Use '/' for path
Ex) gitStoragePath = "/home/ubuntu/gitrepos/"
- Java binary is only needed in POSIX
"""

gitStoragePath = "/home/ubuntu/gitrepos/"

pf = platform.platform()
if "Windows" in pf:  # Windows
    gitBinary = "C:\\Program Files\\Git\\bin\\git.exe"
    diffBinary = "C:\\Program Files\\Git\\usr\\bin\\diff.exe"
else:  # POSIX
    gitBinary = "git"
    diffBinary = "diff"
    javaBinary = "java"
