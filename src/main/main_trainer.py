"""
Update Trainer
Now, in main_trainer.py, make sure your model's Embedding Layer matches the vocab_size of your new tokenizer
"""
# If your BPE tokenizer was trained with 5000 tokens:
vocab_size = 5000 
embedding_dim = 128
model = nn.Sequential(
    nn.Embedding(vocab_size, embedding_dim), # New Embedding Layer
    nn.LSTM(embedding_dim, 256, batch_first=True),
    nn.Linear(256, 12)
)

"""
 Running in Termux
Run python bulk_encode.py.
Once finished, you can delete the old corpus_for_tokenizer.txt to save space.
Check your progress: head -n 1 tokenized_train.jsonl to see the new numeric format.
"""
