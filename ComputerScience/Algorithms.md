# Algorithms

### Binary Search

- Is the dataset you have ordered? if it is then there are advantages to this you can use
- This is O(logN) time (logarithmic time), ex. log(4096) = 12 -> you can halve 4096 twelve times to get to 1.
- continuosly halve the search space until you find the value - you never scan ( that would result in O(N) time)

#### Steps:

- Preqrequisite: The Array must be sorted! You can't do binary search on a nonsorted data set.
- to get the midpoint, take the low (start pos. of the array for ex) and add (entire length/2). \*Use the Math.floor of this result.
- check if value is the midpoint and return if found
- Check if value is larger than the midpoint (if v > midpoint), if yes then you search the right half of the data set
  - reset the low start pos. of the set to `low + 1`
- If val is less than midpoint, then reset the high to be the midpoint
  - Be careful of off by one errors - approach could be to think of the low as inclusive and the high position as exclusive
- loop over this algo while the low position is less than the high position (stop when they are at a crossing point, they always keep getting closer to each other on each iteration)

```javascript
function binarySearch(haystack, needle) {
  let start = 0;
  let end = haystack.length;

  while (start < end) {
    let midpoint = Math.floor((end - start) / 2) + start; // add start offset to get correct midpoint index relative to the entire array passed in.
    let midVal = haystack[midpoint];

    if (midVal === needle) {
      return midpoint;
    } else if (midVal < needle) {
      start = midpoint + 1;
    } else {
      end = midpoint;
    }
  }

  return -1;
}
```

#### Crystal Ball Problem

- Given two crystal balls that will break if dropped from a high enough distance, determine the exact spot in which they will break in the most optimized way.
  - Example: You're in 100 story building, and you have two crystal balls and you wnat to find which floor they will break if dropped from it.
- Generalized problem: we have an array of Falses (point at which does not break) and we want to find at which point they start turning to a True value (the first point where you drop a ball and it breaks)
- To avoid linear search (jumping by half still results in linear time due to having a second ball and needing to go back to beginning??), and given this is a sorted data set (Falses, then Trues on the right), we can avoid linear searching, then change the unit of jumping to find the exact point of breakage. for instance, the square root of N. If we jump by this, and need to scan to find the exact point, at most we are scanning the square root of N so the op is O(sqrt(n))
  - If you jump by halfs (binary search), the worst case is that you have to walk half the array, whereby using sqrt(n) the worst case is walking sqrt(n) elements in the array.

```javascript
function twoCrystalBalls(breaks: boolean[]): number {
  // jump by the sqrt of N to avoid linear search (use divide and conquer approach)
  const jumpAmount = Math.floor(Math.sqrt(breaks.length));

  let i = jumpAmount;
  for (; i < breaks.length; i += jumpAmount) {
    // find point where it breaks then jump back sqrt(n) and walk forward sqrt(n)
    if (breaks[i]) {
      // check if we've entered the series of True points in the set
      break;
    }
  }

  i -= jumpAmount; // jump back sqrt N
  // we set j and make sure i is less than the entire set length in case we walk off the upper bound with the jump
  for (let j = 0; j < jumpAmount && i < breaks.length; ++j, ++i) {
    // if we find breaking point, return i
    if (breaks[i]) {
      return i;
    }
  }
  // not found
  return -1;
}
```
