from dataclasses import dataclass



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


@dataclass
class Mode(BaseCapability):
    "На данном этапе режимы задаются вручную"
    value: str
    instance: str = 'work_speed'
    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}


    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}

@dataclass
class Toggle(BaseCapability):
    "На данном этапе режимы задаются вручную"
    value: bool
    instance: str = 'pause'
    @property
    def state(self):
        return {'instance': self.instance,
                'value': self.value}


    def __call__(self, *args, **kwargs):
        return {'type': self._type,
                'state': self.state}
