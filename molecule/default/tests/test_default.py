import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_teleport_installation(host):
    teleport_run = host.run("teleport version")
    tctl_run = host.run("tctl version")
    package = host.file("/tmp/teleport-v3.1.6-linux-amd64/")

    assert 'v3.1.6' in teleport_run.stdout
    assert 'v3.1.6' in tctl_run.stdout
    assert 'Enterprise' not in teleport_run.stdout
    assert not package.exists


@pytest.mark.parametrize('path', [
    '/var/lib/teleport',
    '/etc/teleport/',
    '/etc/teleport/ssl'
])
def test_teleport_directory(host, path):
    dir = host.file(path)

    assert dir.is_directory
    assert dir.exists
    assert dir.user == 'ubuntu'
    assert dir.group == 'ubuntu'


@pytest.mark.parametrize('path', [
    '/etc/teleport/teleport.yml',
    '/etc/systemd/system/teleport.service',
])
def test_teleport_files(host, path):
    file = host.file(path)

    assert file.is_file
    assert file.exists
