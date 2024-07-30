from dacstore.dac_analysis import get_df

data = "data/data.csv"


def main(filename):
    df = get_df(filename)
    # do analysis here


if __name__ == "__main__":
    main(data)
