import pickle

data_path = 'buffer.pkl' 

with open(data_path, 'rb') as f:
    data = pickle.load(f)

print(f"Total samples in buffer: {len(data)}")
sample = data[0]
print(f"Type of first sample: {type(sample)}")

if isinstance(sample, (list, tuple)):
    print(f"Sample length: {len(sample)}")
    print(f"Sample content (first 3 elements): {sample[:3]}")
elif isinstance(sample, dict):
    print(f"Sample keys: {list(sample.keys())}")
    # Print the first few items to see the actual target data
    for key in sample.keys():
        print(f"  Key '{key}' content type: {type(sample[key])}")
