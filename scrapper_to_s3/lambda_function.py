from scrapper_to_s3 import ibov_to_s3 


def lambda_handler(event, context):
    ibov_to_s3()
    return {"statusCode": 200, "body": "ok"}