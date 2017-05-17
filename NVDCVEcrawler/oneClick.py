try:
    import NVDCVEcrawler.cveXmlDownloader as Downloader
except ImportError:
    import cveXmlDownloader as Downloader
try:
    import NVDCVEcrawler.cveXmlDownloader as Parser
except ImportError:
    import cveXmlDownloader as Parser
try:
    import NVDCVEcrawler.cveXmlDownloader as Updater
except ImportError:
    import cveXmlDownloader as Updater


def main():
    Downloader.process()
    Parser.process()
    Updater.process()


if __name__ == '__main__':
    main()
