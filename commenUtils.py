import logging

logger = logging.getLogger(__name__)


def get_input_data(input_file_name: str) -> list[str]:
    f = open(input_file_name, "r")
    lines: list[str] = []
    for line in f:
        lines.append(line.strip())
    f.close()
    return lines
