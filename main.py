import json

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

def determine_winner(score_a, score_b, epsilon=1e-9):
    score_difference = abs(score_a - score_b)

    if score_difference < epsilon:
        return "판정 불가"

    if score_a > score_b:
        return "A"

    return "B"

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

    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
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

    data = load_json_data("data.json")
    filters = data["filters"]
    patterns = data["patterns"]

    print("data.json 로드 완료")
    print(f"필터 크기: {len(filters)}개")
    print(f"패턴: {len(patterns)}개")

    for pattern_key, pattern_data in patterns.items():
        size = extract_size_from_pattern_key(pattern_key)
        expected = normalize_label(pattern_data["expected"])

        filter_size_key = f"size_{size}"
        selected_filters = filters.get(filter_size_key)

        if selected_filters is None:
            print(f"- {pattern_key}: FAIL - 필터를 찾을 수 없음")
            continue

        pattern = pattern_data["input"]
        cross_filter_matrix = selected_filters.get("cross")
        x_filter_matrix = selected_filters.get("x")

        matrices_are_valid = (
            has_expected_size(pattern, size)
            and has_expected_size(cross_filter_matrix, size)
            and has_expected_size(x_filter_matrix, size)
        )

        if not matrices_are_valid:
            print(f"- {pattern_key}: FAIL - 필터 또는 패턴 크기 불일치")
            continue

        print(
            f"- {pattern_key}: {size}x{size}, "
            f"expected={expected}, size-check=PASS"
        )

def main():
    while True:
        print("=== Mini NPU Simulator ===")
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")

        choice = input("선택: ")

        if choice == "1":
            run_user_input_mode()
        elif choice == "2":
            run_json_analysis_mode()
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("입력 오류: 0, 1, 2 중 하나를 선택하세요.")

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

if __name__ == "__main__":
    main()
