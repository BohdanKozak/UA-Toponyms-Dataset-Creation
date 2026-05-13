import re
import json

class InformationExtractor:
    def __init__(self):
        # Регулярні вирази для 3-х типів полів
        # 1. DATE: YYYY-MM-DD або DD.MM.YYYY
        self.date_pattern = r'(\b\d{4}-\d{2}-\d{2}\b)|(\b\d{2}\.\d{2}\.\d{4}\b)'
        
        # 2. GEO_ID: Ідентифікатори типу ID: 123456
        self.id_pattern = r'(?:geonameid|ID|№|id)[:\s]*(\d{5,10})'
        
        # 3. LOCATION_MARKER: Словникові маркери для типів населених пунктів (через контекст)
        self.loc_markers = r'\b(місто|сел[ои]|смт|обл\.|область|район|вул\.)\s+([A-ZА-ЯІЇЄ][a-zа-яіїє\-’]+)'

    def extract_dates(self, text: str) -> list[dict]:
        matches = []
        for match in re.finditer(self.date_pattern, text):
            raw_val = match.group(0)
            # Нормалізація
            norm_val = raw_val.replace('.', '-') if '.' in raw_val else raw_val
            matches.append({
                "field_type": "DATE",
                "value": norm_val,
                "start_char": match.start(),
                "end_char": match.end(),
                "method": "regex_date_v1"
            })
        return matches

    def extract_ids(self, text: str) -> list[dict]:
        matches = []
        for match in re.finditer(self.id_pattern, text, re.IGNORECASE):
            matches.append({
                "field_type": "GEO_ID",
                "value": match.group(1),
                "start_char": match.start(1),
                "end_char": match.end(1),
                "method": "regex_id_context_v1"
            })
        return matches

    def extract_locations(self, text: str) -> list[dict]:
        matches = []
        for match in re.finditer(self.loc_markers, text, re.IGNORECASE):
            matches.append({
                "field_type": "LOCATION",
                "value": match.group(2),
                "start_char": match.start(2),
                "end_char": match.end(2),
                "method": "dict_context_marker"
            })
        return matches

    def extract_all(self, text: str) -> list[dict]:
        return self.extract_dates(text) + self.extract_ids(text) + self.extract_locations(text)
