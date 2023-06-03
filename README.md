### Run the App
1. Open a terminal and run the following:
2. Build the app using
``docker build -t <image_name> .``
3. Run the app using 
``docker run -p 8080:8080 -e PYTHONUNBUFFERED=1 <image_name>``

### Trigger the ETL
1. Open a separate terminal and run the following:
2. Run the scaffold function using
``python test.py``