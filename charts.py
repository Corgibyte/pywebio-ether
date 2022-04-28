import plotly.express as px


def get_block_miners(web3, n=300):
    latest_block_num = web3.eth.get_block("latest")["number"]
    blocks = []
    for i in range(n):
        blocks.append(web3.eth.get_block(latest_block_num - i))
    miners = {}
    for block in blocks:
        block_miner = block["miner"]
        if block_miner in miners:
            miners[block_miner] += 1
        else:
            miners[block_miner] = 1
    sorted_data = {
        k: v for k, v in sorted(miners.items(), key=lambda item: item[1], reverse=True)
    }
    fig = px.line(
        x=sorted_data.keys(),
        y=sorted_data.values(),
        labels={"x": "Miners", "y": "Number of Blocks Mined"},
        title=f"Number of Previous {n} Blocks Mined by Individual Miners",
        markers=True,
    )
    return fig.to_html(include_plotlyjs="require", full_html=False)
