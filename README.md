# 🎓 Online Course Management Platform

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-Backend-092E20?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=flat-square&logo=postgresql)
![HTML](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-Styling-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Logic-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📚 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [About the Platform](#-about-the-platform)
- [Project Architecture](#-project-architecture)
- [Features & User Roles](#-features--user-roles)
- [System Architecture](#-system-architecture)
- [How to Run](#-how-to-run)
- [Technical Deep Dive](#-technical-deep-dive)
- [Authors](#-authors)

---

## 📌 Overview

This project is a **Web-Based Online Course Management Platform** built in **Django (Python)** and **PostgreSQL** that provides a complete ecosystem for managing an educational technology company's Massively Open Online Courses (MOOCs). The system features a robust backend database, role-based dashboards, and intuitive front-end interfaces to support complex relationships between universities, instructors, courses, and students.

---

## 🧠 Problem Statement

Educational Technology platforms deal with immense amounts of relational data across various user domains. Managing these relationships—such as multiple instructors per course, thousands of students per session, and analytics for performance—requires a structured and optimized information system.

**Key challenges this project addresses:**

- The need for **role-based access control** ensuring privacy and correct functionality for Admins, Instructors, Students, and Analysts
- Managing complex **Many-to-Many relationships** between courses, instructors, topics, textbooks, and universities
- Providing a **dynamic, centralized hub** for course content delivery and student evaluation
- Presenting actionable **statistical insights** to data analysts for course performance monitoring

> 👉 **Our goal:** Build a complete web-based information system having a normalized backend database, a connectivity server, and a form-based web interface tailored to each user type.

---

## 📚 About the Platform

This platform acts as a **comprehensive educational management system** — from core data modeling to a polished UI.

### 🔍 Key Ideas

- Implements a **three-tier architecture** with a PostgreSQL database, Django backend, and responsive HTML/JS frontend
- Highly **normalized database schema** utilizing Primary, Foreign, and Composite Keys across 14 tables
- Utilizes **Django ORM** to bridge Python classes and SQL tables safely to prevent SQL injection
- Features a **dedicated Analytics Dashboard** fetching aggregated course enrollment metrics dynamically

### ⚡ Why it matters

- Ensures **data integrity** for academic records and enrollment status
- Highly **modular architecture** separating business logic (views), data schema (models), and UI (templates)
- Fully **scalable**—designed to be deployed locally or directly onto production lab servers

---

## 🏗️ Project Architecture

```
ONLINE-COURSE-PLATFORM/
│
├── manage.py                 # Django entry point and CLI utility
├── requirements.txt          # Python dependencies (Django, psycopg2)
├── .env                      # Environment configuration (DB credentials)
│
├── course_platform/          # Project Settings
│   ├── settings.py           # DB configuration, Installed Apps
│   └── urls.py               # Main routing dispatcher
│
├── core/                     # Main Application Logic
│   ├── models.py             # Database Schema (ORM mapping)
│   ├── views.py              # Business logic (retrieval, insertion)
│   ├── forms.py              # Input validation layer
│   ├── admin.py              # Admin interface configuration
│   └── migrations/           # Database schema versioning history
│
├── templates/                # HTML Frontend Interface
│   ├── base.html             # Master layout template (Nav/Footer)
│   ├── dashboards/           # Role-specific landing pages
│   ├── instructor/           # Content management & grading UI
│   └── student/              # Course browsing & viewing UI
│
├── static/                   # Static Assets
│   └── js/                   # Frontend logic
│
└── seed_data.py              # Utility script to populate initial sample data
```

---

## ⚙️ Features & User Roles

The platform provides dedicated workflows and dashboards for four primary user roles:

### 1️⃣ System Administrator
- Acts as the master data controller.
- Can create new courses, programs, and user accounts.
- Assigns instructors to specific courses and manages student enrollment overrides.

### 2️⃣ Instructor
- Manages academic content and student progress.
- Can add online content, reference textbooks, and topics to assigned courses.
- Evaluates students, inputs marks, and provides feedback.

### 3️⃣ Student
- The primary consumer of the MOOC platform.
- Can browse available courses, search by topic/category, and register/enroll.
- Accesses course materials and views evaluations.

### 4️⃣ Data Analyst
- Monitors platform performance and user engagement.
- Views aggregated statistics about course enrollments.
- Analyzes average evaluation ratings and generates visual statistical reports.

---

## 📊 System Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   PostgreSQL     │ ──▶ │  Django Models   │ ──▶ │   Django Views   │
│  (Data Layer)    │ ◀── │  (Python ORM)    │ ◀── │ (Business Logic) │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                                            │ ▲
                                                            ▼ │
                                                  ┌──────────────────┐
                                                  │  HTML/JS/CSS     │
                                                  │ (Presentation)   │
                                                  └──────────────────┘
```

**Implementation Stack:**
- **Database:** PostgreSQL (Lab Server) with `psycopg2` adapter
- **Backend:** Django Framework (Python) handling ORM mapping, session management, and routing
- **Frontend:** HTML5, CSS3, JS, Bootstrap for responsive UI

---

## 🚀 How to Run

### 🔹 Prerequisites

| Requirement | Details |
|---|---|
| **Python** | 3.8+ installed |
| **PostgreSQL** | Running locally or via lab server |
| **pip** | Python package manager |

### 🔹 Installation & Execution

1. **Clone and Install Dependencies**
   ```bash
   git clone <repository-url>
   cd online-course-platform-main
   pip install -r requirements.txt
   ```

2. **Database Setup**
   Ensure your database server is running and configured. Apply the migrations to generate the schema:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Seed Initial Data (Recommended)**
   Populate the database with universities, courses, and test accounts:
   ```bash
   python seed_data.py
   ```

4. **Launch the Server**
   ```bash
   python manage.py runserver
   ```
   Navigate to **http://127.0.0.1:8000/** in your browser.

---

## 🔬 Technical Deep Dive

### Database Schema

The core of the system is a highly normalized relational database designed to support complex relationships. It implements 14 tables (Entities and Junctions).

**Core Entities:**
- `University` (university_id, name, country)
- `Instructor` (instructor_id, name, email, expertise)
- `Course` (course_id, name, duration, program_type)
- `Student` (student_id, name, age, country)
- `Topic`, `Textbook`, `Online Content`

**Relational / Junction Tables:**
Because of the complex Many-to-Many nature of educational systems, we implemented strict composite primary keys for junction tables to prevent duplication:
- `Course_Instructor`
- `Course_Topic`
- `Course_Textbook`
- `Course_Content`
- `Enrollment` (Tracks student_id, course_id, status, and enrollment_date)
- `Evaluation` (Tracks student marks and feedback per course)

---

## 🎓 Authors

**Team Fiery Five** — Database Management Systems (CS39003) Lab Assignment

| Name | Roll Number |
|------|-------------|
| Akshat Priyadarshi | 23CS30003 |
| Ritabrata Sarkar | 23CS30045 |
| Hritwik Upadhyay | 23CS30023 |
| Harshit Singhal | 23CS10025 |
| Krishnkant Sahu | 23CS10035 |

---

<p align="center">
  <i>Built as an academic project to explore relational database design and web information systems.</i><br/>
  <i>Department of Computer Science and Engineering • February 2026</i>
</p>