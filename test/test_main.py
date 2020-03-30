from   traceback                     import format_exception
from   click.testing                 import CliRunner
import pytest
from   check_wheel_contents.__main__ import main
from   check_wheel_contents.checker  import NO_CONFIG
from   check_wheel_contents.checks   import Check

def show_result(r):
    if r.exception is not None:
        return ''.join(format_exception(*r.exc_info))
    else:
        return r.output

@pytest.mark.parametrize('options,configargs', [
    (
        [],
        {
            "configpath": None,
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--no-config'],
        {
            "configpath": NO_CONFIG,
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--config', 'foo.cfg'],
        {
            "configpath": 'foo.cfg',
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--config', 'foo.cfg', '--no-config'],
        {
            "configpath": NO_CONFIG,
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--no-config', '--config', 'foo.cfg'],
        {
            "configpath": 'foo.cfg',
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--select', 'W001,W2', '--ignore=W201'],
        {
            "configpath": None,
            "select": {Check.W001, Check.W201, Check.W202},
            "ignore": {Check.W201},
            "toplevel": None,
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--toplevel', 'foo,bar/'],
        {
            "configpath": None,
            "select": None,
            "ignore": None,
            "toplevel": ['foo', 'bar/'],
            "package": (),
            "src_dir": (),
        },
    ),

    (
        ['--package=foo', '--src-dir', 'src'],
        {
            "configpath": None,
            "select": None,
            "ignore": None,
            "toplevel": None,
            "package": ('foo',),
            "src_dir": ('src',),
        },
    ),
])
def test_options2configargs(fs, mocker, options, configargs):
    fs.create_dir('/usr/src/project/foo')
    fs.create_dir('/usr/src/project/src')
    fs.create_file('/usr/src/project/foo.cfg')
    fs.cwd = '/usr/src/project'
    mock_checker = mocker.patch(
        'check_wheel_contents.__main__.WheelChecker',
        autospec=True,
    )
    r = CliRunner().invoke(main, options)
    assert r.exit_code == 0, show_result(r)
    assert mock_checker.method_calls \
        == [mocker.call().configure_options(**configargs)]
