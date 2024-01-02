# Light Novel Downloader & EPUB Converter

## Overview
This Python script is designed for fans of light novels and ebooks. It allows you to scrape light novels from specified websites and convert them into EPUB format. This tool is perfect for reading your favourite novels on the go, even without an internet connection. Given the often extensive length of these novels, spanning thousands of chapters, the script is optimised for handling large-scale downloads.

## Features
- **Web Scraping**: Efficiently scrapes light novel chapters from specified websites.
- **EPUB Conversion**: Converts scraped chapters into the widely-supported EPUB format.
- **Batch Processing**: Capable of handling novels with thousands of chapters.
- **Offline Reading**: Enjoy your favourite novels anytime, without the need for an internet connection.

## Prerequisites
Before you run the script, ensure you have the following prerequisites installed:
- Python 3.x
- Selenium
- EbookLib

You will also need a suitable WebDriver (ie. Google Chrome) installed for Selenium to interact with web browsers.

## Installation
Clone the repository to your local machine:
```sh
git clone git@github.com:mxl1503/lightnovel-epub-converter.git
```

Navigate to the script's directory and install the required Python packages:
```
cd lightnovel-epub-converter
pip install -r requirements.txt
```

## Usage
To use the script, run it from your command line:
```
python3 src/main.py
```

Follow the on-screen prompts to enter the URL of the first chapter of the light novel and other required details.

## Customisation
You can customise the script to suit specific websites or novel formats by modifying the source code. Currently it supports any novel from
the website 'readnovelfull.com'.
