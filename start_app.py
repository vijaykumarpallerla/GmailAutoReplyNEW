
import subprocess
import sys
import os

# Set up paths for database and media
if sys.platform == 'win32':
    LOCALAPPDATA = os.environ.get('LOCALAPPDATA', os.path.expanduser('~'))
    db_dir = os.path.join(LOCALAPPDATA, 'GmailAutoReply')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'db.sqlite3')
    media_dir = os.path.join(db_dir, 'media')
    os.makedirs(media_dir, exist_ok=True)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_path, 'db.sqlite3')
    media_dir = os.path.join(base_path, 'media')
    os.makedirs(media_dir, exist_ok=True)

def run_migrations():
    print('Running migrations...')
    import django
    from django.core import management
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
    django.setup()
    management.call_command('migrate')


def start_server():
    print('Starting Django server...')
    import threading
    import webbrowser
    import os
    import django
    from django.core import management

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gmail_auto_reply.settings')
    django.setup()

    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8000/')

    threading.Thread(target=open_browser, daemon=True).start()
    management.call_command('runserver', '127.0.0.1:8000', use_reloader=False)



if __name__ == '__main__':
    run_migrations()
    start_server()
