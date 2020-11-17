import random
from search import linear_search, binary_search
from datetime import datetime

data = random.sample(range(1000000000), 1000000)
linear_start = datetime.now()
linear_index = linear_search(data, data[-1])
linear_end = datetime.now()
linear_elapsed = linear_end - linear_start
data = sorted(data)
binary_start = datetime.now()
binary_index = binary_search(data, 0, len(data)-1, data[-1])
binary_end = datetime.now()
binary_elapsed = binary_end - binary_start

print(f'Found at {linear_index}.Time taken by linear search {linear_elapsed}')
print(f'Found at {binary_index}.Time taken by binary search {binary_elapsed}')