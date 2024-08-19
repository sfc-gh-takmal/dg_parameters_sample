from snowflake.snowpark import Session
from parameters import fetch_parameters
import sys

def run_training(session: Session, yaml_file_path: str) -> str:
    messages = []
    
    def log(message):
        print(message)  # This will print to the Snowflake query log
        messages.append(message)

    log(f"Attempting to fetch parameters from: {yaml_file_path}")
    params = fetch_parameters(yaml_file_path)
    if params is None:
        log("Failed to fetch parameters")
        return "Failed to fetch parameters\n" + "\n".join(messages)
    
    log(f"Successfully fetched parameters: {params}")
    
    # Use the parameters in your code
    churn_days_training = params['churn_days']['training']
    churn_days_inference = params['churn_days']['inference']

    log(f"Churn days for training: {churn_days_training}")
    log(f"Churn days for inference: {churn_days_inference}")

    # Example usage in training logic
    def train_model():
        log(f"Training model with churn_days = {churn_days_training}")

    train_model()
    return "Done\n" + "\n".join(messages)