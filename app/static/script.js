// Update sliders display value
document.querySelectorAll('input[type="range"]').forEach(input => {
    input.addEventListener('input', function () {
        let valueSpan = document.getElementById(`${this.id}Value`);
        valueSpan.textContent = this.value;
    });
});

function addPolicy() {
    const policyName = document.getElementById('policyName').value;
    const policyDescription = document.getElementById('policyDescriptionAdd').value;
    const securityScore = document.getElementById('addSecurity').value;
    const utilityScore = document.getElementById('addUtility').value;
    const privacyScore = document.getElementById('addPrivacy').value;
    const accessibilityScore = document.getElementById('addAccessibility').value;

    const policyDetails = {
        security: parseInt(securityScore),
        utility: parseInt(utilityScore),
        privacy: parseInt(privacyScore),
        accessibility: parseInt(accessibilityScore)
    };

    fetch('http://localhost:5000/add/policies', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: policyName,
            details: policyDetails,
            description: policyDescription
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Policy added successfully!');
                console.log(data);
                window.location.reload(); // This will reload the page after the user clicks 'OK'
            } else if (data.error) {
                alert('Failed to add policy: ' + data.error);
            }
        })
        .catch(error => console.error('Error adding policy:', error));
}

function updatePolicy() {
    const policySelect = document.getElementById('policySelect');
    const policyName = policySelect.options[policySelect.selectedIndex].text; // Get the selected option's text
    const policyDescription = document.getElementById('policyDescriptionUpdate').value; // Get the description value
    const details = {
        security: parseInt(document.getElementById('security').value),
        utility: parseInt(document.getElementById('utility').value),
        privacy: parseInt(document.getElementById('privacy').value),
        accessibility: parseInt(document.getElementById('accessibility').value)
    };

    fetch('http://localhost:5000/update/policy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            policy_name: policyName,  // Send the policy name
            details: details,
            description: policyDescription
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Policy updated successfully!');
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Failed to update policy:', error);
            alert('Failed to update policy. See console for more details.');
        });
}

function addStakeholder() {
    const stakeholderName = document.getElementById('stakeholderName').value;
    const stakeholderInfluence = document.getElementById('addStakeholderInfluence').value;

    fetch('http://localhost:5000/add/stakeholders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: stakeholderName,
            influence: parseFloat(stakeholderInfluence)
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert('Stakeholder added successfully!');
                window.location.reload(); // Reloads the page after the user clicks 'OK' in the alert
            } else {
                alert('Failed to add stakeholder: Please check the data provided.');
            }
        })
        .catch(error => console.error('Error adding stakeholder:', error));
}

function fetchPolicies() {
    fetch('http://localhost:5000/get/policies')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('policySelect');
            select.innerHTML = '';  // Clear existing options
            data.forEach(policy => {
                let option = new Option(policy.name, policy.name);  // Set option value to policy.name
                select.appendChild(option);
            });
            if (data.length > 0) {
                updatePolicyForm();  // Automatically update form with the first policy's data
            }
        })
        .catch(error => console.error('Error fetching policies:', error));
}

