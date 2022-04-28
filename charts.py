import plotly.express as px
import pickle


def generate_data(web3, n=1000):
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
    with open(chart_data_file, "wb") as fp:
        pickle.dump(sorted_data, fp)
    return sorted_data


def get_block_miners(web3):
    data = get_data(web3)
    fig = px.line(
        x=range(len(data.values())),
        y=data.values(),
        labels={"x": "Miner Rank", "y": "Number of Blocks Mined"},
        title=f"Top Mining Accounts from Sample of 1,000 Blocks",
        #! Doesn't work with older plotly on pywebio build website
        # markers=True,
    )
    return fig.to_html(include_plotlyjs="require", full_html=False)


def get_data(web3):
    global chart_data_file
    chart_data_file = "__chart_data.ob"
    try:
        with open(chart_data_file, "rb") as fp:
            try:
                data = pickle.load(fp)
            except EOFError:
                data = generate_data(web3)
    except:
        data = generate_data(web3)
    return data
