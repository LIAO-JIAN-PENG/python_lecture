import asyncio
import time

async def foo():
    print('Running in foo')
    await asyncio.sleep(1)
    print('Explicit context switch to foo again')


async def bar():
    print('Explicit context to bar')
    await asyncio.sleep(2)
    print('Implicit context switch back to bar')


async def main():
    tasks = [foo(), bar()]
    await asyncio.gather(*tasks)

t_start = time.time()
asyncio.run(main())
print(time.time()-t_start, "seconds passed.")