"""This should not require any 3rd party python packages, because it will run in the deployment workflow without any `pip install`."""

import shutil
import warnings
from functools import cache
from hashlib import sha3_512
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from xml.etree import ElementTree as ET  # nosec B405
from zipfile import ZipFile


class WrongHash(RuntimeError):
    def __init__(self, url: str, expected_hex: str, actual_hex: str):
        super().__init__()
        self.details = {
            "url": url,
            "expected_hex": expected_hex,
            "actual_hex": actual_hex,
        }

    def __str__(self):
        return "\n" + "\n".join(
            [f"\t{key}: {val}" for key, val in self.details.items()]
        )


class WrongLicense(RuntimeError):
    pass


@cache
def install_directory() -> Path:
    path = Path(__file__).parent.absolute().parent / "front_end_deps"
    if path.exists():
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    path.mkdir()
    return path


# TODO: Add chess pieces from https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces
# TODO: Mention images in contributing.md
# TODO: See if the browser can cache them


def download_file(url: str, expected_hex: str):
    with urlopen(url) as f:  # nosec B310
        file_data = f.read()
    actual_hex = sha3_512(file_data).hexdigest()
    if actual_hex != expected_hex:
        raise WrongHash(url, expected_hex, actual_hex)
    return file_data


def parse_commons_api(image: str) -> tuple[str, str]:
    api_url = "https://magnus-toolserver.toolforge.org/commonsapi.php"
    with urlopen(f"{api_url}?image={image}") as f:  # nosec B310
        xml_root = ET.fromstring(f.read().decode())  # nosec B314
    url = xml_root.find("./file/urls/file").text
    lic = xml_root.find("./licenses/license/name").text
    return url, lic


def chess_js():
    file_data = download_file(
        "https://github.com/jhlywa/chess.js/archive/refs/tags/v0.13.4.zip",
        "8d8ef2cef1e9d6c96cbfd8cda5e3fd1024bbebb2e4110c1395779221ad31e7d3b51d0f38b254da9eacba7f069c47ffc7d10527c41608c1d78abc32dd04126cfd",
    )
    with BytesIO(file_data) as file:
        with ZipFile(file) as chess:
            local_license = Path(__file__).parent.absolute() / "chess.txt"
            with chess.open("chess.js-0.13.4/LICENSE") as zip_license:
                if zip_license.read() != local_license.read_bytes():
                    raise WrongLicense("The license for chess.js does not match.")
            chess.extract("chess.js-0.13.4/chess.js", install_directory())


def chess_pieces():
    pieces = [
        (
            "Chess_kdt45.svg",
            "6f701881ae5182ad97036b85495984265f28cf352677d696afbab646b92a7871c148f598ddf5589c293477bb0a22fb002b284ea401b7bdedc2c9776255f67c6a",
        )
    ]
    piece_dir = install_directory() / "pieces"
    piece_dir.mkdir()
    for filename, expected_hex in pieces:
        url, lic = parse_commons_api(filename)
        if lic != "CC-BY-SA-3.0-migrated":
            raise WrongLicense(f"Expected CC-BY-SA-3.0-migrated instead of {lic}")
        file_data = download_file(f"{url}?download", expected_hex)
        (piece_dir / filename).write_bytes(file_data)


def main():
    warnings.simplefilter("error")
    chess_js()
    chess_pieces()
