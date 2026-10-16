
API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 15

SCORE_MIN = 0
SCORE_MAX = 100

BANDS = [
    (0, "low", "Low score", "This score is an estimate, not a diagnosis."),
    (40, "moderate", "Moderate score", "Consider reviewing your daily habits and wellbeing."),
    (70, "high", "High score", "Consider maintaining supportive routines and checking in with yourself."),
]
