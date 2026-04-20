"""
To create a tokenizer like those used in recent models (GPT-4, Gemini, Llama), use Byte-Pair Encoding (BPE). BPE identifies the most common pairs of characters and merges them into tokens. This approach is efficient for domain-specific data.
1. Prerequisites
The tokenizers library is needed. It is developed by Hugging Face.

pip install tokenizers

2. Code: Training a Domain-Specific Tokenizer
This script reads domain data and creates a tokenizer.json file.
"""

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.processors import TemplateProcessing

# 1. Initialize the BPE Model
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))

# 2. Pre-Tokenization: Splitting by Whitespace
tokenizer.pre_tokenizer = Whitespace()

# 3. Configure the Trainer
trainer = BpeTrainer(
    vocab_size=5000, 
    min_frequency=2,
    show_progress=True,
    special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
)

# 4. Train the Tokenizer
files = ["organization_data.txt"] 
tokenizer.train(files, trainer)

# 5. Post-Processing
tokenizer.post_processor = TemplateProcessing(
    single="[CLS] $A [SEP]",
    pair="[CLS] $A [SEP] $B:1 [SEP]:1",
    special_tokens=[("[CLS]", 2), ("[SEP]", 3)],
)

# 6. Save the Tokenizer
tokenizer.save("org_tokenizer.json")
print("✅ Tokenizer created and saved as 'org_tokenizer.json'")

