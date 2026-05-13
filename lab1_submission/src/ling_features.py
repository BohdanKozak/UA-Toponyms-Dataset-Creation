import stanza

# Завантажуємо українську модель (якщо ще не завантажена)
def download_stanza_ua():
    stanza.download('uk')

class LingProcessor:
    def __init__(self):
        # Ініціалізуємо pipeline для української мови
        # processors: tokenize (токенізація), mwt (multi-word token), pos (частини мови), lemma (лематизація)
        self.nlp = stanza.Pipeline(lang='uk', processors='tokenize,mwt,pos,lemma', use_gpu=True)

    def extract_features(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            return {"lemma_text": "", "pos_seq": "", "tokens": []}
        
        doc = self.nlp(text)
        lemmas = []
        pos_tags = []
        tokens = []

        for sent in doc.sentences:
            for word in sent.words:
                lemmas.append(word.lemma if word.lemma else word.text.lower())
                pos_tags.append(word.upos)
                tokens.append(word.text)

        return {
            "lemma_text": " ".join(lemmas),
            "pos_seq": " ".join(pos_tags),
            "tokens": tokens
        }
