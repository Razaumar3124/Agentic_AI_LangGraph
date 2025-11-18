# students = [
#     ("Alice", "Math", 85),
#     ("Alice", "Science", 92),
#     ("Bob", "Math", 78),
#     ("Bob", "Science", 80),
#     ("Charlie", "Math", 90),
#     ("Charlie", "Science", 85)
# ]

# d = {}

# for i in students:
#     name = i[0]
#     sub = i[1]
#     marks = i[2]

#     if name not in d:
#         d[name] = {}
    
#     d[name][sub] = marks

        
# print(d)

# ---------------------------------------------------------------------------------

# arr=[
#     {"fruit":"mango","quantity":10},
#     {"fruit":"apple","quantity":2},
#     {"fruit":"mango","quantity":10},
#     {"fruit":"mango","quantity":10},
#     {"fruit":"banana","quantity":10},
#     ]
# OUTPUT:
# [
#   { fruit: 'mango', quantity: 30 },
#   { fruit: 'apple', quantity: 2 },
#   { fruit: 'banana', quantity: 10 }
# ]

# Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
# You may assume that each input would have exactly one solution, and you may not use the same element twice.
# You can return the answer in any order.
# Input: nums = [2,7,11,15], target = 9 Output: [0,1]Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

nums = [2,7,11,15]
def two_sum(nums, target):
    num_dict = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_dict:
            return [num_dict[complement], i]
        num_dict[num] = i
    return None

print(two_sum(nums, 18))
