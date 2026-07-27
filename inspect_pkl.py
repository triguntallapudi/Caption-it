import pickle
import numpy as np

try:
    with open('features.pkl', 'rb') as f:
        features = pickle.load(f)
    print(f"Type of features.pkl: {type(features)}")
    if isinstance(features, dict):
        print(f"Number of keys: {len(features)}")
        if len(features) > 0:
            key = list(features.keys())[0]
            print(f"Example key: {key}")
            val = features[key]
            print(f"Type of value: {type(val)}")
            if isinstance(val, np.ndarray):
                print(f"Shape of value: {val.shape}")
            elif hasattr(val, 'shape'):
                print(f"Shape of value: {val.shape}")
except Exception as e:
    print(f"Error reading features.pkl: {e}")
