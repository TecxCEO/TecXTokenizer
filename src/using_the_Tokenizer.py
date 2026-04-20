# Using the Tokenizer
#The tokenizer can process text for a model.

from tokenizers import Tokenizer

# Load the custom tokenizer
tokenizer = Tokenizer.from_file("org_tokenizer.json")

# Encode text
text = "Jaisalmer district NREGA budget allocation."
encoded = tokenizer.encode(text)

print(f"IDs: {encoded.ids}")
print(f"Tokens: {encoded.tokens}")

# Decode back to text
decoded = tokenizer.decode(encoded.ids)
print(f"Decoded: {decoded}")

"""
Why this is the "Latest Model" approach:
Byte-Level Safety: Handles emojis and special symbols.
Vocabulary Optimization: It learns that "Jaisalmer" is one important unit. This makes model training faster.
Subword Intelligence: If it sees a new word like "Jaisalmerian", it can break it into Jaisalmer + ian.
"""
