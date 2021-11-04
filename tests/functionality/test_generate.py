import pytest

from facelo.challenge.generate import gen_chall_data_random


@pytest.mark.usefixtures("db")
class TestGenerate:

    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize(
        "users, images, trials, questions, challenges",
        [(10, 20, 20, 1, 0)],
        indirect=True,
    )
    def test_gen_chall_data_random(self):
        chall_data = gen_chall_data_random(12)
