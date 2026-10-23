import json

import typer.testing

from src.streamstats.__main__ import app

runner = typer.testing.CliRunner()

def test_cli_csv(tmp_path):
    input_path = tmp_path / "events.csv"
    output_path = tmp_path / "report.json"

    input_path.write_text(
        "timestamp,level,source,message\n"
        "2024-06-01T12:00:00+00:00,INFO,api,Started\n"
        "2024-06-01T11:30:00+00:00,DEBUG,worker,Preparing job\n"
        "2024-06-01T15:00:00+03:00,WARNING,api,\"Slow response, retrying\"\n"
        "2024-06-01T12:30:00Z,ERROR,db,Connection lost\n"
        "2024-06-01T11:45:00+00:00,CRITICAL,db,Disk full\n"
        "2024-06-01T12:15:00+00:00,ERROR,api,Request failed\n"
        "2024-06-01T12:20:00+00:00,CRITICAL,worker,Сбой задачи\n",
        encoding="utf-8"
    )

    result = runner.invoke(app, ["analyze", str(input_path), "--format",
                        "csv", "--output", str(output_path)])

    assert result.exit_code == 0
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert len(data) == 1
    assert data[0]["event_count"] == 7
    assert data[0]["levels"] == {"DEBUG": 1, "INFO": 1, "WARNING": 1, "ERROR": 2, "CRITICAL": 2}
    assert data[0]["sources"] == {"api": 3, "worker": 2, "db": 2}
    assert data[0]["error_sources"] == {"db": 1, "api": 1}
    assert data[0]["critical_sources"] == {"db": 1, "worker": 1}
    assert data[0]["first_timestamp"] == "2024-06-01T11:30:00+00:00"
    assert data[0]["last_timestamp"] == "2024-06-01T12:30:00+00:00"


def test_cli_json(tmp_path):
    input_path = tmp_path / "events.jsonl"
    output_path = tmp_path / "report.json"

    input_path.write_text(
        "{\"timestamp\":\"2024-06-01T10:00:00+00:00\",\"level\":\"INFO\",\"source\":\"api\",\"message\":\"Accepted\"}\n"
        "{\"timestamp\":\"2024-06-01T10:05:00\",\"level\":\"INFO\",\"source\":\"api\",\"message\":\"No timezone\"}\n"
        "{\"timestamp\":\"not-a-timestamp\",\"level\":\"INFO\",\"source\":\"api\",\"message\":\"Bad timestamp\"}\n"
        "{\"timestamp\":\"2024-06-01T10:10:00+00:00\",\"level\":\"TRACE\",\"source\":\"api\",\"message\":\"Bad level\"}\n"
        "{\"timestamp\":\"2024-06-01T10:15:00+00:00\",\"level\":\"ERROR\",\"source\":\"\",\"message\":\"Empty source\"}\n"
        "{\"timestamp\":\"2024-06-01T10:20:00+00:00\",\"level\":\"ERROR\",\"source\":\"db\",\"message\":\"Recovered\"}\n",
        encoding="utf-8"
    )

    result = runner.invoke(app, ["analyze", str(input_path), "--format",
                        "jsonl", "--output", str(output_path), "--skip-invalid"])

    assert result.exit_code == 0
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert len(data) == 1
    assert data[0]["event_count"] == 2
    assert data[0]["skipped_count"] == 4
    assert data[0]["levels"] == {"INFO": 1, "ERROR": 1}
    assert data[0]["sources"] == {"api": 1, "db": 1}
    assert data[0]["error_sources"] == {"db": 1}
    assert data[0]["first_timestamp"] == "2024-06-01T10:00:00+00:00"
    assert data[0]["last_timestamp"] == "2024-06-01T10:20:00+00:00"
