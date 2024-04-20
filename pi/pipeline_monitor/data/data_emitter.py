import logging
from .sensor_data import SensorData
from config.config import IotdbConfig
from iotdb.Session import Session


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
        self._session = Session(
            host,
            port=port,
            user=user,
            password=password,
            fetch_size=1024,
            zone_id="UTF-8",
            enable_redirection=True,
        )

        self._session_.open(enable_rpc_compression=False)
        self._device_id_ = device_id
        self._logger_ = logging.getLogger(self.__class__)

    def emit(self, data: SensorData):
        """
        Simply write a single record to IoTDB every time this function is called.
        TODO: cache the data and write to IoTDB in batches.
        """

        self._session_.insert_record(
            self._device_id_, data.timestamp_ms, [data.name], [data.timestamp_ms]
        )
        self._logger_.info(f"Interted data: {data}")


class DataEmitterFactory:

    @staticmethod
    def create(config: IotdbConfig):
        return IotdbDataEmitter(
            config.host, config.port, config.user, config.password, config.device_id
        )
