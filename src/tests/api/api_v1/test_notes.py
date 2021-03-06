from src.tests.conftest import client
from sqlalchemy.orm import Session

from src.core.config import settings
from src.tests.utils.utils import random_lower_string
from src.tests.utils.user import create_random_user_by_api, user_authentication_headers
from src.tests.utils.note import creat_random_note


def test_create_note():
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    data = {
        "title": random_lower_string(),
        "content": random_lower_string(),
        "public": False,
    }

    response = client.post(
        f"{settings.API_V1_STR}/notes/",
        headers=token,
        json=data
    )
    note = response.json()

    assert note["author"] == username
    assert note["title"] == data["title"]
    assert note["content"] == data["content"]
    assert note["public"] == data["public"]


def test_get_current_user_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)

    creat_random_note(db, public=False, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/",
        headers=token,
    )
    notes = response.json()

    assert len(notes) == True


def test_get_note_by_id(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/id/?id={note.id}",
        headers=token,
    )
    stored_note = response.json()

    assert stored_note["author"] == note.author
    assert stored_note["title"] == note.title
    assert stored_note["content"] == note.content
    assert stored_note["public"] == note.public


def test_update_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    data = {
        "title": random_lower_string(),
        "content": random_lower_string(),
        "public": False,
    }

    response = client.put(
        f"{settings.API_V1_STR}/notes/?id={note.id}",
        headers=token,
        json=data
    )
    new_note = response.json()

    assert new_note["author"] == username
    assert new_note["title"] == data["title"]
    assert new_note["content"] == data["content"]
    assert new_note["public"] == data["public"]


def test_delete_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    response = client.delete(
        f"{settings.API_V1_STR}/notes/?id={note.id}",
        headers=token,
    )

    assert response.status_code == 200


def test_get_all_public_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    creat_random_note(db, public=True, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/public-all",
    )
    notes = response.json()

    assert response.status_code == 200
    assert len(notes) >= 1


def test_get_public_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    creat_random_note(db, public=True, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/public-author?author={username}",
    )
    notes = response.json()

    assert response.status_code == 200
    assert len(notes) == True


def test_get_public_note_by_id(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=True, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/public-id?id={note.id}",
    )
    stored_note = response.json()

    assert response.status_code == 200
    assert stored_note["author"] == note.author
    assert stored_note["title"] == note.title
    assert stored_note["content"] == note.content
    assert stored_note["public"] == note.public


def test_search_all_public_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=True, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/public-search-all?text={note.title}",
    )
    search_result = response.json()

    assert response.status_code == 200
    assert len(search_result) >= 1


def test_search_public_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=True, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/public-search-author?text={note.title}&author={note.author}",
    )
    search_result = response.json()

    assert response.status_code == 200
    assert len(search_result) == True
    assert search_result[0]["author"] == username


def test_search_current_user_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    token = user_authentication_headers(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    response = client.get(
        f"{settings.API_V1_STR}/notes/search?text={note.title}",
        headers=token,
    )
    search_result = response.json()

    assert response.status_code == 200
    assert len(search_result) == True
    assert search_result[0]["author"] == username
    assert search_result[0]["public"] == False
