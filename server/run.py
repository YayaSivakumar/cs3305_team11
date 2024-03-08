from app.app import create_app, start_scheduler

"""
This is the entry point of the application.
It will create the app instance and start the scheduler.
"""

if __name__ == '__main__':
    app_instance = create_app()
    start_scheduler(app_instance)
    app_instance.run(debug=True)
