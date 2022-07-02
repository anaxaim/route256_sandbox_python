def iterative_topological_sort(graph, start, compiles):
    seen = set()
    stack = []
    order = []
    q = [start]
    while q:
        v = q.pop()
        if v not in seen:
            seen.add(v)
            q.extend(graph[v])

            while stack and v not in graph[stack[-1]]:
                order.append(stack.pop())
            if v not in compiles:
                stack.append(v)

    dps = stack + order[::-1]
    compiles.update(dps)

    return dps[::-1], compiles


if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        input()

        n = int(input())
        ms = {}
        for _ in range(n):
            base_module, deps = input().split(':')
            if deps:
                ms[base_module] = deps.split()
            else:
                ms[base_module] = []

        compile_modules = set()
        q = int(input())
        for _ in range(q):
            m = input()
            dd, compile_modules = iterative_topological_sort(ms, m, compile_modules)
            for d in dd:
                ms[d] = []
            print(len(dd), *dd)
