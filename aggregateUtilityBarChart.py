import matplotlib.pyplot as plt

# Example aggregate utilities (replace this with your actual data)
aggregate_utilities = {
    "Policy A": 7.2,
    "Policy B": 6.8,
    "Policy C": 7.4
}

# Data preparation
policies = list(aggregate_utilities.keys())
utilities = list(aggregate_utilities.values())

# Plotting
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(policies, utilities, color='skyblue')

ax.set_title('Aggregate Utility of Policies')
ax.set_ylabel('Aggregate Utility Score')
ax.set_xlabel('Policy')
ax.set_ylim([0, max(utilities) + 1])  # Adjust y-axis to show all utilities clearly

# Adding utility scores above bars for clarity
for i, utility in enumerate(utilities):
    ax.text(i, utility + 0.05, f'{utility:.2f}', ha='center', va='bottom')

plt.tight_layout()  # Adjust layout to make room for the labels
plt.show()
