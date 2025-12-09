"""
create-likert-plots
====================

Purpose
-------
- Generate publication-quality Likert and auxiliary plots for survey data on
    Direct Air Capture (DAC) and CO2 storage (knowledge, support, trust, risk,
    distance, and demographics).

Inputs
------
- A pandas DataFrame produced via `dacstore.utils.get_data`, optionally with
    translated column names and normalized response labels.

Outputs
-------
- PNG figures saved under `figs/` using transparent backgrounds and tight
    bounding boxes, suitable for papers and slide decks.

Usage
-----
- Call the high-level helpers (e.g., `plot_support`, `plot_knowledge`) with a
    prepared DataFrame and an output path. Use `create_likert_plot` for custom
    groups.

Notes
-----
- Color maps and category orders come from `dacstore.config`.
- Computation of Likert counts and stacked rows is handled by
    `dacstore.dac_analysis.to_results` and related utilities.
"""

from dacstore.config import agreement_cmap, categories, colors
from dacstore.dac_analysis import to_results, value_counts
from dacstore.utils import get_data
from dacstore.plot import likert_plot
from dacstore.config import groups_translated
import matplotlib.pyplot as plt


import seaborn as sns  # noqa


sns.set_theme(style="darkgrid")

dpi = 300


def create_likert_plot(
    df,
    fname,
    group,
    scale=None,
    colors=colors,
    dpi=300,
    labels=None,
    height=None,
    figsize=None,
    title=None,
    textwrap_width=45,
):
    """Render a Likert stacked bar chart for the specified question group.

    Parameters
    ----------
    df : pandas.DataFrame
        Source survey responses.
    fname : str or pathlib.Path
        Output file path for the exported PNG (e.g., `figs/support.png`).
    group : str or list[str]
        A key from `groups_translated` or a list of column names to plot.
    scale : str, optional
        Category key in `dacstore.config.categories` defining ordered labels
        (e.g., `support_en`, `agreement_en`). If omitted, order is inferred.
    colors : dict or list, optional
        Color mapping for categories. Defaults to `dacstore.config.colors`.
    dpi : int, optional
        Export resolution in dots per inch. Default is 300.
    labels : dict, optional
        Optional mapping of long question text to shorter wrapped labels.
    height : float, optional
        Row height scaling of the stacked bars.
    figsize : tuple[float, float], optional
        Matplotlib figure size in inches.
    title : str, optional
        Optional figure title.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    print(f"Creating Likert plot for group: {group}")
    if isinstance(group, str):
        group = groups_translated[group]
    cols = df[group].dropna()
    if scale is not None:
        category_names = categories[scale]
    else:
        category_names = None
    counts = value_counts(cols)
    results = to_results(counts, category_names, labels=labels)
    likert_plot(
        results,
        category_names,
        colors=colors,
        fname=fname,
        dpi=dpi,
        height=height,
        figsize=figsize,
        title=title,
        textwrap_width=textwrap_width,
    )


def create_bar_plot(df, fname, title=None, min_count=10, dpi=300):
    """Create a labeled bar chart of non-null counts per column and export.

    Parameters
    ----------
    df : pandas.Series or pandas.DataFrame
        Input data; counts are computed per column.
    fname : str or pathlib.Path
        Output file path for the exported PNG.
    title : str, optional
        Optional chart title.
    min_count : int, optional
        Minimum bar height to annotate with a count label. Default is 10.
    dpi : int, optional
        Export resolution in dots per inch. Default is 300.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    ax = df.count().plot(kind="bar", title=title)
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > min_count:
            ax.text(
                x + width / 2,
                y + height / 2,
                "{:.0f}".format(height),
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=8,
            )
    fig = ax.get_figure()
    fig.savefig(fname, transparent=True, bbox_inches="tight", dpi=dpi)
    plt.close(fig)


