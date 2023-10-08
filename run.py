from super_admin_1 import create_app
from super_admin_1.products.event_logger import generate_log_file_d
from uuid import uuid4

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
