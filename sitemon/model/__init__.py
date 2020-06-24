import dataclasses
from functools import partial
from typing import Optional


@dataclasses.dataclass
class SiteReport:
    url: str
    response_time: int
    error: Optional[str] = None
    pattern: Optional[str] = None
    pattern_match: Optional[bool] = None


def skip_none_dict_factory(values):
    return {k : v for k, v in values if v is not None}


asdict = partial(dataclasses.asdict, dict_factory=skip_none_dict_factory)
