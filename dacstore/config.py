import numpy as np

groups = {
    "Climate Change": [
        "Der Klimawandel findet tatsächlich statt.",
        "Der Klimawandel ist ein ernstes Problem.",
        "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.",
        "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.",
    ],
    "DAC Awareness": [
        "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?",
    ],
    "DAC Knowledge": [
        "Wie gut sind ihre Kenntnisse dieser Technologien?",
    ],
    "Storage Awareness": [
        "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?",
    ],
    "Initial Storage Support": [
        "CO2-Speicherung",
    ],
    "Final Storage Support": [
        "CO2-Speicherung.1",
    ],
    "Tampering": [
        #     "DAC ist eine ausgereifte saubere Technologie.",
        "Menschen sollten die Natur nicht auf diese Weise manipulieren.",
        "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.",
        "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.",
    ],
    "Transport": [
        "LKW",
        "Eisenbahn",
        "Pipeline (Rohrleitungstransport)",
        "Tanker (Schiff)",
        "Mit keiner",
        "Weiß nicht",
    ],
    "Risk": [
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
        "CO2-Speicherung könnte Erdbeben verursachen.",
        "CO2-Speicherung könnte Explosionen verursachen.",
        "CO2-Speicherung könnte CO2-Leckagen verursachen.",
    ],
    "Trust": [
        "Politik",
        "Industrie",
        "Wissenschaft",
        "Vereinte Nationen (UNO)",
        "Europäische Union",
        "Nichtregierungs- und Umweltschutzorganisationen",
        "Medien",
    ],
    "Emotion": [
        "Glück",
        "Hoffnung",
        "Begeisterung",
        "Wut",
        "Sorge",
        "Angst",
    ],
    "Benefit": [],
    "Safety": [],
    "NIMBY": [],
    "Distance": [
        "DAC Anlage",
        "CO2-Speicherung im Boden",
        "CO2-Speicherung im Meeresboden",
    ],
    "Socio Demographic": [
        "Geschlecht",
        "Altersgruppe",
        # "Höchster Bildungsabschluss",
        # "Beruf",
    ],
}


weighting_groups = {
    "climate_change_perception": [
        "Der Klimawandel findet tatsächlich statt.",
        "Der Klimawandel ist ein ernstes Problem.",
        "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.",
        "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.",
    ],
    "tampering_with_nature": [
        #     "DAC ist eine ausgereifte saubere Technologie.",
        "Menschen sollten die Natur nicht auf diese Weise manipulieren.",
        "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.",
        "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.",
    ],
    "maturity_of_technology": [
        "DAC ist eine ausgereifte saubere Technologie.",
    ],
    "benefit_perception": [
        "DAC könnte dazu beitragen, schwer vermeidbare Emissionen aus Sektoren wie Landwirtschaft oder Zementproduktion zu entnehmen.",
        "Die Implementierung von DAC als Teil einer Gesamtstrategie kann Deutschland dabei helfen, seine Klimaziele zu erreichen und den Klimawandel auf 1,5 °C zu begrenzen.",
        "DAC ist eine effiziente Technologie zur Bekämpfung des Klimawandels.",
    ],
    "cost": [
        "Emissionen zu reduzieren wäre kosteneffizienter als DAC.",
        # "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.",
    ],
    # "transport": [
    #     "LKW",
    #     "Eisenbahn",
    #     "Pipeline (Rohrleitungstransport)",
    #     "Tanker (Schiff)",
    #     "Mit keiner",
    #     "Weiß nicht",
    # ],
    "risk": [
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
        "CO2-Speicherung könnte Erdbeben verursachen.",
        "CO2-Speicherung könnte Explosionen verursachen.",
        "CO2-Speicherung könnte CO2-Leckagen verursachen.",
    ],
    "trust": [
        "Politik",
        "Industrie",
        "Wissenschaft",
        "Vereinte Nationen (UNO)",
        "Europäische Union",
        "Nichtregierungs- und Umweltschutzorganisationen",
        "Medien",
    ],
    "emotion": [
        "Welche Hauptemotion empfinden Sie gegenüber DAC-Technologien?",
    ],
    "distance": [
        "DAC Anlage",
        "CO2-Speicherung im Boden",
        "CO2-Speicherung im Meeresboden",
    ],
    # "socio_demographic": [
    #     "Geschlecht",
    #     "Altersgruppe",
    #     # "Höchster Bildungsabschluss",
    #     # "Beruf",
    # ],
    # "dac_awareness": [
    #    "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?",
    # "Wie gut sind ihre Kenntnisse dieser Technologien?",
    # ],
    "dac_knowledge": [
        "Wie gut sind ihre Kenntnisse dieser Technologien?",
        # "Direct Air Capture (DAC)",
    ],
    # "storage_awareness": [
    #    "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?",
    # ],
    "storage_knowledge": [
        "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?",
    ],
    "initial_storage_support": [
        "CO2-Speicherung",
    ],
    "final_storage_support": [
        "CO2-Speicherung.1",
    ],
    "initial_dac_support": [
        "Direct Air Capture (DAC)",
    ],
    "final_dac_support": [
        "Direct Air Capture (DAC).1",
    ],
    "age": [
        "Altersgruppe",
    ],
    "gender": [
        "Geschlecht",
    ],
    "education": [
        "Höchster Bildungsabschluss",
    ],
    "occupation": [
        "Beruf",
    ],
    "state": [
        "Bundesland",
    ],
    "trust_in_science": [
        "Wissenschaft",
    ],
    "trust_in_politics": [
        "Politik",
    ],
    "trust_in_industry": [
        "Industrie",
    ],
    "trust_in_un": [
        "Vereinte Nationen (UNO)",
    ],
    "trust_in_eu": [
        "Europäische Union",
    ],
    "trust_in_ngos": [
        "Nichtregierungs- und Umweltschutzorganisationen",
    ],
    "trust_in_media": [
        "Medien",
    ],
}


