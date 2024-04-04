import matplotlib.pyplot as plt
import pandas as pd
# Sample DataFrame creation (replace this with your actual utilities data)
# Each row represents a policy, and columns represent utilities from different stakeholders
utilities_data = {
    "Environmental Group": [7.2, 6.5, 5.8],
    "Local Government": [6.9, 7.1, 6.4],
    "Business Owners": [6.0, 7.3, 7.5]
}
utilities_df = pd.DataFrame(utilities_data, index=["Policy A", "Policy B", "Policy C"])

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot a bar graph
utilities_df.plot(kind='bar', ax=ax)

ax.set_title('Utility Score Distribution by Stakeholder')
ax.set_ylabel('Utility Score')
ax.set_xlabel('Policy')
ax.legend(title='Stakeholder')

plt.xticks(rotation=45)  # Rotate policy names for better readability
plt.tight_layout()  # Adjust layout to not cut off labels
plt.show()