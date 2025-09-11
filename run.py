# Development server entry point for Portfolio Analyzer - runs Flask app in debug mode
"""Runs the application"""


from app import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)