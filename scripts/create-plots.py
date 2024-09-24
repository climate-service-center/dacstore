from dacstore.config import agreement_cmap, categories, colors
from dacstore.dac_analysis import to_results, value_counts
from dacstore.utils import get_data
from dacstore.plot import plot


def plot_knowledge(fname="figs/knowledge.png"):
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

    plot(results, category_names, fname=fname)


def plot_support(fname):
    acceptance = [
        "Initial DAC Support",
        "Final DAC Support",
        "Initial Storage Support",
        "Final Storage Support",
    ]

    acceptance = df[acceptance].dropna()

    category_names = categories["support_en"]
    counts = value_counts(acceptance)
    results = to_results(counts, category_names)

    plot(results, category_names, colors=colors, fname=fname)


def plot_trust(fname):
    trust = [
        "Politicians",
        "Industry",
        "Science",
        "United Nations (UN)",
        "European Union",
        "Environmental Protection Organizations and NGOs",
        "Media",
    ]
    trust = df[trust].dropna()

    category_names = categories["trust_en"]
    counts = value_counts(trust)
    results = to_results(
        counts,
        category_names,
        labels={
            "Environmental Protection Organizations and NGOs": "Environmental Protection\n Organizations and NGOs"
        },
    )

    colors = agreement_cmap
    plot(results, category_names, colors=colors, fname=fname)
    # plt.show()


def plot_risk(fname):
    risk = [
        "DAC is a safe technology",
        "CO2-Storage is a safe technology",
        "CO2-Storage could cause earthquakes",
        "CO2-Storage could cause explosions",
        "CO2-Storage could cause toxic leaks",
    ]
    risk = df[risk].dropna()

    category_names = categories["agreement_en"]
    counts = value_counts(risk)

    results = to_results(counts, category_names)
    plot(results, category_names, colors=agreement_cmap, fname=fname)


def plot_aux(fname):
    bonus = [
        "Climate change is really happening",
        "Climate change is a serious problem",
        "Human activities are the main cause of climate change",
        "We should all make an effort to reduce or CO2 emissions",
        "Humans should not be tampering with nature in this way",
        "I don’t think that injecting CO2 into the ground is a good idea",
        "DAC is a mature clean technology",
        "Trying to influence the climate system by using DAC reflects human arrogance",
        "Reducing CO2 emissions would be more cost efficient than using DAC",
        "Paying €100 to capture 1 ton of CO2 is a reasonable price",
        "DAC could help capture emissions from hard-to-abate sectors such as agriculture or cement production",
        "Including DAC as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C",
        "DAC is an efficient technology to fight climate change",
    ]

    category_names = categories["agreement_en"]
    labels = {
        "Reducing CO2 emissions would be more cost efficient than using DAC": "Reducing CO2 emissions would be more\n cost efficient than using DAC",
        "DAC could help capture emissions from hard-to-abate sectors such as agriculture or cement production": "DAC could help capture emissions from hard-to-abate\n sectors such as agriculture or cement production",
        "Trying to influence the climate system by using DAC reflects human arrogance": "Trying to influence the climate system\n by using DAC reflects human arrogance",
        "Including DAC as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C": "Including DAC as a part of an overall strategy can help\n Germany achieve its climate goals and limit\n climate change to 1.5°C",
    }
    counts = value_counts(df[bonus].dropna())
    results = to_results(counts, category_names, labels=labels)
    plot(
        results,
        category_names,
        colors=agreement_cmap,
        fname=fname,
        height=0.8,
        figsize=(25, 15),
    )


if __name__ == "__main__":
    df = get_data(
        source="./data/data.csv", drop=False, translate=True, drop_invalid=True
    )
    print(f"creating plots from {len(df)} valid responses...")
    plot_knowledge("figs/knowledge.png")
    plot_support("figs/support.png")
    plot_trust("figs/trust.png")
    plot_risk("figs/risk.png")
    plot_aux("figs/aux.png")
