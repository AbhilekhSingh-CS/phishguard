import time
from lookups import get_lookups

for attempt in [1, 2]:
    start = time.time()
    result = get_lookups("google.com")
    seconds = time.time() - start
    print(f"Attempt {attempt}: {result} took {seconds:.2f} seconds")