from enum import Enum

class RfcLanguage(Enum):
    English = "en-US"
    Espanol = "es-ES"
    Italiano = "it-IT"
    Deutsche = "de-DE"
    Francais = "fr-FR"


#print(RfcLanguage['Italiano'].value)