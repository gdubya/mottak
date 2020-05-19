# What is needed to get this running on Azure w/minio gw or AWS

For AWS og Minio:
 * AWS_ACCESS_KEY_ID
 * AWS_SECRET_ACCESS_KEY
 * AWS_REGION
 * ENDPOINT
 * BUCKET

See start.sh for details. 

For GCS - set OBJECTSTORE to gcs and mount the GCS secret JSON file and point GCS_SERVICE_ACCOUNT_FILE to it.


