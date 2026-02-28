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


def test_filter_returns_empty_for_non_existent_item_id() -> None:
    """
    Edge case: filtering with an item_id that doesn't match any interaction.
    Should return an empty list.
    """
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2), _make_log(3, 3, 3)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


def test_filter_with_negative_item_id() -> None:
    """
    Edge case: filtering with a negative item_id.
    Negative IDs are invalid in the database but the filter should handle them gracefully.
    """
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, -1)
    assert result == []


def test_filter_with_zero_item_id() -> None:
    """
    Boundary value: zero as item_id.
    Zero is a boundary between negative and positive integers.
    """
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 0)
    assert result == []


def test_filter_single_item_list_matching() -> None:
    """
    Boundary case: single item list with matching item_id.
    Tests the boundary between empty list and multiple items.
    """
    interactions = [_make_log(1, 1, 5)]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].item_id == 5


def test_filter_multiple_same_item_id_different_learner() -> None:
    """
    Edge case: multiple interactions with the same item_id but different learner_ids.
    Ensures all matching interactions are returned regardless of learner_id.
    """
    interactions = [
        _make_log(1, learner_id=10, item_id=5),
        _make_log(2, learner_id=20, item_id=5),
        _make_log(3, learner_id=30, item_id=5),
        _make_log(4, learner_id=40, item_id=6),  # different item_id
    ]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 3
    assert all(r.item_id == 5 for r in result)
    assert {r.learner_id for r in result} == {10, 20, 30}