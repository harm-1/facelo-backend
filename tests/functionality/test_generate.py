import pytest

from facelo.challenge.generate import gen_random, gen_sametrial, created_challenges_list
from facelo.challenge.views import get_recent_challenges, get_recent_challenges


@pytest.mark.usefixtures("db")
class TestGenerate:

    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)],
                             indirect=True)
    def test_gen_chall_data_random(self, user, question):

        existing_challs = created_challenges_list(get_recent_challenges(user, question, 62))
        chall_data = gen_random(12, existing_challs)
        assert chall_data != gen_random(12, existing_challs)
        for trial_pair in chall_data:
            assert trial_pair[0] < trial_pair[1]
            assert trial_pair not in existing_challs

    @pytest.mark.usefixtures("users", "images", "trials", "questions", "challenges")
    @pytest.mark.parametrize("users, images, trials, questions, challenges", [(10, 20, 20, 1, 300)],
                             indirect=True)
    def test_gen_chall_data_sametrial(self, user, question):
        # first find the completed challenges of that user
        completed = get_recent_challenges(user, question, 62)

        existing_challs = created_challenges_list(get_recent_challenges(user, question, 62))
        chall_data = gen_sametrial(12, completed, existing_challs)
        assert chall_data != gen_sametrial(12, completed, existing_challs)
        for trial_pair in chall_data:
            assert trial_pair[0] < trial_pair[1]
            assert trial_pair not in existing_challs


# class TestFilters:

# def test

# class TestOther:
