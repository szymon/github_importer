import importlib
import importlib.util
import os
import sys
from importlib._bootstrap import ModuleSpec

import pip
import pip._internal.cli.main
import requests

CONFIG = {}


class GHRemotePackage(ModuleSpec):
    def __init__(self, name, loader, *, origin=None):
        super().__init__(name=name, loader=loader, origin=origin, is_package=True)


class GithubImporter:
    @classmethod
    def find_spec(cls, fullpath, path, target=None):
        # from github.<username> import <repo>
        # if path is not None we want to create a dummy module
        # and only load the correct repo when path is None
        # fullpath would then be something linke github.<username>.<repo>

        if not fullpath.startswith("github"):
            return None

        if path:
            spec = GHRemotePackage(fullpath, cls, origin="hell")
            spec._top_level = True
        else:
            repo_owner, repo_name = cls._split_path(fullpath)
            spec = GHRemotePackage(fullpath, cls, origin="hell")
            spec._top_level = False
            spec._repo_owner, spec._repo_name = repo_owner, repo_name
            spec._url = cls._get_url(repo_owner, repo_name)
            spec._directory = CONFIG.get("install_directory", "/tmp/tmp.uftSxrhdGN")
            spec._force_upgrade = CONFIG.get("force_upgrade", True)
            spec._verbose = CONFIG.get("verbose", False)

        spec._path = path
        return spec

    @classmethod
    def exec_module(cls, module):
        pass

    @classmethod
    def create_module(cls, spec):
        if spec._top_level:
            return spec

        args = ["install", f"--target={spec._directory}"]
        if not spec._verbose:
            args.append("--quiet")

        if spec._force_upgrade:
            args.append("--upgrade")
        args.append(spec._url)

        module_dir = spec._directory + "/" + spec._repo_name

        if not os.path.isdir(module_dir) or spec._force_upgrade:
            pip._internal.cli.main.main(args)

        if spec._directory not in sys.path:
            sys.path.insert(0, spec._directory)

        # spec = importlib.util.spec_from_file_location(spec._repo_name)
        # module = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(module)

        module = importlib.import_module(spec._repo_name)

        return module

    @classmethod
    def load_module(cls, module):

        return module

    @staticmethod
    def _split_path(name):

        parts = name.split(".")

        if len(parts) > 3:
            raise ImportError(
                f"Cannot import {name}. Can only import as 'from github.<owner> import <repo>'.\n"
                f"Probably used from {'.'.join(parts[:-1])} import {parts[-1]}"
            )

        repo_owner = parts[1]
        repo_name = parts[2]

        return repo_owner, repo_name

    @staticmethod
    def _get_url(repo_owner, repo_name):

        url = f"https://github.com/{repo_owner}/{repo_name}"

        try:
            resp = requests.get(url)

            if resp.status_code == 200:
                return "git+" + url

            else:
                raise ImportError()
        except:
            raise ImportError()


sys.meta_path.append(GithubImporter())
