"""
The Python script to convert your CSV data into JSONL format. This format is ideal for training on your Android phone because it processes one line at a time, keeping RAM usage low.
"""
import csv
import json

def convert(csv_input, jsonl_output):
    with open(csv_input, mode='r', encoding='utf-8') as f_in, \
         open(jsonl_output, mode='w', encoding='utf-8') as f_out:
        
        reader = csv.DictReader(f_in)
        for row in reader:
            # 1. Process the state string into a list of integers
            # Cleans up brackets and splits by comma
            raw_state = row['state'].strip("[]").split(',')
            state_ints = [int(x.strip()) for x in raw_state]
            
            # 2. Build the JSON object
            data_point = {
                "input": state_ints,
                "label": int(row['label']),
                "metadata": {
                    "difficulty": row.get('difficulty', 'unknown'),
                    "depth": int(row.get('scramble_depth', 0))
                }
            }
            
            # 3. Write as a single line in the JSONL file
            f_out.write(json.dumps(data_point) + '\n')

# Run the conversion
convert('train_data.csv', 'train_data.jsonl')
print("Conversion complete: train_data.jsonl is ready for training.")

"""
Steps to Run in Termux
Save the file: Copy the code above into a file named csv_to_jsonl.py in your Termux home directory.
Ensure your CSV is present: Make sure your train_data.csv is in the same folder.
Execute:
bash
python csv_to_jsonl.py
Use code with caution.
Verify: Type ls to see the new train_data.jsonl file.
Why this helps your training
Sequential Loading: In your training loop, you can use for line in open('train_data.jsonl'): to load data without using all your phone's memory.
Error Isolation: If one line in your data is corrupted, the JSONL reader will skip just that line instead of crashing the entire dataset load.
"""
