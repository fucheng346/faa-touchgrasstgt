import os


def init_files():
    """
    Create required data files if they don't exist
    """

    if not os.path.exists("moods.txt"):
        with open("moods.txt", "w") as f:
            f.write("")

    if not os.path.exists("users.txt"):
        with open("users.txt", "w") as f:
            f.write("")
