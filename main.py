
import logging
import os
from flask import Flask
from controller.measurement_controller import MeasurementController

# Flask App Initialization
app = Flask(__name__)

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Environment Variables for App Configuration
host = os.getenv('FLASK_HOST', '0.0.0.0')
port = os.getenv('FLASK_PORT', 5000)
debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Controller Initialisation
try:
    measurement_controller = MeasurementController()
    app.register_blueprint(measurement_controller.blueprint, url_prefix='/api')
except Exception as e:
    logging.error(f'Error setting up controllers: {e}')

# Main Execution
if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug_mode)
