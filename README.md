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
 ```
social_book/
├── manage.py
├── requirement.txt
├── social_book/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── templates/
    └── static/
```
