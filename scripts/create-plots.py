from dacstore.config import categories
from dacstore.dac_analysis import to_results, value_counts
from dacstore.utils import get_data
from dacstore.plot import plot


df = get_data(source="./data/data.csv", drop=False, translate=True, drop_invalid=True)

shorts = {
    "DAC Awareness": "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?",
    "DAC Knowledge": "Wie gut sind ihre Kenntnisse dieser Technologien?",
    "Storage Awareness": "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?",
    "Storage Knowledge": "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?",
    "Initial Storage Support": "CO2-Speicherung",
    "Final Storage Support": "CO2-Speicherung.1",
    "Initial DAC Support": "Direct Air Capture (DAC)",
    "Final DAC Support": "Direct Air Capture (DAC).1",
}

DAC_KNOWLEDGE_DE = "Wie gut sind ihre Kenntnisse dieser Technologien?"
STORAGE_KNOWLEDGE_DE = "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?"
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


plot(results, category_names, fname="figs/knowledge.png")
