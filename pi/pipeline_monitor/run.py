import logging.config
import yaml
from config.config import Config
from iotdb_demo import IotdbDemo


def config_logging():
    with open("logging.yaml", "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)


def run():
    with open("config.yaml", "r") as f:
        yaml_config_obj = yaml.load(f, Loader=yaml.FullLoader)
    config = Config.from_obj(yaml_config_obj)
    demo = IotdbDemo.load_config(config)
    demo.run()


if __name__ == "__main__":
    config_logging()
    run()
