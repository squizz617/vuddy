import os

originalDir = os.path.dirname(os.path.abspath(__file__))  # vuddy root directory

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


def main():
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
    print "*** Please modify config.py before running scripts in src/ ***"


if __name__ == '__main__':
    main()
