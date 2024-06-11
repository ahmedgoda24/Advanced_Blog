# Advanced_Blog
# Django Blog API

This is a blog application built with Django and Django REST Framework.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Docker (for containerization)
- Mysql (or any preferred database)

### Installation

1. **Clone the repository:**

    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database:**

    - Ensure PostgreSQL is running and create a database for the project.

    - Update the `DATABASES` setting in `settings.py`:

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'your_db_name',
                'USER': 'your_db_user',
                'PASSWORD': 'your_db_password',
                'HOST': 'localhost',
                'PORT': '',
            }
        }
        ```

    - Run migrations:

        ```sh
        python manage.py migrate
        ```

5. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

### Docker Setup

1. **Build the Docker image:**

    ```sh
    docker build -t django-blog-api .
    ```

2. **Run the Docker container:**

    ```sh
    docker-compose up
    ```
###  Endpoints blog app

- **Posts:**
    - List and detail: `GET /blog/`, `POST /api/posts/`
    - Retrieve, Update, and Delete: `GET /blog/<id>/`, `PUT /blog/<id>/edit/`, `DELETE /blog/<id>/delete/`


- **Comments:**
     Create `POST /blog/<id>/comment/`
  

### API Endpoints blog app

- **Posts:**
    - List and Create: `GET /api/posts/`, `POST /api/posts/`
    - Retrieve, Update, and Delete: `GET /api/posts/<id>/`, `PUT /api/posts/<id>/`, `DELETE /api/posts/<id>/`

- **Categories:**
    - List: `GET /api/categories/`

- **Tags:**
    - List: `GET /api/tags/`

- **Comments:**
    - List and Create: `GET /api/comments/`, `POST /api/comments/`
    - Delete: `DELETE /api/comments/<id>/`
###  Endpoints Accounts app

 -Login and Logout and Signup       `accounts/ login/` ,   `accounts/ logout/` ,  `accounts/ signup` 
- Retrieve and Update:    `accounts/ profile` , `accounts/ profile/edit` 
### API Endpoints Accounts app
-Login and Logout api  `accounts/ api/login/`  `accounts/ api/logout/` 
 -Retrieve and Update and Signup :`accounts/ api/profile/` , `accounts/api/registration/`

### Authentication

This API uses basic authentication. To access protected endpoints, provide your username and password.


### Testing

1. **Run tests:**

    ```sh
    python manage.py app_name
    ```

### Deployment

1. **Collect static files:**

    ```sh
    python manage.py collectstatic
    ```

2. **Run the application using Gunicorn:**

    ```sh
    gunicorn your_project_name.wsgi:application
    ```

3. **Using Docker:**

    ```sh
    docker-compose up --build
    ```

### Contributing

Contributions are welcome! Please create an issue or submit a pull request.

### License

This project is licensed under the MIT License.
