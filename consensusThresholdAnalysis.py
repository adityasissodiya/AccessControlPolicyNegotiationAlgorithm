import matplotlib.pyplot as plt
import numpy as np
from experimentImplementation import calculate_utility
from experimentImplementation import policies
from experimentImplementation import stakeholders

#The plot visualizes how the ability of policies to achieve consensus among 
#stakeholders changes as the utility threshold varies. 
#It provides insights into the sensitivity of consensus achievement to the 
#utility threshold, which can be crucial for decision-making processes 
#where stakeholder agreement is important.

def consensus_for_threshold(policies, stakeholders, threshold):
    """
    Determine the number of policies achieving consensus at a given utility threshold.
    
    Parameters:
    - policies: List of policy dictionaries.
    - stakeholders: List of stakeholder dictionaries with weights.
    - threshold: Utility threshold for consensus.
    
    Returns:
    - Integer representing the number of policies achieving consensus.
    """
    count = 0
    for policy in policies:
        if all(calculate_utility(policy, stakeholder) >= threshold for stakeholder in stakeholders):
            count += 1
    return count

# Define a range of utility thresholds to analyze
thresholds = np.linspace(5, 10, 20)

# Calculate the number of policies achieving consensus for each threshold
consensus_counts = [consensus_for_threshold(policies, stakeholders, threshold) for threshold in thresholds]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(thresholds, consensus_counts, marker='o', linestyle='-', color='blue')

plt.title('Consensus Achievement vs. Utility Threshold')
plt.xlabel('Utility Threshold')
plt.ylabel('Number of Policies Achieving Consensus')
plt.grid(True)
plt.xticks(np.arange(min(thresholds), max(thresholds)+1, 0.5))
plt.yticks(range(0, len(policies)+1))

plt.tight_layout()
plt.show()