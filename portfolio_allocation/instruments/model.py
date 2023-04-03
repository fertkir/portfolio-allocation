from dataclasses import dataclass, field


@dataclass
class InstrumentData:
    instrument: str
    countries: dict[str, float] = field(default_factory=dict)
    industries: dict[str, float] = field(default_factory=dict)
    fee: float = 0
    currencies: dict[str, float] = field(default_factory=dict)
    classes: dict[str, float] = field(default_factory=dict)


class InstrumentDataSource:
    def get(self, instruments: list[str]) -> dict[str, InstrumentData]:
        pass
