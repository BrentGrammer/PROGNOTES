# Polling and Streaming

- Useful for frequently or regularly changing data that needs to be observed.
  - Temperature data or chat messages
- Polling and Streaming help systems observe and get this data as it updates

## Polling

- Client issues request for data it wants on recurring basis, following a set interval (every X seconds)

### Limitations of Polling

- **Updates when data changes are not instantaneous**: updated data is not retreived instantly - polling depends on interval set
- Not good for a chat app for example.

## Streaming

- Better for getting instantaneous updates when data changes
- Client opens a longstanding connection (a Socket) with a server
- Socket: A file that lives on the client(or server??) that it can write to and read from to communicate with another computer
  - Like a portal into another machine that you can communicate through without having to send repeated requests - the connection remains open as long as the machines don't close it or the network is healthy
  - Client listens and streams data from the server - the server pushes data as it arrives or updates
- This is a "pushing" model - sending data proactively to clients
- In contrast to polling - you have one connection as opposed to many (with repeated requests)
- Good for a chat app and better than polling

## Streaming vs Polling
- Streaming is good for needing data updates instantaneuously and frequently
  - Currency exchange, stock prices, chat apps
- Polling is good for needing updated data less frequently at some interval (30s, every minute etc.)
  - Dashboard that monitors data to get a snapshot at a given point of times, monitoring temperature (if no need for frequent instant updates)
