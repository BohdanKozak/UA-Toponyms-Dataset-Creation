import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # 1. Whitespace cleaning
    text = re.sub(r'\s+', ' ', text).strip()
    # 2. HTML artifacts
    text = re.sub(r'<[^>]*>', '', text)
    return text

def normalize_text(text: str) -> str:
    # 1. Уніфікація апострофів
    text = re.sub(r"['`‘´]", "’", text)
    # 2. Уніфікація тире/дефісів
    text = re.sub(r"[–—−]", "-", text)
    return text

def mask_pii(text: str) -> str:
    text = re.sub(r'http[s]?://\S+|www\.\S+', '<URL>', text)
    text = re.sub(r'\S+@\S+', '<EMAIL>', text)
    text = re.sub(r'\+?\d{10,12}', '<PHONE>', text)
    return text

def sentence_split(text: str) -> list[str]:
    # Використовуємо простіший підхід для розділення, щоб уникнути помилок look-behind
    # Розділяємо по крапці з пробілом, якщо перед крапкою не скорочення
    # Спрощений список скорочень
    abbr_list = ['м.', 'вул.', 'р.', 'обл.', 'смт.']
    
    # Тимчасово замінюємо крапки в скороченнях на спеціальний символ
    temp_text = text
    for abbr in abbr_list:
        temp_text = temp_text.replace(abbr, abbr.replace('.', '@@@'))
    
    # Розділяємо
    parts = re.split(r'(?<=[.!?])\s+(?=[A-ZА-ЯІЇЄ])', temp_text)
    
    # Повертаємо крапки назад
    sentences = [p.replace('@@@', '.') for p in parts if p.strip()]
    return sentences

def preprocess(text: str) -> dict:
    cleaned = clean_text(text)
    normalized = normalize_text(cleaned)
    masked = mask_pii(normalized)
    return {
        "original": text,
        "clean": cleaned,
        "normalized": normalized,
        "masked": masked,
        "sentences": sentence_split(masked)
    }
