import os
import shutil

try:
    import tools.nvdcrawler.cveXmlDownloader as Downloader
except ImportError:
    import cveXmlDownloader as Downloader
try:
    import tools.nvdcrawler.cveXmlParser as Parser
except ImportError:
    import cveXmlParser as Parser
try:
    import tools.nvdcrawler.cveXmlUpdater as Updater
except ImportError:
    import cveXmlUpdater as Updater

def main():
    cwd = os.getcwd()
    print "Running NVD CVE Crawler..."

    os.chdir("tools/nvdcrawler")
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

    print "[+] Copying CVE data file...",
    shutil.copy("cvedata.pkl", os.path.join(cwd, "src", "cvedata.pkl"))

    os.chdir(cwd)

    print "(CVE data ready)\n"
    print "*Please modify config.py before running scripts.*"


if __name__ == '__main__':
    main()
