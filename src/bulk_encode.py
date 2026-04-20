"""

To prepare your Organization's Expert System for high-speed training, you need to "Pre-tokenize" your dataset. This script converts your text-based train_data.jsonl into a numeric tokenized_train.jsonl file that your model can read instantly.
1. The Bulk Encoder Script (bulk_encode.py)
This script uses your new org_tokenizer.json to process the entire dataset.
"""
import json
from tokenizers import Tokenizer

def bulk_encode_dataset(input_jsonl, output_jsonl, tokenizer_path):
    # Load your custom BPE tokenizer
    tokenizer = Tokenizer.from_file(tokenizer_path)
    
    with open(input_jsonl, 'r') as f_in, open(output_jsonl, 'w') as f_out:
        for line in f_in:
            data = json.loads(line)
            
            # 1. Encode the text input into Token IDs
            # We use .ids to get the numeric list
            encoded = tokenizer.encode(str(data['input']))
            
            # 2. Build the numeric data point
            tokenized_item = {
                "input": encoded.ids, # Now a list of numbers, not text
                "label": data['label'],
                "metadata": data.get('metadata', {})
            }
            
            f_out.write(json.dumps(tokenized_item) + '\n')

# Run the bulk processing
bulk_encode_dataset('train_data.jsonl', 'tokenized_train.jsonl', 'org_tokenizer.json')
print("✅ Bulk Encoding Complete: 'tokenized_train.jsonl' is ready.")

"""
2. Benefits for your "Organization" Pipeline
Zero Latency: The model no longer has to "think" about characters during training; it just reads the IDs directly from the file.
Smaller File Size: Because BPE compresses text (e.g., "Jaisalmer" becomes one ID instead of nine characters), your dataset will take up 30% to 50% less storage on your phone.
Consistency: Every time you train or test, the same words will always map to the exact same IDs, preventing "logic drift" in your medical or engineering models.
"""
