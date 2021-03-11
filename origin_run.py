import time

def job(t):
    print("正在執行 job", t)
    time.sleep(t)
    print("job", t, " 執行", t, "sec")

def main():
    [job(t) for t in range(1, 3)]

t_start = time.time()
main() # 執行程式
print("="*20)
print("共執行", time.time()-t_start, " sec")