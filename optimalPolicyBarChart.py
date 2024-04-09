import matplotlib.pyplot as plt

# Updated policies and stakeholders
policies = [
    {"name": "policyA", "security": 7, "utility": 8, "privacy": 9, "accessibility": 8},
    {"name": "policyB", "security": 9, "utility": 9, "privacy": 5, "accessibility": 6},
    {"name": "policyC", "security": 8, "utility": 6, "privacy": 10, "accessibility": 7}
]

stakeholders = [
    {"name": "car_workshop", "weights": {"security": 0.1, "utility": 0.3, "privacy": 0.2, "accessibility": 0.4}},
    {"name": "car_owner", "weights": {"security": 0.3, "utility": 0.1, "privacy": 0.5, "accessibility": 0.1}},
    {"name": "car_manufacturer", "weights": {"security": 0.3, "utility": 0.4, "privacy": 0.2, "accessibility": 0.2}},
    {"name": "insurance_company", "weights": {"security": 0.4, "utility": 0.3, "privacy": 0.2, "accessibility": 0.1}}
]

alpha = {
    "car_workshop": 1.5,
    "car_owner": 1.0,
    "car_manufacturer": 0.5,
    "insurance_company": 0.2
}

def calculate_utility(policy, stakeholder):
    utility_score = 0
    for criterion, weight in stakeholder['weights'].items():
        policy_score = policy.get(criterion, 0)
        utility_score += weight * policy_score
    return utility_score

def calculate_aggregate_utility(policies, stakeholders, alpha):
    aggregate_utilities = {}
    for policy in policies:
        aggregate_utility = 0
        for stakeholder in stakeholders:
            utility = calculate_utility(policy, stakeholder)
            stakeholder_influence = alpha.get(stakeholder['name'], 1)
            aggregate_utility += stakeholder_influence * utility
        aggregate_utilities[policy['name']] = aggregate_utility
    return aggregate_utilities

def find_optimal_policy(aggregate_utilities):
    return max(aggregate_utilities.items(), key=lambda x: x[1])

# Calculate the aggregate utilities and find the optimal policy
aggregate_utilities = calculate_aggregate_utility(policies, stakeholders, alpha)
optimal_policy_name, _ = find_optimal_policy(aggregate_utilities)
optimal_policy = next(policy for policy in policies if policy['name'] == optimal_policy_name)

# Calculate the utility of the optimal policy for each stakeholder
optimal_utilities = [calculate_utility(optimal_policy, stakeholder) for stakeholder in stakeholders]
stakeholder_names = [stakeholder['name'] for stakeholder in stakeholders]

# Plotting
plt.figure(figsize=(10, 6))
bars = plt.bar(stakeholder_names, optimal_utilities, color='skyblue')

# Mark the utility threshold
utility_threshold = 7
plt.axhline(y=utility_threshold, color='r', linestyle='--')
plt.title(f'Utility Scores for Optimal Policy "{optimal_policy_name}" Across Stakeholders')
plt.ylabel('Utility Score')
plt.xlabel('Stakeholder')
plt.xticks(rotation=45)

# Annotate bars with their utility scores
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval,2), va='bottom')

plt.show()
