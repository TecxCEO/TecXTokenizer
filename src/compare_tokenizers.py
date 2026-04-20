"""
To see exactly how much more efficient your new BPE Tokenizer is compared to the old Character-level (nanoGPT style) method, we will run a comparison script.
This script calculates the Compression Ratio. A higher ratio means your model can "read" more text while using less memory on your Android phone.
1. The Comparison Script (compare_tokenizers.py)
Run this in Termux to see the savings:
"""
import json
from tokenizers import Tokenizer

def compare_efficiency(tokenizer_path, sample_text):
    # 1. Modern BPE Method
    tokenizer = Tokenizer.from_file(tokenizer_path)
    bpe_tokens = tokenizer.encode(sample_text).ids
    bpe_count = len(bpe_tokens)

    # 2. Old Character-level Method (1 char = 1 token)
    char_count = len(sample_text)

    # 3. Calculate Savings
    reduction = ((char_count - bpe_count) / char_count) * 100
    
    print(f"--- 🚀 Tokenizer Efficiency Report ---")
    print(f"Sample Text: '{sample_text[:30]}...'")
    print(f"Character-level Tokens: {char_count}")
    print(f"Modern BPE Tokens:      {bpe_count}")
    print(f"Memory Saved:           {reduction:.2f}%")
    print(f"--------------------------------------")

# Test with your domain data (NREGA / Expert System)
sample = "Jaisalmer district has allocated new funds for rural infrastructure projects."
compare_efficiency("org_tokenizer.json", sample)

"""
2. Why this matters for your Project
Metric	Why it improves with BPE
Context Window	Since 1 word ≈ 1 token (instead of 7 characters), your model can "remember" 7x more information in the same space. [1]
Training Speed	The model processes fewer "steps" per sentence, making your Termux training significantly faster. [2]
Accuracy	The model treats "Jaisalmer" as a single concept rather than just a string of letters, helping it learn Expert Knowledge faster. [3]
3. Next Steps for your "Organization"
Now that you have an efficient tokenizer, you are ready to:
Re-encode your JSONL: Run your training data through the new org_tokenizer.json.
Update Model Config: Set your model's vocab_size to match the tokenizer (e.g., 5000).
Start Training: Use the main_trainer.py we built earlier.
"""
