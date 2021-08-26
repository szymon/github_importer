# Github importer (NSFW)

Import python packages from github without explicitly installing them.
To use it simply install this package (`pip install git+github.com/szymon/github_importer`)
and put `from github.<repository owner> import <repository name> [as new_name])`.

If nothings broken it should download the package in background and use it.


```python
>>> from github.numpy import numpy as np
>>> np.__version__
```

