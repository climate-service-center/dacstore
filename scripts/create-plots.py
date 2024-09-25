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
    scale="agreement_en",
    colors=colors,
    dpi=300,
    labels=None,
    height=None,
    figsize=None,
):
    if isinstance(group, str):
        group = groups_translated[group]
    cols = df[group].dropna()
    category_names = categories[scale]
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
    )


def create_bar_plot(df, fname, title=None, min_count=10, dpi=300):
    """Create a bar plot counting values in a column"""
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
    create_likert_plot(
        df,
        fname,
        "Climate Change",
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
    )


def plot_tampering(df, fname):
    labels = {
        "Trying to influence the climate system by using DAC reflects human arrogance": "Trying to influence the climate system by\n using DAC reflects human arrogance"
    }
    create_likert_plot(
        df,
        fname,
        "Tampering",
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        labels=labels,
    )


def plot_trust(df, fname):
    labels = {
        "Environmental Protection Organizations and NGOs": "Environmental Protection\n Organizations and NGOs"
    }
    create_likert_plot(
        df,
        fname,
        "Trust",
        scale="trust_en",
        colors=agreement_cmap,
        dpi=dpi,
        labels=labels,
    )


def plot_risk(df, fname):
    create_likert_plot(
        df, fname, "Risk", scale="agreement_en", colors=agreement_cmap, dpi=dpi
    )


def plot_aux(df, fname):
    bonus = [
        #  "Humans should not be tampering with nature in this way",
        # "I don’t think that injecting CO2 into the ground is a good idea",
        "DAC is a mature clean technology",
        # "Trying to influence the climate system by using DAC reflects human arrogance",
        "Reducing CO2 emissions would be more cost efficient than using DAC",
        "Paying €100 to capture 1 ton of CO2 is a reasonable price",
        "DAC could help capture emissions from hard-to-abate sectors such as agriculture or cement production",
        "Including DAC as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C",
        "DAC is an efficient technology to fight climate change",
    ]
    labels = {
        "Reducing CO2 emissions would be more cost efficient than using DAC": "Reducing CO2 emissions would be more\n cost efficient than using DAC",
        "DAC could help capture emissions from hard-to-abate sectors such as agriculture or cement production": "DAC could help capture emissions from hard-to-abate\n sectors such as agriculture or cement production",
        "Trying to influence the climate system by using DAC reflects human arrogance": "Trying to influence the climate system\n by using DAC reflects human arrogance",
        "Including DAC as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C": "Including DAC as a part of an overall strategy can help\n Germany achieve its climate goals and limit\n climate change to 1.5°C",
    }
    create_likert_plot(
        df,
        fname,
        bonus,
        scale="agreement_en",
        colors=agreement_cmap,
        dpi=dpi,
        labels=labels,
        height=0.8,
        figsize=(25, 15),
    )


def plot_socio_demographics(df, fname):
    """plot distribution of gender and age"""
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
    transport = df[groups_translated.get("Transport")]
    create_bar_plot(
        transport, fname, title="Which CO2 transportation methods would you agree with?"
    )


def plot_distance(df, fname):
    distance = df[groups_translated.get("Distance")]
    create_bar_plot(
        distance,
        fname,
        title="If the following technologies were introduced in Germany,\n how large should the minimum distance to the nearest settlement be?",
    )


if __name__ == "__main__":
    df = get_data(
        source="./data/data.csv", drop=False, translate=True, drop_invalid=True
    )
    print(f"creating plots from {len(df)} valid responses...")
    plot_knowledge(df, "figs/knowledge.png")
    plot_support(df, "figs/support.png")
    plot_trust(df, "figs/trust.png")
    plot_risk(df, "figs/risk.png")
    plot_aux(df, "figs/aux.png")
    plot_climate_change(df, "figs/climate_change.png")
    plot_socio_demographics(df, "figs/socio_demographic.png")
    plot_tampering(df, "figs/tampering.png")
    plot_transport(df, "figs/transport.png")
    plot_distance(df, "figs/distance.png")
