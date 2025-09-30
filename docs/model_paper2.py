#!/usr/bin/env python
# coding: utf-8

# # Acceptance analysis of Direct Air Capture and Storage

# Documentation of the analysis.

# ## Overview and correlation matrix
# 
# In the first part, we compute certain mean values of groups of questions and plot the correlation matrix:


# uncomment the following lines to enable ../ in sys.path
import sys
import os

#get_ipython().system('pwd')
sys.path.append(os.path.abspath("../"))



import numpy as np
import pandas as pd

import sys
import os

from dacstore.utils import ensure_floats, get_data
from dacstore.model import cronbach_alpha
from dacstore.config import replacer, weighting_groups
from dacstore.dac_analysis import (
    compute_group_averages,
    fix_agreement,
)
import seaborn as sns
import matplotlib.pyplot as plt

# Get the output folder name from the command-line argument
if len(sys.argv) > 1:
    FILTER = sys.argv[1] # first argument is the filter type
    FOLDER_NAME = sys.argv[2] # second argument is the output folder
    
else:
    FILTER = "no_attention"
    FOLDER_NAME = "e1_"


# Create the output folder if it doesn't exist
# took last part of the folder name from the FOLDER_NAME, which is a path, after last /
index = FOLDER_NAME.rfind("/")
output_folder = FOLDER_NAME[index + 1:] + '_' + FILTER

if not os.path.exists(f"../results/{output_folder}"):
    os.makedirs(f"../results/{output_folder}")
    os.makedirs(f"../results/{output_folder}/dac")
    os.makedirs(f"../results/{output_folder}/co2_storage")

# Use the output folder as needed
print(f"Output folder: {output_folder}")

## Here starts the actual analysis:
cols = [
    "climate_change_perception",
    "tampering_with_nature",
    "maturity_of_technology",
    "benefit_perception",
    "cost",
    "risk",
    "trust",
    "emotion",
    "distance",
    "dac_knowledge",
    "storage_knowledge",
    "initial_storage_support",
    "final_storage_support",
    "initial_dac_support",
    "final_dac_support",
    "age",
    "gender",
    "education",
    "occupation",
    "state",
]

independent = [
    "final_dac_support",
    "final_storage_support",
    "initial_storage_support",
    "initial_dac_support",
]


def create_numeric_data(df):
    """Create numeric data for regressions"""
    df = df.replace(replacer)
    df = fix_agreement(df)
    df = ensure_floats(df, weighting_groups)
    df = compute_group_averages(df, weighting_groups)
    return df

# read the raw data and print column names
df_raw = pd.read_csv("../data/data.csv")

print("Raw data columns:")
print(df_raw.columns)
print(f"Total entries in raw data: {len(df_raw)}")

# show unique collectors
print("Unique collectors in raw data:")
print(df_raw["Collector"].unique()) # ['Deutsche Post' 'Deutschland' 'GERICS' 'Bilendi']

# filter df_raw to only include rows where 'bilendi' in column 'Collector'
df_raw = df_raw[df_raw["Collector"] == "Bilendi"]
print(f"Filtered data to Bilendi only, resulting in {len(df_raw)} entries.")

# write to csv to output folder
df_raw.to_csv(f"../results/{output_folder}/data_bilendi_raw.csv", index=False)
#df_raw.to_csv("../data/data_bilendi.csv", index=False)

# we work here with the original column names, no translation
# also, we replace no knowledge with neutral answers and drop invalid entries
df = get_data(
    source="../data/data_bilendi.csv",
    drop=True,
    translate=False,
    drop_invalid= FILTER, # 'no_attention', # one of True, False, 'no_speeding', 'no_straightlining', 'no_attention', 'no_incomplete'. False include incomplete entries (raw data).
    no_knowledge_to_neutral=True,
    set_dependent=True,
)

print("Data retrieved ...")
print(df.head())
print(df.columns)

# print total entries
print(f"Total entries in filtered data: {len(df)}")

# export filtered data to csv to the output folder
df.to_csv(f"../results/{output_folder}/data_bilendi_filtered.csv", index=False)

# filter by 

# an invalid entry (completed but more than 24hr completion time)
#df = df.drop(91621021) # excluded in Bilendi subset ====> TO DO: check if this is still needed or upgraded

# numerica data is created by replacing likert scales with numeric values
# and creating group averages for the weighting groups to create categorical data
df = create_numeric_data(df)

