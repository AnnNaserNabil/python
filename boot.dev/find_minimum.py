''' Find Minimum
As mentioned, an "algorithm" is just a set of instructions that can be carried out to solve a problem.

It's not anymore magical than that.

Assignment
In this course, we'll be building pieces of a pretend social network: LockedIn. LockedIn is a place for professionals to virtue signal about how all the for-profit work they do is actually an altruistic endeavor. Think Facebook meets a job fair. It includes tools for influencers to track their growth.

We need to show our users the accounts they follow with the lowest follower counts. This will help them know who they follow that isn't popular enough to be worth following anymore.

Implement the "find minimum" algorithm in Python by completing the find_minimum() function. It accepts a list of integers nums and returns the smallest number in the list.

Set minimum to positive infinity: float("inf").
If the list is empty, return None.
For each number in the list nums, compare it to minimum. If the number is smaller than minimum, set minimum to that number.
minimum is now set to the smallest number in the list. Return it.
'''


def find_minimum(nums):
    # Return None if the list is empty
    if not nums:
        return None

    # Start with positive infinity
    minimum = float("inf")

    # Iterate through each number in the list
    for num in nums:
        if num < minimum:
            minimum = num

    return minimum
