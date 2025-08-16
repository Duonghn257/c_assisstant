import os
import yaml
from loguru import logger
from ..configs.settings import get_settings


class ConfigLoader:
    def __init__(self, config_path=None):
        if config_path is None:
            configs = get_settings()
            config_path = configs.AGENT_CONFIG_FILE
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        logger.info(f"Loading config from {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return data
        except FileNotFoundError:
            logger.error(f"Agent configuration file not found: {path}")
        except yaml.YAMLError as e:
            logger.error(f"Error loading agent configuration file: {e}")
        except Exception as e:
            logger.error(f"Error loading agent configuration file: {e}")


# Example usage:
# math_config = ConfigLoader().config["Math Agent"]
if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.config["Math Agent"])
    print(type(config_loader.config["Math Agent"]))