# we can filter the data here if needed according to some conditions # ===> TO DO: implement function to filter dataframe based on a condition
# df = post_filter(df, condition='1: All entries')

# we calculate the cronbach alpha for the weighting groups
# this should give an indication of how good our interrelated questions are correlated
cronbach = {
    group: cronbach_alpha(df[cols]).item()
    for group, cols in weighting_groups.items()
    if len(cols) > 1
}

# we drop the columns that are not in the weighting groups and not used in the regression
df = df[weighting_groups.keys()]
df = df[~df.isna().any(axis=1)]
df = df[cols]

# we need to drop the dependent variables from the independent variables
X = df[[c for c in df.columns if c not in independent]]


# Let's check Cronbach alpha for our latent variables 



cronbach


# Let's have a look at the correlation matrix:




# Create the correlation matrix
corr = df.corr()

# Generate a mask for the upper triangle; True = do NOT show
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(12, 12))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
# More details at https://seaborn.pydata.org/generated/seaborn.heatmap.html
sns.heatmap(
    corr,  # The data to plot
    mask=mask,  # Mask some cells
    cmap=cmap,  # What colors to plot the heatmap as
    annot=True,  # Should the values be plotted in the cells?
    vmax=0.5,  # The maximum value of the legend. All higher vals will be same color
    vmin=-0.5,  # The minimum value of the legend. All lower vals will be same color
    center=0,  # The center value of the legend. With divergent cmap, where white is
    square=True,  # Force cells to be square
    linewidths=0.5,  # Width of lines that divide cells
    cbar_kws={
        "shrink": 0.5
    },  # Extra kwargs for the legend; in this case, shrink by 50%
    annot_kws={"fontsize": 9},
)

# to output folder
#f.savefig("../results/correlation_matrix.png")
f.savefig(f"../results/{output_folder}/correlation_matrix.png")
#plt.show()
#plt.close()


# ## Creating the models
# 
# In the first part, we check for multicollinearity to check for high correlation between independen variables:




import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

sns.set_theme(color_codes=True)


def multicollinearity(X):
    """Check for multicollinearity"""
    # Check for multicollinearity using VIF
    X = sm.add_constant(X)  # Add a constant to the model (intercept)
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    return vif_data


def create_ols_model(y, X):
    """Create an OLS model"""
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model


multicollinearity(X)

# export to Excel to output folder
vif_data = multicollinearity(X)
vif_data.to_excel(f"../results/{output_folder}/vif_results.xlsx", index=False)

# This seems to be a good model, as all VIF values are below 5.0. Next, let's define our independent variables that we want to model. These are the final support of DAC after the survey was completed and the responders had all information they needed. We do the same investigation for the support of CO2 storage.

# ## DAC support
# 
# First, we create a model for the final DAC support.




y = df["final_dac_support"]
model = create_ols_model(y, X)
model.summary()

# export to Excel file to output folder
# create a dataframe from the summary
summary_df = pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0]
summary_df.to_excel(f"../results/{output_folder}/dac/ols_dac_summary.xlsx")

# Export the full summary to a text file
with open(f"../results/{output_folder}/dac/ols_dac_full_summary.txt", "w") as f:
    f.write(model.summary().as_text())

