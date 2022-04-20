from pywebio import *
from pywebio.output import *
from pywebio.input import *
import config
from web3 import Web3
import requests
import json


@use_scope('dashboard', clear=True)
def put_addresses(web3):
    address = input(
        type=TEXT,
        required=True,
        label='Ethereum Address',
        placeholder='Enter address to lookup'
    )
    balance = web3.eth.get_balance(address)
    balance_usd = balance * web3.fromWei(balance, "ether")
    transaction_count = web3.eth.get_transaction_count(address)
    put_table(
        tdata=[
            ["Balance", balance],
            ["Transaction Count", transaction_count]
        ],
        header=[
            f'Info on {address}', None
        ]
    )


@use_scope('dashboard', clear=True)
def put_blocks(web3):
    put_text("## Blocks")


@use_scope('dashboard', clear=True)
def put_transactions(web3):
    put_text("## Transactions")


def query_etherscan(module, action, address):
    url = f'https://api.etherscan.io/api?module={module}&action={action}&address={address}&tag=latest&apikey={config.ETHERSCAN_API_KEY}'
    response = requests.get(url).text
    return json.loads(response)["result"]


def main():
    # ? need this stuff?
    web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
    box_style = 'border: solid black 1px; border-radius: 10px; padding: 1rem; margin: 1rem'
    # Setup layout
    session.set_env(title='PyWebIO Ethereum Demo', output_max_width='100%')
    put_row([put_scope('left-navbar'), None,
            put_scope('dashboard')], size='200px 50px 85%')
    with use_scope('left-navbar'):
        put_grid([[
            put_text('PyWebIO Ether Demo'),
            put_markdown('#### Accounts').onclick(lambda: put_addresses(web3)),
            put_markdown('#### Blocks').onclick(lambda: put_blocks(web3)),
            put_markdown('#### Transactions').onclick(
                lambda: put_transactions(web3)),

        ]], direction='column')

    put_addresses(web3)


start_server(main, port=8080)
