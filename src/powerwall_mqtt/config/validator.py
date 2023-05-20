from typing import Dict, Any
import logging


logger = logging.getLogger(__name__)

def find_config() -> str:
    """
    Find config returning a path.

    Goes through reasonable defaults.
    1. Look for a config in the current directory
    2. Look for a config in $XDG_CONFIG_DIRS
    3. Look for a config in etc
    4. Use default config if none is found (embedded in package)
    https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
    :return: path to config file found
    """
    pass
def _read_raw(file: str) -> Dict[str, Any]:
    assert os.path.isfile(file)
    with open(file, "r") as f:
        cfg = yaml.safe_load(f.read())
        return cfg

def read_config(file: Optional[str]) -> Dict[str, Any]:
    if file:
        return _read_raw(file)
    else:
        config_file = find_config()
        logger.info(f"Using config file: '{config_file}'")
        return __read_raw(config_file)
