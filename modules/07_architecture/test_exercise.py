import sqlite3

import pytest


@pytest.fixture(params=["memory", "sqlite"])
def repo(request, impl):
    """Every test using this fixture runs twice: once per adapter."""
    if request.param == "memory":
        yield impl.InMemoryTaskRepository()
    else:
        connection = sqlite3.connect(":memory:")
        yield impl.SqliteTaskRepository(connection)
        connection.close()


@pytest.fixture
def service(impl, repo):
    return impl.TaskService(repo)


# --- Repository contract: both adapters must behave identically. ---


def test_add_assigns_increasing_ids_from_one(repo):
    assert [repo.add("a").id, repo.add("b").id, repo.add("c").id] == [1, 2, 3]


def test_added_task_is_not_done(impl, repo):
    assert repo.add("write tests") == impl.Task(id=1, title="write tests", done=False)


def test_get_returns_the_stored_task(impl, repo):
    repo.add("first")
    repo.add("second")
    assert repo.get(2) == impl.Task(id=2, title="second")


def test_get_unknown_id_returns_none(repo):
    assert repo.get(42) is None


def test_all_returns_tasks_in_id_order(repo):
    for title in ["a", "b", "c"]:
        repo.add(title)
    assert [task.title for task in repo.all()] == ["a", "b", "c"]


def test_all_of_empty_repository(repo):
    assert repo.all() == []


def test_save_persists_changes(repo):
    task = repo.add("ship it")
    task.done = True
    task.title = "shipped"

    repo.save(task)

    stored = repo.get(task.id)
    assert (stored.title, stored.done) == ("shipped", True)


def test_changes_are_not_persisted_without_save(repo):
    repo.add("untouched")

    repo.get(1).done = True
    repo.all()[0].title = "sneaky"

    stored = repo.get(1)
    assert (stored.title, stored.done) == ("untouched", False)


def test_sqlite_repository_survives_being_reopened(impl, tmp_path):
    database = tmp_path / "tasks.db"

    connection = sqlite3.connect(database)
    impl.SqliteTaskRepository(connection).add("persisted")
    connection.close()

    connection = sqlite3.connect(database)
    reopened = impl.SqliteTaskRepository(connection)
    assert [task.title for task in reopened.all()] == ["persisted"]
    connection.close()


# --- Service: the business rules, independent of storage. ---


def test_create_stores_a_task(service, repo):
    task = service.create("learn architecture")
    assert repo.get(task.id).title == "learn architecture"


def test_create_strips_whitespace(service):
    assert service.create("  tidy up  ").title == "tidy up"


@pytest.mark.parametrize("title", ["", "   ", "\n\t"])
def test_create_rejects_empty_titles(service, repo, title):
    with pytest.raises(ValueError):
        service.create(title)
    assert repo.all() == []


def test_complete_marks_task_done_and_persists_it(service, repo):
    task = service.create("finish module 7")

    completed = service.complete(task.id)

    assert completed.done is True
    assert repo.get(task.id).done is True


def test_complete_unknown_task_raises(impl, service):
    with pytest.raises(impl.TaskNotFound):
        service.complete(99)


def test_pending_excludes_completed_tasks(service):
    service.create("one")
    two = service.create("two")
    service.create("three")
    service.complete(two.id)

    assert [task.title for task in service.pending()] == ["one", "three"]
