import os
import sys
import platform

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
    dataDir = os.path.join(originalDir, "data")
    if os.path.exists(dataDir) is False:
        os.makedirs(dataDir)
    print "Running CVE data generator..."

    os.chdir(os.path.join(originalDir, "data")) 
    if "cvedata.pkl" not in os.listdir("./"):
        print "cvedata.pkl not found. Proceeding to download.."
        print "[+] cveXmlDownloader"
        Downloader.process()

        print "[+] cveXmlParser"
        Parser.process()
    else:
        print "cvedata.pkl found. Omitting download.."

    print "[+] cveXmlUpdater"
    Updater.process()

    os.chdir(originalDir)
    print "cvedata.pkl is now up-to-date.\n"
    

    if "Windows" in pf:  # Windows
        if os.path.exists(os.path.join(originalDir, "tools", "FuncParser-opt.exe")) is False:
            print "Downloading function parser for Windows..."
            os.chdir(os.path.join(originalDir, "tools"))
            url = "https://github.com/squizz617/FuncParser-opt/raw/master/FuncParser-opt.zip"
            fileName = "FuncParser-opt.zip"
            common.download_url(url, fileName)
            common.unzip(fileName)
            os.remove(fileName)

    print "*** Please modify config.py before running scripts in src/ ***"

if __name__ == '__main__':
    main()
