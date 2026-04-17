# 👆👆 LeetCode Two Pointers – Revision Notes

## 🗺️ Legend
| Badge | Meaning |
|-------|---------|
| 🔴 | Confused on pattern — need to re-learn |
| 🟡 | Understand pattern — coding needs polish |
| 🟢 | Fully confident — safe zone |

---

## 🧠 Core Concept — What is Two Pointer?

Instead of nested loops **(O(n²))**, place two indices on the array and move them smartly → **O(n)**.

```
Opposite Direction:         Same Direction (Slow/Fast):
[1, 2, 3, 4, 5]            [0, 1, 0, 3, 12]
 ↑           ↑              ↑
 L           R              S
             ←→             F →
```

---

## 🎯 Five Types of Two Pointer

| Type | How It Works | Classic Problems |
|------|-------------|-----------------|
| **1️⃣ Opposite Pointers** | Left at start, right at end, move toward center | Palindrome, Two Sum II, Container Water |
| **2️⃣ Slow & Fast Pointer** | Both move forward, slow waits for condition | Remove Duplicates, Move Zeroes, Remove Element |
| **3️⃣ Sorting + Two Pointer** | Sort first, then opposite pointers | 3Sum, 4Sum, 3Sum Closest |
| **4️⃣ Expand Around Center** | Expand outward from a center index | Longest Palindromic Substring |
| **5️⃣ Three Pointers (DNF)** | low / mid / high — partition array | Sort Colors |

---

## 🔑 Master Templates

### 🔹 Opposite Pointers
```java
int left = 0, right = nums.length - 1;
while (left < right) {
    if (/* condition */) {
        // found answer
    } else if (/* too small */) {
        left++;
    } else {
        right--;
    }
}
```

### 🔹 Slow & Fast Pointer
```java
int slow = 0;
for (int fast = 0; fast < nums.length; fast++) {
    if (/* nums[fast] is valid */) {
        nums[slow] = nums[fast];  // write valid value
        slow++;
    }
}
// slow = count of valid elements
```

### 🔹 Sorting + Two Pointer (3Sum)
```java
Arrays.sort(nums);
for (int i = 0; i < nums.length - 2; i++) {
    if (i > 0 && nums[i] == nums[i-1]) continue;  // skip duplicates
    int left = i + 1, right = nums.length - 1;
    while (left < right) {
        int sum = nums[i] + nums[left] + nums[right];
        if (sum == 0) { /* add to result */ left++; right--; }
        else if (sum < 0) left++;
        else right--;
    }
}
```

### 🔹 Expand Around Center
```java
String expand(String s, int left, int right) {
    while (left >= 0 && right < s.length()
           && s.charAt(left) == s.charAt(right)) {
        left--;
        right++;
    }
    return s.substring(left + 1, right);  // window after expansion
}
// Call for odd:  expand(s, i, i)
// Call for even: expand(s, i, i+1)
```

### 🔹 Dutch National Flag (3 Pointers)
```java
int low = 0, mid = 0, high = nums.length - 1;
while (mid <= high) {
    if      (nums[mid] == 0) swap(nums, low++, mid++);
    else if (nums[mid] == 1) mid++;
    else                     swap(nums, mid, high--);
}
```

---

## 📊 Progress Tracker

