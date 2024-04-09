# Creating a box plot for the distribution of utilities for each policy across all stakeholders
# Re-import necessary libraries and redefine the setup due to execution state reset
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Redefine data structures and functions
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

def calculate_utility(policy, stakeholder):
    utility_score = 0
    for criterion, weight in stakeholder['weights'].items():
        policy_score = policy.get(criterion, 0)  # Default to 0 if criterion not in policy
        utility_score += weight * policy_score
    return utility_score

# Calculate the utility of each policy for each stakeholder to get the data for plotting
utility_data = {policy['name']: [] for policy in policies}  # Initialize dictionary to store utilities for each policy

for policy in policies:
    for stakeholder in stakeholders:
        utility = calculate_utility(policy, stakeholder)
        utility_data[policy['name']].append(utility)

# Prepare the data for plotting
data_to_plot = []
for policy_name, utility_scores in utility_data.items():
    for score in utility_scores:
        data_to_plot.append((policy_name, score))

# Convert to DataFrame
df = pd.DataFrame(data_to_plot, columns=['Policy', 'Utility'])

plt.figure(figsize=(10, 6))
sns.boxplot(x='Policy', y='Utility', data=df)
plt.title('Distribution of Utilities for Each Policy Across All Stakeholders')
plt.ylabel('Utility Score')
plt.xlabel('Policy')
plt.grid(True)
plt.show()
