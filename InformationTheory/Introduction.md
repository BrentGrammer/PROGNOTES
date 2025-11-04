u# Introduction to Information Theory

- [Good lecture by McKay](https://www.youtube.com/watch?v=BCiZc0n6COY)

### The Main Problem

- How to get reliable communication over an unreliable channel

## Channels

- A channel is a conduit information can be sent through.
- A channel has a sender (transmitter), a receiver and a medium:
  - Sound: Voice -> Ear (meduim: Air)
  - Visual: Eye -> Brain/Nervous System (meduim: cytoplasm and electricity)
  - Phone -> Phone (medium: copper wire)
- Channels can go in one direction or be bidirectional
- In all channels **The recieved signal is not identical to the transmitted signal**
  - Due to noise or other processes
  - The received signal is approximately the transmitted signal with some noise added
  - The goal is to have the received signal equal the transmitted signal ideally

### Solutions to Noise

- <u>Physical Solutions</u>: change the wire, replace components, change the physics to reduce the noise
- <u>System Solutions</u>: Noise in the signal is accepted. Encoding and Decoding systems are put in place to turn the channel into a reliable channel.
  - The main idea is that in this case, the system is taken physically as is, but _transformed_ into a reliable system

**Information Theory is a Systems Solution to the problem of Noise in a Channel**

## The Systems Solution

- Source Message -> \[ENCODER\] -> produces Transmission -> send through Channel (noise added) -> Received message (corrupted by noise) -> \[DECODER\] -> $\underline{\hat{s}}$ (_s hat_ = the decoded guess at the message)
- The Encoder adds _REDUNDANCY_
  - Takes into account the transmitted message and guessing the Noise
- The Decoder infers the noise and the guessed transmission $\underline{\hat{s}}$

### The Binary Symmetric Channel

- A simple model with properties for analyzing Information Theory
- The channel accepts an input (0 or 1) and produces an output (0 or 1 which may or may not match the input)
- Assume a 90% chance probability that what comes out is the same as what you put in (0 => 0), and a 10% probability that it is not the same (i.e. 0 produces 1)

### Example

- 10,000 bits on a Hard Drive where 10% probability of bits being wrongly flipped
  - $f = 0.1$ where $f$ is the probability that bits are wrongly flipped after receiving (The disk drive flips 10% of the bits transferred)

#### Getting the Expected Number of Flipped Bits

- Expected flipped bits is roughly 1,000 +/- 30
  - the Variance is the square root of the std deviation.
  - The Variance of a **Binomial Distribution** (A distribution that consists of two possible events or outcomes, like a coin toss)
    - $Npq$ = The variance of a Binomial Distribution
    - The mean of a Binomial distribution is $N \times p$ where $p$ is $f$ (i.e. 0.1, the probability of one outcome, i.e. flipped bits at 10%) and $q$ is the other outcome $1 - f$ (the bits are NOT flipped, or 90%)
      - The mean here is $10,000 \times 0.1 = 1,000$ (1,000 bits are flipped per 10k as 10% chance)
      - The variance $Npq = 900$ to get the +/- variance in the probability of flipped bits is the square of the std deviation $\sigma^2$, so the +/- is 30 bits. (1,000 bits +/- 30 is how many are expected to be flipped on transfer)

#### The Important Question:

- _How small does the flip probability $f$ need to be to make a sale-able Hard Drive?_
- Assuming 1GB transfer/day over 5 years without failure (flipped bits), we want 1,000 happy customers (no failures for 1,000 people using at this rate)
  - $f = 10^{-18}$ - probability of flipped bits needs to be this to make a saleable drive. This is a standard rate the drive industry aims for.

#### Ways to Add Redundancy (The Encoder)

- Parity Coding: $s|p$ where $s$ is the source (i.e a sequence string or byte, or 8 bits) and $p$ is the parity coding (i.e. the sum of all the 1s in the bits to represent it)
  - $[0 1 0 1 1 1 0 1] | 5 | $
- Repitition Code: $R_3$ where $R$ is the repitition and $3$ is the number of repititions total sent
  - 0 -> 000
  - 1 -> 111

**The Decoder users INFERENCE to determine the original signal transmitted**

- One method of a decoder to improve the received signal to mitigate noise over the channel, is to use Majority Vote (if the bit is flipped that bit in the redundancy encoder will be flipped, so the majority of 1s or 0s = the original bit state)
- The reason that Majority Vote works as a good decoder is because Inference uses Inverse Probability

### Inverse Probability

<u>The Two Rules of Probability:</u>

#### 1. The Product Rule:

- get a joint probability (probability that two events happen together) from a marginal probability and a conditional probability:
  $$P(s,r) = P(s)P(r|s)$$
- The Joint Probability of $s$ (source) and $r$ (recieved) is the Probability of $s$ multiplied by the Probability of $r$ given $s$ and vice versa

#### 2. The Sum Rule:

- Get a marginal Probability by adding up all values of a Joint Probability
  $$P(r) = \sum_{s}P(s,r)$$
- Sum the joint probability of $s,r$ for every value $s$, where $s$ is the joint probability $P(s,r)$ for each value of $s$
  - In our case and example, the signal $s$ can only be two values as a bit (0 or 1), we add up the joint probabilities for when the bit is 0 or 1: $P(s=0, r) + P(s=1, r)$

#### Posterior Probability

- If given the recieved signal $r$ and we want to know how probable the corresponding sent transsmission $s$ is given $r$, we want to know the Posterior Probability of $s$
  $$P(s|r) = P(r|s)P(s) \over {P(r)}$$ where $P(r|s)$ is the "Likelihood" of $s$ and $P(s)$ is the "Prior Probability" of $s$
- $P(r)$ on the bottom is computed using the sum rule: $P(r) = P(r|s=0)P(s=0) + P(r|s=1)P(s=1)$

- See timestamp 35:45 for concrete example of using this formula to infer the signal from the recieved

left off at 45 min
