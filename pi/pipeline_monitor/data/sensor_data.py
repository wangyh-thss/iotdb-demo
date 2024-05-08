import time
from common.enum import EnumWithMeta
from distutils.util import strtobool
from typing import Final


class DataType(EnumWithMeta):
    UNKNOWN = 0, lambda v: v
    INT32 = 1, int
    INT64 = 2, int
    FLOAT = 3, float
    DOUBLE = 4, float
    BOOLEAN = 5, lambda v: bool(strtobool(v))
    TEXT = 6, str

    def check_value(self, value):
        return self._meta_(value)


class SensorData:
    name = ""
    data_type = DataType.UNKNOWN

    def __init__(self, value, timestamp_ms: int = None):
        self._value_ = self.data_type.check_value(value)
        if not timestamp_ms:
            timestamp_ms = int(time.time() * 1000)
        self._timestamp_ms_ = timestamp_ms

    def __str__(self):
        formatted_time = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(self._timestamp_ms_ / 1000)
        )
        return f"{self.name}[{self.data_type.name}]: {self._value_} at {formatted_time}"

    @property
    def timestamp_ms(self):
        return self._timestamp_ms_

    @property
    def value(self):
        return self._value_


class BallColorDetectionData(SensorData):
    """
    Data for ball color in integer format, where
      - 1 means blue
      - 2 means white
    """

    name: Final[str] = "ball_color_detection"
    data_type: Final[DataType] = DataType.INT32


class TemperatureData(SensorData):
    """Data for air temperature"""

    name: Final[str] = "temperature"
    data_type: Final[DataType] = DataType.FLOAT


class HumidityData(SensorData):
    """Data for relative humidity"""

    name: Final[str] = "humidity"
    data_type: Final[DataType] = DataType.FLOAT


class HeatIndexData(SensorData):
    """
    Data for head index which is calculated by temperature and humidity
    Wiki: https://en.wikipedia.org/wiki/Heat_index
    """

    name: Final[str] = "heat_index"
    data_type: Final[DataType] = DataType.FLOAT


class SensorType(EnumWithMeta):
    UNKNOWN = 0, EnumWithMeta
    BALL_COLOR = 1, BallColorDetectionData
    TEMPERATURE = 2, TemperatureData
    HUMIDITY = 3, HumidityData
    HEAT_INDEX = 4, HeatIndexData

    @staticmethod
    def from_tag(tag: str):
        try:
            return SensorType[tag]
        except KeyError:
            raise ValueError(f"Invalid tag for sensor type: {tag}")

    def create_sensor_data(self, value, timestamp_ms: int = None) -> SensorData:
        return self._meta_(value, timestamp_ms)


def create_sensor_data(sensor_tag: str, value, timestamp_ms: int = None) -> SensorData:
    return SensorType.from_tag(sensor_tag).create_sensor_data(value, timestamp_ms)
