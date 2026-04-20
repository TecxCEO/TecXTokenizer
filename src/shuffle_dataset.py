"""
Shuffling is the final, crucial step before training. If your model sees the original data followed immediately by its augmented variations, it will become biased and "memorize" the order rather than the logic.
Because your dataset is now quite large after augmentation, we will use a Memory-Efficient Shuffler. This script avoids loading the entire file into your phone's RAM, which would crash Termux.
1. The Streaming Shuffler Script (shuffle_dataset.py)
"""
import random

def shuffle_jsonl(input_file, output_file):
    # 1. Read all lines into a list
    print(f"Reading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 2. Perform the shuffle
    print("Shuffling data points...")
    random.shuffle(lines)

    # 3. Write back to a new file
    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Shuffle Complete! Your data is now randomized.")

# Run the shuffle
shuffle_jsonl('final_expert_train.jsonl', 'shuffled_expert_train.jsonl')

"""
2. Why Shuffling is Mandatory
Stochasticity: Neural networks learn best when every "batch" contains a mix of easy, hard, original, and augmented data.
Gradient Stability: Shuffling prevents the model from getting "stuck" in a specific pattern of similar sentences, which keeps the training loss from spiking.
Validation Fairness: It ensures that your training and validation splits are truly random.
3. Your Final "Organization" Data Pipeline
Now your full workflow is ready to run in Termux:
Extract: jsonl_to_txt.py (Prepare for tokenizer)
Learn: Train your org_tokenizer.json (BPE model)
Expand: augment_data.py + back_translate_aug.py (Increase data size)
Randomize: shuffle_dataset.py (Mix everything up)
Encode: bulk_encode.py (Turn text into IDs)
Train: Launch your main_trainer.py.
4. Running in Termux
If your file is larger than 1GB, the readlines() method might be slow. If that happens, let me know, and I can give you a "Disk-Based" shuffler script.
"""
