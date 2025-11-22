import torch #serve per caricare il modello
from transformers import AutoModelForCausalLM, AutoTokenizer #serve per caricare il modello
from PIL import Image #serve per caricare l'immagine

class Vision:
    def __init__(self):
        print("Caricamento modello Vision (Moondream)...")
        self.model_id = "vikhyatk/moondream2"
        self.revision = "2024-08-26"
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            trust_remote_code=True, 
            revision=self.revision
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, revision=self.revision)
        print("Modello Vision caricato.")

    def describe(self, image: Image.Image) -> str:
        enc_image = self.model.encode_image(image)
        description = self.model.answer_question(enc_image, "Describe this image.", self.tokenizer)
        return description