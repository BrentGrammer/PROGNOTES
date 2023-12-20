# Trees

- Traversal pattern: Visit a node, and then recurse (think of pushing and popping parts of the path on a Stack)
- Traversals are O(N) Linear runtime complexity (as tree nodes grow operations grow)

## Types of Traversals

- https://frontendmasters.com/courses/algorithms/tree-traversals/

### Pre-order Traversal (root is visited at beginning) - depth first search

- First visit the node, then recurse to traverse (left then right).
  - Visit node go to left child, recurse until you get to a leaf and go back up and then to the right node child.
  - The root node is at the beginning of visits and you start there

### In order traversal (Root visitied in middle) - depth first search

- Go down to the left until hitting a leaf, visit that node and then go back up and Recurse Right (the root node will be visited in the middle on your way back up and then to the right half of tree)
- Start at a node and recurse in a direction until you get to a terminus leaf node - operate on that and then go back up to previous node and recurse other direction
- Can be used in binary tree to print out an ordered array of the values.

### Post order traversal (Root visited at the end) - depth first search

- Useful for memory clean up - you get through the children and on the way back up/out you can clean up.
- The root node of the tree will be at the end and visited last using this method
- Start at root, recurse left to visit a terminus and then back up and right, go all the way up and down the right half in the same way and then at the end you visit the root node.

## Depth first search

- Preserves the shape of the tree (i.e. if you are comparing two trees)
  - Breadth first search does not preserve shape
- uses recursion (breadth first traversal uses iteration)

### Coding a traversal (Depth First Search)

- The base case for travsersing is when the node is undefined (you have reached a leaf/terminus)

```javascript
function walk(curr, path) {
  // base case (no node to go to so we've reached a leaf/terminus)
  if (!curr) return path; // path keeps track of all visited nodes

  // Now recurse - 3 steps: pre, recurse and post step

  // pre step: push the current visited node into our path
  path.push(curr.value);
  // recurse: go left and right, if we hit node that doesn't exist walk just returns, otherwise keeps going to the bottom
  walk(curr.left, path); // after hitting a leaf, goes back up stack and then goes the other way with walk right below..
  walk(curr.right, path);
  //post step - return out the path
  return path;
}

function preOrderSearch(head) {
  // note in JS everything you pass in except numbers is passed as a pointer, so walk will mutate the path [] passed in and update it
  return walk(head, []);
}
```

```javascript
// in order traversal
function walk(curr, path) {
  // base case (no node to go to so we've reached a leaf/terminus)
  if (!curr) return path; // path keeps track of all visited nodes

  // walk left until you can't anymore, visit node, then walk right and let algo redo itself
  walk(curr.left, path);
  path.push(curr.value); // move visitation in between walking left and right for in order traversal
  walk(curr.right, path);

  return path;
}

function InOrderSearch(head) {
  // note in JS everything you pass in except numbers is passed as a pointer, so walk will mutate the path [] passed in and update it
  return walk(head, []);
}
```

```javascript
// post order traversal
function walk(curr, path) {
  // base case (no node to go to so we've reached a leaf/terminus)
  if (!curr) return path; // path keeps track of all visited nodes

  // walk left until you can't anymore, visit node, then walk right and let algo redo itself
  walk(curr.left, path);
  walk(curr.right, path);
  path.push(curr.value); // move visitation after going left and right for post order traversal

  return path;
}

function postOrderTraversal(head) {
  // note in JS everything you pass in except numbers is passed as a pointer, so walk will mutate the path [] passed in and update it
  return walk(head, []);
}
```

## Breadth First Search

- The underlying implicit data structure is a queue (the opposite of depth first search which uses a stack)
- Using a Queue, the runtime complexity is O(N)
  - Note: careful about using a array list which has more expensive shift and unshifting operations , then it makes the runtime O(N^2)
- With breadth first you do not need to use recursion. Instead of recursing we push items into a queue
- Basic algo is get node, run op, push in it's children to the queue

```javascript
// assumes binary tree
function bfs(head, needle) {
  const q = [head]; // should use a real queue, arrays are more expensive with shifting ops

  while (q.length) {
    const curr = q.shift(); // remove first item from queue
    if (!curr) continue; // move to next iteration which will break the loop

    if (curr.value === needle) {
      return true;
    }

    // push on children to queue (at the end)
    q.push(curr.left);
    q.push(curr.right);
  }

  // if here then entire tree is traversed and we have not found value
  return false;
}
```

### Compare trees

```javascript
function compare(a, b) {
  // structure check - we are at same point in structure (and end leaf on both sides) and other value check did not fail, so tree matches at this point
  if (a === null && b === null) {
    return true;
  }

  // structure check - structure is different, trees are different so return false
  if (a === null || b === null) {
    return false;
  }
  // value check - are the values at this point in tree equal
  if (a.value !== b.value) {
    return false;
  }

  // recurse over the sections of the tree (going left and then compare vals on right) - bool combinations will bubble up and combine - will fail if any one is false.
  return compare(a.left, b.left) && compare(a.right, b.right);
}
```
