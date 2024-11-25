import os
from keyval_storage.config_provider import ConfigProvider, PathData
from keyval_storage.storage_provider import StorageConfig, StorageProvider

STORAGE_PATH_KEY = 'storage_path'

class ConfigStorageInteraction:
    def __init__(self, appDataFolder: str):
        self._configProvider = ConfigProvider(PathData(os.path.join('C:\\', appDataFolder), 'config.json'))
        self._storageProvider = StorageProvider(StorageConfig(STORAGE_PATH_KEY, 'storage.json'))

    def interact(self):
        config = self._configProvider.load_file()
        if config:
            _ = self._storageProvider.load_storage(config[STORAGE_PATH_KEY])
        else:
            _, storageFilePath = self._storageProvider.save_storage()
            self._configProvider.save_file({STORAGE_PATH_KEY: storageFilePath})
