import os
from pathlib import Path
from keyval_storage.constants import APP_DATA_FOLDER, KEY_VALUE_STORAGE_PATH_KEY
from keyval_storage.config_provider import ConfigProvider, PathData
from keyval_storage.storage import KeyValueStorage
from keyval_storage.storage_provider import StorageConfig, StorageProvider

class ConfigAndKeyValueStorageDataModel:
    def __init__(self, appName: str):
        self._appName = appName
        self._configProvider = ConfigProvider(PathData(os.path.join('C:\\configs', appName), f'{appName}_config.json'))
        self._storageProvider = StorageProvider(StorageConfig('storage.json'))

    def getKeyValueStorage_NewFileAndConfig(self) -> KeyValueStorage:
        storage, storageFilePath = self._storageProvider.save_storage()
        self._configProvider.save_file({APP_DATA_FOLDER: Path(storageFilePath).parent})
        self._configProvider.save_file({KEY_VALUE_STORAGE_PATH_KEY: storageFilePath})
        return storage

    def getKeyValueStorage_LoadUsingConfig(self) -> KeyValueStorage | None:
        config = self._configProvider.load_file()
        if config:
            return self._storageProvider.load_storage(config[KEY_VALUE_STORAGE_PATH_KEY])
