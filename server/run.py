from app.app import create_app, start_scheduler

if __name__ == '__main__':
    app_instance = create_app()
    start_scheduler(app_instance)
    app_instance.run(debug=True)
