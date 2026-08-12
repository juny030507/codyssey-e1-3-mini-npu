import json
import time

cross_filter = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0],
]

x_filter = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
]

def calculate_mac(pattern, filter_matrix):
    score = 0

    for row_index in range(len(pattern)):
        for column_index in range(len(pattern[row_index])):
            score += (
                pattern[row_index][column_index]
                * filter_matrix[row_index][column_index]
            )

    return score

def flatten_matrix(matrix):
    flat_matrix = []

    for row in matrix:
        for value in row:
            flat_matrix.append(value)

    return flat_matrix

def calculate_mac_flat(flat_pattern, flat_filter):
    if len(flat_pattern) != len(flat_filter):
        raise ValueError(
            "패턴과 필터의 길이가 일치해야 합니다."
        )

    score = 0

    for index in range(len(flat_pattern)):
        score += (
            flat_pattern[index]
            * flat_filter[index]
        )

    return score

def validate_pattern_size(size):
    if not isinstance(size, int):
        raise TypeError(
            "패턴 크기는 정수여야 합니다."
        )

    if size <= 0 or size % 2 == 0:
        raise ValueError(
            "패턴 크기는 양의 홀수여야 합니다."
        )

def generate_cross_pattern(size):
    validate_pattern_size(size)

    center_index = size // 2
    pattern = []

    for row_index in range(size):
        row_values = []

        for column_index in range(size):
            is_cross_position = (
                row_index == center_index
                or column_index == center_index
            )

            if is_cross_position:
                row_values.append(1)
            else:
                row_values.append(0)

        pattern.append(row_values)

    return pattern

def generate_x_pattern(size):
    validate_pattern_size(size)

    pattern = []

    for row_index in range(size):
        row_values = []

        for column_index in range(size):
            is_x_position = (
                row_index == column_index
                or row_index + column_index == size - 1
            )

            if is_x_position:
                row_values.append(1)
            else:
                row_values.append(0)

        pattern.append(row_values)

    return pattern

def measure_mac_average(
    pattern,
    filter_matrix,
    repeat_count=1000,
    measurement_count=10,
):
    total_average_milliseconds = 0

    for _ in range(measurement_count):
        start_time = time.perf_counter()

        for _ in range(repeat_count):
            calculate_mac(pattern, filter_matrix)

        end_time = time.perf_counter()

        elapsed_seconds = end_time - start_time
        average_seconds = elapsed_seconds / repeat_count
        average_milliseconds = average_seconds * 1000
        total_average_milliseconds += average_milliseconds

    return total_average_milliseconds / measurement_count

def measure_mac_flat_average(
    flat_pattern,
    flat_filter,
    repeat_count=1000,
    measurement_count=10,
):
    total_average_milliseconds = 0

    for _ in range(measurement_count):
        start_time = time.perf_counter()

        for _ in range(repeat_count):
            calculate_mac_flat(
                flat_pattern,
                flat_filter,
            )

        end_time = time.perf_counter()

        elapsed_seconds = end_time - start_time
        average_seconds = elapsed_seconds / repeat_count
        average_milliseconds = average_seconds * 1000
        total_average_milliseconds += average_milliseconds

    return total_average_milliseconds / measurement_count

def compare_mac_performance(
    size,
    repeat_count=1000,
    measurement_count=10,
):
    pattern = generate_cross_pattern(size)
    filter_matrix = generate_x_pattern(size)

    flat_pattern = flatten_matrix(pattern)
    flat_filter = flatten_matrix(filter_matrix)

    two_dimensional_score = calculate_mac(
        pattern,
        filter_matrix,
    )
    flat_score = calculate_mac_flat(
        flat_pattern,
        flat_filter,
    )

    if two_dimensional_score != flat_score:
        raise ValueError(
            "2차원 MAC과 1차원 MAC의 점수가 다릅니다."
        )

    two_dimensional_time = measure_mac_average(
        pattern,
        filter_matrix,
        repeat_count,
        measurement_count,
    )
    flat_time = measure_mac_flat_average(
        flat_pattern,
        flat_filter,
        repeat_count,
        measurement_count,
    )

    return two_dimensional_time, flat_time

