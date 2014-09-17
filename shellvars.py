# http://stackoverflow.com/questions/19429074/how-to-get-the-environment-variable-set-by-a-bash-script-from-inside-a-python-sc
# http://stackoverflow.com/questions/11161373/list-all-environment-variable-names-in-busybox

from subprocess import Popen, PIPE
from os import path

IGNORE_DEFAULT = set(["SHLVL", "PWD", "_"])


def _noscripterror(script_path):
    return IOError("File does not exist: %s" % script_path)


class ShellScriptException(Exception):
    def __init__(self, shell_script, shell_error):
        self.shell_script = shell_script
        self.shell_error = shell_error
        msg = "Error processing script %s: %s" % (shell_script, shell_error)
        Exception.__init__(self, msg)


def list_vars(script_path, ignore=IGNORE_DEFAULT):
    """
    Given a shell script, returns a list of shell variable names.
    Note: this method executes the script, so beware if it contains side-effects.
    :param script_path: Path the a shell script
    :type script_path: str or unicode
    :param ignore: variable names to ignore.  By default we ignore variables
                    that env injects into the script's environment.
                    See IGNORE_DEFAULT.
    :type ignore: iterable
    :return: Key value pairs representing the environment variables defined
            in the script.
    :rtype: list
    """
    if path.isfile(script_path):
        input = (""". "%s"; env | awk -F = '/[a-zA-Z_][a-zA-Z_0-9]*=/ """ % script_path +
                 """{ if (!system("[ -n \\"${" $1 "}\\" ]")) print $1 }'""")
        cmd = "env -i bash".split()

        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data, stderr_data = p.communicate(input=input)
        if stderr_data:
            raise ShellScriptException(script_path, stderr_data)
        else:
            lines = stdout_data.split()
            return [elt for elt in lines if elt not in ignore]
    else:
        raise _noscripterror(script_path)


def get_vars(script_path, ignore=IGNORE_DEFAULT):
    """
    Gets the values of environment variables defined in a shell script.
    Note: this method executes the script potentially many times.
    :param script_path: Path the a shell script
    :type script_path: str or unicode
    :param ignore: variable names to ignore.  By default we ignore variables
                    that env injects into the script's environment.
                    See IGNORE_DEFAULT.
    :type ignore: iterable
    :return: Key value pairs representing the environment variables defined
            in the script.
    :rtype: dict
    """

    # Iterate over every var independently:
    # This is slower than using env, but enables us to capture multiline variables
    return dict((var, get_var(script_path, var)) for var in list_vars(script_path))


def get_var(script_path, var):
    """
    Given a script, and the name of an environment variable, returns the
    value of the environment variable.
    :param script_path: Path the a shell script
    :type script_path: str or unicode
    :param var: environment variable name
    :type var: str or unicode
    :return: str
    """
    if path.isfile(script_path):
        input = '. "%s"; echo -n "$%s"\n'% (script_path, var)
        pipe = Popen(["bash"],  stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data, stderr_data = pipe.communicate(input=input)
        if stderr_data:
            raise ShellScriptException(script_path, stderr_data)
        else:
            return stdout_data
    else:
        raise _noscripterror(script_path)


