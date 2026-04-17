# 🪟 LeetCode Sliding Window – Revision Notes

## 🗺️ Legend
| Badge | Meaning |
|-------|---------|
| 🔴 | Confused on pattern — need to re-learn |
| 🟡 | Understand pattern — coding needs polish |
| 🟢 | Fully confident — safe zone |

---

## 🧠 Core Concept — What is Sliding Window?

A **sliding window** is a subarray/substring that moves across the data structure.
Instead of recomputing from scratch each time → **reuse previous computation**.

```
Array:  [a, b, c, d, e, f]
           |_____|          ← window moves right →
                |_____|
```

### Two Types
| Type | Window Size | When to Use |
|------|-------------|-------------|
| **Fixed Window** | Always exactly `k` | "subarray/substring of size k" |
| **Variable Window** | Grows & shrinks | "longest/shortest satisfying condition" |

---

## 🔑 Master Templates

### 🔹 Fixed Window Template
```java
int windowSum = 0;
for (int i = 0; i < nums.length; i++) {
    windowSum += nums[i];                    // expand
    if (i >= k - 1) {
        // ✅ update answer here
        windowSum -= nums[i - k + 1];        // shrink — remove leftmost
    }
}
```

### 🔹 Variable Window Template
```java
int start = 0;
for (int end = 0; end < nums.length; end++) {
    // expand: add nums[end] to window
    while (/* condition is violated */) {
        // shrink: remove nums[start] from window
        start++;
    }
    // ✅ update answer here (window is valid)
}
```

### 🔹 AtMost Trick (for Exactly K problems)
```
exactly(K)  =  atMost(K)  −  atMost(K − 1)
```
> Use when "exactly K" is hard to track but "at most K" is easy.

### 🔹 Prefix Sum Template
```java
Map<Integer, Integer> prefixCount = new HashMap<>();
prefixCount.put(0, 1);  // empty subarray base
int sum = 0, count = 0;
for (int num : nums) {
    sum += num;
    count += prefixCount.getOrDefault(sum - k, 0);
    prefixCount.put(sum, prefixCount.getOrDefault(sum, 0) + 1);
}
```

---

## 📊 Progress Tracker

