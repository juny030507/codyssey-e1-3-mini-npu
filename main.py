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

cross_score = calculate_mac(cross_filter, cross_filter)
x_score = calculate_mac(cross_filter, x_filter)

assert cross_score == 5
assert x_score == 1

print(f"Cross 점수: {cross_score}")
print(f"X 점수: {x_score}")
