from helpers import config


def save_plot(fig, name):
    fig.write_html(f"{config['dir']['figures']}/plotly/{name}.html",
                   full_html=False, include_plotlyjs=False)
