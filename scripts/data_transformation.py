import pandas as pd

if __name__=="__main__":
    df = pd.read_json (r'data/raw_data.json')
    df.to_csv (r'data/raw_data.csv', index = None)