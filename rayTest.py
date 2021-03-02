import threading, time

def worker():
    """thread worker function"""
    print('Worker')
    return

threads = []
for i in range(5):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()
    print('Thread')

time.sleep(0.1)
print(threads[0].is_alive())