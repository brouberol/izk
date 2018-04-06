import pytest
import unittest.mock as mock

from kazoo.exceptions import NoNodeError, NotEmptyError

from izk.validation import CommandValidationError
import izk.runner


@pytest.fixture
def zk_runner():
    """A runner of shell commands with a mocked zk client"""
    zkcli = mock.MagicMock(read_only=True)
    return izk.runner.ZkCommandRunner(zkcli)


@pytest.fixture
def rw_zk_runner():
    """A runner of shell commands with a mocked zk client"""
    zkcli = mock.MagicMock(read_only=False)
    return izk.runner.ZkCommandRunner(zkcli)


def test_command_usage():
    expected = """Usage: help [command]
Examples:
- help     # shows the list of commands
- help ls  # shows a command help"""
    assert izk.runner.command_usage('help') == expected


def test_run_invalid_command(zk_runner):
    with pytest.raises(CommandValidationError):
        zk_runner.run('ls')


def test_tokenize(zk_runner):
    cmd = "set /test '{\"k\": \"v\"}'"
    assert zk_runner._tokenize(cmd) == ['set', '/test', "'{\"k\": \"v\"}'"]


def test_exit(zk_runner):
    with pytest.raises(KeyboardInterrupt):
        zk_runner.run('exit')


def test_quit(zk_runner):
    with pytest.raises(KeyboardInterrupt):
        zk_runner.run('quit')


def test_help_general(zk_runner):
    out = zk_runner.run('help')
    expected = """Commands:
- create: Recursively create a path if it doesn't exist
- delete: Delete a leaf ZNode
- edit: Edit the content of a ZNode
- exit: Close the shell
- get: Display the content of a ZNode
- help: Print the help of a command
- ls: Display the children of a ZNode
- quit: Close the shell
- raw: Send the 4-letter-word command to the zookeeper server
- rmr: Recursively delete all children ZNodes, along with argument node.
- set: Set or update the content of a ZNode
- stat: Display a ZNode's metadata
- toggle_write: Activate/deactivate read-only mode"""
    assert out == expected


def test_help_ls(zk_runner):
    out = zk_runner.run('help ls')
    expected = """Display the children of a ZNode

Usage: ls <path>
Example: ls /test"""
    assert out == expected


def test_ls_nonexisting_path(zk_runner):
    with mock.patch.object(zk_runner.zkcli, 'get_children', side_effect=NoNodeError):
        with pytest.raises(NoNodeError):
            zk_runner.run('ls /nope')


def test_ls(zk_runner):
    with mock.patch.object(
        zk_runner.zkcli, 'get_children', side_effect=[
            ['a', 'b', 'c'],  # 3 nodes found in path
            [], [], [],  # none of these 3 nodes have children nodes
        ]
    ):
        nodes = zk_runner.run('ls /')
        assert nodes.split() == ['a', 'b', 'c']


def test_get_nonexisting_node(zk_runner):
    with mock.patch.object(zk_runner.zkcli, 'get', side_effect=NoNodeError):
        with pytest.raises(NoNodeError):
            zk_runner.run('get /nope')


def test_get(zk_runner):
    data = 'somedata'.encode('utf-8')
    with mock.patch.object(zk_runner.zkcli, 'get', return_value=(data, None)):
        assert zk_runner.run('get /test') == 'somedata'


def test_create_writes_disabled(zk_runner):
    with pytest.raises(izk.runner.UnauthorizedWrite):
        with mock.patch.object(zk_runner.zkcli, 'ensure_path', return_value=None):
            zk_runner.run('create /test')


def test_create(rw_zk_runner):
    with mock.patch.object(rw_zk_runner.zkcli, 'ensure_path', return_value=None):
        assert rw_zk_runner.run('create /test') is None


def test_set_with_data_node_not_exist(rw_zk_runner):
    with mock.patch.object(rw_zk_runner.zkcli, 'exists', return_value=False):
        rw_zk_runner.run("set /test 'plop'")
        rw_zk_runner.zkcli.create.assert_called_once_with('/test', b'plop')


def test_set_with_data_node_exists(rw_zk_runner):
    with mock.patch.object(rw_zk_runner.zkcli, 'exists', return_value=True):
        rw_zk_runner.run("set /test 'plop'")
        rw_zk_runner.zkcli.set.assert_called_once_with('/test', b'plop')


@mock.patch('izk.runner.ask_for_confirmation', return_value=False)
def test_delete_no_confirmation(confirm_mock, rw_zk_runner):
    rw_zk_runner.run('delete /test')
    assert rw_zk_runner.zkcli.delete.call_count == 0


@mock.patch('izk.runner.ask_for_confirmation', return_value=True)
def test_delete_with_confirmation(confirm_mock, rw_zk_runner):
    rw_zk_runner.run('delete /test')
    rw_zk_runner.zkcli.delete.assert_called_once_with('/test')


@mock.patch('izk.runner.ask_for_confirmation', return_value=True)
def test_delete_not_empty(confirm_mock, rw_zk_runner):
    rw_zk_runner.zkcli.delete.side_effect = NotEmptyError
    with pytest.raises(NotEmptyError):
        rw_zk_runner.run('delete /test')


@mock.patch('izk.runner.ask_for_confirmation', return_value=True)
def test_delete_does_not_exist(confirm_mock, rw_zk_runner):
    rw_zk_runner.zkcli.delete.side_effect = NoNodeError
    with pytest.raises(NoNodeError):
        rw_zk_runner.run('delete /test')


@mock.patch('izk.runner.ask_for_confirmation', return_value=False)
def test_rmr_no_confirmation(confirm_mock, rw_zk_runner):
    rw_zk_runner.run('rmr /test')
    assert rw_zk_runner.zkcli.delete.call_count == 0


@mock.patch('izk.runner.ask_for_confirmation', return_value=True)
def test_rmr_with_confirmation(confirm_mock, rw_zk_runner):
    rw_zk_runner.run('rmr /test')
    rw_zk_runner.zkcli.delete.assert_called_once_with('/test', recursive=True)


def test_toggle_write(zk_runner):
    assert zk_runner.zkcli.read_only is True
    zk_runner.toggle_write()
    assert zk_runner.zkcli.read_only is False


def test_raw(zk_runner):
    zk_runner.run('raw srvr')
    zk_runner.zkcli.command.assert_called_once_with(b'srvr')
