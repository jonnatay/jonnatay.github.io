"""
Run with:
manim -pql  --resolution 1920,1080 manimTest.py -o BinarySearch -- --mainScene examples/BinarySearch.py
"""
arr = ManimList([1, 3, 3, 6, 7, 19, 32])

high = len(arr)-1
low = 0
target = 2
ans = -1
while (low <= high):
    manimScene.onScreenPrint(f"low:{low}, high:{high}, mid:{mid}, target:{target}")
    mid = (high + low)//2
    if arr[mid] == target:
        ans = mid
        break
    elif arr[mid] > target:
        high = mid-1
    else:
        low = mid+1
manimScene.onScreenPrint(f"low:{low}, high:{high}, mid:{mid}, target:{target}, answer:{ans}")
print(ans)
