Serverless knowledge catalog management system
A knowledge catalog item represents a resource that is used for teaching in a particular course. It can be a paper, a slide deck, a web site, etc...


Requirements
Knowledge catalog items are identified by their name and the course to which they belong. The same catalog item can belong to different courses. Additionally, for each catalog item we must store the academic year for which it was created. Additional fields must be permitted.


IE needs to be able to perform the following operations through the API:

Add a knowledge catalog item
Retrieve a knowledge catalog item by its id
Delete a knowledge catalog item by its id
Retrieve all knowledge catalog items in the database
Retrieve all the knowledge catalog items of a particular course
Retrieve all the knowledge catalog items of a particular year


Implementation requirements:
The application must be implemented using AWS Lambda, Amazon ApiGateway and AWS DynamoDB.
You can only use the scan operation to implement the endpoint that retrieves all the items in the database.
If you implement the solution using IaC, it must be through CDK and you can only use L1 and L2 constructs.


Considerations
Think about the different client errors that can occur, and return the appropriate HTTP status code when needed.
The CDK project and any other code resource that you implement can be written in the programming language of your choice.
To test the API, you can use Postman.




