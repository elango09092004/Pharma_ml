document.getElementById('predictionForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const startDate = document.getElementById('start_date').value;
    const endDate = document.getElementById('end_date').value;
    const drug = document.getElementById('drug').value;

    const data = {
        start_date: startDate,
        end_date: endDate,
        drug: drug
    };

    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.error) {
            resultDiv.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            let output = '<h3>Total Predicted Sales:</h3>';

            let totalQuantity = 0;
            
            // Calculate the total predicted quantity
            data.forEach(item => {
                totalQuantity += item.predicted_quantity;
            });
            
            // Display the total predicted quantity
            output += `<p>Total Predicted Quantity: ${totalQuantity.toFixed(2)}</p>`;
            
            resultDiv.innerHTML = output;
            
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
