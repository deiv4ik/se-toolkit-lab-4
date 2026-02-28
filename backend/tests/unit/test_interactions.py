"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1

def test_filter_excludes_interaction_with_different_learner_id():
    """
    Тест проверяет, что при фильтрации по item_id=1
    возвращаются interactions с item_id=1,
    даже если у них learner_id отличается от item_id.
    
    Это unit-тест — он тестирует только функцию _filter_by_item_id
    без реальной БД и без моков.
    """
    # Создаём простые объекты с атрибутами learner_id и item_id
    class SimpleInteraction:
        def __init__(self, learner_id, item_id):
            self.learner_id = learner_id
            self.item_id = item_id
    
    # Создаём тестовые данные
    interactions = [
        SimpleInteraction(learner_id=2, item_id=1),  # должен попасть
        SimpleInteraction(learner_id=1, item_id=2),  # НЕ должен попасть
        SimpleInteraction(learner_id=3, item_id=1),  # должен попасть
    ]
    
    # Импортируем функцию фильтрации
    from app.routers.interactions import _filter_by_item_id
    
    # Применяем фильтр по item_id=1
    filtered = _filter_by_item_id(interactions, 1)
    
    # Проверяем результат
    assert len(filtered) == 2
    assert filtered[0].item_id == 1
    assert filtered[1].item_id == 1
    assert filtered[0].learner_id == 2
    assert filtered[1].learner_id == 3