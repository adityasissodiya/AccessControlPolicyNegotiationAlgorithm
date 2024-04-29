// Update sliders display value
document.querySelectorAll('input[type="range"]').forEach(input => {
    input.addEventListener('input', function() {
        let valueSpan = document.getElementById(`${this.id}Value`);
        valueSpan.textContent = this.value;
    });
});

function addPolicy() {
    const policyName = document.getElementById('policyName').value;
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
        body: JSON.stringify({ name: policyName, details: policyDetails })
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
        })
        .catch(error => console.error('Error updating policy form:', error));
}


// Call fetchPolicies on page load or setup
document.addEventListener('DOMContentLoaded', function() {
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
