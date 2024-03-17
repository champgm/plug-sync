from pathlib import Path
from pydantic import BaseModel
from typing import List
import yaml


class PlugSet(BaseModel):
    primary_ip: str
    mirror_ips: List[str]


class Config(BaseModel):
    plug_sets: List[PlugSet]
    check_interval: int


def get_config() -> Config:
    current_file_directory = Path(__file__).parent
    config_path = current_file_directory / "../configuration.yaml"
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        return Config(**data)
