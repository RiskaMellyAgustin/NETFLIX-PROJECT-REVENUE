# 🎬 Netflix-Inspired Revenue Cycle Management System

A Django-based web system simulating the **Revenue Cycle** of a subscription-based business like **Netflix**, developed for the Accounting Information System course at **President University**.

> 📅 Submission Date: May 23, 2025  
> 👨‍🏫 Lecturer: Mr. Muhamad Safiq  
> 📚 Course: Accounting Information System  
> 👩‍💻 Faculty of Computer Science – Information System – Data Science 1

---

## 📽️ Demo Video

🔗 [Watch Project Demo](https://drive.google.com/drive/u/0/folders/1SAYRC4m_Jo5LJJuxbNE_Yuhmy9kgp2xZ)

---

## 👥 Team Members (Group 2)
| Name                           | Student ID        |
|--------------------------------|-------------------|
| Alysia Dapyaraka               | 012202300069      |
| Jeny Fattahul Sisca Anjar Aeni| 012202300118      |
| **Riska Melly Agustin**       | 012202300123      |
| Valencia Greace Simeone       | 012202300134      |

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


