from glob import glob
from config import ROOT_DIR


# load fixtures
pytest_plugins = [
    file.replace("/", ".").replace(".py", "") for file in glob("fixtures/**/*.py", recursive=True, root_dir=ROOT_DIR)
]
