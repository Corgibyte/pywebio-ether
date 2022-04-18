from pywebio import *
import config
from web3 import Web3


def ether_price(web3):
    # TODO get real data
    return 3007.84


def market_cap(web3):
    # TODO get real data
    return 357447543603.00


def transactions(web3):
    # TODO get real data
    transaction_data = 1543.43
    return f"{transaction_data} M"


def gas_price(web3):
    # TODO get real data
    gas_data = 53
    dollar_price = 3.35
    return f"{gas_data} Gwei ({dollar_price})"


def difficulty(web3):
    # TODO get real data
    difficulty_data = 13610.06
    return f"{difficulty_data} TH"


def hash_rate(web3):
    # TODO get real data
    hash_rate_data = 1053608.37
    return f"{hash_rate_data} GH/s"


def output_ether(web3):
    ether_data = [
        ["ETHER PRICE", ether_price(web3)],
        ["MARKET CAP", market_cap(web3)],
        ["TRANSACTIONS", transactions(web3)],
        ["MED GAS PRICE", gas_price(web3)],
        ["DIFFICULTY", difficulty(web3)],
        ["HASH RATE", hash_rate(web3)]
    ]
    ether_output = []
    for i in range(len(ether_data)):
        ether_output.append(output.put_column([
            output.put_text(ether_data[i][0]),
            output.put_text(ether_data[i][1])
        ]))
    return [
        output.put_column([ether_output[0], ether_output[1]]),
        output.put_column([ether_output[2], ether_output[3]]),
        output.put_column([ether_output[4], ether_output[5]])
    ]


def latest_blocks(web3):
    block = web3.eth.get_block('latest')
    blocks = [output.put_text("BLOCKS"), None]
    row_style = 'border-bottom: solid black 1px; margin-top:0.25rem'
    for i in range(10):
        this_block = web3.eth.get_block(block.number - i)
        blocks.append(output.put_row([
            output.put_text(this_block.number),
            output.put_text(this_block.miner),
            None,
            output.put_text(this_block.difficulty)
        ]).style(row_style))
    return blocks


def main():
    web3 = Web3(Web3.HTTPProvider(config.INFURA_URL))
    box_style = 'border: solid black 1px; border-radius: 10px; padding: 1rem; margin: 1rem'
    output.put_row(output_ether(web3)).style(box_style)
    output.put_column(latest_blocks(web3)).style(box_style)


start_server(main, port=8080)
