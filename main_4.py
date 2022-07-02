def check_login(login: str):
    len_login = len(login)
    if login.startswith('-') or len_login < 2 or len_login > 24:
        return False
    else:
        return all(a.isalpha() or a.isdigit() or a in ['_', '-'] for a in set(login))


if __name__ == '__main__':
    for _ in range(int(input())):
        logins = set()
        for _ in range(int(input())):
            st = input().lower()
            if check_login(st):
                if st in logins:
                    print('NO')
                else:
                    logins.add(st)
                    print('YES')
            else:
                print('NO')
        print('')