| # | Problem | Type | Pattern | Status |
|---|---------|------|---------|--------|
| 1 | [Valid Palindrome](#1️⃣-valid-palindrome) | Opposite | Compare from both ends | ✅ |
| 2 | [Remove Duplicates from Sorted Array](#2️⃣-remove-duplicates-from-sorted-array) | Slow/Fast | Overwrite unique in-place | ✅ |
| 3 | [Two Sum II](#3️⃣-two-sum-ii-sorted-array) | Opposite | Adjust by sum comparison | ✅ |
| 4 | [Container With Most Water](#4️⃣-container-with-most-water) | Opposite | Move smaller height pointer | ✅ |
| 5 | [3Sum](#5️⃣-3sum) | Sort+Two Pointer | Fix one, 2Sum on rest | ✅ |
| 6 | [Trapping Rain Water](#6️⃣-trapping-rain-water) | Opposite+MaxTrack | leftMax & rightMax | ✅ |
| 7 | [Reverse String](#7️⃣-reverse-string) | Opposite | Swap chars | ✅ |
| 8 | [Squares of a Sorted Array](#8️⃣-squares-of-a-sorted-array) | Opposite | Fill result from end | ✅ |
| 9 | [Partition Labels](#9️⃣-partition-labels) | Greedy+Pointer | Track last index of each char | ✅ |
| 10 | [Move Zeroes](#🔟-move-zeroes) | Slow/Fast | Move non-zero forward | ✅ |
| 11 | [4Sum](#1️⃣1️⃣-4sum) | Sort+Two Pointer | Extend 3Sum logic | ✅ |
| 12 | [3Sum Closest](#1️⃣2️⃣-3sum-closest) | Sort+Two Pointer | Minimize diff from target | ✅ |
| 13 | [Remove Element](#1️⃣3️⃣-remove-element) | Slow/Fast | Overwrite unwanted values | ✅ |
| 14 | [Sort Colors (DNF)](#1️⃣4️⃣-sort-colors-dutch-national-flag) | 3 Pointers | Dutch National Flag | ✅ |
| 15 | [Valid Palindrome II](#1️⃣5️⃣-valid-palindrome-ii) | Opposite+Skip | Allow one deletion | ✅ |
| 16 | [Backspace String Compare](#1️⃣6️⃣-backspace-string-compare) | Reverse Pointer | Traverse from end | ✅ |
| 17 | [Boats to Save People](#1️⃣7️⃣-boats-to-save-people) | Greedy+Two Pointer | Pair lightest + heaviest | ✅ |
| 18 | [Longest Palindromic Substring](#1️⃣8️⃣-longest-palindromic-substring) | Expand Around Center | Expand left/right | ✅ |

---

## ── TYPE 1: OPPOSITE POINTERS ──────────────────────────

## 1️⃣ Valid Palindrome
🔗 [LeetCode #125](https://leetcode.com/problems/valid-palindrome/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers – Compare Chars**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` (may have spaces, punctuation, mixed case) |
| **Output** | `boolean` — `true` if it reads the same forwards and backwards (ignoring non-alphanumeric, case-insensitive) |

### 💡 Examples
```
Input:  s = "A man, a plan, a canal: Panama"
Output: true   ← "amanaplanacanalpanama"

Input:  s = "race a car"
Output: false  ← "raceacar" is not a palindrome

Input:  s = " "
Output: true   ← empty string is palindrome
```

### 🔑 Key Points to Remember
- Skip non-alphanumeric characters: `Character.isLetterOrDigit(c)`
- Compare case-insensitively: `Character.toLowerCase(c)`
- Move both pointers inward after each match
- Stop when `left >= right`

### ✍️ Solution
```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0, right = s.length() - 1;

        while (left < right) {
            while (left < right && !Character.isLetterOrDigit(s.charAt(left)))  left++;
            while (left < right && !Character.isLetterOrDigit(s.charAt(right))) right--;

            if (Character.toLowerCase(s.charAt(left)) !=
                Character.toLowerCase(s.charAt(right))) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 3️⃣ Two Sum II (Sorted Array)
🔗 [LeetCode #167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers – Adjust by Sum**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] numbers` (sorted ascending, 1-indexed), `int target` |
| **Output** | `int[]` — 1-indexed positions `[i, j]` such that `numbers[i] + numbers[j] == target` |
| **Constraint** | Exactly one solution; use O(1) extra space |

### 💡 Examples
```
Input:  numbers = [2, 7, 11, 15],  target = 9
Output: [1, 2]   ← 2+7=9

Input:  numbers = [2, 3, 4],  target = 6
Output: [1, 3]   ← 2+4=6

Input:  numbers = [-1, 0],  target = -1
Output: [1, 2]
```

### 🔑 Key Points to Remember
- Array is **sorted** → Two Pointer works perfectly (unlike unsorted → use HashMap)
- `sum < target` → need bigger number → `left++`
- `sum > target` → need smaller number → `right--`
- Return **1-indexed** answer: `[left+1, right+1]`

### 🔍 Visualization
```
numbers = [2, 7, 11, 15],  target = 9

 2   7  11  15
 ↑           ↑     sum = 2+15 = 17 > 9 → right--
 ↑       ↑         sum = 2+11 = 13 > 9 → right--
 ↑   ↑             sum = 2+7  =  9 ✅  → return [1,2]
```

### ✍️ Solution
```java
class Solution {
    public int[] twoSum(int[] numbers, int target) {
        int left = 0, right = numbers.length - 1;

        while (left < right) {
            int sum = numbers[left] + numbers[right];
            if      (sum == target) return new int[]{left + 1, right + 1};
            else if (sum < target)  left++;
            else                    right--;
        }
        return new int[]{-1, -1};
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 4️⃣ Container With Most Water
🔗 [LeetCode #11](https://leetcode.com/problems/container-with-most-water/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers – Move Smaller Height**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] height` — heights of vertical lines |
| **Output** | `int` — maximum water area between any two lines |

### 💡 Examples
```
Input:  height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49   ← lines at index 1 (h=8) and index 8 (h=7): min(8,7) × (8-1) = 49

Input:  height = [1, 1]
Output: 1
```

### 🔑 Key Points to Remember
- Area = `Math.min(height[left], height[right]) × (right - left)`
- Always move the **smaller** height pointer inward
  - Moving the taller side can only decrease or keep width same — not helpful
  - Moving the shorter side gives a chance for a taller wall → might increase area
- Never move both at once

### 🔍 Visualization
```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
          ↑                          ↑
        left=0                    right=8
  area = min(1,7) × 8 = 8  → move left (smaller)
          
             ↑                     ↑
           left=1               right=8
  area = min(8,7) × 7 = 49 ✅  → update max
```

### ✍️ Solution
```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0, right = height.length - 1;
        int maxWater = 0;

        while (left < right) {
            int water = Math.min(height[left], height[right]) * (right - left);
            maxWater = Math.max(maxWater, water);

            if (height[left] < height[right]) left++;
            else                              right--;
        }
        return maxWater;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 7️⃣ Reverse String
🔗 [LeetCode #344](https://leetcode.com/problems/reverse-string/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers – Swap**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `char[] s` (modify in-place) |
| **Output** | `void` — array reversed in-place |

### 💡 Examples
```
Input:  s = ['h','e','l','l','o']
Output:      ['o','l','l','e','h']

Input:  s = ['H','a','n','n','a','h']
Output:      ['h','a','n','n','a','H']
```

### 🔑 Key Points to Remember
- Classic swap while `left < right`
- No extra space — swap in-place
- Simplest two-pointer problem — good warmup

### ✍️ Solution
```java
class Solution {
    public void reverseString(char[] s) {
        int left = 0, right = s.length - 1;
        while (left < right) {
            char temp = s[left];
            s[left]  = s[right];
            s[right] = temp;
            left++;
            right--;
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

## 8️⃣ Squares of a Sorted Array
🔗 [LeetCode #977](https://leetcode.com/problems/squares-of-a-sorted-array/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers – Fill Result from End**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` sorted in non-decreasing order (may have negatives) |
| **Output** | `int[]` — squares of each number sorted in non-decreasing order |

### 💡 Examples
```
Input:  nums = [-4, -1, 0, 3, 10]
Output: [0, 1, 9, 16, 100]

Input:  nums = [-7, -3, 2, 3, 11]
Output: [4, 9, 9, 49, 121]
```

### 🔑 Key Points to Remember
- After squaring, largest values are at the **two ends** (most negative or most positive)
- Compare `|left|` vs `|right|`, place larger square at end of result array
- Fill result array **from right to left** using an index pointer `pos`
- This avoids sorting after squaring (O(n log n) → O(n))

### 🔍 Visualization
```
nums = [-4, -1, 0, 3, 10]
         ↑               ↑
        left            right
  sq(-4)=16, sq(10)=100 → 100 is bigger → result[4]=100, right--

         ↑          ↑
       left        right
  sq(-4)=16, sq(3)=9  → 16 is bigger  → result[3]=16,  left++
```

### ✍️ Solution
```java
class Solution {
    public int[] sortedSquares(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];
        int left = 0, right = n - 1, pos = n - 1;

        while (left <= right) {
            int leftSq  = nums[left]  * nums[left];
            int rightSq = nums[right] * nums[right];

            if (leftSq > rightSq) {
                result[pos--] = leftSq;
                left++;
            } else {
                result[pos--] = rightSq;
                right--;
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
| Space | O(n) — output array |

---

## ── TYPE 2: SLOW & FAST POINTER ─────────────────────────

## 2️⃣ Remove Duplicates from Sorted Array
🔗 [LeetCode #26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) &nbsp;|&nbsp; 🟢 Pattern: **Slow/Fast – Overwrite Unique In-place**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` sorted in non-decreasing order |
| **Output** | `int` — count `k` of unique elements; first `k` elements of `nums` are the unique values |

### 💡 Examples
```
Input:  nums = [1, 1, 2]
Output: 2,  nums = [1, 2, _]

Input:  nums = [0,0,1,1,1,2,2,3,3,4]
Output: 5,  nums = [0, 1, 2, 3, 4, _, _, _, _, _]
```

### 🔑 Key Points to Remember
- `slow` = where the next unique element should go
- `fast` scans ahead for new unique values
- When `nums[fast] != nums[slow]` → copy to `slow+1`, advance `slow`
- Return `slow + 1` as the count

### 🔍 Visualization
```
nums = [1, 1, 2]
        ↑  ↑
       slow fast
  nums[fast]==nums[slow] → fast++

        ↑     ↑
       slow  fast
  nums[fast]!=nums[slow] → slow++, nums[slow]=nums[fast]
             ↑
           slow=fast → done, return slow+1 = 2
```

### ✍️ Solution
```java
class Solution {
    public int removeDuplicates(int[] nums) {
        int slow = 0;
        for (int fast = 1; fast < nums.length; fast++) {
            if (nums[fast] != nums[slow]) {
                slow++;
                nums[slow] = nums[fast];
            }
        }
        return slow + 1;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 1️⃣3️⃣ Remove Element
🔗 [LeetCode #27](https://leetcode.com/problems/remove-element/) &nbsp;|&nbsp; 🟢 Pattern: **Slow/Fast – Overwrite Unwanted Values**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int val` |
| **Output** | `int` — count `k` of elements not equal to `val`; first `k` elements of `nums` are those values |

### 💡 Examples
```
Input:  nums = [3,2,2,3],  val = 3
Output: 2,  nums = [2, 2, _, _]

Input:  nums = [0,1,2,2,3,0,4,2],  val = 2
Output: 5,  nums = [0,1,3,0,4, _, _, _]
```

### 🔑 Key Points to Remember
- Same pattern as Remove Duplicates but condition is `nums[fast] != val`
- `slow` tracks where to write the next valid element
- Order of remaining elements doesn't need to be preserved (overwrite freely)

### ✍️ Solution
```java
class Solution {
    public int removeElement(int[] nums, int val) {
        int slow = 0;
        for (int fast = 0; fast < nums.length; fast++) {
            if (nums[fast] != val) {
                nums[slow] = nums[fast];
                slow++;
            }
        }
        return slow;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 🔟 Move Zeroes
🔗 [LeetCode #283](https://leetcode.com/problems/move-zeroes/) &nbsp;|&nbsp; 🟢 Pattern: **Slow/Fast – Move Non-Zero Forward**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (modify in-place) |
| **Output** | `void` — all zeroes moved to end; non-zero order maintained |

### 💡 Examples
```
Input:  nums = [0, 1, 0, 3, 12]
Output:        [1, 3, 12, 0, 0]

Input:  nums = [0]
Output:        [0]
```

### 🔑 Key Points to Remember
- First pass: write all non-zero elements using `slow` pointer
- Second pass: fill from `slow` to end with zeros
- Maintains relative order of non-zero elements

### ✍️ Solution
```java
class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        for (int fast = 0; fast < nums.length; fast++) {
            if (nums[fast] != 0) nums[slow++] = nums[fast];
        }
        while (slow < nums.length) nums[slow++] = 0;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## ── TYPE 3: SORTING + TWO POINTER ──────────────────────

## 5️⃣ 3Sum
🔗 [LeetCode #15](https://leetcode.com/problems/3sum/) &nbsp;|&nbsp; 🟢 Pattern: **Sort + Two Pointer – Fix One, Solve 2Sum**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` |
| **Output** | `List<List<Integer>>` — all unique triplets that sum to zero |
| **Constraint** | No duplicate triplets in result |

### 💡 Examples
```
Input:  nums = [-1, 0, 1, 2, -1, -4]
Output: [[-1,-1,2],[-1,0,1]]

Input:  nums = [0, 0, 0]
Output: [[0,0,0]]

Input:  nums = [1, 2, -2, -1]
Output: []
```

### 🔑 Key Points to Remember
- Sort the array first → enables two-pointer + easy duplicate skipping
- Fix `nums[i]`, then find pair `nums[left] + nums[right] == -nums[i]`
- Skip duplicates for `i`: `if (i > 0 && nums[i] == nums[i-1]) continue`
- Skip duplicates for `left/right` after adding a result
- Early exit: if `nums[i] > 0` → no triplet possible (all remaining are positive)

### 🔍 Visualization
```
nums = [-4, -1, -1, 0, 1, 2]  (after sort)
         ↑
         i=0, target = 0-(-4) = 4
              ↑            ↑
             left          right   → -1+2=1 < 4 → left++
                  ↑        ↑       → -1+2=1 < 4 → left++
                      ↑    ↑       → 0+2=2 < 4  → left++ (cross) done

i=1, nums[1]=-1, target=1
                  ↑        ↑       → 0+2=2 > 1  → right--
                  ↑     ↑          → 0+1=1 ✅   → add [-1,0,1]
```

### ✍️ Solution
```java
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();

        for (int i = 0; i < nums.length - 2; i++) {
            if (nums[i] > 0) break;                         // optimization
            if (i > 0 && nums[i] == nums[i-1]) continue;   // skip duplicate i

            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    while (left < right && nums[left]  == nums[left+1])  left++;   // skip dup left
                    while (left < right && nums[right] == nums[right-1]) right--;  // skip dup right
                    left++; right--;
                } else if (sum < 0) left++;
                else                right--;
            }
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n²) — O(n log n) sort + O(n²) scan |
| Space | O(1) extra |

---

## 1️⃣2️⃣ 3Sum Closest
🔗 [LeetCode #16](https://leetcode.com/problems/3sum-closest/) &nbsp;|&nbsp; 🟢 Pattern: **Sort + Two Pointer – Minimize Diff**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int target` |
| **Output** | `int` — sum of three integers closest to `target` |
| **Constraint** | Exactly one answer guaranteed |

### 💡 Examples
```
Input:  nums = [-1, 2, 1, -4],  target = 1
Output: 2   ← (-1+2+1)=2, closest to 1

Input:  nums = [0, 0, 0],  target = 1
Output: 0
```

### 🔑 Key Points to Remember
- Same structure as 3Sum — sort first, fix `i`, two-pointer for rest
- Track `closest` = the running best sum found
- `Math.abs(sum - target) < Math.abs(closest - target)` → update closest
- If `sum == target` → return immediately (can't get closer)

### ✍️ Solution
```java
class Solution {
    public int threeSumClosest(int[] nums, int target) {
        Arrays.sort(nums);
        int closest = nums[0] + nums[1] + nums[2];

        for (int i = 0; i < nums.length - 2; i++) {
            int left = i + 1, right = nums.length - 1;
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (Math.abs(sum - target) < Math.abs(closest - target)) {
                    closest = sum;
                }
                if      (sum == target) return sum;
                else if (sum < target)  left++;
                else                    right--;
            }
        }
        return closest;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n²) |
| Space | O(1) |

---

## 1️⃣1️⃣ 4Sum
🔗 [LeetCode #18](https://leetcode.com/problems/4sum/) &nbsp;|&nbsp; 🟢 Pattern: **Sort + Two Pointer – Extend 3Sum**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums`, `int target` |
| **Output** | `List<List<Integer>>` — all unique quadruplets summing to `target` |

### 💡 Examples
```
Input:  nums = [1,0,-1,0,-2,2],  target = 0
Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]

Input:  nums = [2,2,2,2,2],  target = 8
Output: [[2,2,2,2]]
```

### 🔑 Key Points to Remember
- 4Sum = fix two indices (`i` and `j`), then two-pointer for remaining two
- Two layers of duplicate skipping: for `i` and for `j`
- Use `long` for sum to avoid integer overflow: `(long)nums[i] + nums[j] + nums[l] + nums[r]`
- Same duplicate skip pattern as 3Sum after finding a valid quad

### ✍️ Solution
```java
class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        List<List<Integer>> result = new ArrayList<>();

        for (int i = 0; i < nums.length - 3; i++) {
            if (i > 0 && nums[i] == nums[i-1]) continue;

            for (int j = i + 1; j < nums.length - 2; j++) {
                if (j > i + 1 && nums[j] == nums[j-1]) continue;

                int left = j + 1, right = nums.length - 1;
                while (left < right) {
                    long sum = (long)nums[i] + nums[j] + nums[left] + nums[right];
                    if (sum == target) {
                        result.add(Arrays.asList(nums[i], nums[j], nums[left], nums[right]));
                        while (left < right && nums[left]  == nums[left+1])  left++;
                        while (left < right && nums[right] == nums[right-1]) right--;
                        left++; right--;
                    } else if (sum < target) left++;
                    else                     right--;
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
| Time | O(n³) |
| Space | O(1) extra |

---

## ── TYPE 4: EXPAND AROUND CENTER ───────────────────────

## 1️⃣8️⃣ Longest Palindromic Substring
🔗 [LeetCode #5](https://leetcode.com/problems/longest-palindromic-substring/) &nbsp;|&nbsp; 🟢 Pattern: **Expand Around Center**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` |
| **Output** | `String` — the longest palindromic substring |

### 💡 Examples
```
Input:  s = "babad"
Output: "bab"  (or "aba" — both valid)

Input:  s = "cbbd"
Output: "bb"

Input:  s = "racecar"
Output: "racecar"
```

### 🔑 Key Points to Remember
- Every palindrome expands from a **center** (single char or pair of chars)
- Two cases for center:
  - **Odd length**: center = single char → expand(`i, i`)
  - **Even length**: center = pair → expand(`i, i+1`)
- For each index, call both and take the longer result
- Extract result using `s.substring(left + 1, right)` after expansion stops

### 🔍 Visualization
```
s = "babad"

Center at i=0 ('b'):  odd→"b"
Center at i=1 ('a'):  odd→"bab"  ← longest so far
Center at i=2 ('b'):  odd→"aba"
Center at i=3 ('a'):  odd→"a"
Center at i=0,1 pair: even→"" (b≠a)
Center at i=1,2 pair: even→"" (a≠b)
```

### ✍️ Solution
```java
class Solution {
    private String expand(String s, int left, int right) {
        while (left >= 0 && right < s.length()
               && s.charAt(left) == s.charAt(right)) {
            left--;
            right++;
        }
        return s.substring(left + 1, right); // window after last valid expansion
    }

    public String longestPalindrome(String s) {
        String result = "";
        for (int i = 0; i < s.length(); i++) {
            String odd  = expand(s, i, i);       // odd-length palindromes
            String even = expand(s, i, i + 1);   // even-length palindromes
            if (odd.length()  > result.length()) result = odd;
            if (even.length() > result.length()) result = even;
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n²) |
| Space | O(1) |

---

## ── TYPE 5: THREE POINTERS ──────────────────────────────

## 1️⃣4️⃣ Sort Colors (Dutch National Flag)
🔗 [LeetCode #75](https://leetcode.com/problems/sort-colors/) &nbsp;|&nbsp; 🟢 Pattern: **3 Pointers – Dutch National Flag**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` — only values 0, 1, 2 |
| **Output** | `void` — sorted in-place: all 0s, then 1s, then 2s |
| **Constraint** | O(n) time, O(1) space — single pass |

### 💡 Examples
```
Input:  nums = [2, 0, 2, 1, 1, 0]
Output:        [0, 0, 1, 1, 2, 2]

Input:  nums = [2, 0, 1]
Output:        [0, 1, 2]
```

### 🔑 Key Points to Remember
- **3 pointers**: `low` (0s go here), `mid` (scanner), `high` (2s go here)
- `nums[mid] == 0` → swap with `low`, both `low++` and `mid++`
- `nums[mid] == 1` → it's in place → `mid++` only
- `nums[mid] == 2` → swap with `high`, `high--` only (don't move `mid`!)
  - After swapping with `high`, the swapped-in element hasn't been checked yet
- Loop continues while `mid <= high`

### 🔍 Visualization
```
[2, 0, 2, 1, 1, 0]
 ↑              ↑
low=0  mid=0  high=5

mid=0: nums[0]=2 → swap(0,5) → [0,0,2,1,1,2], high=4
mid=0: nums[0]=0 → swap(0,0) → [0,0,2,1,1,2], low=1, mid=1
mid=1: nums[1]=0 → swap(1,1) → [0,0,2,1,1,2], low=2, mid=2
mid=2: nums[2]=2 → swap(2,4) → [0,0,1,1,2,2], high=3
mid=2: nums[2]=1 → mid=3
mid=3: nums[3]=1 → mid=4
mid(4) > high(3) → DONE ✅
```

### ✍️ Solution
```java
class Solution {
    public void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;

        while (mid <= high) {
            if (nums[mid] == 0) {
                int temp = nums[low]; nums[low] = nums[mid]; nums[mid] = temp;
                low++; mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                int temp = nums[mid]; nums[mid] = nums[high]; nums[high] = temp;
                high--;   // ← don't mid++ here! newly swapped element unchecked
            }
        }
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) — single pass |
| Space | O(1) |

---

## ── SPECIAL PATTERNS ─────────────────────────────────────

## 6️⃣ Trapping Rain Water
🔗 [LeetCode #42](https://leetcode.com/problems/trapping-rain-water/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers + Max Tracking**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] height` — elevation map |
| **Output** | `int` — total units of rain water trapped |

### 💡 Examples
```
Input:  height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6

Input:  height = [4,2,0,3,2,5]
Output: 9
```

### 🔑 Key Points to Remember
- Water at position `i` = `min(maxLeft, maxRight) - height[i]`
- Two-pointer approach: maintain `leftMax` and `rightMax` as you go
- If `height[left] < height[right]` → process left side (leftMax determines water)
- If `height[right] <= height[left]` → process right side
- Water trapped at a bar = `max(0, maxSide - height[i])`

### 🔍 Visualization
```
height = [4, 2, 0, 3, 2, 5]

       █              █
       █     █  █     █
       █  █  █  █  █  █
       4  2  0  3  2  5

Water above index 1: min(4,5)-2 = 2
Water above index 2: min(4,5)-0 = 4
Water above index 4: min(4,5)-2 = 2
             Total = 9 ✅
```

### ✍️ Solution
```java
class Solution {
    public int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0;
        int water = 0;

        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else water += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else water += rightMax - height[right];
                right--;
            }
        }
        return water;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 1️⃣5️⃣ Valid Palindrome II
🔗 [LeetCode #680](https://leetcode.com/problems/valid-palindrome-ii/) &nbsp;|&nbsp; 🟢 Pattern: **Opposite Pointers + Skip One**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` (lowercase, no spaces) |
| **Output** | `boolean` — can we make it a palindrome by removing **at most one** character? |

### 💡 Examples
```
Input:  s = "aba"
Output: true  ← already palindrome

Input:  s = "abca"
Output: true  ← remove 'c' → "aba"

Input:  s = "abc"
Output: false
```

### 🔑 Key Points to Remember
- Normal palindrome check until a mismatch
- On mismatch: try **skipping left** OR **skipping right**, check if either gives a palindrome
- Use a helper `isPalindrome(s, left, right)` for the sub-check
- Only one skip allowed — don't recurse

### ✍️ Solution
```java
class Solution {
    private boolean isPalin(String s, int l, int r) {
        while (l < r) {
            if (s.charAt(l) != s.charAt(r)) return false;
            l++; r--;
        }
        return true;
    }

    public boolean validPalindrome(String s) {
        int left = 0, right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) {
                // try skipping left char OR right char
                return isPalin(s, left + 1, right) || isPalin(s, left, right - 1);
            }
            left++; right--;
        }
        return true;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n) |
| Space | O(1) |

---

## 1️⃣6️⃣ Backspace String Compare
🔗 [LeetCode #844](https://leetcode.com/problems/backspace-string-compare/) &nbsp;|&nbsp; 🟢 Pattern: **Reverse Two Pointers – Traverse from End**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s`, `String t` (may contain `#` = backspace) |
| **Output** | `boolean` — `true` if both strings are equal after processing backspaces |

### 💡 Examples
```
Input:  s = "ab#c",  t = "ad#c"
Output: true   ← "ac" == "ac"

Input:  s = "ab##",  t = "c#d#"
Output: true   ← "" == ""

Input:  s = "a#c",   t = "b"
Output: false  ← "c" != "b"
```

### 🔑 Key Points to Remember
- Traverse **from right to left** — process backspaces as you encounter them
- Count skips: `skip++` when `#` seen, skip next real char when `skip > 0`
- Compare characters from both strings simultaneously
- O(1) space solution (vs O(n) if you build new strings)

### ✍️ Solution
```java
class Solution {
    public boolean backspaceCompare(String s, String t) {
        int i = s.length() - 1, j = t.length() - 1;
        int skipS = 0, skipT = 0;

        while (i >= 0 || j >= 0) {
            while (i >= 0) {
                if (s.charAt(i) == '#') { skipS++; i--; }
                else if (skipS > 0)     { skipS--; i--; }
                else break;
            }
            while (j >= 0) {
                if (t.charAt(j) == '#') { skipT++; j--; }
                else if (skipT > 0)     { skipT--; j--; }
                else break;
            }
            if (i >= 0 && j >= 0 && s.charAt(i) != t.charAt(j)) return false;
            if ((i >= 0) != (j >= 0)) return false;  // one exhausted, other not
            i--; j--;
        }
        return true;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n + m) |
| Space | O(1) |

---

## 1️⃣7️⃣ Boats to Save People
🔗 [LeetCode #881](https://leetcode.com/problems/boats-to-save-people/) &nbsp;|&nbsp; 🟢 Pattern: **Greedy + Opposite Pointers**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] people` (weights), `int limit` (max weight per boat) |
| **Output** | `int` — minimum number of boats to carry everyone |
| **Constraint** | Each boat carries at most 2 people |

### 💡 Examples
```
Input:  people = [1, 2],  limit = 3
Output: 1   ← one boat carries both

Input:  people = [3, 2, 2, 1],  limit = 3
Output: 3   ← [1,2], [2], [3]

Input:  people = [3, 5, 3, 4],  limit = 5
Output: 4   ← each person needs own boat
```

### 🔑 Key Points to Remember
- Sort first, then greedily pair lightest + heaviest
- If `people[left] + people[right] <= limit` → pair them → `left++, right--, boats++`
- Otherwise → heaviest must go alone → `right--, boats++`
- Each iteration always decrements `right` (boat always taken by heaviest)

### ✍️ Solution
```java
class Solution {
    public int numRescueBoats(int[] people, int limit) {
        Arrays.sort(people);
        int left = 0, right = people.length - 1;
        int boats = 0;

        while (left <= right) {
            if (people[left] + people[right] <= limit) left++;  // pair them
            right--;   // heaviest always takes a boat
            boats++;
        }
        return boats;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n log n) — sort dominates |
| Space | O(1) |

---

## 9️⃣ Partition Labels
🔗 [LeetCode #763](https://leetcode.com/problems/partition-labels/) &nbsp;|&nbsp; 🟢 Pattern: **Greedy + Pointer – Track Last Index**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `String s` (lowercase letters) |
| **Output** | `List<Integer>` — sizes of each partition such that each letter appears in at most one part |

### 💡 Examples
```
Input:  s = "ababcbacadefegdehijhklij"
Output: [9, 7, 8]
  ← "ababcbaca" | "defegde" | "hijhklij"

Input:  s = "eccbbbbdec"
Output: [10]
```

### 🔑 Key Points to Remember
- Pre-compute `lastIndex[c]` = last occurrence of each character
- Traverse with a `windowEnd` pointer that expands to the furthest last index seen
- When current index `i == windowEnd` → partition ends here
- Partition size = `i - start + 1`, then set `start = i + 1`

### ✍️ Solution
```java
class Solution {
    public List<Integer> partitionLabels(String s) {
        int[] last = new int[26];
        for (int i = 0; i < s.length(); i++) last[s.charAt(i) - 'a'] = i;

        List<Integer> result = new ArrayList<>();
        int start = 0, windowEnd = 0;

        for (int i = 0; i < s.length(); i++) {
            windowEnd = Math.max(windowEnd, last[s.charAt(i) - 'a']);
            if (i == windowEnd) {             // partition boundary reached
                result.add(i - start + 1);
                start = i + 1;
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

## 🧠 Pattern Cheat Sheet

| Pattern | When to Use | Signal Words |
|---------|------------|--------------|
| **Opposite Pointers** | Sorted array, pair sum, palindrome check | "sorted", "pair", "palindrome", "two ends" |
| **Slow / Fast Pointer** | Remove/overwrite in-place, filter values | "in-place", "remove", "duplicates", "move" |
| **Sort + Two Pointer** | Triplet/quadruplet sum, minimize/maximize | "3Sum", "4Sum", "closest", "unique triplets" |
| **Expand Around Center** | Find palindromic substrings | "palindromic substring", "expand" |
| **3 Pointers (DNF)** | Partition array into 3 sections | "sort colors", "0,1,2", "Dutch flag" |
| **Greedy + Two Pointer** | Pairing elements for optimal result | "pair lightest+heaviest", "partition labels" |
| **Reverse Pointer** | Process string from end (backspace, etc.) | "#", "backspace", "process from right" |

---

## ⚡ Quick Decision Guide

```
Is array sorted?
    AND need pair/triplet sum?  → Opposite Pointers (Two Sum II / 3Sum)
    AND need in-place modify?   → Slow/Fast Pointer

Is it a palindrome problem?
    Check whole string?         → Opposite Pointers
    Find longest substring?     → Expand Around Center
    Allow one deletion?         → Opposite + isPalin() helper

Need to remove/overwrite?       → Slow/Fast (slow=write pos, fast=scanner)

Need to sort 0,1,2?             → Dutch National Flag (3 Pointers)

Pair smallest+largest greedily? → Sort + Opposite Pointers (Boats)

Partition by last occurrence?   → Greedy Pointer (Partition Labels)
```

---

## 🆚 Two Pointer vs Sliding Window

| | Two Pointer | Sliding Window |
|--|-------------|----------------|
| **Direction** | Often opposite (inward) | Always same direction (rightward) |
| **Window** | No fixed structure | Explicit start/end window |
| **Use case** | Pairs, sums, palindromes | Subarrays, substrings |
| **Shrink** | Move one pointer on condition | Shrink `start` while invalid |
| **Sorted needed?** | Often yes | Usually no |

---

*Last updated: March 2026*