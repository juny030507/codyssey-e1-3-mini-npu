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

def run_json_analysis_mode():
    print("=== data.json 분석 모드 ===")

    data = load_json_data("data.json")
    filters = data["filters"]
    patterns = data["patterns"]

    print("data.json 로드 완료")
    print(f"필터 크기: {len(filters)}개")
    print(f"패턴: {len(patterns)}개")

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

if __name__ == "__main__":
    main()
