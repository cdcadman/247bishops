"""This should not require any 3rd party python packages, because it will run in the deployment workflow without any `pip install`."""

import shutil
import warnings
from hashlib import sha3_512
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile


class InstallError(RuntimeError):
    pass


def install_directory() -> Path:
    path = Path(__file__).parent.absolute().parent / "front_end_deps"
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    path.mkdir()
    return path


def main():
    warnings.simplefilter("error")
    install_dir = install_directory()
    with urlopen(
        "https://github.com/jhlywa/chess.js/archive/refs/tags/v0.13.4.zip"
    ) as f:
        file_data = f.read()
    if (
        sha3_512(file_data).hexdigest()
        != "8d8ef2cef1e9d6c96cbfd8cda5e3fd1024bbebb2e4110c1395779221ad31e7d3b51d0f38b254da9eacba7f069c47ffc7d10527c41608c1d78abc32dd04126cfd"
    ):
        raise InstallError("The hash for frontfire does not match.")
    with BytesIO(file_data) as file:
        with ZipFile(file) as chess:
            local_license = Path(__file__).parent.absolute() / "chess.txt"
            with chess.open("chess.js-0.13.4/LICENSE") as zip_license:
                if zip_license.read() != local_license.read_bytes():
                    raise InstallError("The license for chess.js does not match.")
            chess.extract("chess.js-0.13.4/chess.js", install_dir)
