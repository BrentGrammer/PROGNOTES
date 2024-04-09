# Numbers in GoLang

### Numbers

- 8-bit: int8/uint8
- 16-bit: int16/uint16
- 32-bit: int32/uint32
- 64-bit: int64/uint64
- 32- or 64-bit based on system architecture: int/uint
- Synonym for int32: rune
- synonym for int8: byte
- Floating-Point Numbers
- Floating-point numbers can contain a decimal point. There are two different sizes.

#### Floats

- 32-bit: float32
- 64-bit: float64

#### Complex

- 32-bit float + imaginary number: complex64
- 64-bit float + imaginary number: complex128

#### When to use which:

- By default just use int. It's 32 bits or 64 bits depending on your arch
- If you know it might be bigger than about 2 billions, use int64. Otherwise you'll get an overflow on a 32 bits arch.
- If you know you will have a lot of them in memory, AND it's small enough to fit a int8/int16/int32, you can use that. But most of the time there is no significant gain to do so
- probably want uint32 for IDs (4 billion positive ints)
- uint8 is 0 to 255
