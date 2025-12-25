"""
A simple HTTP honeypot that mimics a WordPress admin login page.

This module uses the Flask web framework to serve a fake login page. It captures
any submitted credentials and logs them for analysis, along with details about
the client such as their IP address and User-Agent.
"""

import logging
from flask import Flask, render_template, request
from honeypot.core.logging import setup_logger

# Set up a dedicated logger for HTTP credential attempts.
http_logger = setup_logger("http.auth", "http/credentials.log")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates")

    @app.route("/", methods=["GET"])
    @app.route("/wp-admin", methods=["GET"])
    @app.route("/wp-login.php", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "N/A")
            password = request.form.get("password", "N/A")

            # Log the captured credentials and client information.
            http_logger.info(
                f"Login attempt from {request.remote_addr} - "
                f"Username: '{username}', Password: '{password}' - "
                f"Agent: {request.headers.get('User-Agent', 'N/A')}"
            )

            # Always return a failed login response.
            return render_template("wp-admin.html", login_error=True), 401
        
        # For GET requests, just show the login page.
        return render_template("wp-admin.html", login_error=False)

    return app


def run_web_honeypot(address: str, port: int) -> None:
    web_app = create_app()
    # In a real deployment, a production-grade WSGI server like Gunicorn or uWSGI
    # should be used instead of Flask's built-in development server.
    web_app.run(debug=False, port=port, host=address)