# ### Interpretation of OLS Regression Results for DAC Support
# 
# The OLS regression results provide insights into the factors influencing support for Direct Air Capture (DAC) of CO2 in the German population. Here is a detailed interpretation of the key metrics and coefficients:
# 
# #### Model Summary
# - **R-squared: 0.656**: This indicates that approximately 65.6% of the variance in the dependent variable (`final_dac_support`) is explained by the independent variables in the model. This suggests a good fit.
# - **Adjusted R-squared: 0.652**: This value adjusts for the number of predictors in the model and is slightly lower than the R-squared, indicating that the model is still a good fit after accounting for the number of predictors.
# - **F-statistic: 166.8**: This tests the overall significance of the model. A high F-statistic value with a very low p-value (Prob (F-statistic): 4.45e-310) indicates that the model is statistically significant.
# - **AIC: 2902 and BIC: 2991**: These are information criteria used for model selection. Lower values generally indicate a better-fitting model.
# 
# #### Coefficients and Significance
# - **const (1.2052, p<0.0001)**: The intercept term, which represents the expected value of `final_dac_support` when all predictors are zero.
# - **climate_change_perception (0.0763, p=0.003)**: A positive and significant coefficient, indicating that higher perception of climate change is associated with increased support for DAC.
# - **tampering_with_nature (-0.2527, p<0.0001)**: A negative and highly significant coefficient, suggesting that concerns about tampering with nature are associated with decreased support for DAC.
# - **maturity_of_technology (0.1022, p<0.0001)**: A positive and significant coefficient, indicating that perceptions of technology maturity are associated with increased support for DAC.
# - **benefit_perception (0.5242, p<0.0001)**: A strong positive and highly significant coefficient, suggesting that higher perceived benefits are strongly associated with increased support for DAC.
# - **cost (-0.0233, p=0.276)**: A negative but not statistically significant coefficient, indicating that perceived cost is not a strong predictor of DAC support.
# - **risk (-0.0593, p=0.128)**: A negative but not statistically significant coefficient, suggesting that perceived risk is not a significant predictor of DAC support.
# - **trust (0.1277, p<0.0001)**: A positive and significant coefficient, indicating that higher trust in institutions is associated with increased support for DAC.
# - **emotion (0.2172, p<0.0001)**: A positive and significant coefficient, suggesting that emotional responses are associated with increased support for DAC.
# - **distance (-0.0429, p=0.018)**: A negative and significant coefficient, indicating that greater perceived distance is associated with decreased support for DAC.
# - **dac_knowledge (0.0796, p=0.002)**: A positive and significant coefficient, indicating that higher knowledge of DAC is associated with increased support.
# - **storage_knowledge (0.0360, p=0.153)**: A positive but not statistically significant coefficient, suggesting that knowledge of CO2 storage is not a significant predictor of DAC support.
# - **age (-0.0474, p=0.001)**: A negative and significant coefficient, indicating that older age is associated with decreased support for DAC.
# - **gender (-0.0084, p=0.830)**: A negative but not statistically significant coefficient, suggesting that gender is not a significant predictor of DAC support.
# - **education (0.0316, p=0.011)**: A positive and significant coefficient, indicating that higher education levels are associated with increased support for DAC.
# - **occupation (-0.0177, p=0.166)**: A negative but not statistically significant coefficient, suggesting that occupation is not a significant predictor of DAC support.
# - **state (-0.0074, p=0.057)**: A negative coefficient, close to being statistically significant, indicating that the state of residence may be associated with decreased support for DAC.
# 
# #### Diagnostic Metrics
# - **Omnibus (30.436, p=0.000)**: Indicates that the residuals are not normally distributed.
# - **Durbin-Watson (1.994)**: Close to 2, suggesting no significant autocorrelation in the residuals.
# - **Jarque-Bera (51.270, p=7.36e-12)**: Indicates that the residuals are not normally distributed.
# - **Skew (-0.166)**: Slightly negative skewness in the residuals.
# - **Kurtosis (3.871)**: Slightly higher than 3, indicating heavier tails than a normal distribution.
# - **Condition Number (217)**: Indicates potential multicollinearity issues if the value is high (generally above 30).
# 
# ### Conclusion
# The model explains a significant portion of the variance in support for DAC, with several predictors showing strong and significant relationships. Key factors influencing support include perceptions of climate change, tampering with nature, technology maturity, perceived benefits, trust, emotional responses, and knowledge of DAC. Some predictors, such as perceived cost, risk, and knowledge of CO2 storage, are not significant. The diagnostic metrics suggest that the model is statistically significant and provides a good fit for the data. Further investigation may be needed to address any potential issues with residual normality and multicollinearity.
# ```

# ### Additional statistical plots
# 
# We will plot some more statistics to get some insight into our data and check our assumption for linearity. In the following plots, we will plot the dependencies between our independent variable `final_dac_support` and the individual factors. Note that we jitter the data points to get a better visual interpretation of the likert scale.




# Create a 4x4 panel plot
fig, axes = plt.subplots(4, 4, figsize=(20, 20), sharex=False, sharey=True)
axes = axes.flatten()

# Plot each scatter plot in the grid
for i, column in enumerate(X.columns):
    sns.regplot(
        y=df["final_dac_support"], x=df[column], x_estimator=np.mean, ax=axes[i]
    )
    if i % 4 == 0:
        axes[i].set_ylabel("Final DAC")
    else:
        axes[i].set_ylabel(None)

plt.tight_layout()
#fig.savefig("../results/dac/final_dac_support_dependencies.png")
fig.savefig(f"../results/{output_folder}/dac/final_dac_support_dependencies.png")
#plt.show()
#plt.close()





# Extract residuals
residuals = model.resid

