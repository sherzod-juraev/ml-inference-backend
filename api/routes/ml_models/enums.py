from enum import Enum


class ModelType(str, Enum):
    single = 'single'
    ensemble = 'ensemble'


class ModelStatus(str, Enum):
    ready = 'ready'
    failed = 'failed'