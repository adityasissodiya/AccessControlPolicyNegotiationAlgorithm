import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from experimentImplementation import calculate_utility, policies, stakeholders
# Assuming the calculate_utility function and your policies and stakeholders are defined

# Calculate utilities for each policy-stakeholder combination and store in a nested dictionary
utilities = {policy['name']: {stakeholder['name']: calculate_utility(policy, stakeholder)
                              for stakeholder in stakeholders} for policy in policies}

# Convert the nested dictionary into a Pandas DataFrame for easier plotting
utilities_df = pd.DataFrame(utilities).T  # Transpose to have policies as rows and stakeholders as columns

# Plotting the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(utilities_df, annot=True, cmap='viridis', fmt=".2f")

plt.title('Stakeholder Utility Heatmap')
plt.xlabel('Stakeholder')
plt.ylabel('Policy')
plt.xticks(rotation=45)
plt.yticks(rotation=0)

plt.show()
