
import json
import boto3
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('KnowledgeCatalog')
    
    try:
        catalog_id = event['pathParameters']['CatalogItemID'].replace('%20', ' ')
        course_id = event['pathParameters']['CourseID']
        
        response = table.delete_item(
            Key={
                'CatalogItemID': catalog_id,
                'CourseID': course_id
            },
            ReturnValues='ALL_OLD'  
        )
        
        # Check if the delete was successful by checking if Attributes are returned
        if 'Attributes' in response:
            return {
                'statusCode': 200,
                'body': json.dumps('Item deleted successfully')
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found or already deleted')
            }

    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {e.response['Error']['Message']}")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"An unexpected error occurred: {str(e)}")
        }
