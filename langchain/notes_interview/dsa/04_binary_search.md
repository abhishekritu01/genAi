# 🔍 LeetCode Binary Search – Revision Notes

## 🗺️ Legend
| Badge | Meaning |
|-------|---------|
| 🔴 | Confused on pattern — need to re-learn |
| 🟡 | Understand pattern — coding needs polish |
| 🟢 | Fully confident — safe zone |

---

## 🧠 Core Concept — What is Binary Search?

On a **sorted** (or monotonic) space, instead of scanning every element (O(n)),
cut the search space **in half** each step → **O(log n)**.

```
Array:  [1, 3, 5, 7, 9, 11, 13]
         ↑        ↑           ↑
        low      mid         high

mid too small → search RIGHT half
mid too large → search LEFT half
mid == target → FOUND ✅
```

---

## ⚠️ The #1 Bug — Getting the Template Right

There are **3 valid templates**. Pick ONE and stick to it.

### 🔹 Template 1 — Classic (find exact match)
```java
int low = 0, high = nums.length - 1;
while (low <= high) {                        // ← <= (includes single element)
    int mid = low + (high - low) / 2;        // ← avoids integer overflow
    if      (nums[mid] == target) return mid;
    else if (nums[mid] <  target) low  = mid + 1;
    else                          high = mid - 1;
}
return -1;  // not found
```

### 🔹 Template 2 — Find Left Boundary (first position)
```java
int low = 0, high = nums.length - 1;
int result = -1;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (nums[mid] >= target) {   // candidate — try to go further LEFT
        result = mid;
        high = mid - 1;
    } else {
        low = mid + 1;
    }
}
return result;
```

### 🔹 Template 3 — Find Right Boundary (last position)
```java
int low = 0, high = nums.length - 1;
int result = -1;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (nums[mid] <= target) {   // candidate — try to go further RIGHT
        result = mid;
        low = mid + 1;
    } else {
        high = mid - 1;
    }
}
return result;
```

### 🔹 Template 4 — Binary Search on Answer Space
```java
// Use when searching on a VALUE RANGE, not array index
int low = minPossibleAnswer, high = maxPossibleAnswer;
while (low <= high) {
    int mid = low + (high - low) / 2;
    if (canAchieve(mid)) {   // custom feasibility check
        result = mid;
        high = mid - 1;      // or low = mid + 1 depending on min/max
    } else {
        low = mid + 1;
    }
}
return result;
```

---

## 🎯 Five Types of Binary Search

| Type | Key Idea | Classic Problems |
|------|----------|-----------------|
| **1️⃣ Classic Search** | Find exact target index | Binary Search, Search in Rotated Array |
| **2️⃣ Left Boundary** | Find first occurrence / leftmost valid | First Bad Version, Search Insert Position |
| **3️⃣ Right Boundary** | Find last occurrence / rightmost valid | Find First & Last Position |
| **4️⃣ Answer Space (Minimise)** | BS on value range, minimise result | Koko Eating Bananas, Min Days to Make Bouquets |
| **5️⃣ Rotated / Modified** | Array not fully sorted | Search in Rotated, Find Min in Rotated |

---

## 📊 Progress Tracker

