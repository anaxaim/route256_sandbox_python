if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        phone_book = {}
        n = int(input())
        for _ in range(n):
            name, phone = input().split()
            book = phone_book.get(name)
            if book:
                if phone in book:
                    phone_book[name].remove(phone)
                phone_book[name].insert(0, phone)
                if len(book) > 5:
                    phone_book[name].pop()
            else:
                phone_book[name] = [phone]
        for key, val in sorted(phone_book.items()):
            s = f'{key}: {len(val)} {" ".join(x for x in val)}'
            print(s)
        print('')