# Plot histogram of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title("Histogram of Residuals")
plt.xlabel("Residuals")
plt.ylabel("Frequency")
#plt.show()
#plt.savefig("../results/dac/residuals_histogram.png")
plt.savefig(f"../results/{output_folder}/dac/residuals_histogram.png")
#plt.close()

# Plot Q-Q plot of residuals
plt.figure(figsize=(10, 6))
sm.qqplot(residuals, line="45", fit=True)
plt.title("Q-Q Plot of Residuals")
#plt.savefig("../results/dac/residuals_qq.png")
plt.savefig(f"../results/{output_folder}/dac/residuals_qq.png")
#plt.show()
#plt.close()

# Plot residuals vs fitted values
fitted_values = model.fittedvalues
plt.figure(figsize=(10, 6))
sns.residplot(
    x=fitted_values, y=residuals, lowess=True, line_kws={"color": "red", "lw": 1}
)
plt.title("Residuals vs Fitted Values")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
#plt.savefig("../results/dac/residuals_vs_fitted.png")
plt.savefig(f"../results/{output_folder}/dac/residuals_vs_fitted.png")
#plt.show()
#plt.close()


# ## Support of CO2 storage
# 
# Now, we look at the final support of CO2 storage.




y = df["final_storage_support"]
model = create_ols_model(y, X)
model.summary()

# export to Excel file to output folder
# create a dataframe from the summary
summary_df = pd.read_html(model.summary().tables[1].as_html(), header=0, index_col=0)[0]
summary_df.to_excel(f"../results/{output_folder}/co2_storage/ols_co2_storage_summary.xlsx")

# Export the full summary to a text file
with open(f"../results/{output_folder}/co2_storage/ols_co2_storage_full_summary.txt", "w") as f:
    f.write(model.summary().as_text())

# ### Interpretation of OLS Regression Results for CO2 Storage Support
# 
# The OLS regression results provide insights into the factors influencing support for CO2 storage in the German population. Here is a detailed interpretation of the key metrics and coefficients:
# 
# #### Model Summary
# - **R-squared: 0.632**: This indicates that approximately 63.2% of the variance in the dependent variable (`final_storage_support`) is explained by the independent variables in the model. This suggests a good fit.
# - **Adjusted R-squared: 0.628**: This value adjusts for the number of predictors in the model and is slightly lower than the R-squared, indicating that the model is still a good fit after accounting for the number of predictors.
# - **F-statistic: 150.2**: This tests the overall significance of the model. A high F-statistic value with a very low p-value (Prob (F-statistic): 1.17e-289) indicates that the model is statistically significant.
# - **AIC: 3119 and BIC: 3209**: These are information criteria used for model selection. Lower values generally indicate a better-fitting model.
# 
# #### Coefficients and Significance
# - **const (2.5420, p<0.0001)**: The intercept term, which represents the expected value of `final_storage_support` when all predictors are zero.
# - **climate_change_perception (0.0994, p<0.0001)**: A positive and significant coefficient, indicating that higher perception of climate change is associated with increased support for CO2 storage.
# - **tampering_with_nature (-0.2852, p<0.0001)**: A negative and highly significant coefficient, suggesting that concerns about tampering with nature are associated with decreased support for CO2 storage.
# - **maturity_of_technology (0.0745, p=0.012)**: A positive and significant coefficient, indicating that perceptions of technology maturity are associated with increased support for CO2 storage.
# - **benefit_perception (0.4060, p<0.0001)**: A strong positive and highly significant coefficient, suggesting that higher perceived benefits are strongly associated with increased support for CO2 storage.
# - **cost (-0.0418, p=0.070)**: A negative coefficient, close to being statistically significant, indicating that higher perceived cost may be associated with decreased support for CO2 storage.
# - **risk (-0.2858, p<0.0001)**: A negative and highly significant coefficient, suggesting that higher perceived risk is associated with decreased support for CO2 storage.
# - **trust (0.0735, p=0.009)**: A positive and significant coefficient, indicating that higher trust in institutions is associated with increased support for CO2 storage.
# - **emotion (0.2643, p<0.0001)**: A positive and significant coefficient, suggesting that emotional responses are associated with increased support for CO2 storage.
# - **distance (-0.0826, p<0.0001)**: A negative and significant coefficient, indicating that greater perceived distance is associated with decreased support for CO2 storage.
# - **dac_knowledge (0.0123, p=0.650)**: A positive but not statistically significant coefficient, suggesting that knowledge of DAC is not a significant predictor of CO2 storage support.
# - **storage_knowledge (0.0936, p=0.001)**: A positive and significant coefficient, indicating that higher knowledge of CO2 storage is associated with increased support.
# - **age (-0.0362, p=0.022)**: A negative and significant coefficient, indicating that older age is associated with decreased support for CO2 storage.
# - **gender (0.0035, p=0.934)**: A positive but not statistically significant coefficient, suggesting that gender is not a significant predictor of CO2 storage support.
# - **education (0.0171, p=0.198)**: A positive but not statistically significant coefficient, indicating that education level is not a strong predictor of CO2 storage support.
# - **occupation (-0.0182, p=0.187)**: A negative but not statistically significant coefficient, suggesting that occupation is not a significant predictor of CO2 storage support.
# - **state (0.0004, p=0.925)**: A positive but not statistically significant coefficient, indicating that the state of residence is not a strong predictor of CO2 storage support.
# 
# #### Diagnostic Metrics
# - **Omnibus (38.286, p=0.000)**: Indicates that the residuals are not normally distributed.
# - **Durbin-Watson (1.964)**: Close to 2, suggesting no significant autocorrelation in the residuals.
# - **Jarque-Bera (50.948, p=8.64e-12)**: Indicates that the residuals are not normally distributed.
# - **Skew (-0.299)**: Slightly negative skewness in the residuals.
# - **Kurtosis (3.711)**: Slightly higher than 3, indicating heavier tails than a normal distribution.
# - **Condition Number (217)**: Indicates potential multicollinearity issues if the value is high (generally above 30).
# 
# ### Conclusion
# The model explains a significant portion of the variance in support for CO2 storage, with several predictors showing strong and significant relationships. Key factors influencing support include perceptions of climate change, tampering with nature, technology maturity, perceived benefits, perceived risk, trust, emotional responses, and perceived distance. Some predictors, such as knowledge of DAC, gender, education, occupation, and state of residence, are not significant. The diagnostic metrics suggest that the model is statistically significant and provides a good fit for the data. Further investigation may be needed to address any potential issues with residual normality and multicollinearity.
# ```

