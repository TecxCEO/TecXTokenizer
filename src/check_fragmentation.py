"""

To check for Token Fragmentation, you want to ensure that your most important domain terms (like "NREGA", "Jaisalmer", or "Pneumonia") are being treated as single units rather than being chopped into meaningless bits like N + RE + GA.
If a word is fragmented, the model has to work much harder to "remember" the full concept.
1. The Fragmentation Inspector Script (check_fragmentation.py)
Run this in Termux to see if your tokenizer respects your organization's key terms.

"""

from tokenizers import Tokenizer

def inspect_tokens(tokenizer_path, important_words):
    tokenizer = Tokenizer.from_file(tokenizer_path)
    
    print(f"{'Word':<15} | {'Status':<12} | {'Fragments'}")
    print("-" * 45)
    
    for word in important_words:
        encoded = tokenizer.encode(word)
        tokens = encoded.tokens
        
        status = "✅ WHOLE" if len(tokens) == 1 else "⚠️ FRAGMENTED"
        
        print(f"{word:<15} | {status:<12} | {tokens}")

# List your critical domain terms here
keywords = ["NREGA", "Jaisalmer", "allocation", "infrastructure", "Rajasthan"]
inspect_tokens("org_tokenizer.json", keywords)


"""
2. How to Fix Fragmentation
If your key terms are showing up as ⚠️ FRAGMENTED, you have three options to fix it:
Decrease min_frequency: Lowering this to 1 or 2 in your BpeTrainer forces the tokenizer to create a token for a word even if it appears only a few times [1].
Increase vocab_size: Giving the tokenizer more "slots" allows it to keep more full words instead of breaking them down to save space [2].
Add "Added Tokens": You can manually force certain words to never be split:
python
tokenizer.add_tokens(["NREGA", "Jaisalmer"])
Use code with caution.
3. Why this matters for Expert Systems
Logical Integrity: In an engineering model, if "safety_factor" is split into safe + ty + fac + tor, the model might confuse it with other "safe" or "factor" related terms.
Training Speed: Whole tokens mean fewer steps for the model to process a sentence, which is essential for low-power training on Android [3].
Final Quality Check
A "perfect" tokenizer for your organization should show ✅ WHOLE for at least 90% of your primary technical terms.
"""
