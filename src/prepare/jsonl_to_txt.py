"""
To prepare your data for training a modern BPE tokenizer, you must extract the text from your JSONL (or JSON) files and save it as a clean .txt file. The tokenizer trainer needs a plain text file where it can count character frequencies.
1. Python Script: jsonl_to_txt.py
This script iterates through your JSONL entries, extracts the "input" or "text" field, and writes it to a single text file.
"""
import json

def convert_to_text(input_jsonl, output_txt, text_key='input'):
    """
    input_jsonl: Path to your dataset (e.g., train_data.jsonl)
    output_txt: Name of the text file to create
    text_key: The key in your JSON where the text is stored (e.g., 'input' or 'text')
    """
    count = 0
    with open(input_jsonl, 'r', encoding='utf-8') as f_in, \
         open(output_txt, 'w', encoding='utf-8') as f_out:
        
        for line in f_in:
            try:
                data = json.loads(line)
                # Extract the text and write it with a newline
                text_content = str(data.get(text_key, ""))
                if text_content:
                    f_out.write(text_content + "\n")
                    count += 1
            except json.JSONDecodeError:
                continue
                
    print(f"✅ Success! Processed {count} lines into {output_txt}")

# Run the conversion
# Use 'input' if that's what your NREGA/Puzzle data uses
convert_to_text('train_data.jsonl', 'corpus_for_tokenizer.txt', text_key='input')

"""
Why this step is vital for your "Organization"
Vocabulary Discovery: By feeding the tokenizer your entire text corpus, it "discovers" words unique to your project (like specific NREGA block names or engineering terms).
Frequency Weights: The Byte-Pair Encoding (BPE) algorithm will prioritize merging characters into the tokens you use most often in your JSONL data.
Clean Training: Removing the JSON brackets {} and keys "label": ensures the tokenizer doesn't waste space learning JSON syntax as part of its vocabulary.
4. Running in Termux
Save the script as jsonl_to_txt.py.
Run python jsonl_to_txt.py.
Check the file size with ls -lh corpus_for_tokenizer.txt.
"""
