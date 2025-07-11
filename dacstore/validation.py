import pandas as pd
import copy


COMPLETION_TIME_LIMIT = pd.Timedelta(156, "sec")

SCORE_LIMIT = 0.45

NOT_COMPLETED = 1
COMPLETION_TIME_TOO_LONG = 2
STRAIGHTLINING = 3
NO_ATTENTION = 4

status_dict = {
    NOT_COMPLETED: {"description": "survey was not completed", "status": False},
    COMPLETION_TIME_TOO_LONG: {
        "description": f"completion time was longer than {COMPLETION_TIME_LIMIT}",
        "status": False,
    },
    STRAIGHTLINING: {"description": "answers seem to be random", "status": False},
    NO_ATTENTION: {"description": "failed attention check", "status": False},
}


check_cols = {
    "Stimme weder zu noch lehne ich ab": [
        "Der Klimawandel findet tatsächlich statt.",
        "Der Klimawandel ist ein ernstes Problem.",
        "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.",
        "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.",
        "DAC ist eine ausgereifte saubere Technologie.",
        "Menschen sollten die Natur nicht auf diese Weise manipulieren.",
        "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.",
        "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.",
        "Emissionen zu reduzieren wäre kosteneffizienter als DAC.",
        "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.",
        "DAC könnte dazu beitragen, schwer vermeidbare Emissionen aus Sektoren wie Landwirtschaft oder Zementproduktion zu entnehmen.",
        "Die Implementierung von DAC als Teil einer Gesamtstrategie kann Deutschland dabei helfen, seine Klimaziele zu erreichen und den Klimawandel auf 1,5 °C zu begrenzen.",
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
        "DAC ist eine effiziente Technologie zur Bekämpfung des Klimawandels.",
        "CO2-Speicherung könnte Erdbeben verursachen.",
        "CO2-Speicherung könnte Explosionen verursachen.",
        "CO2-Speicherung könnte CO2-Leckagen verursachen.",
    ],
    "Weiß nicht": [
        "Der Klimawandel findet tatsächlich statt.",
        "Der Klimawandel ist ein ernstes Problem.",
        "Menschliche Aktivitäten sind die Hauptursache des Klimawandels.",
        "Wir alle sollten uns bemühen, unseren CO2-Ausstoß zu reduzieren.",
        "DAC ist eine ausgereifte saubere Technologie.",
        "Menschen sollten die Natur nicht auf diese Weise manipulieren.",
        "Ich denke nicht, dass das Einbringen von CO2 in den Boden eine gute Idee ist.",
        "Versuche, das Klimasystem durch die Anwendung von DAC zu beeinflussen, zeugen von menschlichem Hochmut.",
        "DAC Anlage",
        "CO2-Speicherung im Boden",
        "CO2-Speicherung im Meeresboden",
        "Emissionen zu reduzieren wäre kosteneffizienter als DAC.",
        "100 € für die Entnahme von 1 Tonne CO2 zu zahlen, ist ein angemessener Preis.",
        "DAC könnte dazu beitragen, schwer vermeidbare Emissionen aus Sektoren wie Landwirtschaft oder Zementproduktion zu entnehmen.",
        "Die Implementierung von DAC als Teil einer Gesamtstrategie kann Deutschland dabei helfen, seine Klimaziele zu erreichen und den Klimawandel auf 1,5 °C zu begrenzen.",
        "DAC ist sicher.",
        "CO2-Speicherung ist sicher.",
        "DAC ist eine effiziente Technologie zur Bekämpfung des Klimawandels.",
        "CO2-Speicherung könnte Erdbeben verursachen.",
        "CO2-Speicherung könnte Explosionen verursachen.",
        "CO2-Speicherung könnte CO2-Leckagen verursachen.",
        "Politik",
        "Industrie",
        "Wissenschaft",
        "Vereinte Nationen (UNO)",
        "Europäische Union",
        "Nichtregierungs- und Umweltschutzorganisationen",
        "Medien",
    ],
    "Neutral": [
        "Direct Air Capture (DAC)",
        "CO2-Speicherung",
        "Politik",
        "Industrie",
        "Wissenschaft",
        "Vereinte Nationen (UNO)",
        "Europäische Union",
        "Nichtregierungs- und Umweltschutzorganisationen",
        "Medien",
        "Direct Air Capture (DAC).1",
        "CO2-Speicherung.1",
    ],
}


attention_col = {
    "Bei dieser Frage ignorieren Sie bitte die folgenden Optionen und wählen Sie 'Stimme nicht zu'.": "Stimme nicht zu"
}


def total_cols(row):
    all_cols = 0
    for questions in check_cols.values():
        all_cols += len(row[questions][~row[questions].isnull()])
    return all_cols


def create_row_status(status):
    report = ""
    for k, v in status.items():
        if v["status"] is True:
            report += " | " if report else ""
            report += v["description"]
    if not report:
        report = "valid"
    return report


def check_answers(row):
    score = 0
    for answer, questions in check_cols.items():
        # check if answer might be random
        score += row[questions].value_counts().get(answer, 0)
    # print(total_cols(row))
    return score / total_cols(row)


def check_row(row):
    """Check valid status of a row"""
    status = copy.deepcopy(status_dict)

    if row.Status != "Completed":
        status[NOT_COMPLETED]["status"] = True
        return create_row_status(status)

    if row.completion_time < COMPLETION_TIME_LIMIT:
        status[COMPLETION_TIME_TOO_LONG]["status"] = True
        status[COMPLETION_TIME_TOO_LONG]["description"] = "completion time too short"

    for k, v in attention_col.items():
        if row[k] != v:
            status[NO_ATTENTION]["status"] = True

    score = check_answers(row)

    if score > SCORE_LIMIT:
        status[STRAIGHTLINING]["status"] = True
        status[STRAIGHTLINING]["description"] = "straightlining"

    return create_row_status(status)


def gender_age(df):
    """Return gender age groups of valid answers"""
    return (
        df[
            df.valid == "valid"
        ]  # .sort_values(['Geschlecht','Altersgruppe'],ascending=False)
        .groupby("Geschlecht")
        .Altersgruppe.value_counts(normalize=False)
        .sort_index()
    )


def valid(df):
    "add a colum with validation check"
    return df.apply(check_row, axis=1)


def highlight_invalid(row):
    """Highlight cells"""
    invalid = row.valid != "valid"
    # print(invalid)
    return ["background-color: red" if invalid else ""] * len(row)
