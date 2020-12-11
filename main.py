from commenUtils import get_input_data
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--log", default="info")

options = parser.parse_args()

level = logging.INFO

if options.log.lower() == "debug":
    level = logging.DEBUG

logging.basicConfig(format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                    level=level)

logger = logging.getLogger(__name__)


def make_padded_area(area: list[str]) -> list[str]:
    width: int = len(area[0])
    padded_area: list[str] = ["+"*(width + 2)]
    for line in area:
        padded_area.append("+" + line + "+")
    padded_area.append("+"*(width + 2))
    return padded_area


def pretty_print(area: list[str]) -> str:
    output_str: str = "\n"
    for line in area[:-1]:
        output_str += line
        output_str += "\n"
    output_str += area[-1]
    return output_str


def count_adjacent_seats(area: list[str], x: int, y: int) -> int:
    count: int = area[x-1][y-1:y+2].count('#')
    count += (area[x][y-1] + area[x][y+1]).count('#')
    count += area[x+1][y-1:y+2].count('#')
    return count


def test_direction(area: list[str], x: int, y: int, direction: tuple[int, int]) -> bool:
    current_x: int = x + direction[0]
    current_y: int = y + direction[1]
    while area[current_x][current_y] != "+":
        if area[current_x][current_y] == "#":
            return True
        if area[current_x][current_y] == "L":
            return False
        current_x += direction[0]
        current_y += direction[1]
    return False


def count_part_2_adjacent_seats(area: list[str], x: int, y: int) -> int:
    directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    count: int = 0
    for direction in directions:
        count += int(test_direction(area, x, y, direction))
    return count


def one_round(area: list[str]) -> bool:
    width: int = len(area[0])
    height: int = len(area)
    padded_area = make_padded_area(area)
    changed: bool = False
    for n in range(1, height + 1):
        for m in range(1, width + 1):
            if padded_area[n][m] == ".":
                continue
            if padded_area[n][m] == "L":
                if count_adjacent_seats(padded_area, n, m) == 0:
                    changed = True
                    area[n-1] = area[n-1][:m-1] + "#" + area[n-1][m:]
            if padded_area[n][m] == "#":
                if count_adjacent_seats(padded_area, n, m) >= 4:
                    changed = True
                    area[n-1] = area[n-1][:m-1] + "L" + area[n-1][m:]
    logger.debug(pretty_print(area))
    return changed


def count_occupied_seats(area: list[str]) -> int:
    count: int = area[0].count('#')
    for line in area[1:]:
        count += line.count('#')
    return count


def solution_part_1(file_name: str) -> int:
    area: list[str] = get_input_data(file_name)
    while one_round(area):
        pass
    return count_occupied_seats(area)


def one_round_part_2(area: list[str]) -> bool:
    width: int = len(area[0])
    height: int = len(area)
    padded_area = make_padded_area(area)
    changed: bool = False
    for n in range(1, height + 1):
        for m in range(1, width + 1):
            if padded_area[n][m] == ".":
                continue
            if padded_area[n][m] == "L":
                if count_part_2_adjacent_seats(padded_area, n, m) == 0:
                    changed = True
                    area[n-1] = area[n-1][:m-1] + "#" + area[n-1][m:]
            if padded_area[n][m] == "#":
                if count_part_2_adjacent_seats(padded_area, n, m) >= 5:
                    changed = True
                    area[n-1] = area[n-1][:m-1] + "L" + area[n-1][m:]
    logger.debug(pretty_print(area))
    return changed


def solution_part_2(file_name: str) -> int:
    area: list[str] = get_input_data(file_name)
    logger.debug(pretty_print(area))
    while one_round_part_2(area):
        pass
    return count_occupied_seats(area)


if __name__ == '__main__':
    logger.info(solution_part_1("inputData.txt"))
    logger.info(solution_part_2("inputData.txt"))
