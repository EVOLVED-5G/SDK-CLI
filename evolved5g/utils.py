from cookiecutter.main import cookiecutter


def cookiecutter_generate(location, no_input=False, **kwargs):
    """ Create project from the cookiecutter template in location given
    with the appropriate arguments. """
    # extra_context = kwargs['extra_context']
    cookiecutter(location, no_input=no_input) #, extra_context=extra_context)
