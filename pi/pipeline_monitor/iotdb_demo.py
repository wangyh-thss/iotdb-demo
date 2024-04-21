import logging
from config.config import Config
from data.data_source import DataSource, DataSourceFactory
from data.data_emitter import DataEmitter, DataEmitterFactory


class IotdbDemo:

    def __init__(self, data_source: DataSource, data_emitter: DataEmitter):
        self._data_source_ = data_source
        self._data_emitter_ = data_emitter
        self._logger_ = logging.getLogger(self.__class__.__name__)

    @classmethod
    def load_config(cls, config: Config):
        return cls(
            DataSourceFactory.create(config.data_source),
            DataEmitterFactory.create(config.iotdb),
        )

    def run(self):
        self._logger_.info("IoTDB demo running...")
        while True:
            try:
                data = self._data_source_.read_data_blocking()
            except TimeoutError:
                self._logger_.warn("Read data from source timeout.")

            if data:
                self._data_emitter_.emit(data)