| # | Problem | Type | Pattern | Status |
|---|---------|------|---------|--------|
| 1 | [Binary Search](#1️⃣-binary-search) | Classic | Exact match | ⬜ |
| 2 | [Search Insert Position](#2️⃣-search-insert-position) | Left Boundary | First pos ≥ target | ⬜ |
| 3 | [First Bad Version](#3️⃣-first-bad-version) | Left Boundary | First true in F..FT..T | ⬜ |
| 4 | [Find First & Last Position](#4️⃣-find-first-and-last-position-of-element) | Left + Right Boundary | Two binary searches | ⬜ |
| 5 | [Search in Rotated Sorted Array](#5️⃣-search-in-rotated-sorted-array) | Rotated | Find sorted half | ⬜ |
| 6 | [Find Minimum in Rotated Array](#6️⃣-find-minimum-in-rotated-sorted-array) | Rotated | Locate rotation point | ⬜ |
| 7 | [Koko Eating Bananas](#7️⃣-koko-eating-bananas) | Answer Space | Minimise max speed | ⬜ |
| 8 | [Capacity to Ship Packages](#8️⃣-capacity-to-ship-packages-within-d-days) | Answer Space | Minimise capacity | ⬜ |
| 9 | [Find Peak Element](#9️⃣-find-peak-element) | Modified | Move toward higher side | ⬜ |
| 10 | [Search a 2D Matrix](#🔟-search-a-2d-matrix) | Classic | Treat matrix as flat array | ⬜ |
| 11 | [Time Based Key-Value Store](#1️⃣1️⃣-time-based-key-value-store) | Right Boundary | BS on timestamps | ⬜ |
| 12 | [Median of Two Sorted Arrays](#1️⃣2️⃣-median-of-two-sorted-arrays) | Hard | Binary search on partition | ⬜ |

---

## ── TYPE 1: CLASSIC SEARCH ──────────────────────────────

## 1️⃣ Binary Search
🔗 [LeetCode #704](https://leetcode.com/problems/binary-search/) &nbsp;|&nbsp; 🟢 Pattern: **Classic – Exact Match**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (sorted ascending, no duplicates), `int target` |
| **Output** | `int` — index of `target`, or `-1` if not found |

### 💡 Examples
```
Input:  nums = [-1, 0, 3, 5, 9, 12],  target = 9
Output: 4

Input:  nums = [-1, 0, 3, 5, 9, 12],  target = 2
Output: -1
```

### 🔑 Key Points to Remember
- `mid = low + (high - low) / 2` — never `(low + high) / 2` (overflow risk)
- `while (low <= high)` — the `=` handles the single-element case
- `low = mid + 1` / `high = mid - 1` — never `mid` alone (infinite loop risk)
- Loop ends → `low > high` → element not present → return `-1`

### 🔍 Dry Run
```
nums = [-1, 0, 3, 5, 9, 12],  target = 9
low=0, high=5

Step 1: mid=2, nums[2]=3  < 9 → low = 3
Step 2: mid=4, nums[4]=9 == 9 → return 4 ✅
```

### ✍️ Solution
```java
class Solution {
    public int search(int[] nums, int target) {
        int low = 0, high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if      (nums[mid] == target) return mid;
            else if (nums[mid] <  target) low  = mid + 1;
            else                          high = mid - 1;
        }
        return -1;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## 🔟 Search a 2D Matrix
🔗 [LeetCode #74](https://leetcode.com/problems/search-a-2d-matrix/) &nbsp;|&nbsp; 🟢 Pattern: **Classic – Treat Matrix as Flat Array**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[][] matrix` (each row sorted, first element of row > last of prev row), `int target` |
| **Output** | `boolean` — `true` if target exists in matrix |

### 💡 Examples
```
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]],  target = 3
Output: true

Input:  same matrix,  target = 13
Output: false
```

### 🔑 Key Points to Remember
- Treat the whole matrix as a **flat sorted array** of size `m × n`
- Convert flat index `mid` → 2D: `row = mid / n`, `col = mid % n`
- `low = 0`, `high = m * n - 1`
- Standard binary search after that

### 🔍 Visualization
```
[[1,  3,  5,  7],       Flat indices:
 [10, 11, 16, 20],      0  1  2  3
 [23, 30, 34, 60]]      4  5  6  7
                         8  9  10 11

mid=5 → row=5/4=1, col=5%4=1 → matrix[1][1] = 11
```

### ✍️ Solution
```java
class Solution {
    public boolean searchMatrix(int[][] matrix, int target) {
        int m = matrix.length, n = matrix[0].length;
        int low = 0, high = m * n - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int val = matrix[mid / n][mid % n];   // ← key conversion
            if      (val == target) return true;
            else if (val <  target) low  = mid + 1;
            else                    high = mid - 1;
        }
        return false;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log(m × n)) |
| Space | O(1) |

---

## ── TYPE 2 & 3: BOUNDARY SEARCH ────────────────────────

## 2️⃣ Search Insert Position
🔗 [LeetCode #35](https://leetcode.com/problems/search-insert-position/) &nbsp;|&nbsp; 🟢 Pattern: **Left Boundary – First Position ≥ Target**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (sorted, distinct), `int target` |
| **Output** | `int` — index of target if found, else index where it **would be inserted** |

### 💡 Examples
```
Input:  nums = [1, 3, 5, 6],  target = 5  → Output: 2  (found)
Input:  nums = [1, 3, 5, 6],  target = 2  → Output: 1  (insert between 1 and 3)
Input:  nums = [1, 3, 5, 6],  target = 7  → Output: 4  (insert at end)
Input:  nums = [1, 3, 5, 6],  target = 0  → Output: 0  (insert at start)
```

### 🔑 Key Points to Remember
- When loop ends, `low` = first index where `nums[low] >= target`
- This is naturally the **insert position**
- No special handling needed — just return `low` after the loop
- This is the **lower_bound** concept from C++ STL

### 🔍 Dry Run
```
nums = [1, 3, 5, 6],  target = 2
low=0, high=3

Step 1: mid=1, nums[1]=3 >= 2 → high = 0
Step 2: mid=0, nums[0]=1 <  2 → low  = 1
low(1) > high(0) → return low = 1 ✅
```

### ✍️ Solution
```java
class Solution {
    public int searchInsert(int[] nums, int target) {
        int low = 0, high = nums.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if      (nums[mid] == target) return mid;
            else if (nums[mid] <  target) low  = mid + 1;
            else                          high = mid - 1;
        }
        return low;   // ← insert position when not found
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## 3️⃣ First Bad Version
🔗 [LeetCode #278](https://leetcode.com/problems/first-bad-version/) &nbsp;|&nbsp; 🟢 Pattern: **Left Boundary – First True in F..FT..T**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int n` — total versions; API `isBadVersion(v)` returns bool |
| **Output** | `int` — first bad version number |
| **Constraint** | Once bad, all following are bad: `[good, good, ..., bad, bad, bad]` |

### 💡 Examples
```
Input:  n=5, bad=4  →  [F, F, F, T, T]
Output: 4

Input:  n=1, bad=1  →  [T]
Output: 1
```

### 🔑 Key Points to Remember
- Array shape: `[F, F, F, ..., T, T, T]` → find first `T`
- When `isBadVersion(mid) == true` → it might be the first, save it and go LEFT
- When `false` → go RIGHT
- This is the **classic left-boundary template** applied to an API

### 🔍 Visualization
```
Versions: 1  2  3  4  5
           F  F  F  T  T
                    ↑ ← first bad = 4

low=1, high=5
mid=3: isBad(3)=F → low=4
mid=4: isBad(4)=T → result=4, high=3
low(4) > high(3) → return 4 ✅
```

### ✍️ Solution
```java
public class Solution extends VersionControl {
    public int firstBadVersion(int n) {
        int low = 1, high = n;
        int result = n;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (isBadVersion(mid)) {
                result = mid;    // candidate, try to find earlier
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## 4️⃣ Find First and Last Position of Element
🔗 [LeetCode #34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) &nbsp;|&nbsp; 🟢 Pattern: **Left Boundary + Right Boundary**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (sorted, may have duplicates), `int target` |
| **Output** | `int[]` — `[firstIndex, lastIndex]` of target; `[-1,-1]` if not found |

### 💡 Examples
```
Input:  nums = [5,7,7,8,8,10],  target = 8
Output: [3, 4]

Input:  nums = [5,7,7,8,8,10],  target = 6
Output: [-1, -1]

Input:  nums = [],  target = 0
Output: [-1, -1]
```

### 🔑 Key Points to Remember
- Run **two separate binary searches** — one for first, one for last
- First occurrence: when match found → save and go **left** (`high = mid - 1`)
- Last occurrence: when match found → save and go **right** (`low = mid + 1`)
- If first occurrence is `-1` → target not present → return `[-1, -1]`

### ✍️ Solution
```java
class Solution {
    public int[] searchRange(int[] nums, int target) {
        return new int[]{findFirst(nums, target), findLast(nums, target)};
    }

    private int findFirst(int[] nums, int target) {
        int low = 0, high = nums.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) { result = mid; high = mid - 1; }  // go left
            else if (nums[mid] < target) low = mid + 1;
            else                         high = mid - 1;
        }
        return result;
    }

    private int findLast(int[] nums, int target) {
        int low = 0, high = nums.length - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) { result = mid; low = mid + 1; }   // go right
            else if (nums[mid] < target) low = mid + 1;
            else                         high = mid - 1;
        }
        return result;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) — two passes |
| Space | O(1) |

---

## ── TYPE 4: ANSWER SPACE (BS ON VALUE) ─────────────────

## 7️⃣ Koko Eating Bananas
🔗 [LeetCode #875](https://leetcode.com/problems/koko-eating-bananas/) &nbsp;|&nbsp; 🟢 Pattern: **Answer Space – Minimise Speed**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] piles` (bananas per pile), `int h` (hours available) |
| **Output** | `int` — minimum eating speed `k` (bananas/hour) to finish all piles in `h` hours |

### 💡 Examples
```
Input:  piles = [3, 6, 7, 11],  h = 8
Output: 4
  ← at speed 4: ceil(3/4)+ceil(6/4)+ceil(7/4)+ceil(11/4) = 1+2+2+3 = 8 hours ✅

Input:  piles = [30, 11, 23, 4, 20],  h = 5
Output: 30
```

### 🔑 Key Points to Remember
- Search space for `k`: `[1 ... max(piles)]`
  - Minimum speed = 1 (must eat at least 1/hour)
  - Maximum speed = max pile (eating faster doesn't help)
- For a given speed `k`: hours needed = `sum of ceil(pile / k)` for each pile
- Use `Math.ceil(pile / k)` = `(pile + k - 1) / k` in integer math
- **Monotonic**: higher `k` → fewer hours → binary search works
- If `canFinish(mid)` → valid candidate → try smaller → `high = mid - 1`

### 🔍 Visualization
```
piles = [3, 6, 7, 11],  h = 8
Search space: k = [1 ... 11]

k=6: hours = 1+1+2+2=6 ≤ 8  ✅ → go left (try smaller)
k=3: hours = 1+2+3+4=10 > 8 ❌ → go right
k=4: hours = 1+2+2+3=8  ≤ 8 ✅ → go left
k=3: already checked → done

Answer = 4 ✅
```

### ✍️ Solution
```java
class Solution {
    public int minEatingSpeed(int[] piles, int h) {
        int low = 1, high = 0;
        for (int p : piles) high = Math.max(high, p);  // max pile

        int result = high;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canFinish(piles, mid, h)) {
                result = mid;       // valid — try slower
                high = mid - 1;
            } else {
                low = mid + 1;      // too slow — go faster
            }
        }
        return result;
    }

    private boolean canFinish(int[] piles, int speed, int h) {
        int hours = 0;
        for (int pile : piles) {
            hours += (pile + speed - 1) / speed;  // ceil(pile / speed)
        }
        return hours <= h;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n log m) — m = max pile |
| Space | O(1) |

---

## 8️⃣ Capacity to Ship Packages Within D Days
🔗 [LeetCode #1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) &nbsp;|&nbsp; 🟢 Pattern: **Answer Space – Minimise Capacity**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] weights`, `int days` |
| **Output** | `int` — minimum ship capacity to ship all packages in `days` days (in order) |

### 💡 Examples
```
Input:  weights = [1,2,3,4,5,6,7,8,9,10],  days = 5
Output: 15
  ← [1-5], [6-7], [8], [9], [10] — 5 days ✅

Input:  weights = [3,2,2,4,1,4],  days = 3
Output: 6
```

### 🔑 Key Points to Remember
- Search space: `[max(weights) ... sum(weights)]`
  - Minimum = max single weight (must carry heaviest package)
  - Maximum = sum of all (ship everything in 1 day)
- For a given capacity `cap`: simulate days needed greedily
- **Same pattern as Koko**: binary search on answer, check feasibility
- If `canShip(mid, days)` → valid, try smaller → `high = mid - 1`

### ✍️ Solution
```java
class Solution {
    public int shipWithinDays(int[] weights, int days) {
        int low = 0, high = 0;
        for (int w : weights) {
            low  = Math.max(low, w);   // must carry heaviest
            high += w;                  // max = ship all at once
        }

        int result = high;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (canShip(weights, mid, days)) {
                result = mid;
                high = mid - 1;
            } else {
                low = mid + 1;
            }
        }
        return result;
    }

    private boolean canShip(int[] weights, int cap, int days) {
        int daysNeeded = 1, currentLoad = 0;
        for (int w : weights) {
            if (currentLoad + w > cap) {
                daysNeeded++;
                currentLoad = 0;
            }
            currentLoad += w;
        }
        return daysNeeded <= days;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(n log(sum)) |
| Space | O(1) |

---

## ── TYPE 5: ROTATED / MODIFIED ARRAY ───────────────────

## 5️⃣ Search in Rotated Sorted Array
🔗 [LeetCode #33](https://leetcode.com/problems/search-in-rotated-sorted-array/) &nbsp;|&nbsp; 🟢 Pattern: **Rotated – Find Sorted Half**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (sorted, then rotated at some pivot; no duplicates), `int target` |
| **Output** | `int` — index of target, or `-1` |

### 💡 Examples
```
Input:  nums = [4,5,6,7,0,1,2],  target = 0
Output: 4

Input:  nums = [4,5,6,7,0,1,2],  target = 3
Output: -1

Input:  nums = [1],  target = 0
Output: -1
```

### 🔑 Key Points to Remember
- After rotation, **one half is always sorted** — identify which one
- `if nums[low] <= nums[mid]` → **left half is sorted**
  - Check if target is in `[nums[low], nums[mid]]` → search left, else right
- Else → **right half is sorted**
  - Check if target is in `[nums[mid], nums[high]]` → search right, else left
- One comparison tells you which half to trust

### 🔍 Visualization
```
[4, 5, 6, 7, 0, 1, 2],  target = 0
 ↑        ↑           ↑
low=0    mid=3       high=6

nums[low]=4 <= nums[mid]=7 → LEFT half [4..7] is sorted
target=0 NOT in [4,7] → search RIGHT → low = mid+1 = 4

[0, 1, 2]
 ↑  ↑   ↑
lo  mid  hi

nums[low]=0 <= nums[mid]=1 → LEFT half [0..1] sorted
target=0 IN [0,1] → search LEFT → high = mid-1 = 4

mid=4, nums[4]=0 == target → return 4 ✅
```

### ✍️ Solution
```java
class Solution {
    public int search(int[] nums, int target) {
        int low = 0, high = nums.length - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] == target) return mid;

            if (nums[low] <= nums[mid]) {           // LEFT half is sorted
                if (nums[low] <= target && target < nums[mid]) high = mid - 1;
                else                                            low  = mid + 1;
            } else {                                // RIGHT half is sorted
                if (nums[mid] < target && target <= nums[high]) low  = mid + 1;
                else                                             high = mid - 1;
            }
        }
        return -1;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## 6️⃣ Find Minimum in Rotated Sorted Array
🔗 [LeetCode #153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) &nbsp;|&nbsp; 🟢 Pattern: **Rotated – Locate Rotation Point**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (sorted then rotated, no duplicates) |
| **Output** | `int` — minimum element |

### 💡 Examples
```
Input:  nums = [3, 4, 5, 1, 2]
Output: 1   ← rotated at index 3

Input:  nums = [4, 5, 6, 7, 0, 1, 2]
Output: 0

Input:  nums = [11, 13, 15, 17]
Output: 11  ← not rotated
```

### 🔑 Key Points to Remember
- Minimum is always at the **rotation point** (start of the smaller part)
- If `nums[mid] > nums[high]` → min is in **right half** → `low = mid + 1`
- If `nums[mid] <= nums[high]` → min is in **left half (including mid)** → `high = mid`
- `high = mid` (not `mid - 1`) because `mid` itself could be the minimum
- Loop ends when `low == high` → that's the minimum

### 🔍 Visualization
```
[4, 5, 6, 7, 0, 1, 2]
             ↑ ← minimum is here

low=0, high=6, mid=3: nums[3]=7 > nums[6]=2 → min in RIGHT → low=4
low=4, high=6, mid=5: nums[5]=1 ≤ nums[6]=2 → min in LEFT  → high=5
low=4, high=5, mid=4: nums[4]=0 ≤ nums[5]=1 → min in LEFT  → high=4
low==high==4 → return nums[4] = 0 ✅
```

### ✍️ Solution
```java
class Solution {
    public int findMin(int[] nums) {
        int low = 0, high = nums.length - 1;

        while (low < high) {                      // ← strict < (stop at single element)
            int mid = low + (high - low) / 2;
            if (nums[mid] > nums[high]) low  = mid + 1;  // min in right half
            else                        high = mid;       // min in left half (mid included)
        }
        return nums[low];
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## ── SPECIAL PATTERNS ─────────────────────────────────────

## 9️⃣ Find Peak Element
🔗 [LeetCode #162](https://leetcode.com/problems/find-peak-element/) &nbsp;|&nbsp; 🟢 Pattern: **Modified – Move Toward Higher Neighbor**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums` (adjacent elements are not equal) |
| **Output** | `int` — index of any peak element (`nums[i] > nums[i-1]` and `nums[i] > nums[i+1]`) |
| **Constraint** | `nums[-1] = nums[n] = -∞` (boundaries count as valleys) |

### 💡 Examples
```
Input:  nums = [1, 2, 3, 1]
Output: 2   ← nums[2]=3 is peak

Input:  nums = [1, 2, 1, 3, 5, 6, 4]
Output: 1 or 5   ← both valid peaks
```

### 🔑 Key Points to Remember
- We don't need THE peak — just ANY peak
- If `nums[mid] < nums[mid+1]` → slope going UP on right → a peak exists on the right → `low = mid + 1`
- If `nums[mid] > nums[mid+1]` → slope going DOWN → a peak exists on the left (including mid) → `high = mid`
- Use `while (low < high)` — stops when converged to a single element (the peak)

### ✍️ Solution
```java
class Solution {
    public int findPeakElement(int[] nums) {
        int low = 0, high = nums.length - 1;

        while (low < high) {
            int mid = low + (high - low) / 2;
            if (nums[mid] < nums[mid + 1]) low  = mid + 1;  // go right (uphill)
            else                            high = mid;       // go left (or mid is peak)
        }
        return low;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log n) |
| Space | O(1) |

---

## 1️⃣1️⃣ Time Based Key-Value Store
🔗 [LeetCode #981](https://leetcode.com/problems/time-based-key-value-store/) &nbsp;|&nbsp; 🟢 Pattern: **Right Boundary – BS on Timestamps**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `set(key, value, timestamp)` and `get(key, timestamp)` operations |
| **Output** | `String` — value at largest timestamp ≤ given timestamp; `""` if none |
| **Constraint** | timestamps in `set` are strictly increasing |

### 💡 Examples
```
set("foo", "bar", 1)
set("foo", "bar2", 4)
get("foo", 4) → "bar2"   ← exact match at t=4
get("foo", 5) → "bar2"   ← largest t ≤ 5 is t=4
get("foo", 3) → "bar"    ← largest t ≤ 3 is t=1
get("foo", 0) → ""       ← no timestamp ≤ 0
```

### 🔑 Key Points to Remember
- Store: `Map<String, List<int[], String>>` or `Map<String, List<Pair<timestamp, value>>>`
- For `get`: binary search the list for **largest timestamp ≤ given timestamp** → Right Boundary
- Timestamps are sorted (inserted in order) → binary search is valid
- If `timestamps[mid] <= target` → valid candidate, go right → `low = mid + 1`

### ✍️ Solution
```java
class TimeMap {
    private Map<String, List<int[]>> timeMap;   // key → list of [timestamp, valueIndex]
    private Map<String, List<String>> valMap;

    public TimeMap() {
        timeMap = new HashMap<>();
        valMap  = new HashMap<>();
    }

    public void set(String key, String value, int timestamp) {
        timeMap.computeIfAbsent(key, k -> new ArrayList<>()).add(new int[]{timestamp});
        valMap.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }

    public String get(String key, int timestamp) {
        if (!timeMap.containsKey(key)) return "";
        List<int[]> times = timeMap.get(key);
        List<String> vals = valMap.get(key);

        int low = 0, high = times.size() - 1, result = -1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (times.get(mid)[0] <= timestamp) {
                result = mid;        // valid candidate — try going right
                low = mid + 1;
            } else {
                high = mid - 1;
            }
        }
        return result == -1 ? "" : vals.get(result);
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Set | O(1) |
| Get | O(log n) |
| Space | O(n) total |

---

## 1️⃣2️⃣ Median of Two Sorted Arrays
🔗 [LeetCode #4](https://leetcode.com/problems/median-of-two-sorted-arrays/) &nbsp;|&nbsp; 🔴 Pattern: **Hard – Binary Search on Partition**

### 📥 Input / 📤 Output
| | Value |
|--|-------|
| **Input** | `int[] nums1`, `int[] nums2` (both sorted) |
| **Output** | `double` — median of the combined sorted array |
| **Constraint** | O(log(m+n)) time required |

### 💡 Examples
```
Input:  nums1 = [1,3],  nums2 = [2]
Output: 2.0   ← merged [1,2,3], median = 2

Input:  nums1 = [1,2],  nums2 = [3,4]
Output: 2.5   ← merged [1,2,3,4], median = (2+3)/2 = 2.5
```

### 🔑 Key Points to Remember
- Binary search on **smaller array** (fewer iterations)
- Find partition point `i` in `nums1` such that left halves combined = right halves combined
- Partition in `nums2`: `j = (m + n + 1) / 2 - i`
- Valid partition: `nums1[i-1] ≤ nums2[j]` AND `nums2[j-1] ≤ nums1[i]`
- Use `INT_MIN` / `INT_MAX` as guards for edge partitions
- Median: if total length is **odd** → `max(left sides)`; if **even** → avg of `max(left)` and `min(right)`

### ✍️ Solution
```java
class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        if (nums1.length > nums2.length) return findMedianSortedArrays(nums2, nums1);
        int m = nums1.length, n = nums2.length;
        int low = 0, high = m;

        while (low <= high) {
            int i = low + (high - low) / 2;      // partition in nums1
            int j = (m + n + 1) / 2 - i;         // partition in nums2

            int maxLeft1  = (i == 0) ? Integer.MIN_VALUE : nums1[i - 1];
            int minRight1 = (i == m) ? Integer.MAX_VALUE : nums1[i];
            int maxLeft2  = (j == 0) ? Integer.MIN_VALUE : nums2[j - 1];
            int minRight2 = (j == n) ? Integer.MAX_VALUE : nums2[j];

            if (maxLeft1 <= minRight2 && maxLeft2 <= minRight1) {
                if ((m + n) % 2 == 1)
                    return Math.max(maxLeft1, maxLeft2);
                else
                    return (Math.max(maxLeft1, maxLeft2) + Math.min(minRight1, minRight2)) / 2.0;
            } else if (maxLeft1 > minRight2) {
                high = i - 1;
            } else {
                low = i + 1;
            }
        }
        return 0.0;
    }
}
```

### ⏱️ Complexity
| | Value |
|--|-------|
| Time | O(log(min(m,n))) |
| Space | O(1) |

---

## 🧠 Pattern Cheat Sheet

| Pattern | Signal in Problem | Template |
|---------|-------------------|----------|
| **Classic** | "sorted array, find target" | `if ==` return, else move low/high |
| **Left Boundary** | "first position", "first bad", "insert position" | On match: save + `high = mid - 1` |
| **Right Boundary** | "last position", "latest timestamp ≤ t" | On match: save + `low = mid + 1` |
| **Answer Space (min)** | "minimum speed/capacity to achieve X" | BS on `[min..max]`, check `canAchieve(mid)` |
| **Answer Space (max)** | "maximum value such that condition holds" | BS on `[min..max]`, check `canAchieve(mid)` |
| **Rotated Array** | "rotated sorted", "find min in rotated" | Identify sorted half first |
| **Peak Element** | "find any peak", "mountain" | Move toward higher neighbor |
| **2D Matrix** | "sorted matrix, search" | Flatten: `row = mid/n`, `col = mid%n` |

---

## ⚡ Quick Formula Recall

```
Mid calculation (always use this — avoids overflow):
  mid = low + (high - low) / 2

When to use low < high vs low <= high:
  low <= high  → when you return inside the loop (exact match / boundary search)
  low < high   → when you return nums[low] after loop (peak, min in rotated)

Answer Space boundaries:
  Koko:    low=1,          high=max(piles)
  Ship:    low=max(weight), high=sum(weights)
  Generic: low=min possible answer, high=max possible answer

Ceiling division (integer):
  ceil(a / b) = (a + b - 1) / b

Rotated array — which half is sorted?:
  nums[low] <= nums[mid]  → LEFT half sorted
  else                    → RIGHT half sorted
```

---

## 🆚 Binary Search vs Linear Search vs Two Pointer

| | Linear Scan | Two Pointer | Binary Search |
|--|-------------|-------------|---------------|
| **Sorted needed?** | No | Often yes | Yes (or monotonic) |
| **Time** | O(n) | O(n) | O(log n) |
| **Use when** | Unsorted, any array | Pair sums, palindromes | Sorted, search/minimise |
| **Key insight** | Check every element | Use order to skip | Eliminate half each step |

---

## 🎯 Interview Fast-Checklist

Before coding, ask yourself:
```
1. Is the array sorted (or monotonic)?     → Binary Search candidate
2. Am I looking for exact target?          → Classic template
3. Am I looking for first/last occurrence? → Left/Right Boundary
4. Am I minimising/maximising a value?     → Answer Space BS
5. Is the array rotated?                   → Identify sorted half first
6. Is it a 2D matrix?                      → Flatten to 1D index
```

---

*Last updated: March 2026*