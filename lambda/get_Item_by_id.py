import boto3
import json
from aws_cdk import aws_dynamodb as dynamodb

TABLE_NAME = "KnowledgeCatalog"
resource_dynamo_db = dynamodb.resource_custom()

def lambda_handler(event, context):
    try:
        print(f"Received event: {event}")

        query_params = event.get("queryStringParameters", {})
        if query_params is not None:
            return {
                "statusCode": 400,
                "body": json.dumps("Error: Error, input parameters are not supported."),
            }

        catalog_item_id = event['pathParameters'].get('CatalogItemID')
        course_id = event['pathParameters'].get('CourseID')
        
        if not catalog_item_id or not course_id:
            return {
                "statusCode": 400,
                "body": json.dumps("Error: Missing CatalogItemID or CourseID in path parameters."),
            }

        # Get item from DynamoDB
        table = resource_dynamo_db.Table(TABLE_NAME)
        try:
            response = table.get_item(Key={'CatalogItemID': catalog_item_id, 'CourseID': course_id})
            if 'Item' in response:
                return {"statusCode": 200, "body": json.dumps(response['Item'])}
            else:
                return {
                    "statusCode": 404,
                    "body": json.dumps(f"No items found with CatalogItemID: {catalog_item_id} and CourseID: {course_id}")
                }
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps(f"Error retrieving item: {str(e)}")
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"An unexpected error occurred: {str(e)}"}),
        }
