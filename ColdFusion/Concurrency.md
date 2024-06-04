# Concurrency in CFML

## Locking
- stick to named locks so you can have pin-point accuracy when dealing with code synchronization. Remember that locking can be expensive.
  - [Avoid scope locking if possible](https://modern-cfml.ortusbooks.com/cfml-language/locking#scoped-locking).
- [Dead Locks](https://modern-cfml.ortusbooks.com/cfml-language/locking#deadlocks)

### Race Conditions
- [Handling race conditions with a double lock](https://modern-cfml.ortusbooks.com/cfml-language/locking#race-conditions-double-locking)

## Threading
- See [Ortus Solutions entry](https://modern-cfml.ortusbooks.com/cfml-language/threading)