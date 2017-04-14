import os
import shutil

cwd = os.getcwd()

print "Running NVD CVE Crawler..."

os.chdir("tools/nvdcrawler")
if "cvedata.pkl" not in os.listdir("./"):
    print "cvedata.pkl not found. Proceeding to download.."
    print "[+] cveXmlDownloader"
    os.system("python cveXmlDownloader.py")
    print "[+] cveXmlParser"
    os.system("python cveXmlParser.py")
else:
    print "cvedata.pkl found. Omitting download.."

print "[+] cveXmlUpdater"
os.system("python cveXmlUpdater.py")

print "[+] Copying CVE data file..."
shutil.copy("cvedata.pkl", os.path.join(cwd, "src", "cvedata.pkl"))

os.chdir(cwd)
