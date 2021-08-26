import time

try:
    import tqdm
except ImportError:
    print("Cannot import tqdm with 'import tqdm'")

from github import CONFIG

CONFIG["verbose"] = True
CONFIG["install_directory"] = "/tmp/tmp.uftSxrhdGN"
CONFIG["force_upgrade"] = False

from github.tqdm import tqdm  # noqa
from github.numpy import numpy as np  # noqa
from github.pypa import packaging  # noqa

for i in tqdm.tqdm(range(10)):
    time.sleep(0.1)


print(np.random.rand(3, 2))
