d = {'a': 1, 'b': 2}
import pickle
with open("mem.txt", 'wb') as f:
    pickle.dump(d, f)
