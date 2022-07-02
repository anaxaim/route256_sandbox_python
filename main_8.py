def create_extended_matrix(rows, cols):
    first_row = []
    for _ in range(cols + 2):
        first_row.append('.')
    ext_matrix = [first_row]
    for i in range(rows):
        sub = ['.']
        next_line = input()
        for j in next_line:
            sub.append(j)
        sub.append('.')
        ext_matrix.append(sub)
    last_row = first_row
    ext_matrix.append(last_row)

    return ext_matrix


def count_by_orthogonal(matrix, i, j):
    count = 0
    if matrix[i - 1][j] == '*':
        count += 1
    if matrix[i + 1][j] == '*':
        count += 1
    if matrix[i][j - 1] == '*':
        count += 1
    if matrix[i][j + 1] == '*':
        count += 1

    return count


def count_by_diagonal(matrix, i, j):
    count = 0
    if matrix[i - 1][j - 1] == '*':
        count += 1
    if matrix[i + 1][j + 1] == '*':
        count += 1
    if matrix[i + 1][j - 1] == '*':
        count += 1
    if matrix[i - 1][j + 1] == '*':
        count += 1

    return count


def get_direction(matrix, i, j):
    c, di, dj = 0, 0, 0
    if matrix[i - 1][j] == '*':
        di = -1
        c = 0
    if matrix[i + 1][j] == '*':
        di = 1
        c = 1
    if matrix[i][j - 1] == '*':
        dj = -1
        c = 2
    if matrix[i][j + 1] == '*':
        dj = 1
        c = 3

    return c, di, dj, di == 0 and dj == 0


def processing(matrix):
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            if matrix[i][j] != '.' and matrix[i][j] != '*':
                return 'NO', []

            if matrix[i][j] == '*':
                o = count_by_orthogonal(matrix, i, j)
                d = count_by_diagonal(matrix, i, j)
                check = (o == 1 and d == 0) or (o == 2 and d == 0) or \
                        (o == 1 and d == 1) or (o == 0 and d == 0) or \
                        (o == 2) and (d == 1)
                if not check:
                    return 'NO', []
                if o == 2 and d == 1:
                    check = matrix[i + 1][j] == matrix[i - 1][j] or matrix[i][j + 1] == matrix[i][j - 1]
                    if not check:
                        return 'NO', []
                if o == 1 and d == 1:
                    if matrix[i + 1][j] == "*":
                        check = matrix[i + 1][j] == matrix[i + 1][j + 1] or matrix[i + 1][j] == matrix[i + 1][j - 1]
                    if matrix[i - 1][j] == "*":
                        check = matrix[i - 1][j] == matrix[i - 1][j + 1] or matrix[i - 1][j] == matrix[i - 1][j - 1]
                    if matrix[i][j + 1] == "*":
                        check = matrix[i][j + 1] == matrix[i - 1][j + 1] or matrix[i][j + 1] == matrix[i + 1][j + 1]
                    if matrix[i][j - 1] == "*":
                        check = matrix[i][j - 1] == matrix[i - 1][j - 1] or matrix[i][j - 1] == matrix[i + 1][j - 1]

                    if not check:
                        return 'NO', []

    size = []
    for i in range(1, len(matrix) - 1):
        for j in range(len(matrix[i]) - 1):
            if matrix[i][j] == '*':
                o = count_by_orthogonal(matrix, i, j)
                if o == 0:
                    size.append(1)
                if o == 1:
                    la = 1
                    rot_count = 0
                    i1, j1 = i, j
                    direction, di, dj, stop = get_direction(matrix, i1, j1)
                    if di != 0 and dj != 0:
                        return 'NO', []
                    matrix[i1][j1] = '.'
                    dir_old = direction
                    while not stop:
                        la += 1
                        i1 += di
                        j1 += dj

                        direction, di, dj, stop = get_direction(matrix, i1, j1)
                        if di != 0 and dj != 0:
                            return 'NO', []

                        matrix[i1][j1] = '.'
                        if direction != dir_old and not stop:
                            rot_count += 1
                            dir_old = direction

                    if rot_count != 1:
                        return 'NO', []

                    if abs(i1 - i) != abs(j1 - j):
                        return 'NO', []

                    size.append(la)

    if not size:
        return 'NO', []

    return 'YES', sorted(size)


if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        n, m = input().split()
        n = int(n)
        m = int(m)

        ext_matrix = create_extended_matrix(n, m)

        ans, ships = processing(ext_matrix)
        print(ans)
        if ships:
            print(' '.join(str(sh) for sh in ships))
