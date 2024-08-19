import os
import yaml
from snowflake.snowpark.files import SnowflakeFile

def load_data_from_package(package, filename):
    try:
        # Attempt to construct the file path directly
        data_path = os.path.join(os.path.dirname(package.__file__), filename)
        if os.path.exists(data_path):
            with open(data_path, 'rt') as file:
                return file.read()
        else:
            # Path does not exist, likely a zip import
            raise FileNotFoundError
    except (AttributeError, FileNotFoundError):
        # __file__ is not set or path doesn't exist, use the loader
        if hasattr(package, '__loader__'):
            return package.__loader__.get_data(filename).decode('utf-8')
        else:
            raise Exception(f"Failed to load data from {filename}")

def fetch_parameters(file: str) -> dict:
    """Get parameters from a YAML file.
    
    Parameters:
    file: str
        Name of the YAML file containing parameters for the notebook.
    
    Returns:
    params: dict
        Parameters loaded from the YAML file.
    """
    try:
        # First, try to load the file from the package
        import parameters
        yaml_data = load_data_from_package(parameters, file)
        print(f"Parameter file {file} loaded from package")
    except Exception as e:
        print(f"Failed to load from package: {e}")
        # If loading from package fails, try to open as a SnowflakeFile
        try:
            with SnowflakeFile.open(file, 'r') as f:
                yaml_data = f.read()
            print(f"Parameter file {file} loaded from SnowflakeFile")
        except Exception as e:
            print(f"Failed to fetch parameters: {e}")
            return None

    # Parse the YAML content
    try:
        params = yaml.safe_load(yaml_data)
        return params
    except Exception as e:
        print(f"Failed to parse YAML: {e}")