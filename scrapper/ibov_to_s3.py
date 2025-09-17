import datetime
import os, io, boto3

def ibov_df_to_s3(df):
    bucket = os.environ["BUCKET_NAME"]
    folder = os.environ.get("OBJECT_PREFIX", "raw")
    prefix = "b3"
    date_str = datetime.date.today().strftime("%Y-%m-%d")
    filename = f"{prefix}_{date_str}.parquet"

    key = f"{folder}/date={date_str}/{filename}"

    buf = io.BytesIO()
    df.to_parquet(buf, index=False, engine="pyarrow", compression="snappy")
    buf.seek(0)    

    boto3.client("s3").put_object(
        Bucket=bucket,
        Key=key,
        Body=buf.getvalue(),
        ContentType="application/octet-stream" 
    )