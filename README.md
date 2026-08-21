# ⭐ STAR AI

**STAR AI** is an AI-powered Procurement ERP system that transforms manual procurement into a near-zero-touch workflow—from RFQ creation and quotation analysis to intelligent vendor selection, Purchase Order generation, inventory updates, and finance synchronization.

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, TypeScript, Tailwind CSS v4, shadcn/ui, Motion, Lucide React, Recharts |
| Backend | FastAPI, Python 3.11+, SQLAlchemy 2.0 (async), Pydantic v2 |
| AI | Groq API (STAR AI Engine) |
| Database | SQLite (demo) / Supabase PostgreSQL (production) |
| Documents | PyPDF, OpenPyXL, Pytesseract, ReportLab |

## 📁 Project Structure

```
star-ai/
├── frontend/          # Next.js application
│   ├── src/
│   │   ├── app/       # Pages (login, dashboard, rfq, vendors, quotations, analysis, purchase-orders, inventory, finance, analytics)
│   │   ├── components/
│   │   │   ├── ui/    # shadcn/ui components
│   │   │   ├── layout/# Sidebar, Header
│   │   │   ├── ai/    # STAR AI Chat
│   │   │   ├── dashboard/
│   │   │   ├── rfq/
│   │   │   ├── vendors/
│   │   │   └── quotations/
│   │   └── lib/       # API client, utils
│   └── public/
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── routes/    # API endpoints
│   │   └── services/  # STAR AI, scoring, TCO, risk, PO generator
│   ├── seed.py        # Database seeder with demo data
│   └── requirements.txt
├── sample-data/       # Sample quotation files
├── documents/         # Uploaded documents
└── README.md
```

## ⚡ Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Groq API key ([Get one here](https://console.groq.com/keys))

### 1. Clone & Install

```bash
cd frontend
npm install

cd ../backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite+aiosqlite:///./starai.db
SECRET_KEY=your_secret_key_here
```

### 3. Seed Database

```bash
cd backend
python seed.py
```

This creates demo users, vendors, RFQs, quotations, scores, purchase orders, inventory, and finance records.

### 4. Run Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 5. Run Frontend

```bash
cd frontend
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 6. Login

Use one of the demo accounts:
- **Admin**: `admin@starai.com` / `admin123`
- **Manager**: `manager@starai.com` / `manager123`
- **Procurement**: `procurement@starai.com` / `proc123`

## 🎯 Demo Flow

The recommended hackathon demo flow:

1. **Login** → Enter demo credentials
2. **Dashboard** → View stats, STAR AI chat
3. **RFQs** → Create new RFQ for laptops
4. **Quotations** → Upload 3 vendor quotations (PDF/Excel/Image)
5. **Analysis** → STAR AI scans, extracts data, calculates TCO, detects risks, scores vendors
6. **Vendor Selection** → ABC Technologies recommended with 91/100 score
7. **Approve** → Manager approves with one click
8. **PO Generated** → Professional PDF purchase order
9. **Inventory & Finance** → Auto-created inbound shipment and accounts payable
10. **Analytics** → View spend trends, savings, vendor performance

## 🏆 Demo Data

Three pre-seeded vendors for the demo:

| Vendor | TCO | Delivery | Warranty | Payment | Risk | Score |
|--------|-----|----------|----------|---------|------|-------|
| ABC Technologies | ₹55.4L | 10 days | 3 years | Net 30 | Low | 91 |
| Global Systems | ₹57.2L | 35 days | 1 year | 100% Advance | High | 73 |
| TechWorld | ₹56.1L | 12 days | 3 years | Net 45 | Low | 87 |

## 🧠 STAR AI Features

- **Document Extraction**: AI extracts structured data from PDF, Excel, and image quotations
- **TCO Engine**: Calculates true procurement cost including hidden fees
- **Risk Detection**: Identifies payment, delivery, contract, and vendor risks
- **Vendor Scoring**: Deterministic weighted scoring (Price 40%, Delivery 20%, Quality 15%, Warranty 10%, Payment 10%, Reliability 5%)
- **Procurement Copilot**: Chat interface to ask questions about vendors, RFQs, and spend
- **Auto PO Generation**: One-click PO creation with PDF output
- **Audit Trail**: Complete activity logging

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | Get JWT token |
| GET | `/rfqs` | List RFQs |
| POST | `/rfqs` | Create RFQ |
| GET | `/vendors` | List vendors |
| POST | `/vendors` | Add vendor |
| POST | `/quotations/upload` | Upload quotation |
| POST | `/analysis/analyze/{rfq_id}` | Run STAR AI analysis |
| GET | `/analysis/results/{rfq_id}` | Get analysis results |
| POST | `/purchase-orders/{id}/approve` | Approve PO |
| GET | `/inventory` | List inventory |
| GET | `/finance` | List finance records |
| GET | `/audit/logs` | Get audit trail |

## 🚦 Build Phases

| Phase | Focus |
|-------|-------|
| 1 | Next.js, Tailwind, shadcn/ui, Layout, Sidebar, Login, Dashboard |
| 2 | RFQ, Vendors, Quotation Upload UI |
| 3 | FastAPI, Database, RFQ API, Vendor API, Quotation API |
| 4 | Document extraction, Groq, STAR AI structured output |
| 5 | TCO, Scoring, Risk Engine, Recommendation |
| 6 | PO, Inventory, Finance, Audit |
| 7 | Motion, Charts, STAR AI Copilot, Loading animations, Polishing |
| 8 | Testing, Demo data, Deployment, Judge presentation |

## 📝 License

MIT

---

Built with ⭐ STAR AI — Intelligent Procurement Platform
