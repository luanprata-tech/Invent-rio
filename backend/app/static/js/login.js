    const tabLdap = document.getElementById('tab-ldap');
    const tabGovbr = document.getElementById('tab-govbr');
    const secLdap = document.getElementById('section-ldap');
    const secGovbr = document.getElementById('section-govbr');

    if (tabLdap && tabGovbr && secLdap && secGovbr) {
      tabLdap.addEventListener('click', () => {
        tabLdap.classList.add('bg-surface-container-lowest', 'text-on-surface', 'shadow-sm');
        tabLdap.classList.remove('text-on-surface-variant');
        tabGovbr.classList.remove('bg-surface-container-lowest', 'text-on-surface', 'shadow-sm');
        tabGovbr.classList.add('text-on-surface-variant');
        secLdap.classList.remove('hidden');
        secGovbr.classList.add('hidden');
      });

      tabGovbr.addEventListener('click', () => {
        tabGovbr.classList.add('bg-surface-container-lowest', 'text-on-surface', 'shadow-sm');
        tabGovbr.classList.remove('text-on-surface-variant');
        tabLdap.classList.remove('bg-surface-container-lowest', 'text-on-surface', 'shadow-sm');
        tabLdap.classList.add('text-on-surface-variant');
        secGovbr.classList.remove('hidden');
        secGovbr.classList.add('flex');
        secLdap.classList.add('hidden');
      });
    }

    const mfaInputs = document.querySelectorAll('.mfa-digit');
    mfaInputs.forEach((input, idx) => {
      input.addEventListener('input', (e) => {
        if (e.target.value.length === 1 && idx < mfaInputs.length - 1) {
          mfaInputs[idx + 1].focus();
        }
      });
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Backspace' && !e.target.value && idx > 0) {
          mfaInputs[idx - 1].focus();
        }
      });
    });

    async function handleLogin(event) {
      event.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
      
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: formData.toString()
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.access_token);
          window.location.href = '/inventario';
        } else {
          alert('Usuário ou senha incorretos!');
        }
      } catch (error) {
        console.error('Erro no login', error);
        alert('Erro ao conectar ao servidor.');
      }
    }
