import pytest

from populus.project import Project
from populus.deployment import deploy_contracts


@pytest.fixture()
def project(request):
    # This should probably be configurable using the `request` fixture but it's
    # unclear what needs to be configurable.
    return Project()


@pytest.yield_fixture()
def chain(request, project):
    # This should probably allow you to specify the test chain to be used based
    # on the `request` object.  It's unclear what the best way to do this is
    # so... punt!
    chain = project.get_chain('testrpc')

    # TODO: this should run migrations.  If `testrpc` it should be snapshotted.
    # In the future we should be able to snapshot the `geth` chains too and
    # save them for faster test runs.

    with chain:
        yield chain


@pytest.fixture()
def web3(chain):
    return chain.web3


@pytest.fixture()
def contracts(chain):
    return chain.contract_factories


@pytest.fixture()
def deployed_contracts(project, web3):
    # TODO: This should really just load from the registrar since at this point
    # the migrations have been run.
    return deploy_contracts(
        web3=web3,
        compiled_contracts=project.compiled_contracts,
    )


@pytest.fixture()
def accounts(web3):
    return web3.eth.accounts
