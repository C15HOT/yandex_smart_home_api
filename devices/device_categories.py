from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .devices import Purifer, VacuumCleaner

if TYPE_CHECKING:
    from api import YandexApi


class DeviceCategories(ABC):
    @property
    def purifer(self):
        return Purifer(self.api_instance)

    @property
    def vacuum_cleaner(self):
        return VacuumCleaner(self.api_instance)

    @property
    @abstractmethod
    def api_instance(self) -> "YandexApi":
        pass
