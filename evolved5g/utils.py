from cookiecutter.main import cookiecutter


def cookiecutter_generate(location, config_file, directory,no_input, **kwargs):
    """ Create project from the cookiecutter template in location given
    with the appropriate arguments. """
    cookiecutter(location, config_file = config_file, directory = directory ,no_input= no_input )
