import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('KnowledgeCatalog')

    try:
        # Parse the body of the request
        catalog = json.loads(event['body'])
        catalog_id = catalog['CatalogItemID']  
        course_id = catalog['CourseID']        

        # Check if an item with the same CourseID already exists
        response = table.get_item(
            Key={
                'CatalogItemID': catalog_id,  
                'CourseID': course_id        
            }
        )

        if 'Item' in response:
            return {
                'statusCode': 400,
                'body': json.dumps('Item exists with this CatalogItemID and CourseID')
            }

        # Create item 
        item = {
            'CatalogItemID': catalog_id,
            'CourseID': course_id,
            **catalog 
        }

        # Put item in DynamoDB
        table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('Item added successfully!')
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error adding item to the table.')
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Internal server error.')
        }
