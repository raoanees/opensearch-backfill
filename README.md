In case of OpenSearch cluster failures, firehose will dump the data into S3 buckets and data will go missing in the OpenSearch dashboards since it’s not ingested into OpenSearch.
 
There is a code snippet to transform and download the failed records from S3 to JSON files. It can be done using the following script:
elastic_bulk.py 
Don’t forget to replace following placeholders with the appropriate values:
HOST_NAME: OpenSearch domain url
USER_NAME: Username of OpenSearch domain
PASSWORD: Password of OpenSearch domain
OUTPUT_FILE: Path for output JSON file
BUCKET_NAME:Name of S3 bucket where failed records are stored
KEY_PATH: Folder path in S3 bucket for which all files should be fetched and data needs to be sent to OpenSearch
 
Once the output file is ready with the JSON formatted data following command can be used to push the data to OpenSearch cluster:
curl -XPOST -u 'master-user:master-user-password' 'domain-endpoint/_bulk' --data-binary @<OUTPUT_FILE_PATH>.json -H 'Content-Type: application/json'
