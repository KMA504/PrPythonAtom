def cache_decorator(func):
    cache = {}
    def cache_storage(arg):
        if arg in cache:
            return cache[arg]
        else:
            cache[arg] = func(arg)
            return cache[arg]
    return cache_storage

@cache_decorator
def fib(n):
    if n==0:
        return 0
    if n in [1, 2]:
        return 1
    return fib(n-2)+fib(n-1)