import pandas as pd
import numpy as np

'''
Possible explicative variables for the discourse in the queer community:
- Political context:
    - Political stability and absence of violence/terrorisme:
        - Measured as Percentile Rank by the World Bank
    - Rule of Law:
        - Measured as Percentile Rank by the World Bank
    - Proportion of seats held by women in national parliaments (%) by the World Bank
    - Voice and Accountability:
        - Measured as Percentile Rank by the World Bank
- Economic context:
    - Income group: as defined by the World Bank
        - High income
        - Upper middle income
        - Lower middle income
        - Low income
    - GDP:
        - Measure as GDP (current US$) by the World Bank
- Education context:
    - Children out of school (% of primary school age) by the World Bank
    - Current education expenditure, total (% of total expenditure in public institutions) by the World Bank
    - Literacy rate, adult total (% of people ages 15 and above) by the World Bank
- Health context:
    - Antiretroviral therapy coverage (% of people living with HIV) by the World Bank
    - Current health expenditure (% of GDP) by the World Bank
    - UHC service coverage index by the World Bank
- LGBT+ context:
    - LGBT+ rights index available here (https://ourworldindata.org/lgbt-rights)
    - Same-sex sexual acts illegal available here (https://ourworldindata.org/lgbt-rights)
    - Censorship of LGBT issues available here (https://ourworldindata.org/lgbt-rights)
    - Gender marker change available here (https://ourworldindata.org/lgbt-rights)
    - Hate crimes based on sexual orientation or gender identity are an aggravating circumstance, 2019 available here (https://ourworldindata.org/lgbt-rights)
'''


def get_WB_features(paths, df, names, income, j = 0):
    for i in paths:       
        j += 1
        feature = pd.read_csv(i, skiprows=4)
        feature.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973',
                          '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991',
                          '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
                          '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
        mean = []
        for index, rows in feature.iterrows():
            mean.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
        feature.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
        df["Country Code"] = feature["Country Code"]
        df[f"feature_{j}"] = mean
    df.rename(columns=names, inplace=True)
    df_merged = df.merge(income, how="right", on="Country Code")
    df_merged.dropna(subset = "Region", inplace=True)
    return df_merged

def get_income(path):
    country_income = pd.read_csv(path)
    country_income.drop(columns=["SpecialNotes", "Unnamed: 5"], inplace = True)
    country_income.rename(columns={"TableName": "Country Name"}, inplace=True)
    return country_income

def get_rights(path, df):
    rights = pd.read_csv(path) # "../data/charactCountry/equality/lgbt_rights_index.csv"
    rights = rights.pivot(index=["Entity", "Code"], columns="Year", values="LGBT+ Policy Index")
    rights.columns.name = None
    rights.reset_index(inplace=True)
    rights.rename(columns={"Code": "Country Code"}, inplace=True)
    rights.drop(columns=[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
                         2015, 2016], inplace = True)
    mean_rights = []
    for index, rows in rights.iterrows():
        mean_rights.append(np.nanmean([rows[2017], rows[2018], rows[2019]]))
    rights["mean_rights"] = mean_rights
    rights.dropna(subset="Country Code", inplace=True)
    rights.drop(columns=[2017, 2018, 2019], inplace = True)
    df1 = df.merge(rights, how="left", on= "Country Code")
    df1.drop(columns="Entity", inplace=True)
    return df1

def get_sex_illegal(path, df):
    sex = pd.read_csv(path) # "../data/charactCountry/equality/sex_illegal.csv"
    sex = sex.pivot(index=["Entity", "Code"], columns="Year", values="Same-sex sexual acts illegal")
    sex.columns.name = None
    sex.reset_index(inplace=True)
    sex.rename(columns={"Code": "Country Code"}, inplace=True)
    sex.drop(columns=[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
                      2015, 2016], inplace = True)
    mean_sex_index = []
    for index, rows in sex.iterrows():
        mean_sex_index.append(np.nanmean([rows[2017], rows[2018], rows[2019]]))
    sex["mean_sex_index"] = mean_sex_index
    sex.dropna(subset="Country Code", inplace=True)
    sex.drop(columns=[2017, 2018, 2019], inplace = True)
    df1 = df.merge(sex, how="left", on= "Country Code")
    df1.drop(columns="Entity", inplace=True)
    return df1

def get_censor(path, df):
    censor = pd.read_csv(path) # "../data/charactCountry/equality/censorship.csv"
    censor.rename(columns={"Censorship of LGBT issues (current)": "censor"}, inplace=True)
    censor.rename(columns={"Code": "Country Code"}, inplace=True)
    censor.loc[censor[censor["Entity"]=="Faeroe Islands"].index, "Country Code"] = "FRO"
    censor.loc[censor[censor["Entity"]=="Timor"].index, "Country Code"] = "TLS"
    df1 = df.merge(censor, how="left", on= "Country Code")
    df1.drop(columns="Entity", inplace=True)
    return df1

