document.getElementById('ruleForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = e.target;
    const data = new FormData(form);
    data.set('enabled', document.getElementById('enabled').checked);
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = '';
    try {
        const response = await fetch('/save_rule/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: data
        });
        if (response.ok) {
            resultDiv.textContent = 'Rule saved successfully!';
            form.reset();
        } else {
            const error = await response.text();
            resultDiv.textContent = 'Error: ' + error;
        }
    } catch (err) {
        resultDiv.textContent = 'Network error.';
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
