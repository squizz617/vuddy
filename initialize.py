import os
import sys
import platform
# cveXmlDownloader.py 파일이 있는 경로를 추가
sys.path.append(r'E:\jnu\vuddy-demo\vulnDBGen\tools\cvedatagen')

originalDir = os.path.dirname(os.path.abspath(__file__))  # vuddy root directory
pf = platform.platform()

try:
    import tools.cvedatagen.cveXmlDownloader as Downloader
except ImportError:
    import cveXmlDownloader as Downloader
try:
    import tools.cvedatagen.cveXmlParser as Parser
except ImportError:
    import cveXmlParser as Parser
try:
    import tools.cvedatagen.cveXmlUpdater as Updater
except ImportError:
    import cveXmlUpdater as Updater

import tools.cvedatagen.common as common


def main():
    print("Making directories...")
    dataDir = os.path.join(originalDir, "data", "repolists")
    if os.path.exists(dataDir) is False:
        os.makedirs(dataDir)
    diffDir = os.path.join(originalDir, "diff")
    if os.path.exists(diffDir) is False:
        os.makedirs(diffDir)
    vulDir = os.path.join(originalDir, "vul")
    if os.path.exists(vulDir) is False:
        os.makedirs(vulDir)
    hidxDir = os.path.join(originalDir, "hidx")
    if os.path.exists(hidxDir) is False:
        os.makedirs(hidxDir)


    print("Running CVE data generator...")

    os.chdir(os.path.join(originalDir, "data")) 
    if "cvedata.pkl" not in os.listdir("./"):
        print("cvedata.pkl not found. Proceeding to download..")
        print("[+] cveXmlDownloader")
        Downloader.process()

        print("[+] cveXmlParser")
        Parser.process()
    else:
        print("cvedata.pkl found. Omitting download..")

    print("[+] cveXmlUpdater")
    Updater.process()

    os.chdir(originalDir)
    print("cvedata.pkl is now up-to-date.\n")
    

    if "Windows" in pf:  # Windows
        if os.path.exists(os.path.join(originalDir, "tools", "FuncParser-opt.exe")) is False:
            print("Downloading function parser for Windows...")
            os.chdir(os.path.join(originalDir, "tools"))
            url = "https://github.com/squizz617/FuncParser-opt/raw/master/FuncParser-opt.zip"
            fileName = "FuncParser-opt.zip"
            common.download_url(url, fileName)
            common.unzip(fileName)
            os.remove(fileName)

    print("*** Please modify config.py before running scripts in src/ ***")

if __name__ == '__main__':
    main()
