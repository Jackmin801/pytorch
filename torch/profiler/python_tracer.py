import os
import site
import sys
from typing import List

import torch


def _prefix_regex() -> List[str]:
    """
    Generate a sorted list of path prefixes where Python packages and libraries might be installed.

    This function compiles a list of absolute paths that include:
    - Global site-packages directories.
    - The Python module search paths from `sys.path`.
    - The base directory for user-specific packages.
    - The user-specific site-packages directory.
    - The parent directory of the PyTorch library installation.

    The paths are sorted in descending order of length and are returned with a trailing path separator.
    This list can be used for prefix matching or path validation purposes.

    Returns:
        List[str]: A list of absolute path prefixes, each ending with the platform-specific path separator.
    """

    raw_paths = (
        site.getsitepackages()
        + sys.path
        + [site.getuserbase()]
        + [site.getusersitepackages()]
        + [os.path.dirname(os.path.dirname(torch.__file__))]
    )

    path_prefixes = sorted({os.path.abspath(i) for i in raw_paths}, reverse=True)
    assert all(isinstance(i, str) for i in path_prefixes)
    return [i + os.sep for i in path_prefixes]
