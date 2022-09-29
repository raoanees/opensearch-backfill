from elasticsearch import Elasticsearch
from elasticsearch import helpers
from elasticsearch_dsl import connections
import boto3
import json
import base64
import logger
import requests


es_client = connections.create_connection(hosts=['<HOST_NAME>'],http_auth="<USER_NAME>:<PASSWORD>")
if __name__ == "__main__":
    f = open("<OUTPUT_FILE>.json", "w")
    s3_client = boto3.client('s3')
    s3keys = s3_client.list_objects(Bucket="<BUCKET_NAME>", Prefix='<KEY_PATH>')
    for s3key in s3keys['Contents']:
        print (s3key['Key'])
        file = s3_client.get_object(Bucket="<BUCKET_NAME>", Key=s3key['Key'])
        text = file['Body'].read().decode("utf-8")
        failure_cases = list(map(lambda x: json.loads(x), filter(None, text.split('\n'))))
        body = []
        for case in failure_cases:
            if case['errorCode'] == '403':
                data = {"index": {"_index": case['esIndexName'], "_id": case['esDocumentId']}}
                json.dump(data, f, ensure_ascii=False)
                f.write("\n")
                decodedBytes = base64.b64decode(case['rawData'])
                decodedStr = decodedBytes.decode("ascii") 
                json_str=json.loads(decodedStr)
                json.dump(json_str, f, ensure_ascii=False)
                f.write("\n")
    f.close()