def plot_knowledge(df, fname="figs/knowledge.png"):
    """Plot DAC and CO2 storage knowledge as a Likert chart.

    Missing values are treated as "Never heard". Ordering is taken from
    `categories['knowledge_en']`.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str, optional
        Output PNG path. Default is `figs/knowledge.png`.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    # shorts = {
    #     "DAC Awareness": "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?",
    #     "DAC Knowledge": "Wie gut sind ihre Kenntnisse dieser Technologien?",
    #     "Storage Awareness": "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?",
    #     "Storage Knowledge": "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?",
    #     "Initial Storage Support": "CO2-Speicherung",
    #     "Final Storage Support": "CO2-Speicherung.1",
    #     "Initial DAC Support": "Direct Air Capture (DAC)",
    #     "Final DAC Support": "Direct Air Capture (DAC).1",
    # }

    DAC_KNOWLEDGE_DE = "Wie gut sind ihre Kenntnisse dieser Technologien?"
    STORAGE_KNOWLEDGE_DE = (
        "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?"
    )
    DAC_KNOWLEDGE_EN = "How would you rate your knowledge of DAC?"
    STORAGE_KNOWLEDGE_EN = "How would you rate your knowledge of CO2 Storage?"

    labels = {
        DAC_KNOWLEDGE_DE: "Wie gut sind ihre Kenntnisse von Technologien\n zur Entnahme von Kohlendioxid (CO2) aus der Luft?",
        STORAGE_KNOWLEDGE_DE: "Wie gut sind ihre Kenntnisse\n der CO2-Speicherungstechnologien?",
        DAC_KNOWLEDGE_EN: "How would you rate your\n knowledge of DAC?",
        STORAGE_KNOWLEDGE_EN: "How would you rate your\n knowledge of CO2 Storage?",
    }

    DAC_KNOWLEDGE = DAC_KNOWLEDGE_EN
    STORAGE_KNOWLEDGE = STORAGE_KNOWLEDGE_EN

    # df = df[[DAC_KNOWLEDGE, STORAGE_KNOWLEDGE]]
    df.loc[df[DAC_KNOWLEDGE].isnull(), DAC_KNOWLEDGE] = "Never heard"
    df.loc[df[STORAGE_KNOWLEDGE].isnull(), STORAGE_KNOWLEDGE] = "Never heard"

    knowledge = df[[DAC_KNOWLEDGE, STORAGE_KNOWLEDGE]]

    category_names = categories["knowledge_en"]
    counts = value_counts(knowledge)
    results = to_results(counts, category_names, labels)

    likert_plot(results, category_names, fname=fname, dpi=dpi)


def plot_support(df, fname):
    """Plot initial and final support for DAC and CO2 storage.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    acceptance = [
        "Initial DAC Support",
        "Final DAC Support",
        "Initial Storage Support",
        "Final Storage Support",
    ]
    create_likert_plot(
        df, fname, acceptance, scale="support_en", colors=colors, dpi=dpi
    )


def plot_climate_change(df, fname):
    """Plot climate change agreement statements as a Likert chart.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    create_likert_plot(
        df,
        fname,
        "Climate Change",
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        textwrap_width=30,
    )


def plot_tampering(df, fname):
    """Plot attitudes toward "tampering with nature" with concise labels.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    # labels = {
    #     "Trying to influence the climate system by using DAC reflects human arrogance": "Trying to influence the climate system by\n using DAC reflects human arrogance"
    # }
    create_likert_plot(
        df,
        fname,
        "Tampering",
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        #  labels=labels,
    )


def plot_trust(df, fname):
    """Plot trust in institutions as a Likert chart with wrapped labels.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    create_likert_plot(
        df,
        fname,
        "Trust",
        scale="trust_en",
        colors=agreement_cmap,
        dpi=dpi,
        # labels=labels,
        textwrap_width=30,
    )


def plot_risk(df, fname):
    """Plot perceived risks as a Likert chart.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    create_likert_plot(
        df, fname, "Risk", scale="agreement_en", colors=agreement_cmap, dpi=dpi
    )


def plot_distance(df, fname):
    """Plot preferred minimum distances to settlements for technologies.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    # distance = df[groups_translated.get("Distance")]
    create_likert_plot(
        df,
        fname,
        "Distance",
        scale="distance_en",
        colors=agreement_cmap,
        dpi=dpi,
        title="If the following technologies were introduced in Germany,\n how large should the minimum distance to the nearest settlement be?",
    )


def plot_emotions(df, fname):
    """Alias of `plot_distance`; currently renders Distance group as Likert chart.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    # distance = df[groups_translated.get("Distance")]
    create_likert_plot(
        df,
        fname,
        "Distance",
        scale="distance_en",
        colors=agreement_cmap,
        dpi=dpi,
        title="If the following technologies were introduced in Germany,\n how large should the minimum distance to the nearest settlement be?",
    )


#     create_bar_plot(
#         distance,
#         fname,
#         title="If the following technologies were introduced in Germany,\n how large should the minimum distance to the nearest settlement be?",
#     )


