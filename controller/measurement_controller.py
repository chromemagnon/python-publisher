
import logging

from flask import Blueprint, request, jsonify, make_response
from model.dto.iot_device_measurement_dto import IOTDeviceMeasurementDTO
from pydantic import ValidationError
from service.publisher_service import PublishService


class MeasurementController:
    """
    Controller for handling measurements from IoT devices.
    """
    def __init__(self):
        self.publish_service = PublishService()
        self.blueprint = Blueprint("measurement_blueprint", __name__)
        self._register_routes()

    def _register_routes(self):
        """
        Registers the routes for the measurement controller.
        """
        logging.info("Registering routes")
        self.blueprint.route('/publish', methods=['POST'])(self.publish)

    def publish(self):
        """
        Publishes the measurement data received from an IoT device.
        """
        try:
            measurement = IOTDeviceMeasurementDTO(**request.json)
            logging.info(f"Received message {measurement}")
            self.publish_service.publish_to_queue(measurement.model_dump_json())
            return make_response(jsonify({"message": "Data published successfully"}), 200)
        except ValidationError as e:
            logging.error(f"Validation error: {e}")
            return jsonify({'error': e.errors()}), 400
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return jsonify({'error': str(e)}), 500
