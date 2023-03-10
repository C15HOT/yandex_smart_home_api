from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .devices import Purifer, VacuumCleaner, Light, Tvoc

if TYPE_CHECKING:
    from yandex_smart_home_api.api import YandexApi


class DeviceCategories(ABC):
    @property
    def purifer(self):
        return Purifer(self.api_instance)

    @property
    def vacuum_cleaner(self):
        return VacuumCleaner(self.api_instance)

    @property
    def light(self):
        return Light(self.api_instance)

    @property
    def tvoc(self):
        return Tvoc(self.api_instance)


    @property
    @abstractmethod
    def api_instance(self) -> "YandexApi":
        pass
