import re, sys, collections, difflib, logging, unicodedata
logging.disable(logging.CRITICAL)
sys.path.insert(0, "src")
from verify_text import words, pdf_text, src  # reaproveita normalização
