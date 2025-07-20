const apiUrl = window.location.origin + '/api';
let token = localStorage.getItem('token');

function setToken(newToken) {
    token = newToken;
    localStorage.setItem('token', token);
}

async function apiRequest(path, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
        const res = await fetch(`${apiUrl}${path}`, {
            method,
            headers,
            body: body ? JSON.stringify(body) : null
        });

        // Verificar se a resposta é JSON
        const contentType = res.headers.get('content-type');
        let data;
        
        if (contentType && contentType.includes('application/json')) {
            data = await res.json();
        } else {
            data = await res.text();
        }

        return { 
            status: res.status, 
            data,
            ok: res.ok
        };
    } catch (error) {
        console.error('Erro na requisição:', error);
        return {
            status: 0,
            data: { msg: 'Erro de conexão com o servidor' },
            ok: false
        };
    }
}