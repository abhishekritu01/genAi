# 📘 LeetCode Arrays – Revision Notes

## 🗺️ Legend
| Badge | Meaning |
|-------|---------|
| 🔴 | Confused on pattern — need to re-learn |
| 🟡 | Understand pattern — coding needs polish |
| 🟢 | Fully confident — safe zone |

---

## 📊 Progress Tracker

| # | Problem | Pattern | Status |
|---|---------|---------|--------|
| 1 | [Two Sum](#1️⃣-two-sum) | Hash Map – Complement Lookup | ✅ |
| 2 | [Best Time to Buy and Sell Stock](#2️⃣-best-time-to-buy-and-sell-stock) | Sliding Window / Greedy | ✅ |
| 3 | [Contains Duplicate](#3️⃣-contains-duplicate) | Hash Set | ✅ |
| 4 | [Product of Array Except Self](#4️⃣-product-of-array-except-self) | Prefix + Suffix Product | ✅ |
| 5 | [Maximum Subarray](#5️⃣-maximum-subarray) | Kadane's Algorithm | ✅ |
| 6 | [Subarray Sum Equals K](#6️⃣-subarray-sum-equals-k) | Prefix Sum + Hash Map | ✅ |
| 7 | [Longest Consecutive Sequence](#7️⃣-longest-consecutive-sequence) | Hash Set + Expansion | ✅ |
| 8 | [Majority Element](#8️⃣-majority-element) | Boyer-Moore Voting | ✅ |
| 9 | [Move Zeroes](#9️⃣-move-zeroes) | Two Pointers | ✅ |
| 10 | [Find All Duplicates](#🔟-find-all-duplicates-in-an-array) | Index Mapping | ✅ |
| 11 | [Group Anagrams](#1️⃣1️⃣-group-anagrams) | Hash Map – Frequency Key | ✅ |
| 12 | [Top K Frequent Elements](#1️⃣2️⃣-top-k-frequent-elements) | Bucket Sort | ✅ |
| 13 | [First Missing Positive](#1️⃣3️⃣-first-missing-positive) | Cyclic Sort / Index Placement | ✅ |

---

## 1️⃣ Two Sum
🔗 [LeetCode #1](https://leetcode.com/problems/two-sum/) &nbsp;|&nbsp; 🟢 Pattern: **Hash Map – Complement Lookup**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int target` |
| **Output** | `int[]` — indices `[i, j]` such that `nums[i] + nums[j] == target` |
| **Constraint** | Exactly one valid answer exists |

### 💡 Examples
```
Input:  nums = [2, 7, 11, 15],  target = 9
Output: [0, 1]   ← nums[0] + nums[1] = 2 + 7 = 9 ✅

Input:  nums = [3, 2, 4],  target = 6
Output: [1, 2]
```

### 🔑 Key Points to Remember
- For every element, the **complement = target - nums[i]**
- Store `{ value → index }` in HashMap as you iterate
- Check for complement **before** inserting current number (avoids using same index twice)
- Single pass — no need to pre-fill the map

### ✍️ Solution
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                return new int[]{map.get(complement), i};
            }
            map.put(nums[i], i);
        }
        return new int[]{};
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(n) |

---

## 2️⃣ Best Time to Buy and Sell Stock
🔗 [LeetCode #121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) &nbsp;|&nbsp; 🟢 Pattern: **Greedy – Track Min So Far**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] prices` — price on each day |
| **Output** | `int` — maximum profit possible |
| **Constraint** | Buy before sell; return 0 if no profit |

### 💡 Examples
```
Input:  prices = [7, 1, 5, 3, 6, 4]
Output: 5   ← Buy at 1, Sell at 6

Input:  prices = [7, 6, 4, 3, 1]
Output: 0   ← Prices only fall, no profit possible
```

### 🔑 Key Points to Remember
- Track `minPrice` seen so far (best day to buy)
- At each day, `profit = prices[i] - minPrice`
- Update `maxProfit` if current profit is better
- **Never** look backwards for the sell price

### ✍️ Solution
```java
class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = prices[0];
        int maxProfit = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] < minPrice) {
                minPrice = prices[i];
            }
            maxProfit = Math.max(maxProfit, prices[i] - minPrice);
        }
        return maxProfit;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 3️⃣ Contains Duplicate
🔗 [LeetCode #217](https://leetcode.com/problems/contains-duplicate/) &nbsp;|&nbsp; 🟢 Pattern: **Hash Set – Duplicate Detection**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` |
| **Output** | `boolean` — `true` if any value appears at least twice |

### 💡 Examples
```
Input:  nums = [1, 2, 3, 1]
Output: true   ← 1 appears at index 0 and 3

Input:  nums = [1, 2, 3, 4]
Output: false
```

### 🔑 Key Points to Remember
- `Set.add()` returns `false` if element already exists — use this directly
- No need for a map; only existence matters, not count
- Early return as soon as duplicate is found

### ✍️ Solution
```java
class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            if (!seen.add(num)) return true;
        }
        return false;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(n) |

---

## 4️⃣ Product of Array Except Self
🔗 [LeetCode #238](https://leetcode.com/problems/product-of-array-except-self/) &nbsp;|&nbsp; 🟢 Pattern: **Prefix + Suffix Product**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` |
| **Output** | `int[]` — `result[i]` = product of all elements **except** `nums[i]` |
| **Constraint** | Must run in O(n); no division allowed |

### 💡 Examples
```
Input:  nums = [1, 2, 3, 4]
Output: [24, 12, 8, 6]
  ← result[0] = 2×3×4 = 24
  ← result[1] = 1×3×4 = 12

Input:  nums = [-1, 1, 0, -3, 3]
Output: [0, 0, 9, 0, 0]
```

### 🔑 Key Points to Remember
- **Prefix pass** (left → right): `prefix[i]` = product of all elements to the left of `i`
- **Suffix pass** (right → left): multiply by product of all elements to the right
- Can do it **in-place** in the result array — no extra array needed
- Initialize prefix/suffix multiplier as `1`

### ✍️ Solution (Optimal — O(n) time, O(1) extra space)
```java


 public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4};
        int [] result = new int[arr.length];

        for(int i=0; i< arr.length ; i++){
            int product =1;

            for(int j=0; j<arr.length ;j++){
                if(i != j){
                    product = product * arr[j];
                }
            }
            
            result[i] = product;
        }
        System.out.println(Arrays.toString(result));
    }


--------------------------------------------------------


class Solution {
    public int[] productExceptSelf(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];

        // Left pass: result[i] = product of all elements to the left
        result[0] = 1;
        for (int i = 1; i < n; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }

        // Right pass: multiply by product of all elements to the right
        int suffix = 1;
        for (int i = n - 1; i >= 0; i--) {
            result[i] *= suffix;
            suffix *= nums[i];
        }

        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) extra (output array not counted) |

---

## 5️⃣ Maximum Subarray
🔗 [LeetCode #53](https://leetcode.com/problems/maximum-subarray/) &nbsp;|&nbsp; 🟢 Pattern: **Kadane's Algorithm (DP)**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (can contain negatives) |
| **Output** | `int` — largest sum of a contiguous subarray |

### 💡 Examples
```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6   ← subarray [4, -1, 2, 1]

Input:  nums = [5, 4, -1, 7, 8]
Output: 23  ← entire array

Input:  nums = [1]
Output: 1
```

### 🔑 Key Points to Remember
- `currentSum += nums[i]` — extend the current subarray
- If `currentSum < 0` → **reset to 0** (starting fresh is better)
- Track `maxSum` at each step
- ⚠️ Edge case: if all numbers are negative, initialize `maxSum = nums[0]` and `currentSum = 0`

### ✍️ Solution
```java
class Solution {
    public int maxSubArray(int[] nums) {
        int maxSum = nums[0];
        int current = 0;
        for (int num : nums) {
            current += num;
            maxSum = Math.max(maxSum, current);
            if (current < 0) current = 0;
        }
        return maxSum;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 6️⃣ Subarray Sum Equals K
🔗 [LeetCode #560](https://leetcode.com/problems/subarray-sum-equals-k/) &nbsp;|&nbsp; 🟢 Pattern: **Prefix Sum + Hash Map**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `int` — count of contiguous subarrays that sum to `k` |

### 💡 Examples
```
Input:  nums = [1, 1, 1],  k = 2
Output: 2

Input:  nums = [1, 2, 3],  k = 3
Output: 2   ← [1,2] and [3]
```

### 🔑 Key Points to Remember
- A subarray `[j+1...i]` sums to `k` when `prefixSum[i] - prefixSum[j] == k`
  → i.e., `prefixSum[j] == prefixSum[i] - k`
- Store **frequency of prefix sums** seen so far in a map
- Initialize map with `{0: 1}` to handle subarrays starting from index 0
- Works with **negative numbers** (unlike sliding window)

### ✍️ Solution (Optimal)
```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> prefixCount = new HashMap<>();
        prefixCount.put(0, 1);  // empty subarray base case
        int count = 0, sum = 0;
        for (int num : nums) {
            sum += num;
            count += prefixCount.getOrDefault(sum - k, 0);
            prefixCount.put(sum, prefixCount.getOrDefault(sum, 0) + 1);
        }
        return count;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(n) |

---

## 7️⃣ Longest Consecutive Sequence
🔗 [LeetCode #128](https://leetcode.com/problems/longest-consecutive-sequence/) &nbsp;|&nbsp; 🟢 Pattern: **Hash Set + Sequence Expansion**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (unsorted, may have duplicates) |
| **Output** | `int` — length of the longest consecutive sequence |
| **Constraint** | Must run in O(n) |

### 💡 Examples
```
Input:  nums = [100, 4, 200, 1, 3, 2]
Output: 4   ← sequence [1, 2, 3, 4]

Input:  nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
Output: 9
```

### 🔑 Key Points to Remember
- Add all numbers to a **HashSet** first for O(1) lookup
- Only start counting from **sequence start**: `num` is a start if `num - 1` is NOT in the set
- Expand from the start: keep checking `num + 1`, `num + 2`, ...
- Avoids O(n²) by not re-counting from the middle of a sequence

### ✍️ Solution
```java
class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int num : nums) set.add(num);

        int longest = 0;
        for (int num : set) {
            if (!set.contains(num - 1)) {  // only start from sequence beginning
                int current = num, length = 1;
                while (set.contains(current + 1)) {
                    current++;
                    length++;
                }
                longest = Math.max(longest, length);
            }
        }
        return longest;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(n) |

---

## 8️⃣ Majority Element
🔗 [LeetCode #169](https://leetcode.com/problems/majority-element/) &nbsp;|&nbsp; 🟢 Pattern: **Boyer-Moore Voting Algorithm**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` |
| **Output** | `int` — element that appears **more than n/2 times** |
| **Constraint** | Majority element is **guaranteed** to exist |

### 💡 Examples
```
Input:  nums = [3, 2, 3]
Output: 3

Input:  nums = [2, 2, 1, 1, 1, 2, 2]
Output: 2
```

### 🔑 Key Points to Remember
- HashMap approach: count frequencies, return key where count > n/2 — O(n) space
- Boyer-Moore is O(1) space: keep a `candidate` and `count`
  - Same as candidate → `count++`
  - Different → `count--`
  - Count hits 0 → new candidate
- The majority element always survives this cancellation process

### ✍️ Solution (Boyer-Moore — Optimal)
```java
class Solution {
    public int majorityElement(int[] nums) {
        int candidate = nums[0], count = 1;
        for (int i = 1; i < nums.length; i++) {
            if (count == 0) {
                candidate = nums[i];
                count = 1;
            } else if (nums[i] == candidate) {
                count++;
            } else {
                count--;
            }
        }
        return candidate;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) — Boyer-Moore |

---

## 9️⃣ Move Zeroes
🔗 [LeetCode #283](https://leetcode.com/problems/move-zeroes/) &nbsp;|&nbsp; 🟢 Pattern: **Two Pointers (In-place)**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (modify in-place) |
| **Output** | `void` — zeroes moved to end, non-zero order maintained |

### 💡 Examples
```
Input:  nums = [0, 1, 0, 3, 12]
Output: [1, 3, 12, 0, 0]

Input:  nums = [0]
Output: [0]
```

### 🔑 Key Points to Remember
- Use `insertPos` pointer: tracks where the next non-zero should go
- First pass: write all non-zero elements from front
- Second pass: fill remaining indices with `0`
- Maintains **relative order** of non-zero elements

### ✍️ Solution
```java
class Solution {
    public void moveZeroes(int[] nums) {
        int insertPos = 0;
        for (int num : nums) {
            if (num != 0) nums[insertPos++] = num;
        }
        while (insertPos < nums.length) {
            nums[insertPos++] = 0;
        }
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 🔟 Find All Duplicates in an Array
🔗 [LeetCode #442](https://leetcode.com/problems/find-all-duplicates-in-an-array/) &nbsp;|&nbsp; 🟢 Pattern: **Index Mapping / Sign Marking**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` — values in range `[1, n]`, each appears once or twice |
| **Output** | `List<Integer>` — all elements that appear twice |
| **Constraint** | O(n) time, O(1) extra space (no extra data structure) |

### 💡 Examples
```
Input:  nums = [4, 3, 2, 7, 8, 2, 3, 1]
Output: [2, 3]

Input:  nums = [1, 1, 2]
Output: [1]
```

### 🔑 Key Points to Remember
- Values are in range `[1, n]` → can use the **index as a hash**
- For each `num`, go to index `abs(num) - 1` and **negate** the value there
- If the value at that index is already negative → `num` appeared before → it's a duplicate
- Modifies the array (mark visited by sign), restores it implicitly by absolute value

### ✍️ Solution (Optimal — O(1) Space)
```java
class Solution {
    public List<Integer> findDuplicates(int[] nums) {
        List<Integer> result = new ArrayList<>();
        for (int num : nums) {
            int idx = Math.abs(num) - 1;
            if (nums[idx] < 0) {
                result.add(Math.abs(num));  // seen before → duplicate
            } else {
                nums[idx] = -nums[idx];     // mark as visited
            }
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) extra |

---

## 1️⃣1️⃣ Group Anagrams
🔗 [LeetCode #49](https://leetcode.com/problems/group-anagrams/) &nbsp;|&nbsp; 🟢 Pattern: **Hash Map – Frequency Key**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String[] strs` |
| **Output** | `List<List<String>>` — groups of anagrams |

### 💡 Examples
```
Input:  strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

Input:  strs = [""]
Output: [[""]]
```

### 🔑 Key Points to Remember
- Two words are anagrams if they have the same **character frequency**
- Build a key from a 26-element int array: `"1#1#0#...#"` (counts of a–z)
- Use `#` separator to avoid collision (e.g., `"11"` for 'a' vs `"1"` + `"1"` for 'a' and 'b')
- Alternative key: sorted string (`"aet"` for "eat", "tea", "ate")

### ✍️ Solution
```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String word : strs) {
            int[] count = new int[26];
            for (char c : word.toCharArray()) count[c - 'a']++;
            StringBuilder sb = new StringBuilder();
            for (int n : count) sb.append(n).append('#');
            String key = sb.toString();
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(word);
        }
        return new ArrayList<>(map.values());
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n × L) where L = average word length |
| Space | O(n × L) |

---

## 1️⃣2️⃣ Top K Frequent Elements
🔗 [LeetCode #347](https://leetcode.com/problems/top-k-frequent-elements/) &nbsp;|&nbsp; 🟢 Pattern: **Bucket Sort**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `int[]` — the `k` most frequent elements |

### 💡 Examples
```
Input:  nums = [1, 1, 1, 2, 2, 3],  k = 2
Output: [1, 2]

Input:  nums = [1],  k = 1
Output: [1]
```

### 🔑 Key Points to Remember
- Count frequencies using HashMap
- **Bucket Sort trick**: create `buckets[]` of size `n+1`; index = frequency
- Place numbers into their frequency bucket
- Iterate buckets from **right to left** (highest frequency first)
- Frequency cannot exceed `n` → safe bucket size

### ✍️ Solution
```java
class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        for (int num : nums) freq.put(num, freq.getOrDefault(num, 0) + 1);

        List<Integer>[] buckets = new List[nums.length + 1];
        for (int key : freq.keySet()) {
            int f = freq.get(key);
            if (buckets[f] == null) buckets[f] = new ArrayList<>();
            buckets[f].add(key);
        }

        int[] result = new int[k];
        int idx = 0;
        for (int i = buckets.length - 1; i >= 0 && idx < k; i--) {
            if (buckets[i] != null) {
                for (int num : buckets[i]) {
                    result[idx++] = num;
                    if (idx == k) break;
                }
            }
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(n) |

---

## 1️⃣3️⃣ First Missing Positive
🔗 [LeetCode #41](https://leetcode.com/problems/first-missing-positive/) &nbsp;|&nbsp; 🟢 Pattern: **Cyclic Sort / Index Placement**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (unsorted, may have negatives & duplicates) |
| **Output** | `int` — smallest missing positive integer |
| **Constraint** | O(n) time, O(1) space |

### 💡 Examples
```
Input:  nums = [1, 2, 0]
Output: 3

Input:  nums = [3, 4, -1, 1]
Output: 2

Input:  nums = [7, 8, 9, 11, 12]
Output: 1
```

### 🔑 Key Points to Remember
- The answer is always in range `[1, n+1]` — only those values matter
- **Place each number at its correct index**: `nums[i]` should go to index `nums[i] - 1`
- Keep swapping until `nums[i]` is out of range or already in place
- Second pass: first index where `nums[i] != i + 1` is the answer
- If all positions are correct → answer is `n + 1`

### ✍️ Solution
```java
class Solution {
    public int firstMissingPositive(int[] nums) {
        int n = nums.length;

        // Step 1: Place each number in its correct position
        for (int i = 0; i < n; i++) {
            while (nums[i] >= 1 && nums[i] <= n && nums[i] != nums[nums[i] - 1]) {
                int correctIdx = nums[i] - 1;
                int temp = nums[i];
                nums[i] = nums[correctIdx];
                nums[correctIdx] = temp;
            }
        }

        // Step 2: Find the first missing position
        for (int i = 0; i < n; i++) {
            if (nums[i] != i + 1) return i + 1;
        }

        return n + 1;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 🧠 Pattern Cheat Sheet

| Pattern | When to Use | Key Idea |
|---------|-------------|----------|
| **Hash Map** | Find pairs, frequency count | O(1) lookup by value |
| **Hash Set** | Check existence / duplicates | O(1) lookup, no duplicates |
| **Two Pointers** | In-place array operations | Move one pointer per condition |
| **Prefix Sum** | Subarray sum queries | `sum[i..j] = prefix[j] - prefix[i-1]` |
| **Kadane's Algorithm** | Maximum subarray | Reset running sum when negative |
| **Bucket Sort** | Top K by frequency | Index = frequency, O(n) sort |
| **Cyclic Sort** | Find missing in [1..n] range | Place value at its correct index |
| **Boyer-Moore** | Majority element (> n/2) | Cancel out non-majority votes |

---

*Last updated: March 2026*