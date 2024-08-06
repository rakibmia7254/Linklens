# Linklens

Linklens is a robust URL shortening and click-tracking application built with Django. By leveraging the is.gd API for URL shortening and wrapping, Linklens provides an efficient way to generate custom short links while tracking detailed analytics on each click, including the device, browser, and country of origin.

## Features

- **URL Shortening:** Seamlessly shorten URLs using the is.gd API.
- **Custom Aliases:** Create custom aliases for your short links.
- **Click Tracking:** Track detailed analytics on each click, such as:
  - Device type
  - Browser
  - Country of origin
- **QR Code Generation:** Generate QR codes for your short links for easy sharing.
- **User Management:** Support for multiple users with personalized dashboards.
- **Data Storage:** Securely store link and click data in an SQLite database.
- **Real-time Analytics:** View real-time statistics on link performance.
- **User Verification:** Verify users via email during registration.
- **Password Management:** Send email for forgot password and reset password functionality.
- **Configurable Email Service:** Easily enable or disable the email service by changing a variable (`email_service`) in `/utils/mail.py`.

## Installation

1.  Clone the repository:

        git clone https://github.com/rakibmia7254/linklens.git
        cd linklens

2.  Create a virtual environment and activate it:

        python -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`

3.  Install the dependencies:

        pip install -r requirements.txt

4.  Apply migrations:

        python manage.py migrate

5.  Start the development server:

        python manage.py runserver

## Usage

1.  Register a new account or log in with an existing one.
2.  Create a new short link by providing the original URL and an optional custom alias.
3.  Share the generated short link or QR code.
4.  View detailed analytics on the clicks received, including device, browser, and country information.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the MIT License.
