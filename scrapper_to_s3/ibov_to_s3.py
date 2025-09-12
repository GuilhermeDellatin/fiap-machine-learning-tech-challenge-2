import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import boto3


def ibov_to_s3():
    
    load_dotenv()

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
    AWS_REGION = os.getenv("AWS_REGION")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless") 
    prefs = {"download.default_directory": os.getcwd()}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br")
        time.sleep(3) 

        download_button = driver.find_element(By.LINK_TEXT, "Download")
        download_button.click()
        
        time.sleep(5)
    finally:
        driver.quit()

    files = [f for f in os.listdir() if f.endswith(".csv")]
    if not files:
        raise FileNotFoundError("No CSV found.")
        
    latest_csv = max(files, key=os.path.getctime)
    print("Reading CSV:", latest_csv)

    df = pd.read_csv(latest_csv, sep=";", encoding="latin1", skiprows=2)
    print(df.head())

    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    s3_key = f"ibov/{latest_csv}" # bucket patch
    s3.upload_file(latest_csv, AWS_BUCKET_NAME, s3_key)
    print(f"{latest_csv} sent to s3://{AWS_BUCKET_NAME}/{s3_key}")
    os.remove(latest_csv)
