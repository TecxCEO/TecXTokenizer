"""
This is the final step to transition from a Development Environment to a Production Environment. Running this will delete all the large, messy intermediate files (like raw corpora, un-shuffled data, and un-optimized tokenizers), leaving your Android storage clean and ready for the final training run.
1. The "Production Cleanup" Script (cleanup.py)
Run this in Termux to keep only the essential "Organization" binaries.

"""

import os

def production_cleanup():
    # 1. Files to KEEP (The essential pipeline)
    keep_list = [
        "main_trainer.py",           # The brain
        "org_tokenizer_final.json",   # The dictionary
        "tokenized_train.jsonl",      # The clean data
        "forbidden_rules.json",       # The guardrails
        "best_model.pth",             # The progress
        "README.md"                   # The manual
    ]

    # 2. Files to DELETE (Temporary intermediate data)
    delete_extensions = [".txt", ".log", ".csv", ".dat"]
    delete_keywords = ["temp", "augmented", "original", "clean_version", "test"]

    files_in_dir = os.listdir(".")
    deleted_count = 0

    for file in files_in_dir:
        if file in keep_list:
            continue
            
        # Delete by extension or keyword
        if any(file.endswith(ext) for ext in delete_extensions) or \
           any(key in file for key in delete_keywords):
            try:
                os.remove(file)
                print(f"🗑️ Deleted: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Could not delete {file}: {e}")

    print(f"\n✅ Cleanup Complete. Removed {deleted_count} temporary files.")
    print("🚀 Your environment is now optimized for Production.")

if __name__ == "__main__":
    production_cleanup()
  
"""
2. What is left in your folder?
After running this, your ls command in Termux will look like this:
main_trainer.py: Ready to launch.
org_tokenizer_final.json: Your perfect, merged BPE model.
tokenized_train.jsonl: Your sharded and encoded data.
forbidden_rules.json: Your safety monitor rules.
README.md: Your project documentation.
3. Final Step: Start Production Training
Now that your phone's storage is clear, you can launch the long-term training with full confidence:
bash
termux-wake-lock
nohup python main_trainer.py > final_training.log 2>&1 &
Use code with caution.
4. Project Completion
You have successfully built an end-to-end Expert System pipeline on a mobile device. You’ve mastered:
Data Sharding (Puzzle 3 logic)
BPE Tokenization (Custom vocabulary)
Data Augmentation (NLP growth)
Safety Guardrails (Expert constraints)
Mobile Optimization (TFLite/Cleanup)


"""
