from app import get_message, add_numbers


def test_get_message():
    assert get_message() == "Hello! Welcome to Week 12 CI/CD Pipeline - Version 2."


def test_add_numbers():
    assert add_numbers(10, 20) == 30


def test_add_zero():
    assert add_numbers(5, 0) == 5
