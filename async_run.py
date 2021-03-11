import asyncio
import time

async def job(t):
  print("正在執行 job", t)
  await asyncio.sleep(t)
  print("job", t, " 執行", t, "sec")

async def main():
  tasks = [job(t) for t in range(1, 3)]
  await asyncio.wait(tasks)

t_start = time.time()
asyncio.run(main())
print("="*20)
print("共執行", time.time()-t_start, " sec")