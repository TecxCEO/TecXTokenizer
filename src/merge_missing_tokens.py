"""
To "Merge" missing words back into your cleaned tokenizer, you can use Vocabulary Extension. This is useful when the [UNK] (Unknown) rate is high because your cleaning process removed rare but critical domain terms (like specific village names or medical conditions).
1. The Merge Script (merge_missing_tokens.py)
This script identifies which words are being marked as [UNK] in your dataset and forces them into the new tokenizer.

"""
import json
from tokenizers import Tokenizer, AddedToken

def merge_missing(tokenizer_path, test_data_path, output_path):
    # 1. Load your cleaned tokenizer
    tokenizer = Tokenizer.from_file(tokenizer_path)
    unk_id = tokenizer.token_to_id("[UNK]")
    
    missing_words = set()
    print("Scanning for unknown words...")
    
    # 2. Identify what is being missed
    with open(test_data_path, 'r') as f:
        for line in f:
            text = json.loads(line)['input']
            # Break text into raw words to find the culprit
            for word in str(text).split():
                encoded = tokenizer.encode(word)
                if unk_id in encoded.ids:
                    missing_words.add(word)

    print(f"Found {len(missing_words)} words to rescue.")

    # 3. Force-merge them back
    # Using 'single_word=True' prevents them from being split in the future
    new_tokens = [AddedToken(w, single_word=True) for w in missing_words]
    tokenizer.add_tokens(new_tokens)
    
    # 4. Save the Final "Organization" Tokenizer
    tokenizer.save(output_path)
    print(f"✅ Success! Final vocabulary size: {tokenizer.get_vocab_size()}")

# Run the merge
merge_missing("org_tokenizer_clean.json", "train_data.jsonl", "org_tokenizer_final.json")
"""
2. Why this is better than retraining
Precision: Instead of lowering the min_frequency for everything (which adds noise), you are only adding back the exact words your model needs.
Deterministic: BPE is usually greedy; adding these as "Added Tokens" ensures they are always treated as a single unit regardless of merge rules. 
Hugging Face
Hugging Face
 +2
3. Comparison of Vocabulary Strategies
Strategy 	When to Use	Result
Cleaning	When you have many typos/garbage tokens.	Small, fast model.
Hard-Coding	For critical terms (NREGA, Jaisalmer).	Safe, accurate expert logic.
Merging	When the [UNK] rate is too high (>1%).	Complete domain coverage.
4. Final Deployment Steps
Run the Merge: Create your org_tokenizer_final.json.
Bulk Encode: You must re-run your bulk_encode.py script because adding tokens changes the IDs of other words.
Train: Launch main_trainer.py.
"""