analyze_cols = []
for qs in weighting_groups.values():
    analyze_cols += qs
analyze_cols = list(dict.fromkeys(analyze_cols))


col_shorts = {
    "DAC Awareness": "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?",
    "DAC Knowledge": "Wie gut sind ihre Kenntnisse dieser Technologien?",
    "Storage Awareness": "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?",
    "Storage Knowledge": "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?",
    "Initial Storage Support": "CO2-Speicherung",
    "Final Storage Support": "CO2-Speicherung.1",
    "Initial DAC Support": "Direct Air Capture (DAC)",
    "Final DAC Support": "Direct Air Capture (DAC).1",
}


rename_cols = {
    "Geschlecht": "Gender",
    "Altersgruppe": "Age",
    "Höchster Bildungsabschluss": "Education",
    "Beruf": "Occupation",
    "Bundesland": "State",
    "Der Klimawandel findet tatsächlich statt.": "Climate Change 1",
    "Der Klimawandel ist ein ernstes Problem.": "Climate Change 2",
    "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.": "Climate Change 3",
    "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.": "Climate Change 4",
    "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?": "DAC Awareness",
    "Wie gut sind ihre Kenntnisse dieser Technologien?": "DAC Knowledge",
    "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?": "Storage Awareness",
    "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?": "Storage Knowledge",
    "Direct Air Capture (DAC)": "Initial DAC Support",  # TWO COLUMNS ARE NAMED THE SAME!!!! this one is considering the final support
    "CO2-Speicherung": "Initial Storage Support",
    "Welche Hauptemotion empfinden Sie gegenüber DAC-Technologien?": "First Emotion",
    "DAC ist eine ausgereifte saubere Technologie.": "Maturity",
    "Menschen sollten die Natur nicht auf diese Weise manipulieren.": "Tampering 1",
    "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.": "Tampering 2",
    "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.": "Tampering 3",
    "DAC Anlage": "NIMBY 1",
    "CO2-Speicherung im Boden": "NIMBY 2",
    "CO2-Speicherung im Meeresboden": "NIMBY 3",
    "LKW": "Transport 1",
    "Eisenbahn": "Transport 2",
    "Pipeline (Rohrleitungstransport)": "Transport 3",
    "Tanker (Schiff)": "Transport 4",
    "Mit keiner": "Transport 5",
    "Weiß nicht": "Transport 6",
    "Emissionen zu reduzieren wäre kosteneffizienter als DAC.": "Cost 1",
    "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.": "Cost 2",
    "DAC könnte dazu beitragen, schwer vermeidbare Emissionen aus Sektoren wie Landwirtschaft oder Zementproduktion zu entnehmen.": "Benefit 1",
    "Die Implementierung von DAC als Teil einer Gesamtstrategie kann Deutschland dabei helfen, seine Klimaziele zu erreichen und den Klimawandel auf 1,5 °C zu begrenzen.": "Benefit 2",
    "DAC ist eine effiziente Technologie zur Bekämpfung des Klimawandels.": "Benefit 3",
    "DAC ist sicher.": "Safety 1",
    "CO2-Speicherung ist sicher.": "Safety 2",
    "CO2-Speicherung könnte Erdbeben verursachen.": "Risk 1",
    "CO2-Speicherung könnte Explosionen verursachen.": "Risk 2",
    "CO2-Speicherung könnte CO2-Leckagen verursachen.": "Risk 3",
    "Politik": "Trust 1",
    "Industrie": "Trust 2",
    "Wissenschaft": "Trust 3",
    "Vereinte Nationen (UNO)": "Trust 4",
    "Europäische Union": "Trust 5",
    "Nichtregierungs- und Umweltschutzorganisationen": "Trust 6",
    "Medien": "Trust 7",
    "Direct Air Capture (DAC).1": "Final DAC Support",
    # One more needed for the final DAC support currently an error
    "CO2-Speicherung.1": "Final Storage Support",
    "Ihre E-Mail Adresse": "Engagement",
}

