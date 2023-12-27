
from datetime import datetime
from pydantic import BaseModel, Field


class IOTDeviceMeasurementDTO(BaseModel):
    """
    Data Transfer Object for measurements from an IoT device.

    Attributes:
        device_identifier: Unique identifier of the IoT device.
        temperature: Temperature measurement from the IoT device.
        measurement_time: The time when the measurement was taken.
    """
    device_identifier: str = Field(..., example="de0d880d-c5eb-4d9a-96ca-4542167dcc0b",
                                   description="Unique identifier for the IoT device")
    temperature: float = Field(..., gt=-273, example=25.0,
                               description="Temperature value in Celsius")
    measurement_time: datetime = Field(default_factory=datetime.now,
                                       description="Timestamp when the measurement was recorded")
