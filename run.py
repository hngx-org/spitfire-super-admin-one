from super_admin_1 import create_app
from logs.event_logger import register_action_d
from uuid import uuid4

app = create_app()

@app.route('/log')
def log():
    uuid = str(uuid4)
    register_action_d(uuid, 'suspend', 'product_id')
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
