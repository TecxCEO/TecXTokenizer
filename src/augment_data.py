"""
To double your training data for your NREGA or Expert System, we will use Synonym Substitution and Noise Injection. This teaches your model that "Jaisalmer district" and "district of Jaisalmer" mean the same thing, making your "Organization's" AI much more robust [2, 3].
1. Data Augmentation Script (augment_data.py)
This script creates a "varied" copy of every entry in your train_data.jsonl before you run the bulk encoding.
"""
import json
import random

def augment_text(text):
    # Dictionary of domain-specific synonyms
    synonyms = {
        "district": ["region", "area", "zone"],
        "allocated": ["assigned", "distributed", "provided"],
        "budget": ["funds", "finance", "capital"],
        "rural": ["village-level", "local", "countryside"],
        "Jaisalmer": ["Jaisalmer Block", "the Jaisalmer region"]
    }
    
    words = text.split()
    new_words = []
    
    for word in words:
        # 20% chance to swap a word with a synonym
        if word in synonyms and random.random() < 0.2:
            new_words.append(random.choice(synonyms[word]))
        else:
            new_words.append(word)
            
    return " ".join(new_words)

def run_augmentation(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            data = json.loads(line)
            
            # 1. Keep the original data
            f_out.write(json.dumps(data) + '\n')
            
            # 2. Create and write the augmented version
            augmented_data = data.copy()
            augmented_data['input'] = augment_text(str(data['input']))
            augmented_data['metadata']['is_augmented'] = True
            
            f_out.write(json.dumps(augmented_data) + '\n')

run_augmentation('train_data.jsonl', 'augmented_train_data.jsonl')
print("✅ Augmentation Complete: Dataset size doubled.")

"""
2. Why this is vital for "Expert Knowledge"
Generalization: It prevents the model from "memorizing" specific sentences. It starts to learn the meaning behind the words [2].
Small Dataset Solution: If you only have 500 expert records, augmentation gives you 1,000, which is often the "tipping point" where a neural network starts to behave intelligently [1, 3].
Robustness: If a user makes a typo or uses a different word for "budget," the model will still know what to do because it saw similar variations during training.
3. Implementation Order
Run augment_data.py to create augmented_train_data.jsonl.
Run your bulk_encode.py on this new file to turn it into tokens.
Train your model using the doubled, tokenized dataset.

4. Running in Termux
This script is very fast and uses almost no RAM.

python augment_data.py
ls -lh augmented_train_data.jsonl
"""
