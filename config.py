import platform

gitStoragePath = r"/home/whiteboxDB/gitrepos"
version = "3.1.0" # for use in IoTcube.
pf = platform.platform()
if "Windows" in pf:  # Windows
    gitBinary = r"C:\Program Files\Git\bin\git.exe"
    diffBinary = r"C:\Program Files\Git\usr\bin\diff.exe"
else:  # POSIX
    gitBinary = "git"
    diffBinary = "diff"
    javaBinary = "java"
