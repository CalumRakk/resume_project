class ResumeBuilder {
    constructor(component) {
        this.component = component;

        // Conectar eventos del formulario
        document.getElementById('full-name').addEventListener('input', (e) => {
            this.updateFullName(e.target.value);
        });

        document.getElementById('email').addEventListener('input', (e) => {
            this.updateEmail(e.target.value);
        });

        document.getElementById('summary').addEventListener('input', (e) => {
            this.updateSummary(e.target.value);
        });
    }

    updateFullName(name) {
        if (name.trim() === '') {
            console.warn('El nombre no puede estar vacío.');
            return;
        }
        this.component.setFullName(name);
    }

    updateEmail(email) {
        if (!this.validateEmail(email)) {
            console.warn('Correo electrónico no válido.');
            return;
        }
        this.component.setEmail(email);
    }

    updateSummary(summary) {
        if (summary.length > 500) {
            console.warn('El resumen es demasiado largo.');
            return;
        }
        this.component.setSummary(summary);
    }

    validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
}