def run_mac_optimization_analysis():
    sizes = [3, 5, 13, 25]
    repeat_count = 1000
    measurement_count = 10

    print()
    print("=== 2차원/1차원 MAC 성능 비교 ===")
    print(f"측정 세트: {measurement_count}회")
    print(f"세트당 반복 횟수: {repeat_count:,}회")
    print("크기    | 2차원(ms) | 1차원(ms) | 빠른 방식")
    print("-" * 48)

    for size in sizes:
        two_dimensional_time, flat_time = (
            compare_mac_performance(
                size,
                repeat_count,
                measurement_count,
            )
        )

        if two_dimensional_time < flat_time:
            faster_method = "2차원"
        elif flat_time < two_dimensional_time:
            faster_method = "1차원"
        else:
            faster_method = "동일"

        size_text = f"{size}x{size}"

        print(
            f"{size_text:<7} | "
            f"{two_dimensional_time:>9.6f} | "
            f"{flat_time:>9.6f} | "
            f"{faster_method}"
        )

def measure_mac_performance(
    size,
    repeat_count=1000,
    measurement_count=10,
):
    test_pattern = generate_cross_pattern(size)
    test_filter = generate_x_pattern(size)

    return measure_mac_average(
        test_pattern,
        test_filter,
        repeat_count,
        measurement_count,
    )

def run_performance_analysis():
    sizes = [3, 5, 13, 25]
    repeat_count = 1000
    measurement_count = 10

    print()
    print("=== 성능 분석 ===")
    print(f"측정 세트: {measurement_count}회")
    print(f"세트당 반복 횟수: {repeat_count:,}회")
    print("크기(NxN) | 평균 시간(ms) | 연산 횟수(N²)")
    print("-" * 41)

    for size in sizes:
        average_milliseconds = measure_mac_performance(
            size,
            repeat_count,
            measurement_count,
        )

        operation_count = size * size

        size_text = f"{size}x{size}"

        print(
            f"{size_text:<9} | "
            f"{average_milliseconds:>13.6f} | "
            f"{operation_count:>13}"
        )

    print("시간 복잡도: O(N²)")
    run_mac_optimization_analysis()

def read_row(size):
    while True:
        row_text = input(f"숫자 {size}개를 공백으로 구분해 입력하세요: ")
        text_values = row_text.split()

        if len(text_values) != size:
            print(
                f"입력 형식 오류: 각 줄에 {size}개의 숫자를 "
                "공백으로 구분해 입력하세요."
            )
            continue
        number_values = []
        try:
            for value in text_values:
                number_values.append(float(value))
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요.")
            continue

        return number_values

def read_matrix(name, size):
    print(f"{name} ({size}줄 입력)")

    matrix = []

    for row_index in range(size):
        print(f"{row_index + 1}행")
        row = read_row(size)
        matrix.append(row)

    return matrix

def read_pattern_size():
    while True:
        size_text = input(
            "패턴 크기 N을 입력하세요(양의 홀수): "
        )

        try:
            size = int(size_text)
        except ValueError:
            print("입력 오류: 정수만 입력하세요.")
            continue

        try:
            validate_pattern_size(size)
        except ValueError as error:
            print(f"입력 오류: {error}")
            continue

        return size

def print_matrix(matrix):
    for row in matrix:
        text_values = []

        for value in row:
            text_values.append(str(value))

        print(" ".join(text_values))

def run_pattern_generator_mode():
    size = read_pattern_size()

    cross_pattern = generate_cross_pattern(size)
    x_pattern = generate_x_pattern(size)

    print()
    print(f"=== 자동 생성 패턴 ({size}x{size}) ===")

    print("[Cross]")
    print_matrix(cross_pattern)

    print()
    print("[X]")
    print_matrix(x_pattern)

def determine_winner(
    score_a,
    score_b,
    label_a="A",
    label_b="B",
    undecided_label="판정 불가",
    epsilon=1e-9,
):
    score_difference = abs(score_a - score_b)

    if score_difference < epsilon:
        return undecided_label

    if score_a > score_b:
        return label_a

    return label_b

