# Modeling in Python

- Can use dataclasses (standard library from python 3.7+), attrs or Pydantic (offers focus on validation)

# Nullable Optional Fields:

- `field: Optional[float] = None`
  - If the field is ommitted, then the default will be set with the field added to the instance
  - If you do not use Optional, then 
