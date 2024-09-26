import numpy as np
import matplotlib.pyplot as plt


try:
    import seaborn  # noqa
except ImportError:
    pass


def likert_plot(
    results,
    category_names,
    colors=None,
    limit=5.0,
    height=None,
    figsize=None,
    fname=None,
    dpi=300,
    title=None,
):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    if height is None:
        height = 0.8
    if figsize is None:
        figsize = (25, 5)
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    if colors is None:
        category_colors = plt.get_cmap("RdYlGn")(np.linspace(0.15, 0.85, data.shape[1]))
    else:
        category_colors = colors

    fig, ax = plt.subplots(figsize=figsize)
    if title:
        plt.title(title, y=1.2, fontsize=24)
        # plt.text(0.5, 1.2, title, horizontalalignment='center', fontsize=24, transform = ax.transAxes)
        # fig.suptitle(title, fontsize=24)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(
            labels,
            widths,
            left=starts,
            height=height,
            label=colname,
            color=color,
            # edgecolor="black",
        )
        ax.legend(loc="best", fontsize=24)
        # ax.set_xlabel(colname, fontsize = 20)
        xcenters = starts + widths / 2

        # r, g, b, _ = color
        text_color = "black"  # "white" if r * g * b < 0.5 else "darkgrey"
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            if c > limit:
                ax.text(
                    x,
                    y,
                    "{:3.2f} %".format(c),
                    ha="center",
                    va="center",
                    color=text_color,
                    size=16,
                )

    ax.legend(
        ncol=len(category_names),
        bbox_to_anchor=(0, 1),
        loc="lower left",
        fontsize=18,  # "large",
    )

    ax.set_yticks(np.arange(len(labels)), labels=labels, size=16)

    if fname:
        fig.savefig(fname, transparent=True, bbox_inches="tight", dpi=dpi)
        plt.close(fig)
    return fig, ax
