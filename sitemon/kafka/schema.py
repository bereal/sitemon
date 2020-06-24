import dataclasses
import io
import fastavro

from typing import Optional

@dataclasses.dataclass
class SiteReport:
    url: str
    response_time: int = 0
    response_code: Optional[int] = None

    pattern: Optional[str] = None
    pattern_match: Optional[bool] = None

    error_text: Optional[str] = None


schema = fastavro.parse_schema({
    'namespace': 'sitemon',
    'type': 'record',
    'name': 'SiteReport',
    'fields': [
        {'name': 'url', 'type': 'string'},
        {'name': 'response_time', 'type': 'int'},
        {'name': 'response_code', 'type': ['int', 'null']},
        {'name': 'pattern', 'type': ['string', 'null']},
        {'name': 'pattern_match', 'type': ['boolean', 'null']},
        {'name': 'error_text', 'type': ['string', 'null']},
    ]
})


def serialize_report(report: SiteReport) -> bytes:
    buf = io.BytesIO()
    fastavro.schemaless_writer(buf, schema, dataclasses.asdict(report))
    return buf.getvalue()


def read_report(b: bytes) -> SiteReport:
    buf = io.BytesIO(b)
    d = fastavro.schemaless_reader(buf, schema)
    return SiteReport(**d)
