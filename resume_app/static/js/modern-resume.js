// // Definimos una clase para manejar el estado
// class ResumeState {
//   constructor(initialData = {}) {
//     this.listeners = new Set();
//     this._state = new Proxy(initialData, {
//       set: (target, property, value) => {
//         target[property] = value;
//         this.notify();
//         return true;
//       }
//     });
//   }

//   subscribe(listener) {
//     this.listeners.add(listener);
//     return () => this.listeners.delete(listener);
//   }

//   notify() {
//     this.listeners.forEach(listener => listener(this._state));
//   }

//   updateField(field, value) {
//     if (field.includes('.')) {
//       const [parent, child] = field.split('.');
//       this._state[parent] = {
//         ...this._state[parent],
//         [child]: value
//       };
//     } else {
//       this._state[field] = value;
//     }
//   }

//   getState() {
//     return this._state;
//   }
// }

const template = document.createElement("template");
template.innerHTML = `
    <style>
        :host {
            display: flex;
            font-family: var(--font-family, Arial, sans-serif);
            font-size: var(--font-size, 16px);
            background-color: var(--header-bg-color, #ffffff);
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            width: 700px;
            flex-direction: column;
        }
        header {
            background-color: var(--header-bg-color, #ffffff);
            padding: 10px;
            text-align: center;
            border-radius: 8px 8px 0 0;
            color: #333;
        }
        .editable {
            cursor: pointer;
            padding: 2px 5px;
            border-radius: 3px;
        }
        .editable:hover {
            background-color: #f0f0f0;
        }
        .editing {
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 5px;
        }
        section {
            margin: 20px 0;
        }
        .skills, .experiences {
            list-style: none;
            padding: 0;
        }
        .skills li, .experiences li {
            margin: 5px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .delete-btn {
            color: red;
            cursor: pointer;
            opacity: 0.7;
        }
        .delete-btn:hover {
            opacity: 1;
        }
        .add-btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
        }
    </style>
    <header>
        <h1><span id="full-name" class="editable">Nombre completo</span></h1>
        <p><span id="email" class="editable">Correo electrónico</span></p>
    </header>
    <section>
        <h2>Resumen</h2>
        <p><span id="summary" class="editable">Resumen no disponible</span></p>
    </section>
    <section>
        <h2>Habilidades</h2>
        <ul class="skills" id="skills"></ul>
        <button class="add-btn" data-action="add-skill">+ Añadir habilidad</button>
    </section>
    <section>
        <h2>Experiencia</h2>
        <ul class="experiences" id="experiences"></ul>
        <button class="add-btn" data-action="add-experience">+ Añadir experiencia</button>
    </section>
`;

class ModernResume extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._resume = new Proxy({}, {
        set: (target, key, value) => {
            target[key] = value;
            this.render();
            return true;
        }
    });
  }

  get state() {
    return this._resume;
  }
  set state(value) {
    Object.assign(this._resume, value);
  }
  connectedCallback() {
    this.shadowRoot.appendChild(template.content.cloneNode(true));
    this.setupEventListeners();
    this.render();
  }

  setupEventListeners() {
    this.shadowRoot.addEventListener('click', (e) => {
      const target = e.target;

      if (target.classList.contains('editable')) {
        this.makeEditable(target);
      }

      if (target.classList.contains('delete-btn')) {
        const list = target.closest('ul').id;
        const index = Array.from(target.parentNode.parentNode.children).indexOf(target.parentNode);
        this.deleteItem(list, index);
      }

      if (target.classList.contains('add-btn')) {
        const action = target.dataset.action;
        if (action === 'add-skill') {
          this.addItem('skills', 'Nueva habilidad');
        } else if (action === 'add-experience') {
          this.addItem('experiences', 'Nueva experiencia');
        }
      }
    });
  }

  makeEditable(element) {
    const currentElement= element;
    const currentValue = currentElement.textContent;
    const input = document.createElement('input');
    input.value = currentValue;
    input.classList.add('editing');

    const field = element.id.replace('-', '_');
    element.replaceWith(input);
    input.focus();

    const handleUpdate = (e) => {
      const newValue = input.value.trim();
      input.removeEventListener('blur', handleUpdate);
      input.removeEventListener('keypress', handleKeyPress);

      input.replaceWith(currentElement);

      if (field=== 'skills' || field === 'experiences') {
        const index= +currentElement.getAttribute("data-id");
        const data= [...this.state[field]];
        data[index]= newValue;
        this.state[field]= data;
      }
      if (field === 'full_name' || field === 'email' || field === 'summary') {
        this.state[field]= newValue;
      }
    };
    const handleKeyPress = (e) => {
      if (e.key === 'Enter') {
        handleUpdate();
      }
    };
    input.addEventListener('blur', handleUpdate);
    input.addEventListener('keypress', handleKeyPress);
  }

  addItem(section_name, defaultValue) {
    const currentItems = this.state[section_name];
    const data= [...currentItems, defaultValue]
    this.state[section_name]= data;
  }

  deleteItem(section_name, index) {
    const currentItems = this.state[section_name];
    const data= [...currentItems]
    data.pop(index);
    this.state[section_name]= data;
  }

  render() {
    const resume = this.state;
    
    const fullName = this.shadowRoot.querySelector("#full-name");
    const email = this.shadowRoot.querySelector("#email");
    const summary = this.shadowRoot.querySelector("#summary");

    if (fullName && resume.full_name) {
      fullName.textContent = resume.full_name;
    }
    if (email && resume.email) {
      email.textContent = resume.email;
    }
    if (summary && resume.summary) {
      summary.textContent = resume.summary;
    }

    const skillsList = this.shadowRoot.querySelector("#skills");
    if (skillsList) {
      skillsList.innerHTML = resume.skills.map((skill, index) => `
        <li>
          <span id="skills" class="editable" data-id="${index}">${skill}</span>
          <span class="delete-btn">×</span>
        </li>
      `).join('');
    }

    const experiencesList = this.shadowRoot.querySelector("#experiences");
    if (experiencesList) {
      experiencesList.innerHTML = resume.experiences.map((exp, index) => `
        <li>  
          <span id="experiences" class="editable" data-id="${index}">${exp}</span>
          <span class="delete-btn">×</span>
        </li>
      `).join('');
    }


    // this.shadowRoot.querySelector("#full-name").textContent = resume.full_name;
    // this.shadowRoot.querySelector("#email").textContent = resume.email;
    // this.shadowRoot.querySelector("#summary").textContent = resume.summary;

    // const skillsList = this.shadowRoot.querySelector("#skills");
    // skillsList.innerHTML = resume.skills.map(skill => `
    //   <li>
    //     <span class="editable">${skill}</span>
    //     <span class="delete-btn">×</span>
    //   </li>
    // `).join('');

    // const experiencesList = this.shadowRoot.querySelector("#experiences");
    // experiencesList.innerHTML = resume.experiences.map(exp => `
    //   <li>
    //     <span class="editable">${exp}</span>
    //     <span class="delete-btn">×</span>
    //   </li>
    // `).join('');
  }
}

customElements.define("modern-resume", ModernResume);