# ### Additional statistical plots
# 
# We will plot some more statistics to get some insight into our data and check our assumption for linearity. In the following plots, we will plot the dependencies between our independent variable `final_storage_support` and the individual factors.




# Create a 4x4 panel plot
fig, axes = plt.subplots(4, 4, figsize=(20, 20), sharex=False, sharey=True)
axes = axes.flatten()

# Plot each scatter plot in the grid
for i, column in enumerate(X.columns):
    sns.regplot(
        y=df["final_storage_support"], x=df[column], x_estimator=np.mean, ax=axes[i]
    )
    if i % 4 == 0:
        axes[i].set_ylabel("Final support of CO2 storage")
    else:
        axes[i].set_ylabel(None)

plt.tight_layout()
#fig.savefig("../results/co2_storage/final_storage_support_dependencies.png")
fig.savefig(f"../results/{output_folder}/co2_storage/final_storage_support_dependencies.png")
#plt.show()
#plt.close()




# Extract residuals
residuals = model.resid

# Plot histogram of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title("Histogram of Residuals")
plt.xlabel("Residuals")
plt.ylabel("Frequency")
#plt.show()
#plt.savefig("../results/co2_storage/residuals_histogram.png")
plt.savefig(f"../results/{output_folder}/co2_storage/residuals_histogram.png")
#plt.close()

# Plot Q-Q plot of residuals
plt.figure(figsize=(10, 6))
sm.qqplot(residuals, line="45", fit=True)
plt.title("Q-Q Plot of Residuals")
#plt.savefig("../results/co2_storage/residuals_qq.png")
plt.savefig(f"../results/{output_folder}/co2_storage/residuals_qq.png")
#plt.show()
#plt.close()

# Plot residuals vs fitted values
fitted_values = model.fittedvalues
plt.figure(figsize=(10, 6))
sns.residplot(
    x=fitted_values, y=residuals, lowess=True, line_kws={"color": "red", "lw": 1}
)
plt.title("Residuals vs Fitted Values")
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
#plt.savefig("../results/co2_storage/residuals_vs_fitted.png")
plt.savefig(f"../results/{output_folder}/co2_storage/residuals_vs_fitted.png")
#plt.show()
#plt.close()

print("Analysis complete.")
print(f"Results saved in folder: ../results/{output_folder}")