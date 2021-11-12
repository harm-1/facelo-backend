from typing import Final

CHALLENGE_TYPE_RANDOM: Final[int] = 1
CHALLENGE_TYPE_SAMETRIAL: Final[int] = 2
CHALLENGE_TYPE_TRIANGLE: Final[int] = 3
RANDOM_TRIALS_COUNT: Final[int] = 100
RECENT_CHALLENGES_COUNT: Final[int] = 62
IMAGES_FOLDER: Final[str] = '/backend/images'
ALLOWED_IMAGE_EXTENSIONS: Final[set] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

CHALLENGE_TYPE_DISTIBUTION: Final[dict[int, int]] = {
    CHALLENGE_TYPE_RANDOM: 6,
    CHALLENGE_TYPE_SAMETRIAL: 4,
    CHALLENGE_TYPE_TRIANGLE: 2,
}
