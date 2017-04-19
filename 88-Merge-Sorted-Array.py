class Solution(object):
    def merge(self, nums1, m, nums2, n):
        nums1 = nums1 + [0]*n
        while m > 0 and n > 0:
            if nums1[m-1] >= nums2[n-1]:
                nums1[m+n-1] = nums1[m-1]
                m -= 1
            else:
                nums1[m+n-1] = nums2[n-1]
                n -= 1
        print(nums1)
        
        if n > 0:
            nums1[:n] = nums2[:n]