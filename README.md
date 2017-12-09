# MongoApp
This is a sample Book Review app to connect to a remote MongoDB. It allows users to add new book entries and read reviews for all or specific books.
Before running the app, store MONGO_URL as an environment variable. <export MONGO_URL=hostname:port>
To run this app, clone it and from the MongoApp directory exceute <python MongoApp.py>
To test connection to the application, hit '/test'. Ideally, you should see a json containing "Success".
To add entries, hit '/add'.
To get all the entries, hit '/all'.
Keep reading, keep POSTing.
