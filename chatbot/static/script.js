async function generateSQL() {
    const prompt = document.getElementById("prompt").value;
    const sqlOutput = document.getElementById("sql-output");

    try {
        const response = await fetch('/generate_sql', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        });

        const data = await response.json();
        sqlOutput.textContent = data.sql;
    } catch (error) {
        console.error('Error:', error);
        sqlOutput.textContent = 'Error occurred while processing the prompt.';
    }
}
