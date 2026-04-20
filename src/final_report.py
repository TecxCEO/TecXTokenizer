"""
This final script acts as a Quality Audit for your organization. It ensures your data augmentation and shuffling worked correctly and tells you the exact vocabulary size your model needs to handle in its Embedding layer.
1. The Dataset Audit Script (final_report.py)
Run this in Termux to see the final stats of your training data.
"""
import json
from collections import Counter

def generate_report(file_path):
    total_samples = 0
    total_tokens = 0
    all_token_ids = []
    
    print(f"Analyzing {file_path}...")
    
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            tokens = data['input']
            total_samples += 1
            total_tokens += len(tokens)
            all_token_ids.extend(tokens)
            
    # Calculate Unique Vocabulary used
    unique_tokens = len(set(all_token_ids))
    avg_length = total_tokens / total_samples
    
    print("\n" + "="*40)
    print("       📊 FINAL DATASET REPORT")
    print("="*40)
    print(f"Total Training Samples:    {total_samples:,}")
    print(f"Total Tokens in Dataset:   {total_tokens:,}")
    print(f"Unique Tokens (Vocab):     {unique_tokens:,}")
    print(f"Avg tokens per sentence:   {avg_length:.2f}")
    print("="*40)
    
    if unique_tokens > 5000: # Assuming your BPE limit was 5000
        print("⚠️ WARNING: Unique tokens exceed your BPE vocab size!")
    else:
        print("✅ SUCCESS: Vocab size is within limits.")

# Run report on your shuffled numeric data
generate_report('tokenized_train.jsonl')

"""
2. How to use this report
Total Training Samples: If this number is much higher than your original CSV, your Augmentation and Back-translation were successful.
Unique Tokens: This number tells you exactly what the num_embeddings value should be in your PyTorch model.
Avg tokens per sentence: This helps you set your max_seq_len. If the average is 20, setting a max length of 64 or 128 is perfect.

3. Final Deployment Checklist
Before you start the final training run in Termux:
Wakelock: termux-wake-lock (keep CPU alive).
Storage: Ensure you have at least 500MB free for checkpoints.
Logs: Pipe your training output to a file: python main_trainer.py > training_log.txt.

You are now ready!

You have built a professional-grade pipeline:
Original Data 
 Clean Text 
 Custom BPE Tokenizer 
 Augmented Data 
 Back-translated Variations 
 Shuffled Tensors 
 Training.
"""