| # | Problem | Type | Pattern | Status |
|---|---------|------|---------|--------|
| 1 | [Maximum Average Subarray I](#1️⃣-maximum-average-subarray-i) | Fixed | Window Sum | ✅ |
| 2 | [Permutation in String](#2️⃣-permutation-in-string) | Fixed | Frequency Match | ✅ |
| 3 | [Find All Anagrams in a String](#3️⃣-find-all-anagrams-in-a-string) | Fixed | Sliding Freq Window | ✅ |
| 4 | [Sliding Window Maximum](#4️⃣-sliding-window-maximum) | Fixed | Monotonic Deque | ⬜ |
| 5 | [Minimum Size Subarray Sum](#5️⃣-minimum-size-subarray-sum) | Variable | Shrink when ≥ target | ✅ |
| 6 | [Longest Substring Without Repeating](#6️⃣-longest-substring-without-repeating-characters) | Variable | Set / Map | ✅ |
| 7 | [Longest Repeating Char Replacement](#7️⃣-longest-repeating-character-replacement) | Variable | Max Freq Trick | ✅ |
| 8 | [Longest Substring K Distinct](#8️⃣-longest-substring-with-k-distinct-characters) | Variable | Frequency Map | ✅ |
| 9 | [Fruit Into Baskets](#9️⃣-fruit-into-baskets) | Variable | At Most 2 Types | ✅ |
| 10 | [Max Consecutive Ones III](#🔟-max-consecutive-ones-iii) | Variable | At Most K Zeros | ✅ |
| 11 | [Subarrays with K Different Integers](#1️⃣1️⃣-subarrays-with-k-different-integers) | Variable | AtMost(k)−AtMost(k−1) | ⬜ |
| 12 | [Longest Subarray of 1s After Delete](#1️⃣2️⃣-longest-subarray-of-1s-after-deleting-one) | Variable | One Deletion Window | ✅ |
| 13 | [Minimum Window Substring](#1️⃣3️⃣-minimum-window-substring) | Variable (Hard) | Cover All Required Chars | ⬜ |
| 14 | [Binary Subarrays With Sum](#1️⃣4️⃣-binary-subarrays-with-sum) | Prefix+Window | AtMost on Binary | ⬜ |
| 15 | [Subarray Sum Equals K](#1️⃣5️⃣-subarray-sum-equals-k) | Prefix Sum | HashMap Cumulative Sum | ✅ |
| 16 | [Count Number of Nice Subarrays](#1️⃣6️⃣-count-number-of-nice-subarrays) | AtMost Trick | Exactly K Odds | ✅ |

---

## ── FIXED WINDOW PROBLEMS ──────────────────────────────

## 1️⃣ Maximum Average Subarray I
🔗 [LeetCode #643](https://leetcode.com/problems/maximum-average-subarray-i/) &nbsp;|&nbsp; 🟢 Pattern: **Fixed Window – Sum**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `double` — maximum average of any subarray of length `k` |

### 💡 Examples
```
Input:  nums = [1, 12, -5, -6, 50, 3],  k = 4
Output: 12.75   ← subarray [12, -5, -6, 50] → sum=51, avg=12.75

Input:  nums = [5],  k = 1
Output: 5.0
```

### 🔑 Key Points to Remember
- Maintain a **running sum** — don't recompute from scratch
- When window reaches size `k` → record answer, then subtract the leftmost element
- Final answer: `maxSum / k` — cast to `double` before dividing
- Initialize `maxSum` carefully: use `Integer.MIN_VALUE` or first window sum

### ✍️ Solution
```java
class Solution {
    public double findMaxAverage(int[] nums, int k) {
        int currentSum = 0;
        int maxSum = Integer.MIN_VALUE;
        int start = 0;

        for (int i = 0; i < nums.length; i++) {
            currentSum += nums[i];
            if (i >= k - 1) {
                maxSum = Math.max(maxSum, currentSum);
                currentSum -= nums[start];
                start++;
            }
        }
        return (double) maxSum / k;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 2️⃣ Permutation in String
🔗 [LeetCode #567](https://leetcode.com/problems/permutation-in-string/) &nbsp;|&nbsp; 🟢 Pattern: **Fixed Window – Frequency Match**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s1`, `String s2` |
| **Output** | `boolean` — `true` if any permutation of `s1` exists as a substring in `s2` |

### 💡 Examples
```
Input:  s1 = "ab",  s2 = "eidbaooo"
Output: true   ← "ba" is a permutation of "ab"

Input:  s1 = "ab",  s2 = "eidboaoo"
Output: false
```

### 🔑 Key Points to Remember
- A permutation = same character **frequencies** in the window
- Fixed window size = `s1.length()`
- Slide window: add new char, remove char that fell off the left
- `Arrays.equals(freq1, freq2)` compares both frequency arrays in O(26) = O(1)
- Edge: if `s1.length() > s2.length()` → return `false` immediately

### ✍️ Solution
```java
class Solution {
    public boolean checkInclusion(String s1, String s2) {
        if (s1.length() > s2.length()) return false;

        int[] freq1 = new int[26];
        int[] freq2 = new int[26];

        for (char c : s1.toCharArray()) freq1[c - 'a']++;

        int w = s1.length();
        for (int i = 0; i < s2.length(); i++) {
            freq2[s2.charAt(i) - 'a']++;
            if (i >= w) freq2[s2.charAt(i - w) - 'a']--;  // remove left char
            if (Arrays.equals(freq1, freq2)) return true;
        }
        return false;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) — O(26) comparison is O(1) |
| Space | O(1) — fixed 26-size arrays |

---

## 3️⃣ Find All Anagrams in a String
🔗 [LeetCode #438](https://leetcode.com/problems/find-all-anagrams-in-a-string/) &nbsp;|&nbsp; 🟢 Pattern: **Fixed Window – Collect All Start Indices**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s`, `String p` |
| **Output** | `List<Integer>` — starting indices of all anagrams of `p` in `s` |

### 💡 Examples
```
Input:  s = "cbaebabacd",  p = "abc"
Output: [0, 6]   ← "cba" at 0, "bac" at 6

Input:  s = "abab",  p = "ab"
Output: [0, 1, 2]
```

### 🔑 Key Points to Remember
- Same as Permutation in String — but **collect all** valid start indices
- Start index when match found: `i - windowSize + 1`
- Only record answer when `i >= windowSize - 1` (full window formed)
- This is essentially problem #2 but returns a list instead of boolean

### ✍️ Solution
```java
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        int[] freq1 = new int[26];
        int[] freq2 = new int[26];
        List<Integer> result = new ArrayList<>();

        for (char c : p.toCharArray()) freq1[c - 'a']++;

        int w = p.length();
        for (int i = 0; i < s.length(); i++) {
            freq2[s.charAt(i) - 'a']++;
            if (i >= w) freq2[s.charAt(i - w) - 'a']--;
            if (i >= w - 1 && Arrays.equals(freq1, freq2)) {
                result.add(i - w + 1);   // ← start index
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
| Space | O(1) |

---

## 4️⃣ Sliding Window Maximum
🔗 [LeetCode #239](https://leetcode.com/problems/sliding-window-maximum/) &nbsp;|&nbsp; ⬜ Pattern: **Fixed Window – Monotonic Deque**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `int[]` — maximum value in each window of size `k` |

### 💡 Examples
```
Input:  nums = [1, 3, -1, -3, 5, 3, 6, 7],  k = 3
Output: [3, 3, 5, 5, 6, 7]

Window [1,3,-1] → max 3
Window [3,-1,-3] → max 3
Window [-1,-3,5] → max 5 ...
```

### 🔑 Key Points to Remember
- Brute force: O(n×k) — too slow
- Use a **Monotonic Deque** (decreasing order): front = max of window
- **Add right**: remove all deque elements smaller than `nums[end]` from back
- **Remove left**: if deque front = `start` index → pop it (out of window)
- Deque stores **indices**, not values
- Add result when window is full: `end >= k - 1`

### ✍️ Solution
```java
class Solution {
    public int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] result = new int[n - k + 1];
        Deque<Integer> deque = new ArrayDeque<>(); // stores indices

        for (int end = 0; end < n; end++) {
            // Remove elements out of window
            while (!deque.isEmpty() && deque.peekFirst() < end - k + 1) {
                deque.pollFirst();
            }
            // Remove smaller elements from back (maintain decreasing order)
            while (!deque.isEmpty() && nums[deque.peekLast()] < nums[end]) {
                deque.pollLast();
            }
            deque.offerLast(end);

            if (end >= k - 1) {
                result[end - k + 1] = nums[deque.peekFirst()]; // front = max
            }
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) — each element added/removed once |
| Space | O(k) — deque size |

---

## ── VARIABLE WINDOW PROBLEMS ───────────────────────────

## 5️⃣ Minimum Size Subarray Sum
🔗 [LeetCode #209](https://leetcode.com/problems/minimum-size-subarray-sum/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – Shrink When Valid**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int target`, `int[] nums` (positive integers) |
| **Output** | `int` — length of smallest subarray with sum ≥ target; `0` if none |

### 💡 Examples
```
Input:  target = 7,  nums = [2, 3, 1, 2, 4, 3]
Output: 2   ← subarray [4, 3]

Input:  target = 4,  nums = [1, 4, 4]
Output: 1

Input:  target = 11,  nums = [1, 1, 1, 1, 1]
Output: 0
```

### 🔑 Key Points to Remember
- Expand right → add to `windowSum`
- Once `windowSum >= target` → **record size, then shrink from left**
- Keep shrinking as long as condition holds (we want the **minimum**)
- Return `Integer.MAX_VALUE` check → return `0` if no valid window found

### ✍️ Solution
```java
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int start = 0, windowSum = 0;
        int minLen = Integer.MAX_VALUE;

        for (int end = 0; end < nums.length; end++) {
            windowSum += nums[end];
            while (windowSum >= target) {
                minLen = Math.min(minLen, end - start + 1);
                windowSum -= nums[start];
                start++;
            }
        }
        return minLen == Integer.MAX_VALUE ? 0 : minLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 6️⃣ Longest Substring Without Repeating Characters
🔗 [LeetCode #3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – HashSet**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` |
| **Output** | `int` — length of longest substring with all unique characters |

### 💡 Examples
```
Input:  s = "abcabcbb"
Output: 3   ← "abc"

Input:  s = "bbbbb"
Output: 1   ← "b"

Input:  s = "pwwkew"
Output: 3   ← "wke"
```

### 🔑 Key Points to Remember
- Use a `HashSet` to track characters in current window
- If new char already in set → shrink from left until it's removed
- `maxLen = end - start + 1` after each valid expansion
- Alternative: use `HashMap<char, index>` to jump `start` directly (more optimal)

### ✍️ Solution
```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Set<Character> set = new HashSet<>();
        int start = 0, maxLen = 0;

        for (int end = 0; end < s.length(); end++) {
            char c = s.charAt(end);
            while (set.contains(c)) {
                set.remove(s.charAt(start));
                start++;
            }
            set.add(c);
            maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ✍️ Optimized (HashMap — jump start pointer)
```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        Map<Character, Integer> map = new HashMap<>();
        int start = 0, maxLen = 0;

        for (int end = 0; end < s.length(); end++) {
            char c = s.charAt(end);
            if (map.containsKey(c)) {
                start = Math.max(start, map.get(c) + 1); // jump past duplicate
            }
            map.put(c, end);
            maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(min(n, alphabet)) |

---

## 7️⃣ Longest Repeating Character Replacement
🔗 [LeetCode #424](https://leetcode.com/problems/longest-repeating-character-replacement/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – Max Frequency Trick**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` (uppercase only), `int k` |
| **Output** | `int` — length of longest substring after replacing at most `k` characters |

### 💡 Examples
```
Input:  s = "ABAB",  k = 2
Output: 4   ← Replace both B's or both A's → "AAAA"

Input:  s = "AABABBA",  k = 1
Output: 4   ← "AABA" or "ABBB" (replace 1 char)
```

### 🔑 Key Points to Remember
- A window is valid if: `windowSize - maxFreq ≤ k`
  - `windowSize - maxFreq` = number of characters that need to be replaced
- Track `maxFreq` = count of the **most frequent character** in current window
- When window becomes invalid → shrink from left
- `maxFreq` is never decreased (we only care about growing the window)

### ✍️ Solution
```java
class Solution {
    public int characterReplacement(String s, int k) {
        int[] freq = new int[26];
        int start = 0, maxFreq = 0, maxLen = 0;

        for (int end = 0; end < s.length(); end++) {
            freq[s.charAt(end) - 'A']++;
            maxFreq = Math.max(maxFreq, freq[s.charAt(end) - 'A']);

            while ((end - start + 1) - maxFreq > k) {  // invalid window
                freq[s.charAt(start) - 'A']--;
                start++;
            }
            maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 8️⃣ Longest Substring with K Distinct Characters
🔗 [GFG](https://www.geeksforgeeks.org/problems/longest-k-unique-characters-substring0853/1) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – Frequency Map**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s`, `int k` |
| **Output** | `int` — length of longest substring with **exactly** `k` distinct characters; `-1` if not possible |

### 💡 Examples
```
Input:  s = "aabacbebebe",  k = 3
Output: 7   ← "cbebebe"

Input:  s = "aaaa",  k = 2
Output: -1
```

### 🔑 Key Points to Remember
- Maintain `distinct` count: increment when a char's freq goes from 0 → 1
- Shrink when `distinct > k`: decrement freq, if freq hits 0 → decrement `distinct`
- Update `maxLen` only when `distinct == k` (exactly k, not at most k)
- Return `-1` if answer never updated (no valid window)

### ✍️ Solution
```java
class Solution {
    public int longestKSubstr(String s, int k) {
        int[] freq = new int[26];
        int start = 0, maxLen = -1, distinct = 0;

        for (int end = 0; end < s.length(); end++) {
            char c = s.charAt(end);
            if (freq[c - 'a'] == 0) distinct++;
            freq[c - 'a']++;

            while (distinct > k) {
                freq[s.charAt(start) - 'a']--;
                if (freq[s.charAt(start) - 'a'] == 0) distinct--;
                start++;
            }

            if (distinct == k) maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 9️⃣ Fruit Into Baskets
🔗 [LeetCode #904](https://leetcode.com/problems/fruit-into-baskets/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – At Most 2 Distinct**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] fruits` — each value is a fruit type |
| **Output** | `int` — max fruits you can pick (longest subarray with ≤ 2 distinct types) |

### 💡 Examples
```
Input:  fruits = [1, 2, 1]
Output: 3   ← pick all

Input:  fruits = [0, 1, 2, 2]
Output: 3   ← [1, 2, 2]

Input:  fruits = [1, 2, 3, 2, 2]
Output: 4   ← [2, 3, 2, 2]
```

### 🔑 Key Points to Remember
- "2 baskets" = at most **2 distinct** fruit types in the window
- Use `HashMap<fruitType, count>` — remove key when count hits 0
- This is the exact same pattern as K-distinct with `k = 2`
- Generalizes to "at most K distinct elements"

### ✍️ Solution
```java
class Solution {
    public int totalFruit(int[] fruits) {
        Map<Integer, Integer> map = new HashMap<>();
        int start = 0, maxLen = 0, k = 2;

        for (int end = 0; end < fruits.length; end++) {
            map.put(fruits[end], map.getOrDefault(fruits[end], 0) + 1);

            while (map.size() > k) {
                map.put(fruits[start], map.get(fruits[start]) - 1);
                if (map.get(fruits[start]) == 0) map.remove(fruits[start]);
                start++;
            }

            maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(k) = O(1) |

---

## 🔟 Max Consecutive Ones III
🔗 [LeetCode #1004](https://leetcode.com/problems/max-consecutive-ones-iii/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – At Most K Zeros**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (binary), `int k` |
| **Output** | `int` — max consecutive 1s after flipping at most `k` zeros |

### 💡 Examples
```
Input:  nums = [1,1,1,0,0,0,1,1,1,1,0],  k = 2
Output: 6   ← flip zeros at index 3,4 → [1,1,1,1,1,1,1,1,1,1,0]

Input:  nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1,0],  k = 3
Output: 10
```

### 🔑 Key Points to Remember
- Count `zeroCount` in window
- If `zeroCount > k` → shrink from left until valid
- This is equivalent to: "longest subarray with at most k zeros"
- Similar to #12 (Delete One Element) where `k = 1`

### ✍️ Solution
```java
class Solution {
    public int longestOnes(int[] nums, int k) {
        int start = 0, maxLen = 0, zeroCount = 0;

        for (int end = 0; end < nums.length; end++) {
            if (nums[end] == 0) zeroCount++;

            while (zeroCount > k) {
                if (nums[start] == 0) zeroCount--;
                start++;
            }

            maxLen = Math.max(maxLen, end - start + 1);
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## ── ATMOST TRICK PROBLEMS ──────────────────────────────

## 1️⃣1️⃣ Subarrays with K Different Integers
🔗 [LeetCode #992](https://leetcode.com/problems/subarrays-with-k-different-integers/) &nbsp;|&nbsp; ⬜ Pattern: **AtMost(k) − AtMost(k−1)**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `int` — number of subarrays with **exactly** `k` distinct integers |

### 💡 Examples
```
Input:  nums = [1, 2, 1, 2, 3],  k = 2
Output: 7

Input:  nums = [1, 2, 1, 3, 4],  k = 3
Output: 3
```

### 🔑 Key Points to Remember
- Exactly K = AtMost(K) − AtMost(K−1)
- `atMost(k)` = count of subarrays with **at most** k distinct values
- Count formula inside atMost: `count += end - start + 1`
  (all subarrays ending at `end` and starting from `start` to `end`)
- Use HashMap for frequency of elements in window

### ✍️ Solution
```java
class Solution {
    public int subarraysWithKDistinct(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private int atMost(int[] nums, int k) {
        Map<Integer, Integer> freq = new HashMap<>();
        int start = 0, count = 0;

        for (int end = 0; end < nums.length; end++) {
            freq.put(nums[end], freq.getOrDefault(nums[end], 0) + 1);

            while (freq.size() > k) {
                freq.put(nums[start], freq.get(nums[start]) - 1);
                if (freq.get(nums[start]) == 0) freq.remove(nums[start]);
                start++;
            }

            count += end - start + 1;  // all valid subarrays ending at end
        }
        return count;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(k) |

---

## 1️⃣2️⃣ Longest Subarray of 1s After Deleting One
🔗 [LeetCode #1493](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) &nbsp;|&nbsp; 🟢 Pattern: **Variable Window – At Most 1 Zero**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (binary) |
| **Output** | `int` — length of longest subarray of 1s after deleting **exactly one** element |

### 💡 Examples
```
Input:  nums = [1, 1, 0, 1]
Output: 3   ← delete the 0 → [1,1,1]

Input:  nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]
Output: 5   ← delete first 0 in middle → [1,1,1,0,1,1]

Input:  nums = [1, 1, 1]
Output: 2   ← must delete one element, delete any 1
```

### 🔑 Key Points to Remember
- Allow at most 1 zero in window (we're deleting it)
- Answer is `end - start` (not `+1`) because one element is deleted
- Edge case: all 1s → answer is `n - 1`

### ✍️ Solution
```java
class Solution {
    public int longestSubarray(int[] nums) {
        int start = 0, maxLen = 0, zeroCount = 0;

        for (int end = 0; end < nums.length; end++) {
            if (nums[end] == 0) zeroCount++;

            while (zeroCount > 1) {
                if (nums[start] == 0) zeroCount--;
                start++;
            }

            maxLen = Math.max(maxLen, end - start);  // ← note: no +1 (one deletion)
        }
        return maxLen;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## ── HARD PROBLEMS ──────────────────────────────────────

## 1️⃣3️⃣ Minimum Window Substring
🔗 [LeetCode #76](https://leetcode.com/problems/minimum-window-substring/) &nbsp;|&nbsp; ⬜ Pattern: **Variable Window Hard – Cover All Required Chars**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s`, `String t` |
| **Output** | `String` — smallest substring of `s` that contains all characters of `t`; `""` if impossible |

### 💡 Examples
```
Input:  s = "ADOBECODEBANC",  t = "ABC"
Output: "BANC"

Input:  s = "a",  t = "a"
Output: "a"

Input:  s = "a",  t = "aa"
Output: ""
```

### 🔑 Key Points to Remember
- Track `need` map (freq of t) and `have` vs `required` counters
- `have` counts chars that are **fully satisfied** in current window
- Expand right → when `have == required` → valid window → try to shrink
- Track minimum window with `minLen`, `minStart`
- Shrink from left → update `have` if a char drops below needed count

### ✍️ Solution
```java
class Solution {
    public String minWindow(String s, String t) {
        if (s.length() < t.length()) return "";

        Map<Character, Integer> need = new HashMap<>();
        for (char c : t.toCharArray()) need.put(c, need.getOrDefault(c, 0) + 1);

        int required = need.size(); // distinct chars needed
        int have = 0;
        Map<Character, Integer> window = new HashMap<>();

        int minLen = Integer.MAX_VALUE, minStart = 0;
        int start = 0;

        for (int end = 0; end < s.length(); end++) {
            char c = s.charAt(end);
            window.put(c, window.getOrDefault(c, 0) + 1);

            if (need.containsKey(c) && window.get(c).equals(need.get(c))) {
                have++;  // this char is now fully satisfied
            }

            while (have == required) {  // valid window → try to shrink
                if (end - start + 1 < minLen) {
                    minLen = end - start + 1;
                    minStart = start;
                }
                char leftChar = s.charAt(start);
                window.put(leftChar, window.get(leftChar) - 1);
                if (need.containsKey(leftChar) && window.get(leftChar) < need.get(leftChar)) {
                    have--;  // no longer satisfied
                }
                start++;
            }
        }
        return minLen == Integer.MAX_VALUE ? "" : s.substring(minStart, minStart + minLen);
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(|s| + |t|) |
| Space | O(|s| + |t|) |

---

## ── PREFIX SUM + WINDOW PROBLEMS ──────────────────────

## 1️⃣4️⃣ Binary Subarrays With Sum
🔗 [LeetCode #930](https://leetcode.com/problems/binary-subarrays-with-sum/) &nbsp;|&nbsp; ⬜ Pattern: **AtMost Trick on Binary Array**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (binary), `int goal` |
| **Output** | `int` — number of subarrays with sum equal to `goal` |

### 💡 Examples
```
Input:  nums = [1, 0, 1, 0, 1],  goal = 2
Output: 4

Input:  nums = [0, 0, 0, 0, 0],  goal = 0
Output: 15
```

### 🔑 Key Points to Remember
- Exact sum = AtMost(goal) − AtMost(goal − 1)
- AtMost works here because the array is binary (only 0s and 1s)
- Handle `goal - 1 < 0` edge case → return 0 for that call
- `count += end - start + 1` inside atMost counts all valid subarrays ending at `end`

### ✍️ Solution
```java
class Solution {
    public int numSubarraysWithSum(int[] nums, int goal) {
        return atMost(nums, goal) - atMost(nums, goal - 1);
    }

    private int atMost(int[] nums, int k) {
        if (k < 0) return 0;
        int start = 0, count = 0, sum = 0;

        for (int end = 0; end < nums.length; end++) {
            sum += nums[end];
            while (sum > k) {
                sum -= nums[start];
                start++;
            }
            count += end - start + 1;
        }
        return count;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 1️⃣5️⃣ Subarray Sum Equals K
🔗 [LeetCode #560](https://leetcode.com/problems/subarray-sum-equals-k/) &nbsp;|&nbsp; 🟢 Pattern: **Prefix Sum + HashMap**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (can have negatives), `int k` |
| **Output** | `int` — count of subarrays with sum equal to `k` |

### 💡 Examples
```
Input:  nums = [1, 1, 1],  k = 2
Output: 2

Input:  nums = [1, 2, 3],  k = 3
Output: 2   ← [1,2] and [3]

Input:  nums = [1, -1, 1],  k = 1
Output: 3   ← works because of negatives (sliding window won't work here!)
```

### 🔑 Key Points to Remember
- ⚠️ **Sliding window doesn't work** here because of negative numbers
- Use prefix sum: subarray `[j+1..i]` has sum `k` when `prefix[i] - prefix[j] = k`
  → i.e., look for `prefix[i] - k` in the map
- Initialize `map = {0: 1}` — the empty prefix (sum = 0 seen once)
- This handles subarrays starting from index 0

### ✍️ Solution
```java
class Solution {
    public int subarraySum(int[] nums, int k) {
        Map<Integer, Integer> prefixCount = new HashMap<>();
        prefixCount.put(0, 1);
        int sum = 0, count = 0;

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

## 1️⃣6️⃣ Count Number of Nice Subarrays
🔗 [LeetCode #1248](https://leetcode.com/problems/count-number-of-nice-subarrays/) &nbsp;|&nbsp; 🟢 Pattern: **AtMost Trick – Exactly K Odds**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int k` |
| **Output** | `int` — number of subarrays with **exactly** `k` odd numbers |

### 💡 Examples
```
Input:  nums = [1, 1, 2, 1, 1],  k = 3
Output: 2   ← [1,1,2,1] and [1,2,1,1]

Input:  nums = [2, 4, 6],  k = 1
Output: 0
```

### 🔑 Key Points to Remember
- Exactly K odds = AtMost(K) − AtMost(K−1)
- Inside `atMost`: odd check = `nums[end] % 2 == 1`
- `count += end - start + 1` counts all valid subarrays ending at `end`
- Shrink while `oddCount > k`

### ✍️ Dry Run (atMost(3) for [1,1,2,1,1])
| end | nums[end] | oddCount | start | +count | total |
|-----|-----------|----------|-------|--------|-------|
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 1 | 2 | 0 | 2 | 3 |
| 2 | 2 | 2 | 0 | 3 | 6 |
| 3 | 1 | 3 | 0 | 4 | 10 |
| 4 | 1 | 4→shrink→3 | 1 | 4 | 14 |

**atMost(3) = 14, atMost(2) = 12 → Answer = 2** ✅

### ✍️ Solution
```java
class Solution {
    public int numberOfSubarrays(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private int atMost(int[] nums, int k) {
        int start = 0, count = 0, oddCount = 0;

        for (int end = 0; end < nums.length; end++) {
            if (nums[end] % 2 == 1) oddCount++;

            while (oddCount > k) {
                if (nums[start] % 2 == 1) oddCount--;
                start++;
            }

            count += end - start + 1;
        }
        return count;
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

| Pattern | Trigger Words | Key Formula / Trick |
|---------|--------------|---------------------|
| **Fixed Window** | "subarray of size k", "window of k" | Slide one step at a time; add right, remove left |
| **Variable – Max Length** | "longest subarray/substring with..." | Expand right, shrink left when invalid; `maxLen = end-start+1` |
| **Variable – Min Length** | "smallest/shortest subarray with..." | Shrink while valid; `minLen = end-start+1` inside while |
| **At Most K** | "at most k distinct/zeros/odds" | `while(condition > k) shrink`; `count += end-start+1` |
| **Exactly K** | "exactly k distinct/odds/zeros" | `atMost(k) - atMost(k-1)` |
| **Prefix Sum** | negatives in array, cumulative sum | `count += freq[sum-k]`; init `{0:1}` |
| **Monotonic Deque** | "max/min in each window" | Deque stores indices; maintain decreasing/increasing order |
| **Frequency Match** | "permutation", "anagram" | `int[26]` freq array; `Arrays.equals()` to compare |

---

## ⚡ Quick Formula Recall

```
Fixed Window:
  windowSum += nums[end]
  if (i >= k-1) → answer, then windowSum -= nums[start++]

Variable Window (Max):
  expand → add to window
  while (invalid) → shrink from left
  maxLen = end - start + 1

Variable Window (Min):
  expand → add to window
  while (valid) → update minLen, then shrink
  minLen = end - start + 1

AtMost Trick:
  exactly(K) = atMost(K) - atMost(K-1)
  inside atMost: count += end - start + 1

Prefix Sum:
  map.put(0, 1)
  sum += num
  count += map.getOrDefault(sum - k, 0)
  map.put(sum, map.getOrDefault(sum, 0) + 1)

Count subarrays ending at 'end':
  count += end - start + 1
  (all subarrays from start→end, start+1→end, ..., end→end)
```

---

*Last updated: March 2026*