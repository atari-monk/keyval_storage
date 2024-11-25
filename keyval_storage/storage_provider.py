from dataclasses import dataclass
import os
from cli_logger.logger import setup_logger
from cli_tool.config import LOGGER_CONFIG    
from pytoolbox.folder import ensure_folder_exists
from keyval_storage.storage import KeyValueStorage

logger = setup_logger(__name__, LOGGER_CONFIG)

@dataclass
class StorageConfig:
    storage_path_key: str
    storage_file_name: str

class StorageProvider:
    def __init__(self, config: StorageConfig):
        self._config = config
        self._storage_path_key = config.storage_path_key
        self._storage_file_name = config.storage_file_name

    def load_storage(self, storage_path: str) -> KeyValueStorage | None:
        try:
            storage = KeyValueStorage(storage_path)

            storage_path_from_storage = storage.get(self._storage_path_key)
            
            if storage_path == storage_path_from_storage:
                return storage
            else:
                logger.error(f"Error when loading storage file - {storage_path}: Storage failed data check.")
                return None   
        except Exception as e:
            logger.error(f"Error when loading storage file - {storage_path}: {e}")
            return None

    def save_storage(self) -> tuple[KeyValueStorage, str]:
        try:
            data_folder_path = input("Provide PATH for cli_tool DATA FOLDER:> ").strip()
            ensure_folder_exists(data_folder_path)

            storage_file_path = os.path.join(data_folder_path, self._storage_file_name)

            storage = KeyValueStorage(storage_file_path)
            
            storage.set(self._storage_path_key, storage_file_path)

            return storage, storage_file_path
        except Exception as e:
            logger.error(f"Error when saving storage file: {e}")
   