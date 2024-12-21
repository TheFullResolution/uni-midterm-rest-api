# D&D REST API

## Project Overview

This project is a RESTful web API built using Django and Django REST Framework for the CM3035 - Advanced Web Development
midterm coursework. The API provides endpoints for interacting with a database of classes, proficiencies, races, spells,
schools, subclasses, and related data for a role-playing game scenario.

The application follows best practices for API design, implements serializers for structured data, and provides dynamic
URLs for resource detail views.

## Hosted API

The project is hosted on https://fly.io/ and can be accessed at https://uni-midterm-rest-api.fly.dev/

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
| `/api/classes/`            | POST   | Create a new class              |
| `/api/classes/<id>/`       | GET    | Retrieve a specific class       |
| `/api/classes/<id>/`       | PATCH  | Update a specific class         |
| `/api/classes/<id>/`       | DELETE | Delete a specific class         |
| `/api/proficiencies/`      | GET    | List all proficiencies          |
| `/api/proficiencies/`      | POST   | Create a new proficiency        |
| `/api/proficiencies/<id>/` | GET    | Retrieve a specific proficiency |
| `/api/proficiencies/<id>/` | PATCH  | Update a specific proficiency   |
| `/api/proficiencies/<id>/` | DELETE | Delete a specific proficiency   |
| `/api/races/`              | GET    | List all races                  |
| `/api/races/`              | POST   | Create a new race               |
| `/api/races/<id>/`         | GET    | Retrieve a specific race        |
| `/api/races/<id>/`         | PATCH  | Update a specific race          |
| `/api/races/<id>/`         | DELETE | Delete a specific race          |
| `/api/spells/`             | GET    | List all spells                 |
| `/api/spells/`             | POST   | Create a new spell              |
| `/api/spells/<id>/`        | GET    | Retrieve a specific spell       |
| `/api/spells/<id>/`        | PATCH  | Update a specific spell         |
| `/api/spells/<id>/`        | DELETE | Delete a specific spell         |
| `/api/schools/`            | GET    | List all schools of magic       |
| `/api/schools/`            | POST   | Create a new school             |
| `/api/schools/<id>/`       | GET    | Retrieve a specific school      |
| `/api/schools/<id>/`       | PATCH  | Update a specific school        |
| `/api/schools/<id>/`       | DELETE | Delete a specific school        |
| `/api/subclasses/`         | GET    | List all subclasses             |
| `/api/subclasses/`         | POST   | Create a new subclass           |
| `/api/subclasses/<id>/`    | GET    | Retrieve a specific subclass    |
| `/api/subclasses/<id>/`    | PATCH  | Update a specific subclass      |
| `/api/subclasses/<id>/`    | DELETE | Delete a specific subclass      |

For detailed response structures, refer to the serializers in the `api/serializers/` directory.

## File Structure

```plaintext
├── api/                              # Core application logic for the REST API
│   ├── management/                   # Custom management commands
│   │   ├── commands/                 # Contains the load_data command for seeding data
│   ├── migrations/                   # Tracks database schema changes
│   ├── models/                       # Database models for Classes, Proficiencies, Races, etc.
│   ├── serializers/                  # Serializers for transforming models into JSON responses
│   ├── tests/                        # Unit tests for the API endpoints
│   ├── views/                        # ViewSets for handling API requests
│   ├── urls.py                       # API URL routing
│   ├── permissions.py                # Custom permission classes
├── csv_seed/                         # CSV files for seeding the database
│   ├── …                           # Contains CSV files for Classes, Proficiencies, Races, Spells, etc.
├── dndRestAPI/                       # Django project folder with settings and configurations
│   ├── …                           # Includes settings.py, asgi.py, wsgi.py, and other configuration files
├── static/                           # Static files (CSS, JS, etc.)
│   ├── css/                          # CSS files for styling
│       ├── simple.min.css            # Styling using Simple.css
├── templates/                        # HTML templates for the API root and other views
│   ├── api_root.html                 # Template for the API root view
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
```

# Development

## Testing

To run unit tests:

```bash
python manage.py test
```

## Running the Server

```bash
python manage.py runserver
```

## Loading Data

To load data from CSV files:

```bash
python manage.py load_data
```
