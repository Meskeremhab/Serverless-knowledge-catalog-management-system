from aws_cdk import Stack, aws_lambda as _lambda, aws_apigateway as apigateway
from constructs import Construct
from dynamo_table import KnowledgeCatalog



class NewcatalogStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


    
        # Instantiate the DynamoDB table construct
        self.knowledge_catalog = KnowledgeCatalog(self, "KnowledgeCatalog")

        
        # Helper function to create a Lambda function
        def create_lambda(id, handler):
            return _lambda.Function(
                self, id,
                runtime=_lambda.Runtime.PYTHON_3_8,
                handler=handler,
                code=_lambda.Code.from_asset("lambda")
            )

        # Create Lambda functions
        add_Item_lambda = create_lambda("AddItemFunction", "add_Item.handler")
        get_Item_by_id_lambda = create_lambda("GetItembyIdFunction", "get_Item_by_id.handler")
        delete_Item_by_id_lambda = create_lambda("DeleteItembyIdFunction", "delete_Item_by_id.handler")
        list_Items_lambda = create_lambda("ListItemsFunction", "list_Items.handler")
        list_Items_by_Course_lambda = create_lambda("ListItemsbyCourseFunction", "list_Items_by_Course.handler")
        list_Items_by_year_lambda = create_lambda("ListItemsbyYearFunction", "list_Items_by_year.handler")

        # Use the existing table instance
        table = self.knowledge_catalog.table

        # Grant permissions to Lambda functions
        table.grant_read_write_data(add_Item_lambda)  
        table.grant_read_data(get_Item_by_id_lambda)  
        table.grant_write_data(delete_Item_by_id_lambda)  
        table.grant_read_data(list_Items_lambda)  
        table.grant_read_data(list_Items_by_Course_lambda)  
        table.grant_read_data(list_Items_by_year_lambda)  

        #Create an API Gateway REST API
        api = apigateway.RestApi(self, "Knowledgecatalogapi")

        # Define API resources and methods

        # list items
        items = api.root.add_resource("items")
        items.add_method("GET", apigateway.LambdaIntegration(list_Items_lambda))      

    
        # add item
        add_items = api.root.add_resource("additem")
        add_items.add_method("POST", apigateway.LambdaIntegration(add_Item_lambda))  


        # get item by id
        item_by_id = items.add_resource("by-id").add_resource("{CourseID}") 
        item_by_id.add_method("GET", apigateway.LambdaIntegration(get_Item_by_id_lambda))   
        

        # delete item by id
        catalog_item = items.add_resource("delete-by-id").add_resource("{CatalogItemID}")
        course_id = catalog_item.add_resource("{CourseID}") 
        course_id.add_method("DELETE", apigateway.LambdaIntegration(delete_Item_by_id_lambda))
      

        # list items by course
        items_by_course = items.add_resource("by-course").add_resource("{CatalogItemID}")
        items_by_course.add_method("GET", apigateway.LambdaIntegration(list_Items_by_Course_lambda))
        

        # list items by year
        item_by_year = items.add_resource("by-year").add_resource("{AcademicYear}")
        item_by_year.add_method("GET", apigateway.LambdaIntegration(list_Items_by_year_lambda))
       