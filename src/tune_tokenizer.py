"""
To tune these parameters and see their direct impact on your model's efficiency, we will use a Hyperparameter Grid Search script. This script will train several small tokenizers with different settings and tell you which one "compresses" your expert data the best.
1. The Tokenizer Tuning Script (tune_tokenizer.py)
Run this in Termux. It tests different vocab_size and min_frequency combinations.
"""


from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
import os

def test_tokenizer_config(v_size, m_freq, corpus_file):
    # Setup
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    
    trainer = BpeTrainer(
        vocab_size=v_size,
        min_frequency=m_freq,
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]"]
    )
    
    # Train
    tokenizer.train([corpus_file], trainer)
    
    # Test Compression on a sample sentence
    sample = "Jaisalmer district NREGA funds allocation for rural infrastructure."
    encoded = tokenizer.encode(sample)
    
    # Metrics
    num_tokens = len(encoded.ids)
    compression = (len(sample) - num_tokens) / len(sample) * 100
    
    return num_tokens, compression

# Experiment Grid
v_sizes = [1000, 5000, 10000]
m_freqs = [2, 5, 10]

print(f"{'Vocab':<8} | {'MinFreq':<8} | {'Tokens':<8} | {'Compression':<12}")
print("-" * 50)

for v in v_sizes:
    for f in m_freqs:
        t_count, comp = test_tokenizer_config(v, f, "corpus_for_tokenizer.txt")
        print(f"{v:<8} | {f:<8} | {t_count:<8} | {comp:.2f}%")

  """

  2. How to Read the Results
High Compression %: This is your goal. It means the model treats long words as single units.
Small t_count: If the number of tokens for the sample sentence is low (e.g., 5-8), the model is "reading" faster.
The Trade-off:
If you increase vocab_size, compression goes UP, but your main_trainer.py will use more RAM on your phone.
If you increase min_frequency, compression goes DOWN, but the vocabulary becomes "cleaner" (less noise from typos).
3. Recommendations for your "Organization"
If your dataset is small (< 10k lines): Use vocab_size=1000 and min_frequency=2. This prevents the model from being overwhelmed.
If your dataset is large (> 50k lines): Use vocab_size=5000 and min_frequency=5. This allows the model to learn complex phrases like "infrastructure development" as single tokens.
For Puzzles: Use a very small vocab_size (around 500) because the "language" of a puzzle is very simple (just moves).
4. Setting the "Best" Config
Once you find the best numbers from the report:
Update your train_tokenizer.py with those values.
Re-run bulk_encode.py to refresh your training data.

"""
