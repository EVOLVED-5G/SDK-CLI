from cookiecutter.main import cookiecutter


def cookiecutter_generate(location, directory, **kwargs):
    """ Create project from the cookiecutter template in location given
    with the appropriate arguments. """
    # extra_context = kwargs['extra_context']
    cookiecutter(location, directory="template" ) #, extra_context=extra_context)
