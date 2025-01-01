# How to Use This Repository

Wait until the page on port 5000 pops up, and everything will be set up.

## File Structure

```
FYP_AI-powered_Interactive_Japanese_Academy/
├── app/
│   ├── __init__.py          # Initializes the Flask application and sets up configurations
│   ├── routes.py            # Defines the routes and view functions for the application
│   ├── models.py            # Defines the database models
│   ├── forms.py             # Defines the forms used in the application
│   ├── templates/           # Contains all the HTML templates
│   │   ├── base.html.j2     # Base template that other templates extend from
│   │   ├── index.html.j2    # Home page template
│   │   ├── login.html.j2    # Login page template
│   │   ├── register.html.j2 # Registration page template
│   │   ├── random_post.html.j2 # Template for displaying a random post
│   │   ├── donate.html.j2   # Donation page template
│   │   ├── donate_payment.html.j2 # Donation payment page template
│   │   ├── logout.html.j2   # Logout page template
│   │   ├── lessons.html.j2  # Lessons page template
│   │   ├── practice.html.j2 # Practice page template
│   │   ├── dictionary.html.j2 # Dictionary page template
│   │   ├── community.html.j2 # Community page template
│   │   ├── shared.html.j2   # Shared page template for coming soon features
│   │   ├── 404.html.j2      # 404 error page template
│   ├── static/              # Contains static files like CSS, JavaScript, and images
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── translations/        # Contains translation files
│   ├── babel.cfg            # Configuration file for Babel
├── migrations/              # Database migration files
├── test_data.py             # Script to load mock data into the database
├── requirements.txt         # List of Python dependencies
├── README.md                # This file
├── .env                     # Environment variables
```

### Description of Key Files

- `app/__init__.py`: Initializes the Flask application and sets up configurations.
- `app/routes.py`: Defines the routes and view functions for the application.
- `app/models.py`: Defines the database models.
- `app/forms.py`: Defines the forms used in the application.
- `app/templates/`: Contains all the HTML templates.
  - `base.html.j2`: Base template that other templates extend from.
  - `index.html.j2`: Home page template.
  - `login.html.j2`: Login page template.
  - `register.html.j2`: Registration page template.
  - `random_post.html.j2`: Template for displaying a random post.
  - `donate.html.j2`: Donation page template.
  - `donate_payment.html.j2`: Donation payment page template.
  - `logout.html.j2`: Logout page template.
  - `lessons.html.j2`: Lessons page template.
  - `practice.html.j2`: Practice page template.
  - `dictionary.html.j2`: Dictionary page template.
  - `community.html.j2`: Community page template.
  - `shared.html.j2`: Shared page template for coming soon features.
  - `404.html.j2`: 404 error page template.
- `app/static/`: Contains static files like CSS, JavaScript, and images.
- `app/translations/`: Contains translation files.
- `babel.cfg`: Configuration file for Babel.
- `migrations/`: Database migration files.
- `test_data.py`: Script to load mock data into the database.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This file.
- `.env`: Environment variables.

## Commands That Might Help

### How to Create Translations

Run the following commands:

```bash
cd app/
mkdir translations
pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations -l en
pybabel init -i translations/messages.pot -d translations -l es
pybabel init -i translations/messages.pot -d translations -l zh
pybabel compile -d translations
```

### How to Update Translations

Run the following command:

```bash
cd app/
pybabel update -i translations/messages.pot -d translations
```