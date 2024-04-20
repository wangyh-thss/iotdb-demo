import logging
import serial
from .sensor_data import SensorData, create_sensor_data
from common.timeout import func_with_timeout
from config.config import DataSourceConfig


class DataSource:

    def read_data(self) -> SensorData:
        raise NotImplementedError()

    def read_data_blocking(self, timeout_seconds=None) -> SensorData:
        raise NotImplementedError()


class SerialDataSource(DataSource):
    """
    Data source that generates sensor data from a given serial, such as USB. The data will be passed as utf-8 strings
    and should follow the pattern: `<sensor>|<value>`, where the options of <sensor> is defined in sensor_data.py.
    """

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self._serial_ = serial.Serial(port, baudrate)
        self._logger_ = logging.getLogger(self.__class__)

    def read_data(self) -> SensorData:
        serial_data = self._serial_.readline
        if not serial_data:
            return None
        data_str = serial_data.decode("utf-8")
        self._logger_.info(f"Received raw data string: {data_str}")
        data = self.__parse_data(data_str)
        self._logger_.info(f"Parsed data: {data}")
        return data

    def read_data_blocking(self, timeout_second=None) -> SensorData:
        """
        Reads a sensor data in a blocking manner, i.e., thread will be blocked until a valid sensor data is read from
        serial.
        """
        return func_with_timeout(
            self.read_data, lambda res: res is not None, timeout_second
        )

    def __parse_data(self, data: str) -> SensorData:
        try:
            sensor_tag, value = data.split("|")
        except:
            print(f"Received data [{data}] does not follow the pattern.")

        return create_sensor_data(sensor_tag, value)


class DataSourceFactory:

    @staticmethod
    def create(config: DataSourceConfig):
        if config.type == DataSourceConfig.DataSourceType.SERIAL:
            return SerialDataSource(config.port, config.baudrate)
        raise ValueError(f"Unknown data source type: {config.type}")
