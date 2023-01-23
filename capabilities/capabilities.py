from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any


@dataclass
class BaseCapability:
    type: str

    @property
    def _type(self):
        return f'devices.capabilities.{self.type}'


@dataclass
class OnOff(BaseCapability):
    value: bool
    instance: str = 'on'

    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}

    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}


class ModeFunctions(Enum):
    cleanup_mode = 'cleanup_mode'
    coffee_mode = 'coffee_mode'
    dishwashing = 'dishwashing'
    fan_speed = 'fan_speed'
    heat = 'heat'
    input_source = 'input_source'
    program = 'program'
    swing = 'swing'
    tea_mode = 'tea_mode'
    thermostat = 'thermostat'
    work_speed = 'work_speed'


@dataclass
class Mode(BaseCapability):
    value: str
    instance: ModeFunctions

    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}

    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}


class ToggleFunctions(Enum):
    backlight = 'backlight'
    controls_locked = 'controls_locked'
    ionization = 'ionization'
    keep_warm = 'keep_warm'
    mute = 'mute'
    oscillation = 'oscillation'
    pause = 'pause'


@dataclass
class Toggle(BaseCapability):
    value: bool
    instance: ToggleFunctions

    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}

    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}


class RangeFunctions(Enum):
    brightness = 'brightness'
    channel = 'channel'
    humidity = 'humidity'
    open = 'open'
    temperature = 'temperature'
    volume = 'volume'


@dataclass
class Range(BaseCapability):
    value: Any
    instance: RangeFunctions

    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}

    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}


class ColorFunctions(Enum):
    hsv = 'hsv'
    rgb = 'rgb'
    temperature_k = 'temperature_k'
    scene = 'scene'


@dataclass
class ColorSetting(BaseCapability):
    value: Any
    instance: ColorFunctions

    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}

    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}