function updatePolicyForm() {
    const selectedPolicy = document.getElementById('policySelect').value;
    const encodedName = encodeURIComponent(selectedPolicy);  // Now, 'selectedPolicy' is the policy name
    fetch(`http://localhost:5000/get/policy/${encodedName}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('security').value = data.details.security;
            document.getElementById('securityValue').innerText = data.details.security;
            document.getElementById('utility').value = data.details.utility;
            document.getElementById('utilityValue').innerText = data.details.utility;
            document.getElementById('privacy').value = data.details.privacy;
            document.getElementById('privacyValue').innerText = data.details.privacy;
            document.getElementById('accessibility').value = data.details.accessibility;
            document.getElementById('accessibilityValue').innerText = data.details.accessibility;
            document.getElementById('policyDescriptionUpdate').value = data.description;
        })
        .catch(error => console.error('Error updating policy form:', error));
}


// Call fetchPolicies on page load or setup
document.addEventListener('DOMContentLoaded', function () {
    fetchPolicies();
});


function fetchStakeholders() {
    fetch('http://localhost:5000/get/stakeholders')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('stakeholderSelect');
            select.innerHTML = ''; // Clear existing options
            data.forEach(stakeholder => {
                let option = new Option(stakeholder.name, stakeholder.id);
                select.appendChild(option);
            });
            if (data.length > 0) {
                updateStakeholderForm(data[0].id); // Automatically update form with the first stakeholder's data
            }
        })
        .catch(error => console.error('Error fetching stakeholders:', error));
}
document.addEventListener('DOMContentLoaded', fetchStakeholders);

function upDateStakeholder() {
    const stakeholderName = document.getElementById('stakeholderSelect').selectedOptions[0].text; // Assuming the option text is the name
    const influence = document.getElementById('stakeholderInfluence').value;

    fetch('http://localhost:5000/update_stakeholder_by_name', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: stakeholderName,
            influence: influence
        })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Show a simple alert to the user indicating success or failure
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to update stakeholder');
        });
}

function updateStakeholderForm() {
    const selectedStakeholder = document.getElementById('stakeholderSelect').value;
    const encodedName = encodeURIComponent(selectedStakeholder);
    fetch(`http://localhost:5000/get/stakeholder/${encodedName}`)
        .then(response => response.json())
        .then(data => {
            const influenceInput = document.getElementById('stakeholderInfluence');
            const influenceValueSpan = document.getElementById('stakeholderInfluenceValue');

            // Set the influence directly as fetched, no clamping needed with adjusted slider range
            influenceInput.value = data.influence;
            influenceValueSpan.innerText = data.influence.toFixed(1);  // Format to one decimal place
        })
        .catch(error => console.error('Error updating form:', error));
}
document.getElementById('stakeholderSelect').addEventListener('change', () => {
    const selectedId = document.getElementById('stakeholderSelect').value;
    updateStakeholderForm(selectedId);
});


function fetchPoliciesAssign() {
    fetch('http://localhost:5000/get/policies')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('assignPolicySelect');
            select.innerHTML = '';  // Clear existing options
            data.forEach(policy => {
                let option = new Option(policy.name, policy.name);  // Set option value to policy.name
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching policies:', error));
}

function fetchStakeholdersAssign() {
    fetch('http://localhost:5000/get/stakeholders')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('assignStakeholderSelect');
            select.innerHTML = ''; // Clear existing options
            data.forEach(stakeholder => {
                let option = new Option(stakeholder.name, stakeholder.id);
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching stakeholders:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    fetchPoliciesAssign();
    fetchStakeholdersAssign();
    fetchWeightsAndUpdateForm()
});

function fetchWeightsAndUpdateForm() {
    const policyName = document.getElementById('assignPolicySelect').value;
    const stakeholderName = document.getElementById('assignStakeholderSelect').value;

    const encodedPolicyName = encodeURIComponent(policyName);
    const encodedStakeholderName = encodeURIComponent(stakeholderName);

    fetch(`http://localhost:5000/get/weight/${encodedStakeholderName}/${encodedPolicyName}`)
        .then(response => response.json())
        .then(data => {
            if (data.weights) {
                // Assuming 'weights' is an object with properties: security, utility, privacy, accessibility
                document.getElementById('securityWeightAssign').value = data.weights.security;
                document.getElementById('securityWeightValue').innerText = data.weights.security;
                document.getElementById('utilityWeightAssign').value = data.weights.utility;
                document.getElementById('utilityWeightValue').innerText = data.weights.utility;
                document.getElementById('privacyWeightAssign').value = data.weights.privacy;
                document.getElementById('privacyWeightValue').innerText = data.weights.privacy;
                document.getElementById('accessibilityWeightAssign').value = data.weights.accessibility;
                document.getElementById('accessibilityWeightValue').innerText = data.weights.accessibility;
            } else {
                console.error('Error retrieving weights:', data.error);
                alert('Failed to retrieve weights: ' + data.error);
            }
        })
        .catch(error => console.error('Failed to fetch weights:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    fetchWeightsAndUpdateForm()
});

// You may want to add event listeners to the select elements to automatically fetch weights when the selection changes
document.getElementById('assignPolicySelect').addEventListener('change', fetchWeightsAndUpdateForm);
document.getElementById('assignStakeholderSelect').addEventListener('change', fetchWeightsAndUpdateForm);
// Call fetchPolicies on page load or setup

function updatePolicyWithStakeholderWeights() {
    const policySelect = document.getElementById('assignPolicySelect');
    const stakeholderSelect = document.getElementById('assignStakeholderSelect');

    const policyName = policySelect.options[policySelect.selectedIndex].text;
    const stakeholderName = stakeholderSelect.options[stakeholderSelect.selectedIndex].text;

    const weights = {
        security: parseFloat(document.getElementById('securityWeightAssign').value),
        utility: parseFloat(document.getElementById('utilityWeightAssign').value),
        privacy: parseFloat(document.getElementById('privacyWeightAssign').value),
        accessibility: parseFloat(document.getElementById('accessibilityWeightAssign').value)
    };

    fetch('http://localhost:5000/update/weights', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            policy_name: policyName,
            stakeholder_name: stakeholderName,
            weights: weights
        })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Displays a message from the server about the result
        })
        .catch(error => console.error('Error updating weights:', error));
}

function calculateOptimal() {
    const utilityThresholdInput = document.getElementById('utilityThreshold').value;
    if (!utilityThresholdInput) {
        alert("Please enter a utility threshold");
        return;
    }

    const utilityThreshold = parseFloat(utilityThresholdInput);
    if (isNaN(utilityThreshold)) {
        alert("Please enter a valid number for the utility threshold");
        return;
    }

    fetch('http://localhost:5000/calculate/optimal_policy', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            utilityThreshold: utilityThreshold,
            alphaEnabled: document.getElementById('alphaToggle').checked
        })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('optimalPolicyResult').innerText = `Optimal Policy: ${data.optimal_policy} (Score: ${data.optimal_policy_score}), Consensus: ${data.consensus ? 'Achieved' : 'Not achieved'}`;
        })
        .catch(error => {
            console.error('Error calculating optimal policy:', error);
            document.getElementById('optimalPolicyResult').innerText = 'Error calculating optimal policy.';
        });
}

