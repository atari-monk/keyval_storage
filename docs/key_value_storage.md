# Key Value Storage

## I need a robust system to store key value pair data in json. For my cli app in py. I think it needs to be a repo and module so that can be use as a pip lib used in other pip modules.

Here's a step-by-step plan for implementing a robust JSON-based key-value data storage system as a Python package and making it reusable as a module for other projects via `pip`:

---

### **System Features**

1. **Key-Value Storage**:
    - Store key-value pairs in a JSON file.
    - Allow retrieval, update, deletion, and listing of keys.
2. **CLI Interface**:

    - Provide a command-line interface for CRUD operations.

3. **Robustness**:

    - Validate keys and values.
    - Ensure atomic operations (avoid data corruption).
    - Handle invalid JSON files gracefully.

4. **Reusability**:

    - Packaged as a Python module.
    - Installable via `pip`.

5. **Flexibility**:
    - Allow specifying the storage location (e.g., via environment variables or config files).

---

### **Implementation Plan**

#### 1. **Folder Structure**

Create a folder structure like this:

```
keyval_storage/
│
├── keyval_storage/
│   ├── __init__.py
│   ├── storage.py    # Core logic
│   ├── cli.py        # Command-line interface
│   ├── exceptions.py # Custom exceptions
│
├── tests/
│   ├── test_storage.py
│   ├── test_cli.py
│
├── setup.py          # For pip packaging
├── README.md         # Documentation
├── LICENSE           # License for reuse
├── .gitignore
```

---

#### 2. **Core Module**

Create the core functionality in `storage.py`:

```python
import json
import os
from threading import Lock

class KeyValueStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.lock = Lock()
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _read_data(self):
        with self.lock:
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                raise ValueError("Corrupted JSON file")

    def _write_data(self, data):
        with self.lock:
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)

    def get(self, key: str):
        data = self._read_data()
        return data.get(key, None)

    def set(self, key: str, value):
        data = self._read_data()
        data[key] = value
        self._write_data(data)

    def delete(self, key: str):
        data = self._read_data()
        if key in data:
            del data[key]
            self._write_data(data)

    def list_keys(self):
        data = self._read_data()
        return list(data.keys())
```

---

#### 3. **CLI Interface**

Add a command-line interface in `cli.py` using `argparse`:

```python
import argparse
from keyval_storage.storage import KeyValueStorage

def main():
    parser = argparse.ArgumentParser(description="Key-Value JSON Storage CLI")
    parser.add_argument("--file", required=True, help="Path to the JSON storage file")
    parser.add_argument("--action", required=True, choices=["get", "set", "delete", "list"], help="Action to perform")
    parser.add_argument("--key", help="Key for the action")
    parser.add_argument("--value", help="Value for the 'set' action")

    args = parser.parse_args()
    storage = KeyValueStorage(args.file)

    if args.action == "get":
        if not args.key:
            print("Key is required for 'get' action")
            return
        print(storage.get(args.key))

    elif args.action == "set":
        if not (args.key and args.value):
            print("Key and value are required for 'set' action")
            return
        storage.set(args.key, args.value)
        print(f"Set {args.key} to {args.value}")

    elif args.action == "delete":
        if not args.key:
            print("Key is required for 'delete' action")
            return
        storage.delete(args.key)
        print(f"Deleted key {args.key}")

    elif args.action == "list":
        print(storage.list_keys())
```

---

#### 4. **Packaging for Pip**

Add the `setup.py` file for packaging:

```python
from setuptools import setup, find_packages

setup(
    name="keyval-storage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "keyval-cli=keyval_storage.cli:main"
        ]
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple JSON-based key-value storage library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/keyval-storage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
```

---

#### 5. **Testing**

Write unit tests in the `tests/` folder using `pytest`:

Example for `test_storage.py`:

```python
import os
import pytest
from keyval_storage.storage import KeyValueStorage

@pytest.fixture
def temp_file(tmpdir):
    return os.path.join(tmpdir, "test.json")

def test_set_and_get(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    assert storage.get("key1") == "value1"

def test_delete(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    storage.delete("key1")
    assert storage.get("key1") is None

def test_list_keys(temp_file):
    storage = KeyValueStorage(temp_file)
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    assert set(storage.list_keys()) == {"key1", "key2"}
```

---

#### 6. **Publishing the Package**

1. Build the package:
    ```bash
    python setup.py sdist bdist_wheel
    ```
2. Upload to PyPI using `twine`:
    ```bash
    twine upload dist/*
    ```

---

You can now install the package using `pip install keyval-storage` and use the CLI or the library in other projects.
