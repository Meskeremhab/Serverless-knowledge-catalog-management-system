from aws_cdk import (
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Stack
)
from constructs import Construct

class KnowledgeCatalog(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        self.table = self.__create_table()

    # Create the DynamoDB table
    def __create_table(self):
        partition_key = dynamodb.Attribute(
            name="CatalogItemID", type=dynamodb.AttributeType.STRING
        )

        sort_key = dynamodb.Attribute(
            name="CourseID", type=dynamodb.AttributeType.STRING
        )

        table = dynamodb.Table(
            self,
            id="KnowledgeCatalog",
            table_name="KnowledgeCatalog",
            partition_key=partition_key,
            sort_key=sort_key,
            point_in_time_recovery=True,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        
        # Name: academic_year - index
        academic_year_partition_key = dynamodb.Attribute(
            name="academic_year", type=dynamodb.AttributeType.NUMBER
        )

        table.add_global_secondary_index(
            index_name="academic_year-index",
            partition_key=academic_year_partition_key,
            projection_type=dynamodb.ProjectionType.ALL,
        )

        # Name: course_id - index
        # PK: course_id
        course_id_partition_key = dynamodb.Attribute(
            name="course_id", type=dynamodb.AttributeType.STRING
        )

        table.add_global_secondary_index(
            index_name="course_id-index",
            partition_key=course_id_partition_key,
            projection_type=dynamodb.ProjectionType.ALL,
        )

        return table
