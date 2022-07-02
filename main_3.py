def create_matrix(n_, m_):
    matrix = []
    for _ in range(int(n_)):
        k = 0
        next_n = input().split()
        sub_ = []
        for _ in range(int(m_)):
            sub_.append(next_n[k])
            k += 1
        matrix.append(sub_)

    return matrix


def sort_matrix(mat, row_to_sort):
    new_mt_flip = []
    sorted_row = mat[row_to_sort]

    # sort
    li = sorted([[int(val), idx] for idx, val in enumerate(sorted_row)])

    sort_index = []
    sort_lst = []
    for x in li:
        sort_lst.append(x[0])
        sort_index.append(x[1])

    for idx, vl in enumerate(mat):
        if idx == row_to_sort:
            new_mt_flip.append(sort_lst)
            continue
        s_sub = [vl[ll] for ll in sort_index]
        new_mt_flip.append(s_sub)

    return new_mt_flip


if __name__ == '__main__':
    nums = int(input())
    for _ in range(1, nums + 1):
        input()

        # matrix
        n, m = input().split()
        mt = create_matrix(n, m)

        mt_flip = []
        for i in range(int(m)):
            sub = []
            for j in mt:
                sub.append(j[i])
            mt_flip.append(sub)

        # clicks
        clicks_num = int(input())
        clicks = input().split()

        for cl in clicks:
            row = int(cl) - 1
            mt_flip = sort_matrix(mt_flip, row)

        for a in range(int(n)):
            sub = []
            for i_a in mt_flip:
                sub.append(str(i_a[a]))
            print(' '.join(sub))
