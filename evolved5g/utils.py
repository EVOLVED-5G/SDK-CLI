from cookiecutter.main import cookiecutter


def cookiecutter_generate(location, directory, **kwargs):
    """ Create project from the cookiecutter template in location given
    with the appropriate arguments. """
    cookiecutter(location, directory="template", no_input=True, config_file="evolved5g/my-custom-config.yaml" )