no_replacer = "Nie gehört"

replacer = {
    "Überhaupt nicht": 1,
    "Eher nicht": 2,
    "Neutral": 3,
    "Etwas": 4,
    "Voll und ganz": 5,
    "Nein": 1,
    "Ja": 2,
    no_replacer: 1,
    "Nur gehört / Keine Kenntnisse ": 2,
    "Nur gehört / Keine Kenntnisse": 2,
    "Grundverständnis": 3,
    "Gute Kenntnisse": 4,
    "Sehr gute Kenntnisse": 5,
    "Stimme überhaupt nicht zu": 1,
    "Stimme nicht zu": 2,
    "Stimme weder zu noch lehne ich ab": 3,
    "Stimme zu": 4,
    "Stimme ich zu": 4,
    "Stimme voll und ganz zu": 5,
    "Weiß nicht": np.nan,
    # "Weiß nicht": 0,
    "Männlich": 1,
    "Weiblich": 2,
    "Divers": 3,
    "18 - 19": 1.0,
    "20 - 29": 2.0,
    "30 - 39": 3.0,
    "40 - 49": 4.0,
    "50 - 59": 5.0,
    "60+": 6.0,
    "(noch) kein Abschluss": 1,
    "Volks-/Hauptschule": 2,
    "Weiterführende Schule ohne Abitur": 3,
    "Ausbildung": 4,
    "Abitur/(Fach-)Hochschulreife": 5,
    "Bachelor (BSc.)": 6,
    "Master (MSc.) oder Diplom": 7,
    "Promotion (Dr.) oder Habilitation (Prof.)": 8,
    "Studierende": 1,
    "Angestellt": 2,
    "Selbständig": 3,
    "Öffentlicher Dienst": 4,
    "Arbeitsuchend": 5,
    "im Ruhestand": 6,
    "Baden-Württemberg": 1,
    "Bayern": 2,
    "Berlin": 3,
    "Brandenburg": 4,
    "Bremen": 5,
    "Hamburg": 6,
    "Hessen": 7,
    "Mecklenburg-Vorpommern": 8,
    "Niedersachsen": 9,
    "Nordrhein-Westfalen": 10,
    "Rheinland-Pfalz": 11,
    "Saarland": 12,
    "Sachsen": 13,
    "Sachsen-Anhalt": 14,
    "Schleswig-Holstein": 15,
    "Thüringen": 16,
    "Ich lebe im Ausland": 17,
    "Hoffnung": 2,
    "Begeisterung": 2,
    "Glück": 2,  # SHOULD WE LEAVE THIS BINARY OR IN 1 TO 6?
    "Wut": 1,
    "Sorge": 1,
    "Angst": 1,
    "Nirgendwo in Deutschland": 5,
    # "Nirgendwo in Deutschland": 5,
    "100 km": 4,
    "10 km": 3,
    "1 km": 2,
    "500 m": 1,
    "Überhaupt kein Vertrauen": 1,
    "Geringes Vertrauen": 2,
    "Mäßiges Vertrauen": 4,
    "Starkes Vertrauen": 5,
}


