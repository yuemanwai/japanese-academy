# How to Use This Repository

If you are using Codespaces, simply clone this repository and wait for the page on port 5000 to appear. Everything will be set up automatically.

# Commands that might help

## For Database

### Commands for Initial migration

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

### How to Modify Attributes in Existing Database

You need to **Manually** delete the table from the database and run the following commands to apply the changes:

```bash
# Apply the migration to the database
flask db upgrade

# Generate a new migration after making changes to the models
flask db migrate -m "Description of changes."

# Apply the new migration to the database
flask db upgrade
```

## To use Gemini on the website

Open **.env** file and paste your api key

## To Use Copilot on the Website

You need to install Google Chrome on Linux. Since Copilot does not have an API, Selenium is used instead.

To proceed, download the **latest version** of Google Chrome and ensure that you are using the **same version** for both Chrome and ChromeDriver.

### Verify the versions for Chrome and ChromeDriver

```bash
# Check the installed version of Google Chrome
google-chrome --version

# Check the installed version of ChromeDriver
./chromedriver-linux64/chromedriver --version
```

### Different Versions URL

[https://googlechromelabs.github.io/chrome-for-testing/](https://googlechromelabs.github.io/chrome-for-testing/)
![alt text](./app/static/image/image.png)

## Example

### Stable

| Binary       | Platform | URL                                            |
| ------------ | -------- | ---------------------------------------------- |
| Chrome       | Linux64  | https://xxx/136.x.x.x/chrome-linux64.zip       |
| ChromeDriver | Linux64  | https://xxx/136.x.x.x/chromedriver-linux64.zip |

### How to download Google Chrome (.deb)

```bash
# Download the Google Chrome .deb file
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# If you encounter dependency issues, run the following commands to fix broken packages
sudo apt update
sudo apt --fix-broken install -y

# Install the .deb file
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

### How to download Chrome & ChromeDriver (.zip)

Run the following command to download ChromeDriver:

```bash
curl -O https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.92/linux64/chrome-linux64.zip

curl -O https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.92/linux64/chromedriver-linux64.zip

unzip chrome-linux64.zip
unzip chromedriver-linux64.zip

rm chrome-linux64.zip
rm chromedriver-linux64.zip
```

## For Translations

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

### How to Run Tests and Generate Allure Reports

To run all tests and generate Allure-compatible results, use the following command:

```bash
pytest tests/*.py --alluredir=allure_results
```

> **Note:** Make sure you have `pytest` and the Allure plugin installed. The results will be saved in the `allure-results` directory, which you can use to generate detailed test reports with Allure.

## Additional Resources

- [Download Chrome and ChromeDriver](https://getwebdriver.com/chromedriver)
- [Gemini API Quickstart Guide](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-tw&lang=python)
- [CSS Inspiration](https://codepen.io/topics/)

## Important Note

After creating or updating **anything**, remember to re-run the Flask application to apply the changes:

```bash
flask --debug run --host=0.0.0.0
```
