# Graphs

- A series of nodes with some amount of connections to other nodes.
  - no rules, just none, some or alot of connections
- All trees are Graphs

### Terms

- see [video](https://frontendmasters.com/courses/algorithms/graphs-overview/)
- Cycle: if you visit at least 3 nodes and return to the original node, you have a cycle
  - Visiting A,B,C,A is a cycle
- Acyclic graph: has no cycles
- Connected graph: Every node can reach every other node.
- Directed graph: Connections to nodes are one way or asymmetric.
  - asymmetric means that though two nodes are connected bidirectionally, one way is more expensive than the other way or has a greater weight than the other.
- Undirected graph: no direction between links, can go both ways between nodes.
- Weighted graph: There is some sort of value associated with the direction
  - in undirected graph, the weights are same - symmetric
  - in directed graph, you can have asymmetric weights between two connected nodes.
- dag graph: directed acyclic graph. every path has a terminus and you can't quite make it to every other node
- Vertex: Node can be referred to as a vertex or a point
- Edge: the connection between two nodes.
- Runtime: O(v \* E): for every vertex we visit every single edge in the graph.

### Representing Graphs

- Adjacency List (most common)
  - A list of edges: Each element in the list is a edge that says where it goes to and the weight associated with the connection.
  - it's a list showing what the node is adjacent to
  ```python
  [
    [{to: 1, weight: 10}, {to: 3, weight: 7}], # index 0 is the first node or node with value of 0 and points to nodes 1 and 3
    [], # this is for node 1 - it is a terminus for example and so would be an empty list (no edges it goes to)
    [{to: 0, weight: 5}] # node 2 points to node 0 and has a connection weight of 5
  ]
  ```
- Adjacency matrix (less common to see - takes more memory of O(V^2))

  - Each node is a row and the columns represent the other nodes it can connect to. The values in each row are the weights from node to node
  - Note how this takes up a lot of memory to represent all possible connections explicitly - it grows exponentially as you get more nodes.

  ```python
  [
    [0,10,0,5], # node 0 is not connected to 0, is to 1 with weight 10, is not connection to 2, and is to 3 with weight 5
    [0,0,0,0,0] # node 1 has a assymetric relationship - 1 has connections to it, but does not connect to any other node itself
  ]
  ```

### Searching

- Breadth first search and depth first search are available since all trees are graphs.
- We don't pop and pull off a stack, we call a function and use recursion for searching.
- In a graph, we often want the path associated with a search

```javascript
// Breadth First Search

// we need to know where we're starting from and what we're looking for, and want to return the path we took.
// because we don't use recursion with breadth first, we need to maintain the path ourselves as we search.
// common approach for this is filling an array of `prev` = [-1. ...] (no node has a -1 val).
// The previous array is who I came from (need a seen or visited array as well of Falses)
function bfs(graph, source, needle) {
  // since graph is adjacency matrix there are as many rows as cols, the length rows will = cols
  const seen = new Array(graph.length).fill(false);
  // setup previous array:
  const prev = new Array(graph.length).fill(-1); // fill with default -1s, nothing has parents right now

  // setup the source as seen as the first one
  seen[source] = true;
  const q = [source]; // put source as first in queue, note: source is a number
  // we don't revisit the first source as it would be a waste

  // while queue has length grab the item out of the queue
  do {
    const curr = q.shift();

    if (curr === needle) {
      break; // we found the needle, so exit loop
    }

    // adjacencies:
    // anything we select we grab out the row, by grabbing the row it represents connections to other nodes - i.e. the element in the row says what connection is to the column (node)
    const adjs = graph[curr]; // will have the elements in a row matching to cols to get the connection/edge
    // walk thru and grab each one of the edges
    for (let i = 0; i < adjs.length; i++) {
      // if no edge, then just continue
      if (adjs[i] === 0) {
        continue;
      }
      if (seen[i]) {
        // if we've seen this, then move on
        continue;
      }
      // if not seen, push it into queue, mark as seen and add where it came from
      seen[i] = true;
      // the previous where i came from is the current (the row)
      prev[i] = curr; // the thing we popped from the queue has our i as a child
      // now add i to the queue
      q.push(i);
    }

    // if we haven't found target, then we need to do some book keeping:
    seen[curr] = true;
  } while (q.length);

  // build backwards, walk previouses until we get to a -1
  let curr = needle; // start where are target to find is
  const out = []; // represents our path through the graph starting at the needle back to the source

  // loop until we've found a point that has no parent (if we never found the needle it will be -1 to begin with and we'll immediately stop and return empty path - there is no path from source to target)
  while (prev[curr] !== -1) {
    out.push(curr);
    curr = prev[curr]; // set this to who added me to this search/set it to parent
  }

  // if we did have a path then return and reverse the path
  if (out.length) {
    // we didn't add source because source has a parent of -1, so we need to concat it
    return [source].concat(out.reverse());
  } else {
    // or return nothing if no path
    return null;
  }
}
```

### Depth First Search on Graph (AdjacencyList)

- We will use recursion and pre and post order traversal
- Runtime is O(V+E) - check every single vertex and every single edge worst case

```javascript
function walk(
  graph: AdjList,
  curr: number,
  needle: number,
  seen: boolean[],
  path: number[]
) {
  // base case - found needle
  if (curr === needle) return true;
  // base case - if already seen, we've been here, the needle is not in this area, go somewhere else
  if (seen[curr]) return false;

  // make sure to flip current to true to make it seen and visited
  seen[curr] = true; // opposed to bfs we set seen after passing the base cases

  // now recurse:

  // pre operation - push to path
  path.push(curr); // we are now officially visiting this and pushing it to our pathway
  if (curr === needle) {
    return true; // can exit early here if found, just made sure above that the curr is in the path
  }

  // recurse
  // list of graph edges - who is this node connected to?
  const list = graph[curr]; // the graph edge where it's going to
  // now we walk this list until we find the needle or exhaust our list and return false
  // NOTE: use a for loop, not array methods because you have to be able to return or break out of them
  for (let i = 0; i < list.length; i++) {
    const edge = list[i];
    // if we find the needle in a successful walk, we need to return true
    if (walk(graph, edge.to, needle, seen, path)) {
      // send signal back up recursive stack so that it all pops
      return true;
    }
  }

  // post - pop if we never found the path in this branch of the graph
  path.pop(); // as long as we pop when we push we'll maintain the order of the array in the path we took

  return false;
}

/**
 * source - node where we want to start from
 */
function dfs(graph: AdjList, source: number, needle: number) {
  const seen = new Array(graph.length).fill(false);
  const path = [];

  walk(graph, source, needle, seen, path);

  if (path.length === 0) return null; // might be better to change interface to return empty path instead of null.

  return path; // return the path from the source to the needle
}
```

## Dijkstra's Shortest Path

- Calculate the shortest path from one node to all other nodes in the graph
- Requires and uses a previous array to track path
- Cannot contain any negative weights for any edges
- Greedy algorithm
  - When you find a shortest path, it is the shortest path in the graph at that individual moment (this will update as you continue to iterate and find shorter paths)

### Intuition

pick the single source. pick the nearest neighbor to it with minHeap. if you don't go directly A->C but instead you go A->B->C, you have to update the cost

#### EXAMPLE:

pick (0,A) cause starting A so A is 0

(10,B) and (2,C) neighbor of A. Add A to visitSet

pick (2,C) with minHeap

(5,B) neighbor of C. Add C to visitSet

You do indirect A->B->C so (5,B) is actually (5+C,B) = (7,B)

minHeap right now have (10,B) and (7,B).

Pick (7,B)

### General algorithm

#### SETUP

- Use a previous array and fill it with -1s to initialize
  - This is used to store where we came from (which node)
- Optionally can use a seen array (initialize to all Falses)
  - Depending on data structure, you may not need a seen array
- Use a distances array to calculate what the shortest distance is
  - Initialize to all Inifinities, except for the source node (the distance of our source node is 0), the 0 is placed wherever index the source node is specified

#### Main idea

- Start with getting the nearest unseen/unvisited node to source, try to constantly get the lowest distance node and update all the other distances based on the new lowest path we found.
  - In the beginning that is the source (it is visitable at a distance of 0)
  - Source is a node that has connections to other nodes (it is a row in the matrix with the first element in the array being the node and subsequent ones being connection information to other nodes)
- Start: mark source as seen/visited

### Implementation

```javascript
/**
 * This is the less than optimal solution
 * O(V^2 + E)
 * For optimum sol, use a min heap which eliminates need for seen array - you remove the nodes seen from min heap as you go. results in O(logV(V+E))
 */

function hasUnvisited(seen: boolean[], dists: number[]): boolean {
  // seen is false and the distance for that node is less than infinity
  return seen.some((s, i) => !s && dists[i] < Infinity);
}
// returns index that is lowest unvisited item
// we assume if calling this function there is one
function getLowestUnvisited(seen: boolean[], dists: number[]): number {
  // what is the lowest distance and it has to be an unseen node
  let idx = -1;
  let lowestDistance = Infinity;
  // walk through all the nodes (represented by the seen list) and find the one with lowest distance
  for (let i = 0; i < seen.length; i++) {
    if (seen[i]) {
      // we visited this so skip it
      continue;
    }
    // we can assume dists will be < Infinity per the hasUnvisited condition above being applied
    if (dists[i] < lowestDistance) {
      lowestDistance = dists[i];
      idx = i;
    }
  }

  return idx; // return the index that is the lowest distance
}
function dijkstra_list(source: number, sink: number, arr: AdjencyList) {
  // adjacency list that represents each node and connection to all other nodes
  const seen = new Array(arr.length).fill(false);
  // make a previous list to track path back
  const prev = new Array(arr.length).fill(-1);
  // make the distances list and all distances start at infinity
  const dists = new Array(arr.length).fill(Infinity);

  // smallest distance possible, we're at source already, so distance is 0
  dists[source] = 0; // the distance recorded to our initial source node which is where we start from

  // loop over nodes until we've seen all of them and calculated lowest distances
  while (hasUnvisited(seen, dists)) {
    const curr = getLowestUnvisited(seen, dists);

    seen[curr] = true;

    const adjs = arr[curr]; // arr is the graph, we get a list of our edges

    // go through each edge
    for (let i = 0; i < adjs.length; i++) {
      // grab the edge
      const edge = adjs[i];
      if (seen[edge.to]) {
        // if we've seen it skip
        continue;
      }

      // calc distance - this is the weight of the edge plus my distance (the source has a 0 + distance to next node weight), then we look at the next closest one and adjust all the weights - repeat this process
      const dist = dists[curr] + edge.weight; // distance to this node (the edge node) from the node we are at
      if (dist < dists[edge.to]) {
        // if this distance is less than the known distance of the edge, we need to update
        if (dist < dists[edge.to]) {
          // the distance of the edge becomes the new smaller distance
          dists[edge.to] = dist;
          // previous edge has a new parent (this tracks where we are backwards through the path taken)
          prev[edge.to] = curr;
        }
      }
    }
  }

  // walk the path backwards and return the path
  const out = [];
  let curr = sink; // sink is where we want to go to

  // we walk one parent back at a time
  while (prev[curr] !== -1) {
    out.push(curr); // add it to our path
    // update current to the parent that got us to this point
    curr = prev[curr]; // prev is the last person to update our distance to the shortest known path
  }

  out.push(source); // add original source node to path
  return out.reverse(); // reverse our above walking backwards to get the forward path we took
}
```

### Interview question for graph

- see [vid](https://frontendmasters.com/courses/algorithms/dijkstra-s-shortest-path-run-time/) at timestamp 8:00
- 2d array with 1s and 0s
- Find how many islands there are (any cell with 1 connected to contiguous set of 1s)
- Use a Breadth first or depth first search
  - Start somewhere,
  - increment islands seen so far
  - Scan until finding 1s and scan in all 4 directions
