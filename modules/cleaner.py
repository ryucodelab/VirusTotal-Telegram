import os
import shutil





# ==================================
# REMOVE SINGLE FILE
# ==================================


def remove_file(
    file_path: str
):

    try:

        if os.path.exists(
            file_path
        ):

            os.remove(
                file_path
            )

            return True



        return False



    except Exception:

        return False







# ==================================
# REMOVE DIRECTORY
# ==================================


def remove_directory(
    directory: str
):


    try:

        if os.path.exists(
            directory
        ):

            shutil.rmtree(
                directory
            )

            return True



        return False



    except Exception:

        return False







# ==================================
# CLEAN TEMP FILE
# ==================================


def clean_temp(
    file_path: str
):


    return remove_file(
        file_path
    )