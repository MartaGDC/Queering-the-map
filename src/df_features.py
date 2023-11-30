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

def get_stability(path1, path2):
    stability_score = pd.read_csv(path1, skiprows=4)
    stability_score.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971',
                                  '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988',
                                  '1989', '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005',
                                  '2006', '2007', '2008', '2009', '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
    mean_stability= []
    for index, rows in stability_score.iterrows():
        mean_stability.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
    stability_score["mean_stability"] = mean_stability
    stability_score.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
    
    country_codes = pd.read_csv(path2)
    country_codes.drop(columns=["SpecialNotes", "Unnamed: 5", "TableName"], inplace = True)
    stability = stability_score.merge(country_codes, how="left", on="Country Code")
    stability.dropna(subset = "Region", inplace=True)
    
    return stability


stability = get_stability("../data/charactCountry/stability/global_bank_rank.csv", "../data/charactCountry/stability/Metadata_Country.csv")


def get_GDP(path, df):
    gdp = pd.read_csv(path, skiprows=4)
    gdp.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973',
                      '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991',
                      '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
                      '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
    mean_gdp = []
    for index, rows in gdp.iterrows():
        mean_gdp.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
    gdp["mean_gdp"] = mean_gdp
    gdp.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
    df1 = gdp.merge(df)
    return df1


df1 = get_GDP("../data/charactCountry/gdp/global_bank_gdp.csv", stability)


def get_children_out(path, df):
    child = pd.read_csv(path, skiprows=4)
    child.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967','1968', '1969', '1970', '1971', '1972', '1973',
                        '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991',
                        '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
                        '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
    mean_child_noSchool = []
    for index, rows in child.iterrows():
        mean_child_noSchool.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
    child["mean_child_noSchool"] = mean_child_noSchool
    child.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
    df1 = df.merge(child)
    return df1


df2 = get_children_out("../data/charactCountry/education/global_bank_children_out.csv", df1)


def get_ed_expenditure(path, df):
    ed_exp = pd.read_csv(path, skiprows=4)
    ed_exp.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
                         '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990',
                         '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
                         '2009', '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
    mean_ed_exp = []
    for index, rows in ed_exp.iterrows():
        mean_ed_exp.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
    ed_exp["mean_ed_exp"] = mean_ed_exp
    ed_exp.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
    df1 = df.merge(ed_exp)
    return df1


df3 = get_ed_expenditure("../data/charactCountry/education/global_bank_edExpenditure.csv", df2)


def get_literacy(path, df):
    literacy = pd.read_csv(path, skiprows=4)
    literacy.drop(columns=['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972',
                           '1973', '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990',
                           '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
                           '2009', '2010', "2011", "2012", "2013", "2014", "2015", "2016", 'Unnamed: 67'], inplace = True)
    mean_literacy = []
    for index, rows in literacy.iterrows():
        mean_literacy.append(np.nanmean([rows["2017"], rows["2018"], rows["2019"], rows["2020"], rows["2021"], rows["2022"]]))
    literacy["mean_literacy"] = mean_literacy
    literacy.drop(columns=["2017", "2018", "2019", "2020", "2021", "2022"], inplace = True)
    

"../data/charactCountry/education/literacy.csv"
