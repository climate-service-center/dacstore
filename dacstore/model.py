import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor


def multicollinearity(X):
    """Check for multicollinearity"""
    # Check for multicollinearity using VIF
    X = sm.add_constant(X)  # Add a constant to the model (intercept)
    vif_data = pd.DataFrame()
    vif_data["feature"] = X.columns
    vif_data["VIF"] = [
        variance_inflation_factor(X.values, i) for i in range(X.shape[1])
    ]
    # print("\nVariance Inflation Factor (VIF):")
    # print(vif_data)
    return vif_data


def create_model(y, X):
    """Create a model"""
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model
