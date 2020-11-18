# managemt

This project features inventory management modules including reporting, detailed tracking of the products through their history and log entries, authentication and authorization, real-time barcode reader, an easy-to-use user interface, a dynamic stocktake page and an admin page to reach and modify certain settings in the application. 

I used the <b>Heroku</b> server to host the application, <b>PostgreSQL</b>(MSSQL for production) database to store the data in the demo and <b>AWS(Amazon Web Server) S3 bucket</b> to store the images and invoice files.

<hr>

<b>FEATURES:</b>

<b>Real-Time Barcode Reader:</b> To get rid of the traditional barcode reader machines, I implemented a real-time barcode reader that does not require a barcode reader and reads barcode through any camera. Thanks to this solution, the company saved money where they would otherwise pay for barcode readers. The application connects to the camera stream after the barcode reader is loaded and the camera permission is granted. I used the QuaggaJS library to implement this feature. This library uses the HTML5 getUserMedia method to access the camera stream. QuaggaJS is capable of finding a barcode-like pattern in the camera stream invariant to scale and rotation. Therefore, barcodes do not need to be aligned with the viewport.

<b>Product History:</b> To track the status of the products at any time, I added history to product objects using the Django Simple History library. This library stores the Django model state on every create/update/delete action. This feature is also useful in the report page where the previous versions of the products are queried and displayed.

<b>Storage Reports:</b> Users can download and view reports from the report page through the application. I used xhtml2pdf library to generate PDF files from HTML formatted files.

<b>Task Scheduler:</b> In order to send scheduled emails of the product reports to admin and preferably other users, I used the Django Q library. Django Q is a native Django task queue, scheduler and worker application using Python multiprocessing. In addition, with the help of Django’s admin interface, admin can easily change the frequency of the scheduled emails.

<b>Authorization & Authentication:</b> In this part, Django made my life a lot easier thanks to the built in libraries. I wrote custom view decorators to add user permissions and restrictions.

<b>Managing Databases:</b> I used models in Django which uses Object Relational Mapping(ORM).

<b>Front-end:</b> I used javascript, HTML and CSS for the user interface. I also used bootstrap to create a responsive and easy to use UI.


<hr>
<b> Sources Used: </b>

* HTML
* CSS
* Javascript 
* Python 3
    * xhtml2pdf: To convert HTML to PDF.
    * psycopg2: To connect PostgreSQL server to Django development
      server.
    * boto3: To connect AWS S3 bucket with Django application.
    * Pillow: Python imaging library.
    * pyzbar: To read barcodes.
    * redis: In-memory data structure store that can be used in email
      queueing.
    * whitenoise: For static file serving in python web applications.
    * Django 3:
        * django-filter: To query the databases.
        * django-q: To automate processes.
        * django-simple-history: To store history of any object.
        * django-storages: Helper library to connect AWS S3 bucket. • django-widget-tweaks: To tweak the form field rendering in
        templates.
    
Databases: PostgreSQL(for demo), MSSQL(for production) Servers: Amazon Web Server, Heroku
