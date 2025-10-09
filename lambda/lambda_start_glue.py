import os
import json
import logging
import boto3
import urllib.parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

glue = boto3.client("glue")

GLUE_JOB_NAME = os.environ.get("GLUE_JOB_NAME")

def lambda_handler(event, context):

    #Esta função é acionada por um evento S3 e inicia um job no AWS Glue,
    #passando o caminho completo do arquivo S3 como argumento.
    if not GLUE_JOB_NAME:
        logger.error("Variável de ambiente GLUE_JOB_NAME não definida.")
        return {"statusCode": 500, "body": "GLUE_JOB_NAME not set"}

    try:
        s3_record = event['Records'][0]['s3']
        bucket_name = s3_record['bucket']['name']
        object_key = urllib.parse.unquote_plus(s3_record['object']['key'], encoding='utf-8')

        s3_path = f"s3://{bucket_name}/{object_key}"
        logger.info(f"Arquivo recebido: {s3_path}")

        job_args = {
            "--s3_input_path": s3_path
        }

        response = glue.start_job_run(
            JobName=GLUE_JOB_NAME,
            Arguments=job_args
        )

        job_run_id = response.get("JobRunId")
        logger.info(f"Glue job started: {GLUE_JOB_NAME} / runId={job_run_id} para o arquivo {s3_path}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "GlueJobName": GLUE_JOB_NAME,
                "JobRunId": job_run_id,
                "ProcessedFile": s3_path
            })
        }

    except Exception as e:
        logger.exception("Erro ao disparar Glue Job")
        return {"statusCode": 500, "body": str(e)}