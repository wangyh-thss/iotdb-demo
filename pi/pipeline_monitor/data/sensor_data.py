import time
from distutils.util import strtobool
from enum import Enum
from typing import Final
from common.enum import EnumWithMeta


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
        return "%s[%s]: %s at %s" % (
            self.name,
            self.data_type,
            self._value_,
            self._timestamp_ms_,
        )

    @property
    def timestamp_ms(self):
        return self._timestamp_ms_


class BallColorDetectionData(SensorData):
    """
    Data for ball collor in integer format, where
      - 1 means blue
      - 2 means white
    """

    name: Final[str] = "ball_color_detection"
    data_type: Final[DataType] = DataType.INT32


class SensorType(EnumWithMeta):
    UNKNOWN = 0, EnumWithMeta
    BALL_COLOR = 1, BallColorDetectionData

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
