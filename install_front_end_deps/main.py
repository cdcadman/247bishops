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
        ),
        (
            "Chess_klt45.svg",
            "0931177d4dae3a607559a81c4a6c9d2c37189b966d4f57368661ac40a1a2ba53642163792e2e158b8df2b3a630844f4bb95ba22d7358e94f581a096fa03dfe42",
        ),
        (
            "Chess_qdt45.svg",
            "b0ead023bf0e88e68515a43a74aa30ccb2ab68803e5fed93bec74a64a17bf8696a6bf2e39c043654fbf7a3f256c9ce7daf10ee5f858e86c48551977a4a6fb540",
        ),
        (
            "Chess_qlt45.svg",
            "09b476098cb6909b0d011b1ac9f4a9962e6573461cc4bd32005d46ed97391bf8e4bbedccf882d504a42d287d26128ab1c20260661b0e4272ce0226d7cf2f2deb",
        ),
        (
            "Chess_rdt45.svg",
            "3ad4d024b3683a62048559158f0849ed953cc8e05b43a6cd305170796291f67a8f529a5c5473a9d23289c89e77da89abe33474279687e3dd15cdfc0c357b0d1f",
        ),
        (
            "Chess_rlt45.svg",
            "960e97e2fdc9e57970935c03fd4ab9fa2b3be1cd99cfd82b6e9d981b6de1bfc7280dc4556c4ba52a8f146d55c06f9ce0846410fc3de9bc4cc123aa5825c86bf8",
        ),
        (
            "Chess_bdt45.svg",
            "db06dd8e2c1a2328bdc2cc5126bc76e7a4d84ac672c4288421ce4da644bfcb90d2af6a0253a31791f40cbc4fad2831977ef00f8c525299bc100ab41de77192f9",
        ),
        (
            "Chess_blt45.svg",
            "20b00edf0bfd5c019a21e3d22437448af01850b95b248998b8050b6b60e8c9994a08b65e7cbae196ac09d594ec859b6dac2e1c089caa38d67c5c8598788e68f1",
        ),
        (
            "Chess_ndt45.svg",
            "deb3026da91d0e8223751dc1021547e9bed20f80f3145533a3f506435ee461f87ab3d1230678dacecdc71b39cae309a5b3e1ffb15fb7303035d54c40d87bca8e",
        ),
        (
            "Chess_nlt45.svg",
            "95ea184a4ad5c3c8c6755025aff3ca2d3b937abc56c46807f47f5e70d44301ac0e5925abc5acae157a4eb65dbcd4288df983b81d3e341e3e54cab0fc204affcf",
        ),
        (
            "Chess_pdt45.svg",
            "3888b32936acbc8352070bbc582e5d9e0cfd2cbc8ca108e64ef9c44bec6fe72622c128cf7c4e2314284b0fcdbedb94d6f23e180aa8bd65aab6671203a6cb0748",
        ),
        (
            "Chess_plt45.svg",
            "484b58fa8f9b58cdc390b6373d2dbd5ed14e40624c1f016cc1f191c71c75e8a5583d57c4d929c7c3ab9a28f85e6ac337d92616f92b5377e224d6f4d913d1b432",
        ),
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
