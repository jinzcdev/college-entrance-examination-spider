import os
import pickle


def get_data_from_cache(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return None


def save_data_to_cache(data, file_path):
    with open(file_path, "wb") as f:
        pickle.dump(data, f)
