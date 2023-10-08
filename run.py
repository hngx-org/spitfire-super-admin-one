from super_admin_1 import create_app
from logs.event_logger import generate_log_file_d
from uuid import uuid4

app = create_app()

@app.route('/api/download/log')
def log():
    
    generate_log_file_d()
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
