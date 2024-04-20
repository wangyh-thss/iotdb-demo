from enum import Enum


class DataSourceConfig:

    class DataSourceType(Enum):
        UNKNOWN = 0
        SERIAL = 1

    def __init__(self, type: DataSourceType, port: str, baudrate: int):
        self._type_ = type
        self._port_ = port
        self._baudrate_ = baudrate

    @classmethod
    def from_obj(cls, obj: dict):
        return cls(
            DataSourceConfig.DataSourceType[obj.get("type", "SERIAL")],
            obj.get("port", "/dev/ttyUSB0"),
            obj.get("baudrate", 115200),
        )

    @property
    def type(self) -> DataSourceType:
        return self._type_

    @property
    def port(self) -> str:
        return self._port_

    @property
    def baudrate(self) -> int:
        return self._baudrate_


class IotdbConfig:

    def __init__(self, host: str, port: int, user: str, password: str, device_id: str):
        self._host_ = host
        self._port_ = port
        self._user_ = user
        self._password_ = password
        self._device_id_ = device_id

    @classmethod
    def from_obj(cls, obj):
        return cls(
            obj.get("host", "127.0.0.1"),
            obj.get("port", 6667),
            obj.get("user", "root"),
            obj.get("password", "root"),
            obj.get("device_id", "root.database.device"),
        )

    @property
    def host(self) -> str:
        return self._host_

    @property
    def port(self) -> str:
        return str(self._port_)

    @property
    def user(self) -> str:
        return self._user_

    @property
    def password(self) -> str:
        return self._password_

    @property
    def device_id(self) -> str:
        return self._device_id_


class Config:

    def __init__(self, data_source_config: DataSourceConfig, iotdb_config: IotdbConfig):
        self._data_source_config_ = data_source_config
        self._iotdb_config_ = iotdb_config

    @classmethod
    def from_obj(cls, obj):
        return cls(
            DataSourceConfig.from_obj(obj.get("data_source", {})),
            IotdbConfig.from_obj(obj.get("iotdb")),
        )

    @property
    def data_source(self) -> DataSourceConfig:
        return self._data_source_config_

    @property
    def iotdb(self) -> IotdbConfig:
        return self._iotdb_config_