def run_user_input_mode():
    size = 3

    print("=== 사용자 입력 모드 (3x3) ===")

    filter_a = read_matrix("필터 A", size)
    print("필터 A 저장 완료")

    filter_b = read_matrix("필터 B", size)
    print("필터 B 저장 완료")

    pattern = read_matrix("패턴", size)

    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    winner = determine_winner(score_a, score_b)

    repeat_count = 1000
    measurement_count = 10

    average_time_a = measure_mac_average(
        pattern,
        filter_a,
        repeat_count,
        measurement_count,
    )
    average_time_b = measure_mac_average(
        pattern,
        filter_b,
        repeat_count,
        measurement_count,
    )

    average_time = (
        average_time_a + average_time_b
    ) / 2

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(
        f"연산 시간({measurement_count}개 세트 × "
        f"{repeat_count:,}회 평균): "
        f"{average_time:.6f} ms"
    )
    print(f"판정: {winner}")

def load_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def normalize_label(label):
    label_map = {
        "+": "Cross",
        "cross": "Cross",
        "x": "X"
    }

    normalized_key = label.strip().lower()

    if normalized_key not in label_map:
        raise ValueError(f"지원하지 않는 라벨: {label}")

    return label_map[normalized_key]

def extract_size_from_pattern_key(pattern_key):
    key_parts = pattern_key.split("_")

    is_invalid = (
        len(key_parts) != 3
        or key_parts[0] != "size"
        or not key_parts[1].isdigit()
        or not key_parts[2].isdigit()
    )

    if is_invalid:
        raise ValueError(f"잘못된 패턴 키 형식: {pattern_key}")

    return int(key_parts[1])

def has_expected_size(matrix, expected_size):
    if not isinstance(matrix, list):
        return False

    if len(matrix) != expected_size:
        return False

    for row in matrix:
        if not isinstance(row, list):
            return False

        if len(row) != expected_size:
            return False

    return True

def run_json_analysis_mode():
    print("=== data.json 분석 모드 ===")

    try:
        data = load_json_data("data.json")
        filters = data["filters"]
        patterns = data["patterns"]

        if not isinstance(filters, dict) or not isinstance(patterns, dict):
            raise TypeError("filters와 patterns는 객체여야 합니다.")

    except FileNotFoundError:
        print("JSON 오류: data.json 파일을 찾을 수 없습니다.")
        return

    except json.JSONDecodeError:
        print("JSON 오류: data.json의 JSON 문법이 잘못되었습니다.")
        return

    except (KeyError, TypeError) as error:
        print(f"JSON 오류: 필수 데이터 구조가 잘못되었습니다. ({error})")
        return

    print("data.json 로드 완료")
    print(f"필터 크기: {len(filters)}개")
    print(f"패턴: {len(patterns)}개")

    total_count = len(patterns)
    pass_count = 0
    fail_count = 0
    failure_cases = []

    for pattern_key, pattern_data in patterns.items():
        try:
            size = extract_size_from_pattern_key(pattern_key)
            expected = normalize_label(pattern_data["expected"])

            filter_size_key = f"size_{size}"
            selected_filters = filters.get(filter_size_key)

            if selected_filters is None:
                fail_count += 1
                failure_cases.append(
                    f"{pattern_key}: 필터를 찾을 수 없음"
                )
                print(f"- {pattern_key}: FAIL - 필터를 찾을 수 없음")
                continue

            if not isinstance(selected_filters, dict):
                raise TypeError(
                    f"{filter_size_key} 필터는 객체여야 합니다."
                )

            pattern = pattern_data["input"]
            normalized_filters = {}

            for filter_label, filter_matrix in selected_filters.items():
                standard_label = normalize_label(filter_label)
                normalized_filters[standard_label] = filter_matrix

            cross_filter_matrix = normalized_filters.get("Cross")
            x_filter_matrix = normalized_filters.get("X")

            matrices_are_valid = (
                has_expected_size(pattern, size)
                and has_expected_size(cross_filter_matrix, size)
                and has_expected_size(x_filter_matrix, size)
            )

            if not matrices_are_valid:
                fail_count += 1
                failure_cases.append(
                    f"{pattern_key}: 필터 또는 패턴 크기 불일치"
                )
                print(f"- {pattern_key}: FAIL - 필터 또는 패턴 크기 불일치")
                continue

            cross_score = calculate_mac(pattern, cross_filter_matrix)
            x_score = calculate_mac(pattern, x_filter_matrix)

            prediction = determine_winner(
                cross_score,
                x_score,
                label_a="Cross",
                label_b="X",
                undecided_label="UNDECIDED",
            )

            if prediction == expected:
                result = "PASS"
                pass_count += 1
            else:
                result = "FAIL"
                fail_count += 1
                failure_cases.append(
                    f"{pattern_key}: expected={expected}, actual={prediction}"
                )

            print(f"--- {pattern_key} ---")
            print(f"Cross 점수: {cross_score}")
            print(f"X 점수: {x_score}")
            print(f"판정: {prediction} | expected: {expected} | {result}")

        except (KeyError, TypeError, ValueError) as error:
            fail_count += 1
            failure_cases.append(
                f"{pattern_key}: 데이터 형식 오류 ({error})"
            )
            print(
                f"- {pattern_key}: FAIL - 데이터 형식 오류 ({error})"
            )

    run_performance_analysis()

    print()
    print("=== 결과 요약 ===")
    print(f"총 패턴: {total_count}")
    print(f"PASS: {pass_count}")
    print(f"FAIL: {fail_count}")

    if failure_cases:
        print()
        print("[실패 사례]")

        for failure_case in failure_cases:
            print(f"- {failure_case}")

