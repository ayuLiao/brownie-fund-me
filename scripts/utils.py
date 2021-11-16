from brownie import network, config, accounts, MockV3Aggregator

# Mock
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# Fork
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f'The active network is {network.show_active()}')
    print('Deploying Mocks...')
    # 部署MockV3Aggregator时，判断其长度，大于0，则说明之前部署过，则不再部署
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print('Mocks Deployed')
