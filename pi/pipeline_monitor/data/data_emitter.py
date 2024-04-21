import logging
from .sensor_data import SensorData, DataType
from config.config import IotdbConfig
from iotdb.Session import Session
from iotdb.utils.IoTDBConstants import TSDataType


class DataEmitter:

    def emit(data: SensorData):
        raise NotImplementedError()


class IotdbDataEmitter(DataEmitter):
    _session_: Session = None

    def __init__(
        self,
        host="127.0.0.1",
        port="6667",
        user="root",
        password="root",
        device_id="root.test.device",
    ):
        self._session_ = Session(
            host,
            port=port,
            user=user,
            password=password,
            fetch_size=1024,
            zone_id="UTC+8",
            enable_redirection=True,
        )

        self._device_id_ = device_id
        self._logger_ = logging.getLogger(self.__class__.__name__)
        self._session_.open(enable_rpc_compression=False)

    def __del__(self):
        if self._session_ is not None:
            self._session_.close()

    def emit(self, data: SensorData):
        """
        Simply write a single record to IoTDB every time this function is called.
        TODO: cache the data and write to IoTDB in batches.
        """

        self._session_.insert_record(
            self._device_id_,
            data.timestamp_ms,
            [data.name],
            [self.__convert_data_type(data.data_type)],
            [data.value],
        )
        self._logger_.info(f"Inserted data: {data}")

    def __convert_data_type(self, sensor_data_type: DataType) -> TSDataType:
        try:
            return TSDataType[sensor_data_type.name]
        except:
            raise TypeError(f"Unrecognized sensor data type: {sensor_data_type}")


class DataEmitterFactory:

    @staticmethod
    def create(config: IotdbConfig):
        return IotdbDataEmitter(
            config.host, config.port, config.user, config.password, config.device_id
        )
