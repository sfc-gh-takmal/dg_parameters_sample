import sys, os
from snowflake.snowpark import Session
from snowflake.snowpark.files import SnowflakeFile

import importlib.util
import yaml
import logging

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

def execute_sql_commands_from_yaml(session, yaml_file_path):
    # Find and load the module as a resource
    import procedures
    yaml_data = load_data_from_package(procedures, yaml_file_path)
    
    # Parse the YAML content
    yaml_content = yaml.safe_load(yaml_data)

    # Extract SQL commands from the YAML content
    sql_commands = yaml_content.get('sql_commands', [])

    try:
        # Execute each SQL command
        for command in sql_commands:
            session.sql(command).show()
            print(f"Executed: {command}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage

def run_commands(session: Session, yaml_file_path: str) -> str:
    execute_sql_commands_from_yaml(session,yaml_file_path)
    return "Done"