import json
import datetime
import logging
import requests
import pandas as pd

from sanitize.sanitize import Sanitize
from scrapper.ibov_to_s3 import ibov_df_to_s3

# logging básico
logging.getLogger().setLevel(logging.INFO)

# sessão HTTP com headers que a B3 aceita
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://sistemaswebb3-listados.b3.com.br",
    "Referer": "https://sistemaswebb3-listados.b3.com.br/",
})

URL = (
    "https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/"
    "GetPortfolioDay/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjEyMCwiaW5kZXgiOiJJQk9WIiwic2VnbWVudCI6IjIifQ=="
)

sanitizer = Sanitize()


def download_and_extract():
    current_date = datetime.date.today().isoformat()

    r = SESSION.get(URL, timeout=15)
    r.raise_for_status()  

    payload = r.json().get("results", [])
    if not payload:
        logging.warning("A B3 retornou payload vazio.")
        return

    df = pd.DataFrame(payload)
    df = sanitizer.clean_df(df)  
    df["data_pregao"] = current_date

    
    ibov_df_to_s3(df)


def lambda_handler(event, context):
    try:
        download_and_extract()
        return {"statusCode": 200, "body": json.dumps({"ok": True})}
    except requests.HTTPError as e:
        status = getattr(e.response, "status_code", 500)
        logging.exception("HTTPError na B3 (%s): %s", status, e)
        return {"statusCode": status, "body": "Erro HTTP ao baixar dados da B3"}
    except Exception:
        logging.exception("Falha não tratada")
        # Deixe a Lambda marcar como erro para observabilidade
        raise
