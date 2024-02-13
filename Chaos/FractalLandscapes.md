# fractals and landscape

## Noise

- from [Shaders book](https://thebookofshaders.com/13/)

### Waves

- A wave is a fluctuation over time of some property.
- Audio waves are fluctuations in air pressure, electromagnetical waves are fluctuations in electrical and magnetic fields.
- Two important characteristics of a wave are its amplitude and frequency.

Simple linear wave:

```python
amplitude = 1
frequency = 1
y = amplitude * math.sin(x * frequency)
 #Try changing the values of the frequency and amplitude to understand how they behave.
 # "modulate" a sine wave, and you just created AM (amplitude modulated) and FM (frequency modulated) waves
```

### Superposition

- property of waves is their ability to add up, which is formally called superposition

```python
# Comment/uncomment and tweak the following lines. Pay attention to how the overall appearance changes as we add waves of different amplitudes and frequencies together.
import math

amplitude = 1.0
frequency = 1.0
x = 0.0
y = math.sin(x * frequency)
t = 0.01 * (-u_time * 130.0) # u_time often represents a value that tracks the passage of time, typically in seconds. It could be the time since the start of a program, the time since a particular event occurred, or some other time-related metric used in the context of the program.
y += math.sin(x * frequency * 2.1 + t) * 4.5
y += math.sin(x * frequency * 1.72 + t * 1.121) * 4.0
y += math.sin(x * frequency * 2.221 + t * 0.437) * 5.0
y += math.sin(x * frequency * 3.1122 + t * 4.269) * 2.5
y *= amplitude * 0.06
```

### Perlin Noise

- Perlin noise in its basic form has the same general look and feel as a sine wave. Its amplitude and frequency vary somewhat, but the amplitude remains reasonably consistent, and the frequency is restricted to a fairly narrow range around a center frequency.
- It's not as regular as a sine wave, though, and it's easier to create an appearance of randomness by summing up several scaled versions of noise.
- **It is possible to make a sum of sine waves appear random as well, but it takes many different waves to hide their periodic, regular nature.**

### Fractal Brownian Noise

- adding different iterations of noise (octaves), where we successively increment the frequencies in regular steps (lacunarity) and decrease the amplitude (gain) of the noise we can obtain a finer granularity in the noise and get more fine detail. This technique is called "fractal Brownian Motion" (fBM), or simply "fractal noise"
- lacunarity is about how much you mix things up or vary them as you create patterns or textures. It's a way to control the diversity or randomness in your creation.
- **This technique is commonly used to construct procedural landscapes. The self-similarity of the fBm is perfect for mountains, because the erosion processes that create mountains work in a manner that yields this kind of self-similarity across a large range of scales.**
  - Read [this material](https://iquilezles.org/articles/morenoise/) for more information on applications of this technique for generating landscapes like mountains.
  - Collection of good articles: https://iquilezles.org/articles/

```python
# Properties
octaves = 1
lacunarity = 2.0
gain = 0.5

# Initial values
amplitude = 0.5
frequency = 1.0

# Loop of octaves
y = 0.0
for i in range(octaves):
    y += amplitude * noise(frequency * x)  # Assuming 'noise' function is defined elsewhere
    frequency *= lacunarity
    amplitude *= gain

#     Progressively change the number of octaves to iterate from 1 to 2, 4, 8 and 10. See what happens.
# When you have more than 4 octaves, try changing the lacunarity value.
# Also with >4 octaves, change the gain value and see what happens.

# Note how with each additional octave, the curve seems to get more detail. Also note the self-similarity while more octaves are added. If you zoom in on the curve, a smaller part looks about the same as the whole thing, and each section looks more or less the same as any other section.

```

### Warping Fractal Brownian Noise

- see [article](https://iquilezles.org/articles/warp/)
- Can be useful for creating more chaotic structures like clouds and smoke
