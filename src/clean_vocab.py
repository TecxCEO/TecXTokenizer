"""
Cleaning your vocabulary is a great move for an Expert System. It removes "noise" (like typos or rare character combinations) that can confuse your model and waste memory in Termux.
1. The Vocabulary Cleaning Script (clean_vocab.py)
This script identifies tokens that fall below your threshold and regenerates a "tight" tokenizer.
"""

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

def clean_and_retrain(corpus_file, output_path, min_freq=5):
    """
    Retrains the tokenizer with a higher frequency threshold 
    to remove one-off tokens and 'garbage' data.
    """
    # 1. Initialize
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    
    # 2. Setup Trainer with higher min_frequency
    # Setting min_frequency=5 ensures a token must appear 5 times to exist
    trainer = BpeTrainer(
        vocab_size=5000,
        min_frequency=min_freq, 
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
    )
    
    # 3. Retrain on your clean corpus
    print(f"Cleaning vocabulary... (Filtering tokens with frequency < {min_freq})")
    tokenizer.train([corpus_file], trainer)
    
    # 4. Save the clean version
    tokenizer.save(output_path)
    print(f"✅ Success! Cleaned tokenizer saved to {output_path}")
    print(f"New Vocab Size: {tokenizer.get_vocab_size()}")

# Run the cleaning process
clean_and_retrain("corpus_for_tokenizer.txt", "org_tokenizer_clean.json", min_freq=5)

"""
2. Why this is important for your "Organization"
Reduced Overfitting: By removing rare tokens, the model is forced to learn general patterns instead of memorizing specific typos or unique names.
Faster Training: A "cleaner" embedding layer converges faster because the model doesn't spend time trying to figure out what a rare token (like qx7z) means.
Android Stability: A smaller, cleaner vocabulary reduces the size of your .pth and .tflite files, making them more stable on low-RAM phones.
3. What to do next
Re-Run Export: Run export_vocab.py on this new org_tokenizer_clean.json to see the difference.
Re-Encode: You must run bulk_encode.py again because the token IDs will have changed.
Final Train: Start your main_trainer.py.
4. Comparison Check
Type ls -lh *.json in Termux. You should see that the clean version is slightly smaller than the original.
"""
