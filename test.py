import time

timeout_start = time.time()
interval = 5

while time.time() < timeout_start + interval:
    test = 0
    if test ==5:
        break
    test = test - 1

print("Hooray")