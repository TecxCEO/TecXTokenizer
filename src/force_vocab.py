"""
To "hard-code" your most important terms, you use Special Tokens or Added Tokens. This ensures that even if a word like "NREGA" appears only once, the tokenizer will treat it as a single, unbreakable unit.
1. The Hard-Coding Script (force_vocab.py)
Run this script to update your existing org_tokenizer.json.

"""

from tokenizers import Tokenizer, AddedToken

def add_forced_tokens(tokenizer_path, output_path):
    # 1. Load your trained tokenizer
    tokenizer = Tokenizer.from_file(tokenizer_path)
    
    # 2. Define your Organization's "Power Words"
    # These will NEVER be fragmented.
    power_words = [
        "NREGA", 
        "Jaisalmer", 
        "Rajasthan", 
        "Pneumonia", 
        "Safety_Factor",
        "Gram_Panchayat"
    ]
    
    # 3. Add them as special tokens
    # 'single_word=True' ensures it doesn't match parts of other words
    forced_list = [AddedToken(w, single_word=True) for w in power_words]
    tokenizer.add_tokens(forced_list)
    
    # 4. Save the updated version
    tokenizer.save(output_path)
    print(f"✅ Success! {len(power_words)} words are now hard-coded.")

# Run the update
add_forced_tokens("org_tokenizer.json", "org_tokenizer_final.json")


"""
2. Why this is the "Pro" Move
Zero Ambiguity: The model no longer has to guess what "NREGA" means; it sees one specific ID for that one specific concept.
Sensor/ID Data: If you have specific ID codes in your NREGA or Engineering data (like GP_105), hard-coding them prevents the tokenizer from splitting them into random numbers.
Formatting: You can hard-code formatting markers like [START_DIAGNOSIS] or [END_LOG] to make your output logs easier for your PC to parse.
3. Critical Step: Update your Model
If you add 50 hard-coded words, your total vocabulary size increases by 50. You must update your vocab_size in your training script:
"""
