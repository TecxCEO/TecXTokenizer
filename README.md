# TecXTokenizer
TecX Tokenizer

Expert Knowledge-Based System (v1.0)

Project: Puzzle Solving AI

Environment: Android (Termux / Pydroid 3)
Architecture: BPE Tokenizer + PyTorch LSTM/Transformer + Safety Guardrails
📂 Pipeline Overview
Phase 1: Data Preparation
jsonl_to_txt.py: Extracts raw text from your JSONL datasets to create a training corpus.
train_tokenizer.py: Trains a modern Byte-Pair Encoding (BPE) tokenizer on your specific domain vocabulary (Saved as org_tokenizer.json).
Phase 2: Data Augmentation (Expert Knowledge Growth)
augment_data.py: Uses synonym substitution to double your dataset.
back_translate_aug.py: Uses English ↔ Hindi translation to create natural sentence variations.
shuffle_dataset.py: Randomizes the order of samples to prevent model bias.
Phase 3: Training & Safety
bulk_encode.py: Converts the final text dataset into numeric IDs (Tokens) for fast processing.
main_trainer.py: The core training script. It features:
Streaming Loading: Low RAM usage for mobile.
Safety Monitor: Uses forbidden_rules.json to penalize dangerous or illegal actions.
Checkpointing: Saves best_model.pth automatically.
Phase 4: Deployment & Audit
test_safety.py: Verifies that the Guardrails block forbidden actions.
secure_sync.py: Encrypts logs (AES-256) and pushes them to GitHub.
dashboard.py: Run on PC to analyze the Safety Success Rate and performance trends.
🚀 Quick Start
bash
# 1. Prepare Data
python jsonl_to_txt.py && python train_tokenizer.py

# 2. Augment & Encode
python augment_data.py && python bulk_encode.py

# 3. Train with Wakelock
termux-wake-lock
python main_trainer.py
Use code with caution.
⚠️ Important Notes
Security: Never share your YOUR_SECRET_KEY used in the encryption script.
Hardware: If the phone overheats, reduce batch_size in main_trainer.py.
Medical/Engineering: Always verify model outputs against physical labels and official guidelines.
