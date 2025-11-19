import os
import pathlib

from dynaconf import Dynaconf

ROOT_DIR = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

settings = Dynaconf(
    load_dotenv=True,
    envvar_prefix=False,
    environments=True,
    env="default",  # override via ENV_FOR_DYNACONF env variable
    settings_files=["settings.yaml"],
)
