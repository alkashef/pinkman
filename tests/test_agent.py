from pinkman.agent import generate_reply


def test_generate_reply_constant_on_empty():
    assert generate_reply([]) == "Yeah science!"


def test_generate_reply_constant_on_messages():
    reply = generate_reply([
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello there"},
        {"role": "assistant", "content": "Prev reply"},
    ])
    assert reply == "Yeah science!"
