import matplotlib.pyplot as plt
import numpy as np
from experimentImplementation import calculate_aggregate_utility, policies, stakeholders, find_optimal_policy

# Assuming these are your stakeholder names
stakeholder_names = ["car_workshop", "car_owner", "car_manufacturer", "insurance_company"]

# Initialize a dictionary to hold the optimal policy for each alpha scenario
optimal_policies = {name: [] for name in stakeholder_names}

# Range of alpha values to test (for simplicity, we use a common range for all stakeholders)
alpha_values = np.linspace(0, 1, 11)  # Creates 11 values from 0 to 1 inclusive

for stakeholder in stakeholder_names:
    for alpha in alpha_values:
        # Adjust the alpha for the current stakeholder
        alpha_dict = {name: alpha if name == stakeholder else 1 for name in stakeholder_names}
        
        # Calculate the aggregate utilities for this alpha scenario
        aggregate_utilities = calculate_aggregate_utility(policies, stakeholders, alpha=alpha_dict)
        
        # Determine and record the optimal policy for this scenario
        optimal_policy_name, _ = find_optimal_policy(aggregate_utilities)
        optimal_policies[stakeholder].append(optimal_policy_name)

# Plotting
fig, axes = plt.subplots(1, len(stakeholder_names), figsize=(15, 5), sharey=True)

for i, stakeholder in enumerate(stakeholder_names):
    ax = axes[i]
    ax.plot(alpha_values, optimal_policies[stakeholder], marker='o', label=stakeholder)
    ax.set_title(stakeholder)
    ax.set_xlabel('Alpha Value')
    ax.set_xticks(alpha_values)
    ax.set_xticklabels([f"{alpha:.1f}" for alpha in alpha_values], rotation=45)
    if i == 0:
        ax.set_ylabel('Optimal Policy')

plt.suptitle('Optimal Policy Selection vs. Stakeholder Influence')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
