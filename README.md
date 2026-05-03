
# 🚀 Hiring Signal Agent

An **Agentic AI system** built using LangGraph that detects hiring-related posts, extracts structured job information, and sends real-time notifications via email.

---

## 🧠 Overview

This project demonstrates how to build a **single-agent workflow system** that:

* Analyzes social posts
* Determines if it is a hiring signal
* Extracts key job details (role, company, skills)
* Validates structured output using Pydantic
* Sends notifications via email

---

## ⚙️ Features

* ✅ Agentic workflow (classification → extraction → notification)
* ✅ Conditional execution using LangGraph
* ✅ Structured output validation using Pydantic
* ✅ Email notification system (Gmail SMTP)
* ✅ Modular and extensible design

---

## 🏗️ Architecture

```
Input Text
    ↓
[Classifier Node]
    ↓
(Is Hiring?)
   /   \
 Yes    No
  ↓      ↓
[Extractor]   END
  ↓
[Pydantic Validation]
  ↓
[Email Notification]
```

---

## 🧩 Tech Stack

* Python
* LangGraph
* LangChain
* Pydantic
* Gmail SMTP (Email Notifications)

---

## 📦 Installation

```bash
git clone https://github.com/GAuravY19/Hiring-Signal-Agent.git
cd Hiring-Signal-Agent
pip install -r requirements.txt
```

---

## 🔑 Environment Setup

Create a `.env` file:

```env
EMAIL_ID=your_email@gmail.com
EMAIL_PASS=your_app_password
GEMINI_API_KEY=your_api_key
```

---

## ▶️ Usage

Run the agent:

```bash
python main.py
```

Example input:

```python
"We are hiring Data Scientists at Flipkart. Python and ML required."
```

---

## 🔮 Future Improvements

* Add retry mechanism for failed parsing
* Integrate real-time data sources (Apify / scraping)
* Add database persistence

---
