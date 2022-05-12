import pandas as pd

FINAL_RESULTS_PATH = "test_platform/results/final_results.pkl"

def display_results(file_path:str)->None:
    results = pd.read_pickle(file_path)
    print(results.to_string())

if __name__ == "__main__":
    display_results(FINAL_RESULTS_PATH)