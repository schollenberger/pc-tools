import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(arr)
print(type(arr))

arr = np.array((1, 2, 3, 4, 5))

print(arr)
arr = np.array(42)
print(arr)

arr = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])

print(arr)
print(arr.ndim)

print("Image as ndarray:")
arr = np.zeros([5,5,3])
print(arr)
print("Dimensions:      ",arr.ndim)
print("Total size:      ",arr.size)
print("Size elment 0:   ",arr[0].size)
print("Size elment 0,0: ",arr[0,0].size)
print()
arr_cd = arr[0,0].size
print("Color depth:     ", arr_cd)
arr_xdim = arr.size / arr[0].size
print("X-dim:           ", arr_xdim)
arr_ydim = arr[0].size / arr[0,0].size
print("Y-dim:           ", arr_ydim)