def main():
    while True:
        print("=== Mini NPU Simulator ===")
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("3. 패턴 자동 생성")
        print("0. 종료")

        choice = input("선택: ")

        if choice == "1":
            run_user_input_mode()
        elif choice == "2":
            run_json_analysis_mode()
        elif choice == "3":
            run_pattern_generator_mode()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("입력 오류: 0, 1, 2, 3 중 하나를 선택하세요.")

        print()

assert calculate_mac(cross_filter, cross_filter) == 5
assert calculate_mac(cross_filter, x_filter) == 1
assert determine_winner(5.0, 1.0) == "A"
assert determine_winner(1.0, 5.0) == "B"
assert determine_winner(0.9, 0.8999999999999999) == "판정 불가"
assert normalize_label("+") == "Cross"
assert normalize_label("cross") == "Cross"
assert normalize_label("x") == "X"
assert normalize_label(" X ") == "X"
assert extract_size_from_pattern_key("size_5_1") == 5
assert extract_size_from_pattern_key("size_13_2") == 13
assert extract_size_from_pattern_key("size_25_1") == 25
assert has_expected_size(
    [[0, 1], [1, 0]],
    2,
)
assert not has_expected_size(
    [[0, 1], [1]],
    2,
)
assert determine_winner(
    5.0,
    1.0,
    label_a="Cross",
    label_b="X",
    undecided_label="UNDECIDED",
) == "Cross"
assert determine_winner(
    0.9,
    0.8999999999999999,
    label_a="Cross",
    label_b="X",
    undecided_label="UNDECIDED",
) == "UNDECIDED"
assert generate_cross_pattern(3) == cross_filter
assert generate_x_pattern(3) == x_filter
assert flatten_matrix(cross_filter) == [
    0, 1, 0,
    1, 1, 1,
    0, 1, 0,
]
flat_cross = flatten_matrix(cross_filter)
flat_x = flatten_matrix(x_filter)

assert calculate_mac_flat(flat_cross, flat_cross) == 5
assert calculate_mac_flat(flat_cross, flat_x) == 1
assert (
    calculate_mac(cross_filter, x_filter)
    == calculate_mac_flat(flat_cross, flat_x)
)

if __name__ == "__main__":
    main()
