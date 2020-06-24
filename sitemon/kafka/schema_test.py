from .schema import SiteReport, serialize_report, read_report

def test_serialize_report():
    report = SiteReport(
        url='abc',
        response_time=12,
        response_code=400,
        pattern='test',
        pattern_match=False,
        error_text='fail',
    )

    assert read_report(serialize_report(report)) == report