drop_cols = [
    "Language",
    "IP address",
    "Device",
    "Status",
    "Collector",
    "Sind Sie einverstanden?",
    "Bitte bewerten Sie die folgenden Aussagen über den Klimawandel.",
    "Unterstützen Sie die Einführung der folgenden Technologien?",
    "Bitte bewerten Sie die folgenden Aussagen über die DAC-Technologien.",
    "Wenn die folgenden Technologien in Deutschland eingeführt wären, wie groß sollte der Mindestabstand zur nächsten Siedlung sein?",
    "Mit welchen CO2-Transportwege wären Sie einverstanden?",
    "Inwiefern stimmen Sie den folgenden Aussagen zu?",
    # "Inwiefern vertrauen Sie darauf, dass diese Gruppen im Interesse der Gesellschaft handeln werden?",
    "Unterstützen Sie die Einführung der folgenden Technologien?.1",
    # "Unterstützen Sie die Einführung der folgenden Technologien?.1"
]


translation_columns = {
    "Geschlecht": "Gender",
    "Altersgruppe": "Age",
    "Höchster Bildungsabschluss": "Education",
    "Beruf": "Profession",
    "Bundesland": "State",
    "Der Klimawandel findet tatsächlich statt.": "Climate change is really happening",
    "Der Klimawandel ist ein ernstes Problem.": "Climate change is a serious problem",
    "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.": "Human activities are the main cause of climate change",
    "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.": "We should all make an effort to reduce our CO2 emissions",
    "Haben Sie schon von Technologien zur Entnahme von Kohlendioxid (CO2) aus der Luft (auf Englisch Direct Air Capture (DAC)) gehört?": "Have you heard about Direct Air Capture and Storage (DACCS) technologies?",
    "Wie gut sind ihre Kenntnisse dieser Technologien?": "How would you rate your knowledge of DAC?",
    "Haben Sie schon von Kohlendioxid (CO2)-Speicherung gehört?": "Have you heard about CO2 storage?",
    "Wie gut sind ihre Kenntnisse der CO2-Speicherungstechnologien?": "How would you rate your knowledge of CO2 Storage?",
    "Direct Air Capture (DAC)": "Initial DAC Support",
    "CO2-Speicherung": "Initial Storage Support",
    "Welche Hauptemotion empfinden Sie gegenüber DAC-Technologien?": "What primary emotion do you feel regarding DACCS technologies?",
    "DAC ist eine ausgereifte saubere Technologie.": "DACCS is a mature clean technology",
    "Menschen sollten die Natur nicht auf diese Weise manipulieren.": "Humans should not be tampering with nature in this way",
    "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.": "I don’t think that injecting CO2 into the ground is a good idea",
    "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.": "Trying to influence the climate system by using DACCS reflects human arrogance",
    "DAC Anlage": "DAC facility",
    "CO2-Speicherung im Boden": "CO2 storage underground",
    "CO2-Speicherung im Meeresboden": "CO2 storage in the seabed",
    "LKW": "Truck",
    "Eisenbahn": "Railway",
    "Pipeline (Rohrleitungstransport)": "Pipelines",
    "Tanker (Schiff)": "Tanker",
    "Mit keiner": "With none",
    "Weiß nicht": "Don’t know",
    "Emissionen zu reduzieren wäre kosteneffizienter als DAC.": "Reducing CO2 emissions would be more cost efficient than using DACCS",
    "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.": "Paying €100 to capture 1 ton of CO2 is a reasonable price",
    "DAC könnte dazu beitragen, schwer vermeidbare Emissionen aus Sektoren wie Landwirtschaft oder Zementproduktion zu entnehmen.": "DACCS could help capture emissions from hard-to-abate sectors such as agriculture or cement production",
    "Die Implementierung von DAC als Teil einer Gesamtstrategie kann Deutschland dabei helfen, seine Klimaziele zu erreichen und den Klimawandel auf 1,5 °C zu begrenzen.": "Including DACCS as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C",
    "DAC ist eine effiziente Technologie zur Bekämpfung des Klimawandels.": "DACCS is an efficient technology to fight climate change",
    "DAC ist sicher.": "DAC is a safe technology",
    "CO2-Speicherung ist sicher.": "CO2 storage is a safe technology",
    "CO2-Speicherung könnte Erdbeben verursachen.": "CO2 storage could cause earthquakes",
    "CO2-Speicherung könnte Explosionen verursachen.": "CO2 storage could cause explosions",
    "CO2-Speicherung könnte CO2-Leckagen verursachen.": "CO2 storage could cause CO2 leaks",
    "Politik": "Politicians",
    "Industrie": "Industry",
    "Wissenschaft": "Science",
    "Vereinte Nationen (UNO)": "United Nations (UN)",
    "Europäische Union": "European Union",
    "Nichtregierungs- und Umweltschutzorganisationen": "NGOs and environmental organizations",
    "Medien": "Media",
    "Direct Air Capture (DAC).1": "Final DAC Support",
    "CO2-Speicherung.1": "Final Storage Support",
    "Ihre E-Mail Adresse": "Engagement",
    "Inwiefern vertrauen Sie darauf, dass diese Gruppen im Interesse der Gesellschaft handeln werden?": "How much do you trust in these groups to act in the interest of society?",
}


