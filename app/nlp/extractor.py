import re
from typing import List, Dict

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")

MARKERS = [
    "хочу", "нужно", "проблем", "боль", "неудобн", "сложно",
    "бесит", "нравится", "использую", "трачу", "устал", "не могу",
    "надоело", "приходится", "хотелось бы",
]

def split_insights(transcript: str) -> List[str]:
    sentences = [s.strip() for s in SENT_SPLIT.split(transcript) if s.strip()]
    insights = [s for s in sentences
                if any(m in s.lower() for m in MARKERS)]
    return insights if insights else sentences[:5]

def to_jtbd(texts: List[str]) -> Dict[str, str]:
    joined = " ".join(texts).lower()
    situation = "Когда пользователь работает с продуктом"
    motivation = "он хочет достичь результата быстрее"
    outcome = "чтобы получить ценность без лишних действий"

    if any(w in joined for w in ["быстр", "скорост", "медленн"]):
        motivation = "он хочет ускорить процесс"
    if any(w in joined for w in ["прост", "понятн", "сложн"]):
        motivation = "он хочет простой интерфейс"
    if any(w in joined for w in ["надёжн", "стабильн", "падает"]):
        motivation = "он хочет надёжную работу"
    if any(w in joined for w in ["интеграц", "api", "1с"]):
        motivation = "он хочет интеграцию с другими системами"

    return {"situation": situation, "motivation": motivation,
            "outcome": outcome}
