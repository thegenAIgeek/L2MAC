def minSubArraySum(nums):
	"""
	Given an array of integers nums, find the minimum sum of any non-empty sub-array
	of nums.
	Example
	minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
	minSubArraySum([-1, -2, -3]) == -6
	"""
	min_sum = nums[0]
	running_sum = nums[0]
	for num in nums[1:]:
		if running_sum > 0:
			running_sum = num
		else:
			running_sum += num
		min_sum = min(min_sum, running_sum)
	return min_sum