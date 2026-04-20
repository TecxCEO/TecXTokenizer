"""

To see exactly what your model "knows," you can export the full vocabulary list. This is very helpful for auditing your Expert System to ensure no "garbage" tokens (like typos or fragments) are taking up space.
1. Vocabulary Export Script (export_vocab.py)
Run this in Termux to generate a readable list of all your tokens.
"""


import json
from tokenizers import Tokenizer

def export_vocab(tokenizer_path, output_txt):
    # 1. Load the final tokenizer
    tokenizer = Tokenizer.from_file(tokenizer_path)
    
    # 2. Get the vocabulary (dictionary of token: index)
    vocab = tokenizer.get_vocab()
    
    # 3. Sort by Index so it matches your model's embedding IDs
    sorted_vocab = sorted(vocab.items(), key=lambda x: x[1])
    
    # 4. Write to a text file
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(f"{'ID':<8} | {'Token'}\n")
        f.write("-" * 20 + "\n")
        for token, token_id in sorted_vocab:
            f.write(f"{token_id:<8} | {token}\n")
            
    print(f"✅ Success! Full vocabulary saved to {output_txt}")

# Run the export
export_vocab("org_tokenizer_final.json", "full_vocabulary_list.txt")
"""
2. How to Audit Your Vocabulary
Once you have full_vocabulary_list.txt, look for these three things:
Top Tokens (0-100): These are usually your [PAD], [UNK], and common letters.
The Middle: You should see your "Hard-Coded" words like NREGA or Jaisalmer here.
The Bottom: Look for very strange tokens (e.g., zxcv). If you see too many of these, your min_frequency was likely too low, and you should retrain the tokenizer.
3. Sharing with your Organization
You can move this file to your phone's Downloads folder to read it in any text viewer:
bash
cp full_vocabulary_list.txt ~/storage/downloads/
Use code with caution.
4. Final Verification for Puzzle/Expert Systems
If you are training for Puzzle 3, check that your move IDs (0-11) are clearly listed and haven't been merged into other words. For Expert Systems, ensure that your "Explanation" keywords are present.
"""
