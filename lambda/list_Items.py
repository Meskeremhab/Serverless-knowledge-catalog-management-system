import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('KnowledgeCatalog')
    
    try:
        # Scan the table for all items
        scan_result = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(scan_result['Items'])
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving items from the table.')
        }
    except Exception as e:

        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error.')
        }
