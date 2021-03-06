# tag::PRIMES_PROC_TOP[]
from time import perf_counter
from typing import Tuple, List, NamedTuple
from multiprocessing import Process, SimpleQueue  # <1>
from multiprocessing import queues  # <2>

from primes import is_prime, NUMBERS

class Result(NamedTuple):  # <3>
    flag: bool
    elapsed: float

JobQueue = queues.SimpleQueue[Tuple[int, Result]]  # <4>

def check(n: int) -> Result:  # <5>
    t0 = perf_counter()
    res = is_prime(n)
    return Result(res, perf_counter() - t0)

def job(n: int, results: JobQueue) -> None:  # <6>
    results.put((n, check(n)))  # <7>
# end::PRIMES_PROC_TOP[]

# tag::PRIMES_PROC_MAIN[]
def main() -> None:
    t0 = perf_counter()
    results: JobQueue = SimpleQueue()  # <1>
    workers: List[Process] = []  # <2>

    for n in NUMBERS:
        worker = Process(target=job, args=(n, results))  # <3>
        worker.start()  # <4>
        workers.append(worker)  # <5>

    for _ in workers:  # <6>
        n, (prime, elapsed) = results.get()  # <7>
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')


    time = perf_counter() - t0
    print('Total time:', f'{time:0.2f}s')

if __name__ == '__main__':
    main()
# end::PRIMES_PROC_MAIN[]
