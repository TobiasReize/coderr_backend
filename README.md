# Coderr Backend

## A Django-based Backend project for a freelance developer platform. You can login as a customer or a business user. Customer make orders and create reviews, Business user can create offers and manage the orders. You can use the easy demo login.<br/>
Coderr uses the Django and Django Restframework (DRF) to provide individual endpoints, authentication, permissions, filtering, ordering and pagination.

This project is part of the coderr_frontend_v1.1.0
Changes in the config.js: customer guest username: "customer_gest" and business guest username: "business_guest"

## How to install this repository (Backend):

1. Clone this repository:
```
    git clone <GitHub repository link>
```

2. Create a virtual environment (in the project folder):
```
    python -m venv env
```

3. Install the dependencies:
```
    activate the virtual environment
    pip install -r requirements.txt
```

4. Start the local development server (on path: 127.0.0.1:8000):
```
    python manage.py runserver
```

5. Apply migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

6. Start coderr_frontend:<br/>
clone the repository and run the liveserver on path 127.0.0.1:5500
