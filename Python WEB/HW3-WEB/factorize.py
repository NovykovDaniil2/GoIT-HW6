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


def factorize_process(*nums) -> list:
    result = {}
    for num in nums:
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
        result[num] = divisors
    return result


if __name__ == '__main__':
    
    time_point_1 = perf_counter()
    result_sync = factorize(*range(100000))
    time_point_2 = perf_counter()
    
    with Pool(processes=cpu_count()) as pool:
        result_async = pool.map(factorize_process, range(100000))
    time_point_3 = perf_counter()
    
    time_result_sync = time_point_2 - time_point_1
    time_result_async = time_point_3 - time_point_2

    
    print('\033[1mResult for 100.000 elements:\033[0m')
    print(f'\033[31mSynchronous implementation:\033[0m {time_result_sync}s')
    print(f'\033[32mMultiprocessing implementation:\033[0m {time_result_async}s')
    print(f'\033[1mMultiprocessing is faster than synchronous implementation on: {100 - round((time_result_async * 100) / time_result_sync)}%\033[0m')
