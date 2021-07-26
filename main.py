import time

from github import CONFIG

CONFIG["verbose"] = True
CONFIG["install_directory"] = "/tmp/tmp.uftSxrhdGN"
CONFIG["force_upgrade"] = False

from github.tqdm import tqdm
from github.numpy import numpy as np
from github.pypa import packaging

for i in tqdm.tqdm(range(10)):
    time.sleep(0.1)


print(np.random.rand(3, 2))
