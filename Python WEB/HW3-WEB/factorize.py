from multiprocessing import Pool, cpu_count
from time import perf_counter

def factorize(*number) -> list:
    all_divisors = []
    for num in number:
        divisors=[]
        i=1
        while i * i <= num:
            if not num % i:
                divisors += [i]
                k=num // i
                if k != i:
                    divisors += [k]
            i+=1
        divisors.sort()
        all_divisors.append(divisors)
    return all_divisors


def factorize_process(num: int) -> list:
    divisors=[]
    i=1
    while i * i <= num:
        if not num % i:
            divisors += [i]
            k=num // i
            if k != i:
                divisors += [k]
        i+=1
    divisors.sort()
    return divisors

def start_factorize_process(*number):
    result = []
    with Pool(processes=cpu_count()) as pool:
        result+=pool.map(factorize_process, (num for num in number))
    return result


if __name__ == '__main__':
    time_point_1 = perf_counter()
    factorize(*range(100000))
    time_point_2 = perf_counter()
    start_factorize_process(*range(100000))
    time_point_3 = perf_counter()
    print('\033[1mResult for 10.000 elements:\033[0m')
    print(f'\033[31mSynchronous implementation:\033[0m {time_point_2 - time_point_1}s')
    print(f'\033[32mMultiprocessing implementation:\033[0m {time_point_3 - time_point_2}s')
    print(f'\033[1mMultiprocessing is faster than synchronous implementation on: {round((time_point_3 - time_point_2) / (time_point_2 - time_point_1) * 100)}%\033[0m')