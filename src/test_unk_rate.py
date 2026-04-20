"""
This script is your "Safety Net." If you clean the vocabulary too much, your model will see too many [UNK] (Unknown) tokens and "forget" important words. This test ensures you have the perfect balance between a clean vocabulary and high accuracy.
1. The Tokenizer Stress Test (test_unk_rate.py)
Run this in Termux to compare your original and cleaned tokenizers.

"""
from tokenizers import Tokenizer
import json

def test_unknown_rates(original_path, clean_path, test_data_path):
    # 1. Load both tokenizers
    tok_orig = Tokenizer.from_file(original_path)
    tok_clean = Tokenizer.from_file(clean_path)
    
    unk_id_orig = tok_orig.token_to_id("[UNK]")
    unk_id_clean = tok_clean.token_to_id("[UNK]")

    total_tokens_orig = 0
    total_unks_orig = 0
    total_tokens_clean = 0
    total_unks_clean = 0

    print(f"Reading test data from {test_data_path}...")
    with open(test_data_path, 'r') as f:
        for line in f:
            text = json.loads(line)['input']
            
            # Encode with Original
            ids_orig = tok_orig.encode(str(text)).ids
            total_tokens_orig += len(ids_orig)
            total_unks_orig += ids_orig.count(unk_id_orig)
            
            # Encode with Clean
            ids_clean = tok_clean.encode(str(text)).ids
            total_tokens_clean += len(ids_clean)
            total_unks_clean += ids_clean.count(unk_id_clean)

    # Calculate Rates
    rate_orig = (total_unks_orig / total_tokens_orig) * 100
    rate_clean = (total_unks_clean / total_tokens_clean) * 100

    print("\n" + "="*40)
    print("      🔍 UNKNOWN TOKEN ANALYSIS")
    print("="*40)
    print(f"Original UNK Rate: {rate_orig:.4f}%")
    print(f"Cleaned  UNK Rate: {rate_clean:.4f}%")
    print("-" * 40)
    
    if rate_clean > rate_orig + 2.0:
        print("⚠️ WARNING: Cleaned tokenizer has significantly more unknowns!")
        print("Suggestion: Lower your 'min_freq' in the cleaning script.")
    else:
        print("✅ SUCCESS: Cleaning was safe. Minimal data loss.")
    print("="*40)

# Run the test
test_unknown_rates("org_tokenizer.json", "org_tokenizer_clean.json", "train_data.jsonl")

"""
2. How to Interpret the Numbers
Ideal Result: Your Cleaned UNK rate should be almost identical to the Original (e.g., both < 0.1%).
Bad Result: If your Cleaned UNK rate jumps to 5% or 10%, it means the model is "blind" to 1 out of every 10 words. You should go back to clean_vocab.py and reduce the min_freq (e.g., from 5 to 2).
3. Why this matters for Expert Systems
In NREGA or Medical data, a name like a specific village or a rare medicine might only appear 3 times. If your min_freq is 5, that word becomes [UNK], and the model might give a wrong recommendation because it can't "see" the specific location or drug.
4. Final Deployment
If the test shows ✅ SUCCESS, you can officially delete the old, messy tokenizer and use org_tokenizer_clean.json for all future work.
"""
