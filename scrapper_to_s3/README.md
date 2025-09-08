# B3 IBOV CSV Downloader and S3 Uploader

This Python script automates the process of downloading the daily IBOVESPA (IBOV) CSV file from the B3 website, skipping the first two lines, and uploading it to an AWS S3 bucket. After uploading, the local CSV file is deleted automatically.  

## Features

- Automatically downloads the latest IBOV CSV from B3.
- Skips the first two lines of the CSV when reading it with pandas.
- Uploads the CSV to a specified S3 bucket using credentials stored in a `.env` file.
- Removes the local CSV file after successful upload.

## Requirements

- Python 3.8+
- Google Chrome installed
- ChromeDriver compatible with your Chrome version
- Python libraries (included in `requirements.txt`):

```bash
pip install -r requirements.txt
