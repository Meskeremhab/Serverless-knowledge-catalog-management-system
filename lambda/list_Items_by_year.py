import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('KnowledgeCatalog')

    try:
        # Retrieve the AcademicYear from the path parameter
        academic_year = event['pathParameters']['AcademicYear']

        # Query the table using the academic_year index
        query_result = table.query(
            IndexName='academic_year-index',
            KeyConditionExpression=Key('academic_year').eq(academic_year)
        )

        # Check if any items were found
        if query_result['Items']:
            return {
                'statusCode': 200,
                'body': json.dumps(query_result['Items'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('No catalog found from the year {}'.format(academic_year))
            }

    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error retrieving items from the table.')
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps('AcademicYear parameter is required.')
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('An unexpected error occurred.')
        }
