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
- Java binary is only needed in Linux
"""

gitStoragePath = "/home/ubuntu/gitrepos/"
gitBinary = "git"
diffBinary = "diff"
javaBinary = "java"

pf = platform.platform()
if "Windows" in pf:
    gitBinary = "C:\\Program Files\\Git\\bin\\git.exe"
    diffBinary = "C:\\Program Files\\Git\\usr\\bin\\diff.exe"
elif "Linux" in pf:
    gitBinary = "git"
    diffBinary = "diff"
    javaBinary = "java"
