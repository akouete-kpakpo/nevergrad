import urllib.request
from pathlib import Path
from typing import Optional

from pcse.fileinput import CABOFileReader
from urlpath import URL

SOIL_DATA_URL = URL("https://raw.githubusercontent.com/ajwdewit/pcse_notebooks/master", "data/soil/ec3.soil")
ROOT_DIR = Path(__file__).parent.parent
IRRIGATION_DIR = ROOT_DIR / "nevergrad" / "functions" / "irrigation"


def get_soil_data(soil_data_url: URL = SOIL_DATA_URL, soilfile: Optional[Path] = None) -> dict:
    if soilfile is None:
        soilfile = Path(IRRIGATION_DIR, *soil_data_url.parts[-3:])
    if not soilfile.exists():
        urllib.request.urlretrieve(
            soil_data_url.as_posix(),
            soilfile,
        )
    return CABOFileReader(soilfile)
