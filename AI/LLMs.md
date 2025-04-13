# LLMs (Large Language Models)

- Also see [Learning LLMs](https://github.com/BrentGrammer/learning-LLMs) GitHub Repo

# RAG (Retrieval Augmented Generation)

### What is RAG?

- RAG is a way to make an AI look up extra info before answering you.
- instead of just relying on what the llm already knows, it can grab relevant facts from a pile of documents or data and use that to give you a better answer.
- simple example: you ask, `"What's the best way to cook a potato?"` Without RAG, the LLM would just use general knowledge and say something like, `"Boil it or bake it."` With RAG, it could first search a recipe database, find a specific tip like `"Bake it at 400°F for 45 minutes with salt and oil for crispy skin,"` and then tell you that.
  - The retrieval part is fetching that extra info, and the generation part is it turning it into a clear answer for you.
- RAG is about passing context to an LLM, but it's specifically about fetching that context from somewhere (like a search) rather than just having it handed over in the prompt.

### RAG: an example

- Imagine you're building a chatbot to help people with cooking questions. You want it to give accurate, specific answers based on a collection of 50 recipe PDFs you've got. Here's how you could set up a basic RAG system:

1. Setup: You start by turning those 50 recipe PDFs into a searchable format. You use a tool to extract the text and break it into chunks (like paragraphs or recipes). Then, you store these chunks in a database with a search feature—something like a vector database that can find text based on meaning, not just keywords.
   - **User Asks a Question:** Someone types, `"How do I make a quick pasta sauce?"` The chatbot takes this question as the prompt.
2. **Retrieval Step:** The system searches the database of recipe chunks for anything relevant to "quick pasta sauce." It might find a chunk from one PDF that says, "For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes." The search picks this because it matches the meaning of the question.
3. Pass to the LLM: That retrieved chunk ("simmer canned tomatoes...") gets added to the prompt. So now, instead of just seeing `"How do I make a quick pasta sauce?"` the LLM gets something like: `"Using this info—'For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes'—answer: How do I make a quick pasta sauce?"`
4. Generation Step: The LLM reads the prompt with the extra context and generates an answer: `"To make a quick pasta sauce, simmer canned tomatoes with garlic and olive oil for 10 minutes. Add salt or herbs if you like!"`

#### Step 1: Turning Text into Vectors (Associating Meaning)

A vector database doesn't store plain text—it stores numbers that represent the meaning of the text.
Tool: You use something like a pre-trained model (e.g., a simple one from the `sentence-transformers` library in Python) to convert each snippet into a vector.

- **VECTOR**: A **vector** is just a list of numbers (like [0.1, -0.5, 0.8, ...]) that captures the "meaning" of the text based on patterns it's learned from tons of data.
- Example:
  - Snippet 1 `("fast marinara...")` might become a vector like `[0.2, 0.7, -0.1, ...]` (say, 384 numbers long).
  - Snippet 2 `("bake chicken...")` might be `[0.5, -0.3, 0.9, ...]`.
  - Snippet 3 `("creamy soup...")` might be `[-0.1, 0.4, 0.6, ...]`.
- How Meaning Works: The model makes similar ideas (like "marinara" and "pasta sauce") have vectors that are close together in this number space, while unrelated ideas (like "chicken" and "soup") are farther apart. It's not about exact words—it's about concepts.

#### Visualizing the Vector Space

Imagine a giant 3D cloud (really 384D, for ex.):
Each word or sentence is a dot.

- Dots cluster based on how they're used in real text—like `"apple"` near `"orange," `far from `"truck."`
- The model learns this layout by seeing billions of examples, not by human hands plotting it.
- So, in the code example, `model.encode("quick pasta sauce")` spits out a vector because the model already knows—from its training—where `"pasta sauce"` fits in the meaning-space relative to everything else.

#### Step 2: Storing in a Vector Database

Tool: Use a simple vector database like FAISS (a free library from Facebook) or Chroma (another easy option).

- Process: You load the vectors into the database with labels pointing back to the original snippets. So:
  - Vector `[0.2, 0.7, -0.1, ...]` → Snippet 1.
  - Vector `[0.5, -0.3, 0.9, ...]` → Snippet 2.
  - Vector `[-0.1, 0.4, 0.6, ...]` → Snippet 3.
- Think of the database as a big 3D map (though it's really 384D or more). Each vector is a dot, and dots with similar meanings are clustered together.

#### Step 3: Querying with a Question

- User Asks: `"How do I make a quick pasta sauce?"`
- Convert to Vector: The same model turns this question into a vector, say `[0.25, 0.65, -0.05, ...]`.
- Search: The vector database (e.g., FAISS) compares this question vector to all stored vectors using math (like cosine similarity).
  - It finds the closest match:
    - `[0.25, 0.65, -0.05, ...]` (question) is closest to `[0.2, 0.7, -0.1, ...]` (Snippet 1), because "quick pasta sauce" and "fast marinara" have similar meanings.

#### Step 4: Fetch and Pass to LLM

- Result: The database returns Snippet 1: `"For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes."`
- Prompt: You feed this to the LLM with the question: `"Using 'For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes,' answer: How do I make a quick pasta sauce?"`
- Answer: The LLM says, `"Simmer canned tomatoes with garlic and olive oil for 10 minutes for a quick pasta sauce."`

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a model to make vectors
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your snippets
snippets = [
    "For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes.",
    "Bake chicken at 375°F for 25 minutes with salt and pepper.",
    "Make a creamy soup by blending boiled potatoes with cream."
]

# Turn snippets into vectors
vectors = model.encode(snippets)  # Shape: (3, 384)

# Create a FAISS index (vector database)
index = faiss.IndexFlatL2(384)  # 384 is vector size
index.add(np.array(vectors))    # Add vectors to index

# User question
question = "How do I make a quick pasta sauce?"
question_vector = model.encode([question])  # Shape: (1, 384)

# Search for closest match
distances, indices = index.search(np.array(question_vector), k=1)  # k=1 means top 1 result
best_match = snippets[indices[0][0]]  # Get the snippet

print(f"Found: {best_match}")
# Output: "For a fast marinara, simmer canned tomatoes with garlic and olive oil for 10 minutes."
```

- The sentence-transformers model turns text into vectors based on meaning.
- FAISS stores those vectors and finds the closest one to the question's vector.
- "Close" means "similar in meaning"—that's how it associates "pasta sauce" with "marinara" instead of "chicken" or "soup."

- `model.encode("For a fast marinara, simmer...")` → One vector for the whole sentence.
- `model.encode("How do I make a quick pasta sauce?")` → One vector for the question.
- FAISS matches them because the model's training made "marinara" and "pasta sauce" land in a similar neighborhood of the vector space, thanks to their shared contexts in the training data (e.g., both near "tomatoes," "cook," "quick").

They end up close because the model's training taught it that "pasta sauce" and "marinara" share contextual clues (e.g., both near "tomatoes," "cook," "quick" in the training data). The neural network has baked this understanding into its weights, so it naturally places them nearby in the vector space.

- **The Model Is the Map**: The pre-trained model itself (e.g., all-MiniLM-L6-v2) is the "reference." Its neural network has already learned the relationships between words and contexts during training. When it sees "pasta sauce" and "marinara," it doesn't need a list—it recreates the connection through its learned rules.
  - No Combos Stored: It's not checking a catalog of (pasta, sauce) or (marinara, tomatoes). It's dynamically figuring out the meaning from scratch, using the sentence as a whole.

## Vector Spaces

- Models see that different words that commonly and repeatedly used with the same set of other words based on many text examples get assigned to vector spaces close to each other.
- the model looks at tons of text examples and notices that words (or phrases) repeatedly used with the same context—the same surrounding words or patterns—get assigned vectors that are close together in the vector space. It's all about spotting those consistent relationships in the data.

  - For instance:
    If `"dog"` and `"puppy"` keep showing up near words like `"bark," "leash,"` or `"pet"` across millions of sentences, their vectors end up close.
    Meanwhile, `"dog"` and `"car"` don't share much context (one's with `"fetch,"` the other's with `"drive"`), so their vectors drift apart.
    The model doesn't need anyone to tell it what's similar—it figures that out by crunching the numbers on how words hang out together in real-world text.

- Think of the vector space like a stretchy, infinite 3D map (really 384D or more):
- No Fixed Dots for Combos: There aren't separate dots for (`dog`, `fetch`) or (`dog`, `leash`). Instead, `"dog"` is like a dot that moves a little depending on its neighbors in the sentence.
- Clusters by Meaning: Sentences or words with similar vibes (like `"dog fetches"` and `"puppy retrieves"`) end up in nearby regions, but the exact spot is calculated fresh each time based on the input.
- One Dot per Input: For example, in a recipe related query and RAG context, each recipe snippet (e.g., `"fast marinara..."`) gets one vector, and the question prompt about a recipe gets one vector. The database finds the closest match—no need to predefine every possible pair or trio.

### Assembling Vector Spaces and Trained Vector Sets

- The vectors in models like `sentence-transformers` (or bigger ones like `BERT`) aren't built by humans sitting down and assigning coordinates to words. Instead, they're created through training using machine learning.
- Training Data: The model is fed massive amounts of text—like books, websites, or Wikipedia. billions of sentences.
- Learning Patterns: The model (a neural network) is trained to predict things, like `"What word comes next?"` or `"Does this sentence make sense?"` As it does this, it adjusts millions of internal parameters to get better at guessing.
- Meaning Emerges: While training, the model learns to represent words (and later sentences) as vectors—lists of numbers (how many dimensions, i.e. 384D etc.). It figures out that words with similar meanings (like `"cat"` and `"kitten"`) should have similar vectors, and unrelated ones (like `"cat"` and `"car"`) should be different. This happens because similar words tend to appear in similar contexts in the training data.
- Vector Space: The result is a "vector space" where each word or sentence gets a unique spot (a vector). The distances between these spots reflect how related the meanings are—close for similar, far for different. No human decides this; the model learns it from the patterns in the data.
- Example of How It Learns
  - In the training data, "cat" often appears near words like `"purr," "meow,"` or `"pet,"` while `"car"` shows up near `"drive," "road,"` or `"engine."`
    The model tweaks the vectors so `cat` = `[0.1, 0.5, -0.2, ...]` and `car` = `[0.8, -0.3, 0.9, ...]` end up far apart, while `cat` and `kitten` = `[0.15, 0.45, -0.25, ...]` are close. It's all automatic, driven by processes like gradient descent over millions of examples.
- Not Word-by-Word Numbers
  - **Here's the key:** the individual numbers in a vector (like `0.1` or `-0.2`) don't directly "represent" specific words or features in a way which can be decoded by hand. Instead:
    Each Number Is Part of a Team: The meaning comes from the whole vector—all 384 numbers (or however many) working together. You can't say "0.1 means 'noun'" or "-0.2 means 'animal.'" It's more abstract.
- Context Matters: Early models (like Word2Vec) gave one vector per word, but modern ones (like `sentence-transformers`) adjust vectors based on the sentence. So "bank" in "river bank" gets a different vector than "bank" in "money bank," because it learns from context.
- Humans don't assign coordinates or place words in the vector space. there are millions of words and phrases, and meanings shift subtly. Instead:
- The model starts with random vectors and refines them over time, using math to minimize prediction errors. After training, "dog" and "puppy" naturally end up close because they're used similarly in the data.
- Pre-Trained Models: Libraries like `sentence-transformers` give you a model already trained by experts on huge datasets. You just use it "as is" to turn your text into vectors—no need to train it yourself unless you want to tweak it.
- You don't really "decode" what each number means—it's not like a codebook where `0.5` = `"food."` The decoding happens when you:
  - Compare Vectors: If two vectors are close (using math like cosine similarity), the model assumes the meanings are similar. That's how FAISS found `"marinara"` for `"pasta sauce."`
  - Generate Text: The LLM uses the vectors as input to produce an answer


