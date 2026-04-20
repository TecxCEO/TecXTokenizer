"""

Back-translation is one of the most powerful ways to create natural variations of your expert data. It works by translating your English input into a second language (like Hindi) and then back into English. This often results in different sentence structures that carry the same meaning.
1. The Back-Translation Script (back_translate_aug.py)
Since you are working in Termux, we will use a lightweight library called deep-translator.
# Install the translator in Termux

pip install deep-translator
"""

import json
import time
from deep_translator import GoogleTranslator

def back_translate(text, target_lang='hi'):
    try:
        # Step 1: English -> Hindi
        to_hindi = GoogleTranslator(source='en', target=target_lang).translate(text)
        # Step 2: Hindi -> English
        back_to_en = GoogleTranslator(source=target_lang, target='en').translate(to_hindi)
        return back_to_en
    except Exception as e:
        print(f"Error translating: {e}")
        return text

def run_bt_augmentation(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            data = json.loads(line)
            # 1. Write the original
            f_out.write(json.dumps(data) + '\n')
            
            # 2. Back-translate and write (with a small delay to avoid API limits)
            bt_text = back_translate(str(data['input']))
            if bt_text != data['input']:
                bt_data = data.copy()
                bt_data['input'] = bt_text
                bt_data['metadata']['aug_type'] = 'back_translation'
                f_out.write(json.dumps(bt_data) + '\n')
                time.sleep(0.5) 

# Run the script
run_bt_augmentation('augmented_train_data.jsonl', 'final_expert_train.jsonl')

"""
2. Why this is the "Gold Standard" for Expert Systems
Paraphrasing: It changes "The budget was approved" to "The approval of the budget was granted," which helps the model understand grammar more deeply.
Contextual Variation: It’s especially useful for NREGA data, as many terms have unique direct translations in Hindi that return to English as slightly more formal or "official" sounding phrases.

3. Implementation Order (Final Pipeline)
Original Data: train_data.jsonl
Synonym Swap: Run augment_data.py (Double the data).
Back-Translate: Run back_translate_aug.py (Triple or quadruple the data).
Bulk Encode: Run bulk_encode.py to turn everything into tokens.
Train: Launch your model.
4. Running in Termux
This script requires an internet connection for the Google Translate API. If you have a large dataset, run it overnight with the Wakelock on.
"""
