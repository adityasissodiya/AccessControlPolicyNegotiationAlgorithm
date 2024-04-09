import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from experimentImplementation import calculate_utility

# Updating policies and stakeholders based on the new input
policies = [
    {"name": "policyA", "security": 7, "utility": 8, "privacy": 9, "accessibility": 8},
    {"name": "policyB", "security": 9, "utility": 9, "privacy": 5, "accessibility": 6},
    {"name": "policyC", "security": 8, "utility": 6, "privacy": 10, "accessibility": 7}
]

stakeholders = [
    {"name": "car_workshop", 
     "weights": {"security": 0.1, "utility": 0.3, "privacy": 0.2, "accessibility": 0.4}},
    {"name": "car_owner", 
     "weights": {"security": 0.3, "utility": 0.1, "privacy": 0.5, "accessibility": 0.1}},
    {"name": "car_manufacturer", 
     "weights": {"security": 0.3, "utility": 0.4, "privacy": 0.2, "accessibility": 0.2}},
    {"name": "insurance_company", 
     "weights": {"security": 0.4, "utility": 0.3, "privacy": 0.2, "accessibility": 0.1}}
]

# Calculate the utility of each policy for each stakeholder
utility_data = []
stakeholder_names = [stakeholder['name'] for stakeholder in stakeholders]
policy_names = [policy['name'] for policy in policies]

for stakeholder in stakeholders:
    stakeholder_utilities = []
    for policy in policies:
        utility = calculate_utility(policy, stakeholder)
        stakeholder_utilities.append(utility)
    utility_data.append(stakeholder_utilities)

# Convert the utilities into a DataFrame for plotting
utility_df = pd.DataFrame(utility_data, index=stakeholder_names, columns=policy_names)

# Plotting the heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(utility_df, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Stakeholder Utility Heatmap')
plt.ylabel('Stakeholder')
plt.xlabel('Policy')
plt.show()
