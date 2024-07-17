import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('KnowledgeCatalog')

    try:
        # Retrieve the course_id from path parameters
        course_id = event['pathParameters']['CatalogItemID'].replace('%20', ' ')

        print(f"Looking up items for course ID: {course_id}")

        # Query the table using the course_id index
        query_result = table.query(
            IndexName='course_id-index',
            KeyConditionExpression=Key('course_id').eq(course_id)
        )

        if query_result['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps(query_result['Items'], default=str)
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps(f"No catalog found for the course ID {course_id}")
            }

    except ClientError as e:
        print(f"DynamoDB Client Error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving items from the table.')
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('course_id parameter is required.')
        }
    except Exception as e:
        print(f"General Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('An unexpected error occurred.')
        }