translation_answers = {
    "Überhaupt nicht": "Not at all",
    "Eher nicht": "Rather not",
    "Neutral": "Neutral",
    "Etwas": "Somewhat",
    "Voll und ganz": "Absolutely",
    "Ja": "Yes",
    "Nein": "No",
    "Nie gehört": "Never heard",
    "Nur gehört / Keine Kenntnisse": "I heard about / no knowledge",
    "Grundverständnis": "Basic understanding",
    "Gute Kenntnisse": "Good knowledge",
    "Sehr gute Kenntnisse": "Very good knowledge",
    "Stimme überhaupt nicht zu": "Don’t agree at all",
    "Stimme nicht zu": "Don’t agree",
    "Stimme weder zu noch lehne ich ab": "Neutral",
    "Stimme zu": "Agree",
    "Stimme ich zu": "Agree",
    "Stimme voll und ganz zu": "Totally agree",
    "Weiß nicht": "I don't know",
    "Männlich": "Male",
    "Weiblich": "Female",
    "Divers": "Diverse",
    "18-19": "18 - 19",
    "20 - 29": "20 - 29",
    "30 - 39": "30 - 39",
    "40 - 49": "40 - 49",
    "50 - 59": "50 - 59",
    "60+": "60+",
    "(noch) kein Abschluss": "None",
    "Volks-/Hauptschule": "Elementary school",
    "Weiterführende Schule ohne Abitur": "Another type of degree without highschool",
    "Ausbildung": "Apprenticeship",
    "Abitur/(Fach-)Hochschulreife": "High school",
    "Bachelor (BSc.)": "Bachelor (BSc.)",
    "Master (MSc.) oder Diplom": "Master’s (MSc.)",
    "Promotion (Dr.) oder Habilitation (Prof.)": "PhD or Professorship",
    "Studierende": "Student",
    "Angestellt": "Employee",
    "Selbständig": "Self-employed",
    "Öffentlicher Dienst": "Public sector employee",
    "Arbeitsuchend": "Searching for work",
    "im Ruhestand": "Retired",
    "Baden-Württemberg": "Baden-Württemberg",
    "Bayern": "Bayern",
    "Berlin": "Berlin",
    "Brandenburg": "Brandenburg",
    "Bremen": "Bremen",
    "Hamburg": "Hamburg",
    "Hessen": "Hesse",
    "Mecklenburg-Vorpommern": "Mecklenburg-Western Pomerania",
    "Niedersachsen": "Lower Saxony",
    "Nordrhein-Westfalen": "North Rhine-Westphalia",
    "Rheinland-Pfalz": "Rhineland-Palatinate",
    "Saarland": "Saarland",
    "Sachsen": "Saxony",
    "Sachsen-Anhalt": "Saxony-Anhalt",
    "Schleswig-Holstein": "Schleswig-Holstein",
    "Thüringen": "Thuringia",
    "Ich lebe im Ausland": "I live abroad",
    "Hoffnung": "Hope",
    "Begeisterung": "Enthusiasm",
    "Glück": "Happiness",
    "Wut": "Anger",
    "Sorge": "Worry",
    "Angst": "Fear",
    "Nirgendwo in Deutschland": "Nowhere in Germany",
    "100 km": "100 km",
    "10 km": "10 km",
    "1 km": "1 km",
    "500 m": "500 m",
    "Überhaupt kein Vertrauen": "No trust at all",
    "Geringes Vertrauen": "Low trust",
    "Mäßiges Vertrauen": "Moderate trust",
    "Starkes Vertrauen": "Strong trust",
}


cleaning_dict = {"Stimme ich zu": "Stimme zu"}


scale = [
    "Stimme voll und ganz zu",
    "Stimme zu",
    "Stimme weder zu noch lehne ich ab",
    "Stimme nicht zu",
    "Stimme überhaupt nicht zu",
    "Weiß nicht",
]

knowledge_de = [
    "Nie gehört",
    "Nur gehört / Keine Kenntnisse",
    "Grundverständnis",
    "Gute Kenntnisse",
    "Sehr gute Kenntnisse",
]

trust_en = [
    "No trust at all",
    "Low trust",
    "Neutral",
    "Moderate trust",
    "Strong trust",
    "I don't know",
]

support_en = [
    "Not at all",
    "Rather not",
    "Neutral",
    "Somewhat",
    "Absolutely",
]

agreement_en = [
    "Don’t agree at all",
    "Don’t agree",
    "Neutral",
    "Agree",
    "Totally agree",
    "I don't know",
]

distance = ["Nowhere in Germany", "100 km", "10 km", "1 km", "500 m", "I don't know"]


gender = [
    "Male",
    "Female",
    "Diverse",
]

age = ["18 - 19", "20 - 29", "30 - 39", "40 - 49", "50 - 59", "60+"]

categories = {
    "knowledge_de": knowledge_de,
    "knowledge_en": [translation_answers[de] for de in knowledge_de],
    "trust_en": trust_en,
    "support_en": support_en,
    "agreement_en": agreement_en,
    "gender_en": gender,
    "age": age,
    "distance_en": distance,
}

red = [0.89888504, 0.30549789, 0.20676663, 1.0]
orange = [0.98869666, 0.65736255, 0.36885813, 1.0]
yellow = [0.99730873, 0.91657055, 0.60907343, 1.0]
yellowgreen = [0.89773164, 0.95693964, 0.60907343, 1.0]
lightgreen = [0.62637447, 0.8402153, 0.412995, 1.0]
green = [0.24805844, 0.66720492, 0.3502499, 1.0]

agreement_cmap = [red, orange, yellow, lightgreen, green, "gray"]
colors = [red, orange, yellow, lightgreen, green]


groups_translated = groups.copy()

for k, v in groups.items():
    for col in v:
        groups_translated[k] = [
            (translation_columns.get(col) or translation_answers.get(col)) for col in v
        ]


# encoding = {
#     'Climate change is really happening': categories["agreement_en"],
#     'Climate change is a serious problem' : categories["agreement_en"] ,
#     'Human activities are the main cause of climate change': categories["agreement_en"],
#     'We should all make an effort to reduce or CO2 emissions': categories["agreement_en"],
#     'Have you heard about Direct Air Capture (DAC) technologies?': ["No", "Yes"] ,
#     'How would you rate your knowledge of DAC?': catergories["knowledge_en"],
#     'Have you heard about CO2 storage?': ["No", "Yes"] ,
#     'How would you rate your knowledge of CO2 Storage?': categories["knowledge_en"],
#     'DAC is a mature clean technology': categories["agreement_en"],
#     'Humans should not be tampering with nature in this way': categories["agreement_en"],
#     'I don’t think that injecting CO2 into the ground is a good idea': categories["agreement_en"],
#     'Trying to influence the climate system by using DAC reflects human arrogance': categories["agreement_en"],

#     'Reducing CO2 emissions would be more cost efficient than using DAC': categories["agreement_en"],
#     'Paying €100 to capture 1 ton of CO2 is a reasonable price': categories["agreement_en"],
#     'DAC could help capture emissions from hard-to-abate sectors such as agriculture or cement production': categories["agreement_en"],
#     #    'Including DAC as a part of an overall strategy can help Germany achieve its climate goals and limit climate change to 1.5°C',
#     #    'DAC is a safe technology', 'CO2-Storage is a safe technology',
#     #    'DAC is an efficient technology to fight climate change',
#     #    'CO2-Storage could cause earthquakes',
#     #    'CO2-Storage could cause explosions',
#     #    'CO2-Storage could cause toxic leaks',
# }


encoding = {
    (translation_answers.get(k) or f'no translation for "{k}"'): v
    for k, v in replacer.items()
}
