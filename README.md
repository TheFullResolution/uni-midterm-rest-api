# uni-midterm-rest-api

## Project Overview

This project is a RESTful web API built using Django and Django REST Framework for the CM3035 - Advanced Web Development
midterm coursework. The API provides endpoints for interacting with a database of classes, proficiencies, races, spells,
schools, subclasses, and related data for a role-playing game scenario.

The application follows best practices for API design, implements serializers for structured data, and provides dynamic
URLs for resource detail views.

## Features

* RESTful endpoints for CRUD operations on:
    * Classes and Subclasses
    * Proficiencies
    * Races and Subraces
    * Spells and Spell Descriptions
    * Schools of Magic
* Relationship mappings between resources, such as:
    * Spells linked to Classes and Subclasses
    * Proficiencies associated with Races and Classes
    * Dynamic hyperlinking for detail views in responses.
* Bulk data loading from CSV files.
* SQLite database as the default backend.

## Requirements and Setup

### Prerequisites

* Python 3.13 or above
* pip (Python package installer)
* Virtual Environment (optional but recommended)

### Installation

1. Clone/Download the repository
2. Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate # On Windows: env\Scripts\activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

4. Set up the .env file in the project root with the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

5. Apply database migrations:

```
python manage.py migrate
```

6. Load initial data from CSV files:

```
python manage.py load_data
```

7. Start the development server:

```
python manage.py runserver
```

## Endpoints

**Base URL: /api/**

| Endpoint                   | Method | Description                     |
|----------------------------|--------|---------------------------------|
| `/api/classes/`            | GET    | List all classes                |
| `/api/classes/<id>/`       | GET    | Retrieve a specific class       |
| `/api/proficiencies/`      | GET    | List all proficiencies          |
| `/api/proficiencies/<id>/` | GET    | Retrieve a specific proficiency |
| `/api/races/`              | GET    | List all races                  |
| `/api/races/<id>/`         | GET    | Retrieve a specific race        |
| `/api/spells/`             | GET    | List all spells                 |
| `/api/spells/<id>/`        | GET    | Retrieve a specific spell       |
| `/api/schools/`            | GET    | List all schools of magic       |
| `/api/schools/<id>/`       | GET    | Retrieve a specific school      |
| `/api/subclasses/`         | GET    | List all subclasses             |
| `/api/subclasses/<id>/`    | GET    | Retrieve a specific subclass    |

For detailed response structures, refer to the serializers in the api/serializers/ directory.

File Structure

```
uni-midterm-rest-api/
├── api/
│   ├── serializers/         # Serializers for data representation
│   ├── views/               # ViewSets for API logic
│   ├── urls.py              # API routing
│   ├── models.py            # Database models
│   ├── tests.py             # Unit tests for endpoints
├── dndRestAPI/
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation (this file)
└── .env                     # Environment variables

```

Known Issues
• Admin Middleware Error: Ensure SessionMiddleware is included in MIDDLEWARE before AuthenticationMiddleware.

Development

Testing

To run unit tests:

python manage.py test

Running the Server

python manage.py runserver

Contributions

This project is intended for coursework purposes, and external contributions are not expected.

For questions or issues, contact the developer through your university communication channels.

Author

Developed as part of the CM3035 - Advanced Web Development module midterm assignment.