def plot_maturity(df, fname):
    """Plot a single Likert figure for DAC maturity perception.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path, e.g., `figs/aux_maturity.png`.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    group = ["DACCS is a mature clean technology"]
    create_likert_plot(
        df,
        fname,
        group,
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        height=0.2,
        figsize=(25, 2),
        # title="Perception of DAC technology maturity",
    )


def plot_cost_price(df, fname):
    """Plot Likert figure for cost efficiency and price acceptance statements.

    Includes:
    - Reducing CO2 emissions would be more cost efficient than using DAC
    - Paying €100 to capture 1 ton of CO2 is a reasonable price

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path, e.g., `figs/aux_cost_price.png`.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    group = [
        "Reducing CO2 emissions would be more cost efficient than using DACCS",
        "Paying €100 to capture 1 ton of CO2 is a reasonable price",
    ]
    create_likert_plot(
        df,
        fname,
        group,
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        # height=0.8,
        # figsize=(16, 8),
        # title="Cost efficiency and price acceptance",
    )


def plot_effectiveness(df, fname):
    """Plot Likert figure for DAC effectiveness and role in climate strategy.

    Includes:
    - DAC could help capture emissions from hard-to-abate sectors
    - Including DAC can help Germany achieve climate goals and limit warming
    - DAC is an efficient technology to fight climate change

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path, e.g., `figs/aux_effectiveness.png`.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    group = [
        "DACCS could help capture emissions from hard-to-abate sectors such as agriculture or cement production",
        "Including DACCS as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C",
        "DACCS is an efficient technology to fight climate change",
    ]
    create_likert_plot(
        df,
        fname,
        group,
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        # height=0.8,
        # figsize=(20, 12),
        # title="Perceived effectiveness and role of DAC",
    )


def plot_socio_demographics(df, fname):
    """Plot stacked age distribution by gender with count annotations.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.

    Returns
    -------
    None
        Saves a PNG to `fname`.
    """
    socio_demo = df.groupby(["Age", "Gender"]).Age.count().unstack()
    ax = socio_demo.plot(
        kind="bar", stacked=True, color=["skyblue", "darkmagenta", "sandybrown"]
    )
    # annotate
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 10:
            ax.text(
                x + width / 2,
                y + height / 2,
                "{:.0f}".format(height),
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=8,
            )
    fig = ax.get_figure()
    fig.savefig(fname, transparent=True, bbox_inches="tight", dpi=dpi)
    plt.close(fig)


def plot_transport(df, fname):
    """Plot bar chart of accepted CO2 transportation methods.

    Parameters
    ----------
    df : pandas.DataFrame
        Translated survey data.
    fname : str
        Output PNG path.
    """
    transport = df[groups_translated.get("Transport")]
    create_bar_plot(
        transport,
        fname,
        title="Which CO2 transportation methods would you agree with?",
    )


def plot_emotion(df, fname):
    col = "What primary emotion do you feel regarding DACCS technologies?"
    data = (
        df[col]
        .value_counts()
        .reindex(["Happiness", "Enthusiasm", "Hope", "Worry", "Fear", "Anger"])
    )
    # remove index name so it is not plotted as caption
    data.index.name = None
    ax = data.plot(kind="bar", title=col)
    # annotate
    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        if height > 10:
            ax.text(
                x + width / 2,
                y + height / 2,
                "{:.0f}".format(height),
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=8,
            )
    fig = ax.get_figure()
    fig.savefig(fname, transparent=True, bbox_inches="tight", dpi=dpi)
    plt.close(fig)


# def plot_distance(df, fname):
#     distance = df[groups_translated.get("Distance")]
#     create_bar_plot(
#         distance,
#         fname,
#         title="If the following technologies were introduced in Germany,\n how large should the minimum distance to the nearest settlement be?",
#     )


if __name__ == "__main__":
    df = get_data(
        source="./data/data.csv", drop=False, translate=True, drop_invalid=True
    )
    print(f"creating plots from {len(df)} valid responses...")
    plot_knowledge(df, "figs/knowledge.png")
    plot_support(df, "figs/support.png")
    plot_trust(df, "figs/trust.png")
    plot_risk(df, "figs/risk.png")
    # Split former aux into three focused figures
    plot_maturity(df, "figs/maturity.png")
    plot_cost_price(df, "figs/cost_price.png")
    plot_effectiveness(df, "figs/effectiveness.png")
    plot_climate_change(df, "figs/climate_change.png")
    plot_socio_demographics(df, "figs/socio_demographic.png")
    plot_tampering(df, "figs/tampering.png")
    plot_distance(df, "figs/distance.png")
    plot_transport(df, "figs/transport.png")
    plot_emotion(df, "figs/emotion.png")
