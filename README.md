# How to Use This Repository

Wait until the page on port 5000 pops up, and everything will be set up.

OR

```bash
flask --debug run --host=0.0.0.0
python test_data.py
```

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
│   │   ├── profile.html.j2  # User profile page template
│   │   ├── settings.html.j2 # User settings page template
│   │   ├── notifications.html.j2 # Notifications page template
│   │   ├── messages.html.j2 # Messages page template
│   ├── static/              # Contains static files like CSS, JavaScript, and images
│   │   ├── css/
│   │   │   ├── styles.css   # Main CSS file
│   │   ├── js/
│   │   │   ├── scripts.js   # Main JavaScript file
│   │   ├── images/
│   │       ├── logo.png     # Logo image
│   ├── translations/        # Contains translation files
│   ├── babel.cfg            # Configuration file for Babel
│   ├── config.py            # Configuration file for the Flask application
│   ├── errors.py            # Error handlers for the application
│   ├── utils.py             # Utility functions for the application
├── migrations/              # Database migration files
├── test_data.py             # Script to load mock data into the database
├── requirements.txt         # List of Python dependencies
├── README.md                # This file
├── .env                     # Environment variables
├── .gitignore               # Git ignore file
├── Dockerfile               # Docker configuration file
├── docker-compose.yml       # Docker Compose configuration file
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
  - `profile.html.j2`: User profile page template.
  - `settings.html.j2`: User settings page template.
  - `notifications.html.j2`: Notifications page template.
  - `messages.html.j2`: Messages page template.
- `app/static/`: Contains static files like CSS, JavaScript, and images.
  - `css/`: Contains CSS files.
    - `styles.css`: Main CSS file.
  - `js/`: Contains JavaScript files.
    - `scripts.js`: Main JavaScript file.
  - `images/`: Contains image files.
    - `logo.png`: Logo image.
- `app/translations/`: Contains translation files.
- `babel.cfg`: Configuration file for Babel.
- `config.py`: Configuration file for the Flask application.
- `errors.py`: Error handlers for the application.
- `utils.py`: Utility functions for the application.
- `migrations/`: Database migration files.
- `test_data.py`: Script to load mock data into the database.
- `requirements.txt`: List of Python dependencies.
- `README.md`: This file.
- `.env`: Environment variables.

## Commands That Might Help

### Flask Commands

Run the following commands to manage the Flask application:

```bash
# Initialize the migration repository
flask db init

# Generate an initial migration
flask db migrate -m "Initial migration."

# Apply the migration to the database
flask db upgrade

# Generate a new migration after making changes to the models
flask db migrate -m "Description of changes."

# Apply the new migration to the database
flask db upgrade
```

### How to Modify Columns in Existing Database

If you need to modify some columns in the existing database, follow these steps:

1. Manually delete the table from the database.
2. Run the following commands to apply the changes:

```bash
# Apply the migration to the database
flask db upgrade

# Generate a new migration after making changes to the models
flask db migrate -m "Description of changes."

# Apply the new migration to the database
flask db upgrade
```

### How to Install Google Chrome on Linux

Run the following commands:

```bash
# Download the Google Chrome .deb file
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# If you encounter dependency issues, run the following commands to fix broken packages
sudo apt update
sudo apt --fix-broken install -y

# Install the .deb file
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

### How to Download ChromeDriver

Run the following command to download ChromeDriver:

```bash
wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.204/linux64/chromedriver-linux64.zip
```

### How to Check Chrome and ChromeDriver Versions

Run the following commands to check the versions:

```bash
# Check Chrome version
google-chrome --version

# Check ChromeDriver version
./chromedriver-linux64/chromedriver --version
```

### How to Create Translations

Run the following commands to set up and create translations:

```bash
cd app/
mkdir translations
pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
pybabel init -i translations/messages.pot -d translations -l en
pybabel init -i translations/messages.pot -d translations -l ja
pybabel init -i translations/messages.pot -d translations -l zh
pybabel compile -d translations
```

### How to Update Translations

Run the following commands to update existing translations:

```bash
cd app/
pybabel extract -F babel.cfg -k lazy_gettext -o translations/messages.pot .
pybabel update -i translations/messages.pot -d translations
pybabel compile -d translations
```

### Additional Resources

- [Download Chrome and ChromeDriver](https://getwebdriver.com/chromedriver)
- [Gemini API Quickstart Guide](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-tw&lang=python)
- [CSS Inspiration](https://codepen.io/topics/)

#### Important Note

After creating or updating translations, remember to re-run the Flask application to apply the changes:

```bash
flask --debug run --host=0.0.0.0
```
