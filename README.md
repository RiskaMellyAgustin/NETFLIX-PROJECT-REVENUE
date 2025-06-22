# 🎬 Netflix-Inspired Revenue Cycle Management System

A Django-based web system simulating the **Revenue Cycle** of a subscription-based business like **Netflix**, developed for the Accounting Information System course at **President University**.
  
> 📚 Course: Accounting Information System  
> 👩‍💻 Faculty of Computer Science – Information System – Data Science 1

---
## 🎬 Demo Preview

![Demo](demo_acc.gif)


## 👥 Team Members (Group 2)

| Name                              | Role & Responsibility                                  |
|-----------------------------------|--------------------------------------------------------|
| Alysia Dapyaraka                  | 💡 Idea Generation, Brainstorming, & Concept Planning  |
| Jeny Fattahul Sisca Anjar Aeni   | 🛠️ Admin Page UI Development & Admin Dashboard         |
| **Riska Melly Agustin**          | 🔧 Backend Development & Customer/User Interface       |
| Valencia Greace Simeone Damanaik | 🎨 System Design & UI/UX Flow                          |


---

## 🧠 Project Background

In the digital era, businesses like Netflix rely on recurring revenue models. Managing subscription flow, payment tracking, and revenue analysis requires efficient and secure systems. This project simulates such a system through a **Revenue Cycle Management (RCM)** platform that:
- Allows customers to manage their subscriptions.
- Enables admins to monitor income, generate reports, and maintain financial transparency.

---

## 🎯 Objectives

- Let customers:
  - View subscription status (active/failed).
  - Access invoices & payment history.

- Let administrators:
  - View dashboard with revenue metrics.
  - Track all subscription statuses.
  - Export PDF reports.
  - Use secure role-based access.

---

## 📌 Key Features

### 👤 Customer Side
- Subscribe to plans.
- Track subscription history & status.
- View/download detailed invoices.
- Fully isolated personal data view.

### 🛠️ Admin Side
- Dashboard with charts (monthly revenue, payment ratio).
- Customer & subscription database.
- PDF report export.
- Manual payment update management.
- Role-based restricted access.

---

## ⚙️ Tech Stack

| Layer      | Tools                        |
|------------|------------------------------|
| Backend    | Django, PostgreSQL           |
| Frontend   | HTML, CSS, JavaScript        |
| Visualization | Chart.js                   |
| Styling    | Tailwind CSS (optional)      |
| Deployment | Localhost (dev environment)  |

---
## 🏁 How to Run the Project

## 🛡️ Access Roles
| Role  | Access Rights                    |
| ----- | -------------------------------- |
| Admin | Full dashboard + customer data   |
| User  | View own subscription & invoices |

## 📂 Folder Structure

```text
netflixproject/
├── accounts/         # User login & registration logic
├── adminapp/         # Custom admin dashboard and reports
├── customerapp/      # Customer-side subscription and invoices
├── templates/        # HTML templates (shared across apps)
├── static/           # Static files: CSS, JavaScript, images
├── .env              # Environment variables (not tracked by Git)
├── requirements.txt  # Python dependencies
└── manage.py         # Django project entry point


📢 Disclaimer
This system is designed for academic simulation purposes and does not process real payments. It provides hands-on experience with real-world RCM concepts in a safe environment.


```bash
# Clone the repository
git clone https://github.com/RiskaMellyAgustin/NETFLIX-PROJECT-REVENUE.git
cd NETFLIX-PROJECT-REVENUE

# Create virtual environment
python -m venv venv
venv\Scripts\activate     # on Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
# Create a `.env` file and fill:
# SECRET_KEY=your-secret-key
# DB_NAME=yourdbname
# DB_USER=yourdbuser
# DB_PASSWORD=yourpassword
# DB_HOST=localhost
# DB_PORT=5432

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver


