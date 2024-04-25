# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 16:22:44 2024

@author: Valencia
"""

import pandas as pd
import numpy as np

df = pd.read_csv(
    "Deutschland.csv", index_col=0, parse_dates=True, date_format="%d.%m.%Y %H:%M:%S"
)

# RENAME DATA COLUMNS
Germany = df.rename(
    columns={
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
        "Nichtregierungs- und  Umweltschutzorganisationen": "Trust 6",
        "Medien": "Trust 7",
        # One more needed for the final DAC support currently an error
        "CO2-Speicherung.1": "Final Storage Support",
        "Ihre E-Mail Adresse": "Engagement",
    }
)


replacer = {
    "Überhaupt nicht": 1,
    "Eher nicht": 2,
    "Neutral": 3,
    "Etwas": 4,
    "Voll und ganz": 5,
    "Nein": 1,
    "Nur gehört / Keine Kenntnisse ": 2,
    "Nur gehört / Keine Kenntnisse": 2,
    "Grundverständnis": 3,
    "Gute Kenntnisse": 4,
    "Sehr gute Kenntnisse": 5,
    "Sehr gute Kenntnisse ": 5,  # NOT WORKING FOR DAC
    "Stimme überhaupt nicht zu": 1,
    "Stimme nicht zu": 2,
    "Stimme weder zu noch lehne ich ab": 3,
    "Stimme zu": 4,
    "Stimme ich zu": 4,
    "Stimme voll und ganz zu": 5,
    "Weiß nicht": np.nan,  # MAYBE "NaN" INSTEAD OF A ZERO!?
    "Männlich": 1,
    "Weiblich": 2,
    "Divers": 3,
    "18-19": 1,
    "20 - 29": 2,
    "30 - 39": 3,
    "40 - 49": 4,
    "50 - 59": 5,
    "60+": 6,
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
    "Hoffnung": 1,
    "Begeisterung": 1,
    "Glück": 1,  # SHOULD WE LEAVE THIS BINARY OR IN 1 TO 6?
    "Wut": 2,
    "Sorge": 2,
    "Angst": 2,
    "Nirgendwo in Deutschland": 5,
    "100 km": 4,
    "10 km": 3,
    "1 km": 2,
    "500 m": 1,
    "Überhaupt kein Vertrauen": 1,
    "Geringes Vertrauen ": 2,
    "Mäßiges Vertrauen ": 4,
    "Starkes Vertrauen": 5,
}

cols = Germany.columns[df.dtypes == "object"]
Germany[cols] = Germany[cols].replace(replacer)


Germany.drop(
    columns=[
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
        "Inwiefern vertrauen Sie darauf, dass diese Gruppen im Interesse der Gesellschaft handeln werden?",
        "Unterstützen Sie die Einführung der folgenden Technologien?.1",
    ],
    inplace=True,
)


print(Germany.shape)

# DROP PARTICIPANTS WHO DID NOT FINISH THE SURVEY
nan_percentage = Germany.isna().mean(axis=1) * 100
Germany = Germany[nan_percentage <= 40]
print(Germany.shape)

# COMPLETION TIME
Germany["Started on"] = pd.to_datetime(
    Germany["Started on"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
)
Germany["Last updated on"] = pd.to_datetime(
    Germany["Last updated on"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
)
completion_time = Germany["Last updated on"] - Germany["Started on"]
Germany.insert(
    loc=Germany.columns.get_loc("Last updated on") + 1,
    column="Completion time",
    value=completion_time,
)
Germany.drop(
    columns=["Started on", "Last updated on"], inplace=True
)  # DROP THE COLUMNS ONCE THE COMPLETION TIME IS CALCULATED


# DROP PARTICIPANTS WHO "COMPLETED" THE SURVEY TOO FAST
Germany = Germany[Germany["Completion time"] >= pd.Timedelta(minutes=3)]

# AVERAGE CLIMATE CHANGE AWARENESS
average_ccawareness = Germany[
    ["Climate Change 1", "Climate Change 2", "Climate Change 3", "Climate Change 4"]
].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Climate Change 4") + 1,
    column="CC Awareness",
    value=average_ccawareness,
)
# Germany.drop(columns = ['Climate Change 1', 'Climate Change 2', 'Climate Change 3', "Climate Change 4"], inplace=True) #MIGHT DROP THE COLUMNS ONCE THE AVERAGE IS CALCULATED

# AVERAGE FEELINGS OF TAMPERING WITH NATURE
average_tampering = Germany[["Tampering 1", "Tampering 2", "Tampering 3"]].mean(axis=1)
inverted = (
    6 - average_tampering
)  # THE QUESTIONS RELATED TO TAMPERING WITH NATURE HAVE AN INVERTED RESPONSE SCALE BECAUSE THEY ARE NEGATIVE QUESTIONS
Germany.insert(
    loc=Germany.columns.get_loc("Tampering 3") + 1,
    column="Tampering with nature",
    value=average_tampering,
)
# Germany.insert(loc=Germany.columns.get_loc('Tampering 3') + 2, column="Tampering inverted", value=inverted)

# AVERAGE NIMBY FEELINGS
average_NIMBY = Germany[["NIMBY 1", "NIMBY 2", "NIMBY 3"]].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("NIMBY 3") + 1, column="NIMBY", value=average_NIMBY
)

# AVERAGE TRANSPORT ACCEPTANCE
replacer2 = {"x": 1, "": 0}
columns_to_replace = [
    "Transport 1",
    "Transport 2",
    "Transport 3",
    "Transport 4",
    "Transport 5",
    "Transport 6",
]
Germany[columns_to_replace] = Germany[columns_to_replace].fillna(
    0
)  # SHOULD WE COUNT THEM AS ZERO? WHAT ABOUT THE PEOPLE WHO SAID "WEI? NICHT"?
Germany[columns_to_replace] = Germany[columns_to_replace].replace(replacer2)

avg_transport = Germany[
    ["Transport 1", "Transport 2", "Transport 3", "Transport 4"]
].mean(axis=1)
avg_transport = np.where(Germany["Transport 5"] != 0, 0, avg_transport)
avg_transport = np.where(Germany["Transport 6"] != 0, np.nan, avg_transport)
Germany.insert(
    loc=Germany.columns.get_loc("Transport 6") + 1,
    column="Transport Acceptance",
    value=avg_transport,
)

# AVERAGE COST PERCEPTION
average_cost = Germany[["Cost 1", "Cost 2"]].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Cost 2") + 1,
    column="Cost perception",
    value=average_cost,
)

# AVERAGE BENEFIT PERCEPTION
average_benefit = Germany[["Benefit 1", "Benefit 2", "Benefit 3"]].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Benefit 2") + 1,
    column="Benefit perception",
    value=average_benefit,
)

# AVERAGE SAFETY OF THE TECHNOLOGY PERCEPTION
average_safety = Germany[["Safety 1", "Safety 2"]].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Safety 2") + 1,
    column="Safety perception",
    value=average_safety,
)

# AVERAGE RISK PERCEPTION
average_risk = Germany[["Risk 1", "Risk 2", "Risk 3"]].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Risk 3") + 1,
    column="Risk perception",
    value=average_risk,
)

# AVERAGE TRUST
average_trust = Germany[
    ["Trust 1", "Trust 2", "Trust 3", "Trust 4", "Trust 5", "Trust 6", "Trust 7"]
].mean(axis=1)
Germany.insert(
    loc=Germany.columns.get_loc("Trust 7") + 1, column="Trust", value=average_trust
)

# ENGAGEMENT
Germany["Engagement"].fillna(0, inplace=True)
Germany.loc[Germany["Engagement"] != 0, "Engagement"] = 1

# PLOT THE DATA
from bokeh.palettes import HighContrast3
from bokeh.plotting import figure, show

Tampering = ["Tampering 1", "Tampering 2", "Tampering 3"]
years = [1, 2, 3]

p = figure(
    x_range=Tampering,
    height=250,
    title="Tampering with Nature",
    toolbar_location=None,
    tools="hover",
    tooltips="$name @Tampering: @$name",
)

p.vbar_stack(
    years,
    x="Tampering",
    width=0.9,
    color=HighContrast3,
    source=Germany,
    legend_label=years,
)

p.y_range.start = 0
p.x_range.range_padding = 0.1
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

show(p)

# CORRELATION
# Germany.corr(method="pearsons")
