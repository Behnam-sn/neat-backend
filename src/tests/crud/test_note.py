from sqlalchemy.orm import Session

from src import crud
from src.schemas.note import NoteUpdate
from src.tests.utils.note import creat_random_note
from src.tests.utils.user import create_random_user_by_api
from src.tests.utils.utils import random_lower_string


def test_create_public_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    note = creat_random_note(db, public=True, author=username)

    assert note
    assert note.public == True


def test_create_private_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    note = creat_random_note(db, public=False, author=username)

    assert note
    assert note.public == False


def test_get_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    creat_random_note(db, public=False, author=username)
    notes = crud.get_notes_by_author(db, author=username)

    assert len(notes) == True


def test_get_note_by_id(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)
    stored_note = crud.get_note_by_id(db, id=note.id)

    assert stored_note
    assert stored_note == note
    assert note.id == stored_note.id
    assert note.title == stored_note.title
    assert note.content == stored_note.content
    assert note.author == stored_note.author


def test_update_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    new_title = random_lower_string()
    new_content = random_lower_string()
    note_update = NoteUpdate(
        title=new_title,
        content=new_content,
        public=False
    )
    new_note = crud.update_note(db, id=note.id, note_update=note_update)

    assert note.id == new_note.id
    assert note.author == new_note.author
    assert new_note.title == new_title
    assert new_note.content == new_content


def test_remove_note(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)

    delete_note = crud.remove_note(db, id=note.id)
    stored_note = crud.get_note_by_id(db, id=note.id)

    assert stored_note is None
    assert delete_note == note


def test_get_all_public_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    creat_random_note(db, public=True, author=username)
    notes = crud.get_all_public_notes(db)

    assert notes


def test_get_public_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)

    creat_random_note(db, public=True, author=username)
    notes = crud.get_public_notes_by_author(db, author=username)

    assert len(notes) == True


def test_search_all_public_notes(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=True, author=username)
    search_result = crud.search_all_public_notes(db, text=note.title)

    assert len(search_result) == True


def test_search_public_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=True, author=username)
    search_result = crud.search_public_notes_by_author(
        db,
        text=note.title,
        author=username
    )

    assert len(search_result) == True
    assert search_result[0].author == username


def test_search_notes_by_author(db: Session):
    username = random_lower_string()
    password = random_lower_string()

    create_random_user_by_api(username=username, password=password)
    note = creat_random_note(db, public=False, author=username)
    search_result = crud.search_notes_by_author(
        db,
        text=note.title,
        author=username
    )

    assert len(search_result) == True
    assert search_result[0].author == username
    assert search_result[0].public == False
