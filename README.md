# Instagram Clone
 
## Setup Instructions
 
1. Clone the repository:
 
    ```
    git clone https://github.com/Sagar02411/Instagram-Clone
    ```
    
2. Create virtual environment:
   ```
   virtualenv <your environment>
   ```
3. Activate virtual environment:
   ```
   .\<your environment>\Scripts\activate
   ```
   git
4. Install dependencies:
 
    ```
    pip install -r requirement.txt
    ```
 
5. Apply migrations:
 
    ```
    python manage.py migrate
    ```
 
6. Run the development server:
 
    ```
    python manage.py runserver
    ```
## Project Structure
 
- `manage.py`: Django's command-line utility for administrative tasks.
- `requirement.txt`: List of Python dependencies.
- `project_name/`: social_book.
    - `settings.py`: Project settings and configurations.
    - `urls.py`: URL declarations for the project.
    - `wsgi.py`: WSGI config for deployment.
    - `asgi.py`: ASGI config for Channels.
- `app_name/`: core.
    - `models.py`: Database models.
    - `views.py`: Request handling functions.
    - `urls.py`: URL declarations for the app.
    - `admin.py`: Admin site registrations.
    - `templates/`: HTML templates.
    - `static/`: Static files (CSS, JavaScript, images).
    - `apps.py`: Declarations of apps.
    - `test.py`: Generate testcases.