function deletePolicy() {
    const policySelect = document.getElementById('policySelectDelete');  // Adjusted from 'stakeholderSelect' to 'policySelect'
    const policyName = policySelect.options[policySelect.selectedIndex].text;

    if (!policyName) {
        alert('No policy selected.');
        return;
    }

    fetch(`http://localhost:5000/delete/policy/${encodeURIComponent(policyName)}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Policy deleted successfully.');
            policySelect.remove(policySelect.selectedIndex);
            window.location.reload(); // Reloads the page after successful deletion
        } else if (data.error) {
            alert('Failed to delete policy: ' + data.error);
        }
    })
    .catch(error => console.error('Error deleting policy:', error));
}

function deleteStakeholder() {
    const stakeholderSelect = document.getElementById('stakeholderSelectDelete');  // Confirm this matches your HTML
    const stakeholderName = stakeholderSelect.options[stakeholderSelect.selectedIndex].text;

    if (!stakeholderName) {
        alert('No stakeholder selected.');
        return;
    }

    fetch(`http://localhost:5000/delete/stakeholder/${encodeURIComponent(stakeholderName)}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Stakeholder deleted successfully.');
            stakeholderSelect.remove(stakeholderSelect.selectedIndex);
            window.location.reload(); // Reloads the page after successful deletion
        } else if (data.error) {
            alert('Failed to delete stakeholder: ' + data.error);
        }
    })
    .catch(error => console.error('Error deleting stakeholder:', error));
}

function fetchPoliciesForDeletion() {
    fetch('http://localhost:5000/get/policies')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('policySelectDelete');
            select.innerHTML = '';  // Clear existing options
            data.forEach(policy => {
                let option = new Option(policy.name, policy.name);  // Using policy name as both text and value
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching policies:', error));
}

document.addEventListener('DOMContentLoaded', fetchPoliciesForDeletion);

function fetchStakeholdersForDeletion() {
    fetch('http://localhost:5000/get/stakeholders')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById('stakeholderSelectDelete');
            select.innerHTML = '';  // Clear existing options
            data.forEach(stakeholder => {
                let option = new Option(stakeholder.name, stakeholder.name);  // Using stakeholder name as both text and value
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching stakeholders:', error));
}

document.addEventListener('DOMContentLoaded', fetchStakeholdersForDeletion);

