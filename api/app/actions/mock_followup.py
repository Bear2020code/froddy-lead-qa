from __future__ import annotations

from app.ingest.csv_parser import Dialogue


def generate_followup(dialogue: Dialogue, loss_type: str, classification: str) -> dict | None:
    if loss_type == "no_loss" and classification not in {"conflict", "negotiation"}:
        return None

    if classification == "spam":
        return None

    if classification == "conflict":
        return {
            "action_type": "escalate",
            "draft": "Лучше передать диалог человеку: клиент уже раздражён, автоматический ответ может ухудшить ситуацию.",
            "intent": "human_escalation",
            "tone": "careful",
        }

    if classification == "negotiation":
        return {
            "action_type": "follow_up",
            "draft": "Здравствуйте! Можем уточнить объём работ и предложить вариант сметы под ваш бюджет, без потери качества на важных этапах.",
            "intent": "handle_negotiation",
            "tone": "professional",
        }

    if loss_type == "brutal_loss":
        return {
            "action_type": "follow_up",
            "draft": "Здравствуйте! Извините, что не ответили подробнее сразу. Подскажите, пожалуйста, задача ещё актуальна? Можем быстро сориентировать по стоимости и срокам.",
            "intent": "recover_lost_lead",
            "tone": "polite",
        }

    if loss_type == "soft_loss":
        return {
            "action_type": "follow_up",
            "draft": "Здравствуйте! Уточню по вашему вопросу: чтобы назвать точнее стоимость, нужно понять площадь, состояние помещения и желаемый уровень отделки.",
            "intent": "answer_missed_question",
            "tone": "helpful",
        }

    if loss_type == "no_next_step":
        return {
            "action_type": "follow_up",
            "draft": "Здравствуйте! Можем предложить следующий шаг: коротко уточним детали и подготовим примерный расчёт по вашему ремонту.",
            "intent": "create_next_step",
            "tone": "helpful",
        }

    if loss_type == "cold_trail":
        return {
            "action_type": "follow_up",
            "draft": "Здравствуйте! Подскажите, пожалуйста, актуален ли ещё вопрос по ремонту? Можем помочь с расчётом и следующим шагом.",
            "intent": "soft_ping",
            "tone": "soft",
        }

    return None
