from super_admin_1 import create_app
from uuid import uuid4

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
