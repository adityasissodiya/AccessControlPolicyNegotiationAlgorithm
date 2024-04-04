# ABAC Policy Negotiation Algorithm Experiment

This repository contains the implementation and experimental setup for evaluating an Attribute-Based Access Control (ABAC) policy negotiation algorithm. The algorithm optimizes policy selection based on the collective preferences of multiple stakeholders through utility functions.

## Objective

The primary objective of this experiment is to validate the effectiveness of the ABAC policy negotiation algorithm in identifying the optimal policy $(P^*\)$ that maximizes aggregate utility, considering diverse stakeholder preferences and criteria such as security, usability, and compliance.

## Experiment Setup

### Data Preparation

- **Policies (\(P\))**: A predefined set of potential ABAC policies with varied attributes.
- **Stakeholders (\(A\))**: A group of stakeholders with distinct preferences, represented by weights (\(w_{a_i,l}\)) assigned to different criteria.
- **Criteria Evaluation Functions (\(f_l(P_j)\))**: Functions that assess policies based on specific criteria.

### Implementation Steps

1. **Utility Evaluation**: Calculate the utility for each policy from each stakeholder's perspective.
2. **Aggregate Utility Calculation**: Compute the aggregate utility for each policy.
3. **Optimization**: Identify the policy that maximizes aggregate utility.
4. **Consensus Check**: Determine if the optimal policy achieves consensus among stakeholders.
5. **Policy Selection**: Select the policy if it meets consensus; otherwise, adjust and iterate.

## Metrics

- Individual and aggregate utility scores.
- Degree of consensus among stakeholders.
- Sensitivity to changes in stakeholders' weights and preferences.

## Visualizations

- Bar Chart for Individual Stakeholder Utilities
- Heatmap for Weight Assignments
- Line Graph for Aggregate Utilities
- Scatter Plot for Optimization and Consensus
- Spider Chart for Policy Evaluation on Criteria
- Sensitivity Analysis Graphs

## Analysis

- **Alignment**: Evaluate the alignment of the selected policy with collective preferences.
- **Consensus Achievement**: Assess consensus achievement among stakeholders.
- **Stakeholder Influence Impact**: Investigate the impact of stakeholder influence on policy selection.
- **Policy Attributes Sensitivity**: Examine the sensitivity of policy selection to changes in policy attributes and stakeholder preferences.

## Requirements

- Python 3.x
- Libraries: numpy, matplotlib, seaborn (for visualizations)

## Figures
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/aggregateUtilityOfPolicies.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/consensusAchievementUtilityThreshold.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/stakeholderUtilityMap.png)
![alt text](https://github.com/adityasissodiya/abacPolicyNegotiationAlgorithm/blob/main/figures/utilityScoreDistribution.png)