def get_trans_marker(path, df):
    trans = pd.read_csv(path) # "../data/charactCountry/equality/transitions.csv"
    trans.rename(columns={"Right to change legal gender (current)": "transition"}, inplace=True)
    trans.rename(columns={"Code": "Country Code"}, inplace=True)
    trans.drop(columns="Year", inplace=True)
    trans.loc[trans[trans["Entity"]=="Faeroe Islands"].index, "Country Code"] = "FRO"
    trans.loc[trans[trans["Entity"]=="Timor"].index, "Country Code"] = "TLS"
    df1 = df.merge(trans, how="left", on= "Country Code")
    df1.drop(columns="Entity", inplace=True)
    return df1

def get_hate_protection(path, df):
    hate = pd.read_csv(path) # "../data/charactCountry/equality/hate_protection.csv"
    hate = hate.pivot(index=["Entity", "Code"], columns="Year", values="Hate crime protections")
    hate.columns.name = None
    hate.reset_index(inplace=True)
    hate.rename(columns={"Code": "Country Code"}, inplace=True)
    hate.drop(columns=[1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
                       2015, 2016], inplace = True)
    mean_hate_protection = []
    for index, rows in hate.iterrows():
        mean_hate_protection.append(np.nanmean([rows[2017], rows[2018], rows[2019]]))
    hate["mean_hate_protection"] = mean_hate_protection
    hate.drop(columns=[2017, 2018, 2019], inplace = True)
    df1 = df.merge(hate, how="left", on= "Country Code")
    df1.drop(columns="Entity", inplace=True)
    return df1

def preimpute_features(df):
    df.loc[df[df['IncomeGroup'].isna()].index, "IncomeGroup"] = "Lower middle income"
    df["mean_stability"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_stability"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_law"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_law"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_female_seats"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_female_seats"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_voice"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_voice"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_gdp"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_gdp"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_children_out"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_children_out"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_ed_exp"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_ed_exp"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_literacy"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_literacy"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_ARV_coverage"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_ARV_coverage"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_health_exp"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_health_exp"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_UHC_coverage"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_UHC_coverage"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_rights"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_rights"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_sex_index"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_sex_index"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    df["mean_hate_protection"] = df.drop(columns=["Country Code", "Region", "Country Name"]).groupby(["IncomeGroup", "censor", "transition"])["mean_hate_protection"].apply(lambda x: x.fillna(x.mean())).reset_index(drop=True)
    return df

def get_features_csv(df, name):
    df.to_csv(f"../data/charactCountry/{name}.csv")
    


list_paths_WB = ["../data/charactCountry/stability/global_bank_rank.csv", "../data/charactCountry/equality/rule_law.csv",
                 "../data/charactCountry/equality/female_seats.csv", "../data/charactCountry/equality/voice.csv",
                 "../data/charactCountry/gdp/global_bank_gdp.csv",
                 "../data/charactCountry/education/global_bank_children_out.csv",
                 "../data/charactCountry/education/global_bank_edExpenditure.csv", 
                 "../data/charactCountry/education/literacy.csv", "../data/charactCountry/health/ARV_coverage.csv",
                 "../data/charactCountry/health/health_exp.csv", "../data/charactCountry/health/UHC_coverage.csv"]
column_names = {
    "feature_1": "mean_stability",
    "feature_2": "mean_law",
    "feature_3": "mean_female_seats",
    "feature_4": "mean_voice",
    "feature_5": "mean_gdp",
    "feature_6": "mean_children_out",
    "feature_7": "mean_ed_exp",
    "feature_8": "mean_literacy",
    "feature_9": "mean_ARV_coverage",
    "feature_10": "mean_health_exp",
    "feature_11": "mean_UHC_coverage",
}

country_income = get_income("../data/charactCountry/stability/Metadata_Country.csv")
df = get_WB_features(list_paths_WB, pd.DataFrame(), column_names, country_income)
df1 = get_rights("../data/charactCountry/equality/lgbt_rights_index.csv", df)
df2 = get_sex_illegal("../data/charactCountry/equality/sex_illegal.csv", df1)
df3 = get_censor("../data/charactCountry/equality/censorship.csv", df2)
df4 = get_trans_marker("../data/charactCountry/equality/transitions.csv", df3)
df5 = get_hate_protection("../data/charactCountry/equality/hate_protection.csv", df4)
df5 = preimpute_features(df5)
get_features_csv(df5, "country_features")