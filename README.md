# ♻️ Recicla-me Se For Capaz

> A web platform for managing selective waste collection in Canoinhas, Santa Catarina — connecting residents, drivers, and administrators in a single system.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Figma](https://img.shields.io/badge/Figma-F24E1E?style=flat&logo=figma&logoColor=white)

---

## 🌍 The Problem

Many Brazilian municipalities struggle to manage selective waste collection efficiently. Canoinhas, SC is no exception: residents didn't know collection schedules, drivers had no digital check-in system, and administrators had no centralized view of operations.

**Recicla-me Se For Capaz** was built to solve exactly that.

---

## 💡 What It Does

- 📅 **Neighborhood scheduling** — administrators define collection days per neighborhood (bairro)
- 🚛 **Driver geolocation check-in** — drivers confirm their location at the start of each route
- 🔔 **Resident alert system** — email notifications sent automatically or triggered manually for collection reminders
- 📋 **Public registration via QR code** — residents self-register at community events by scanning a QR code
- 👤 **User and admin management** — role-based access for residents, drivers, and admins
- 📊 **Request tracking** — residents submit and track waste collection requests

---

## 🏗️ Project Structure

```
Recicla_me_Se_For_Capaz/
│
├── app.py                  # Main Flask application & routes
├── conexao.py              # MySQL database connection
├── alertas.py              # Email alert system
│
├── inserir_admin.py        # Admin registration logic
├── inserir_bairro.py       # Neighborhood management
├── inserir_coleta.py       # Collection scheduling
├── inserir_endereco.py     # Address management
├── inserir_solicitacao.py  # Resident request handling
├── inserir_usuario.py      # User registration
│
├── static/                 # CSS, JS, images
└── templates/              # HTML templates (Jinja2)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | MySQL |
| Frontend | HTML5, CSS3, JavaScript |
| Email alerts | SMTP via Python |
| UI Design | Figma |
| Version Control | Git / GitHub |

---

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/LucianeGroskopfZorek/Recicla_me_Se_For_Capaz.git
cd Recicla_me_Se_For_Capaz

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask mysql-connector-python

# 4. Configure your database connection in conexao.py

# 5. Run the app
python app.py
```

> The app will be available at `http://localhost:5000`

---

## 📐 Design & Documentation

- Wireframes and UI screens designed in **Figma**
- Visual identity: 5-color green/orange palette
- Documentation includes: MoSCoW tables, UML diagrams (use case, class, activity), benchmarking against Cataki and eCycle, and test cases (TU001–TU007)

---

## 👩‍💻 About This Project

This is an integrative academic project developed at **SENAC-SC** as part of the *Programador de Sistemas* certificate program.

It was built as a group project to solve a real civic problem in our own city — selective waste collection management in Canoinhas, SC.

---

## 🤝 Authors

- [Luciane Groskopf Zorek](https://github.com/LucianeGroskopfZorek)

---

*Built with purpose. Designed for real communities.*
