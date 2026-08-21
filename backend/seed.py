import asyncio
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from app.database import Base
from app.models.user import User
from app.models.rfq import RFQ
from app.models.vendor import Vendor
from app.models.quotation import Quotation
from app.models.vendor_score import VendorScore
from app.models.purchase_order import PurchaseOrder
from app.models.inventory import Inventory
from app.models.finance import Finance
from app.models.audit_log import AuditLog
from app.utils import hash_password

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./starai.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def seed_users(db: AsyncSession):
    users = [
        User(email="admin@starai.com", hashed_password=hash_password("admin123"), full_name="Admin User", role="admin", is_active=True),
        User(email="manager@starai.com", hashed_password=hash_password("manager123"), full_name="Procurement Manager", role="manager", is_active=True),
        User(email="procurement@starai.com", hashed_password=hash_password("proc123"), full_name="Procurement Officer", role="procurement", is_active=True),
    ]
    db.add_all(users)
    await db.commit()
    for u in users:
        await db.refresh(u)
    return users


async def seed_vendors(db: AsyncSession):
    vendors = [
        Vendor(
            vendor_id="VEN-001",
            name="ABC Technologies",
            email="sales@abctech.com",
            phone="+91-9876543210",
            category="Electronics",
            rating=4.8,
            reliability_score=94.0,
            avg_delivery_days=9,
            total_orders=38,
            address="Bangalore, India",
            gst_number="GSTIN29ABCDE1234F1Z5",
        ),
        Vendor(
            vendor_id="VEN-002",
            name="Global Systems",
            email="contact@globalsys.com",
            phone="+91-8765432109",
            category="IT Infrastructure",
            rating=3.9,
            reliability_score=78.0,
            avg_delivery_days=35,
            total_orders=12,
            address="Mumbai, India",
            gst_number="GSTIN27XYZAB5678C2D3",
        ),
        Vendor(
            vendor_id="VEN-003",
            name="TechWorld Solutions",
            email="info@techworld.in",
            phone="+91-7654321098",
            category="Electronics",
            rating=4.5,
            reliability_score=88.0,
            avg_delivery_days=12,
            total_orders=25,
            address="Hyderabad, India",
            gst_number="GSTIN36PQRST9012E3F4G5",
        ),
    ]
    db.add_all(vendors)
    await db.commit()
    for v in vendors:
        await db.refresh(v)
    return vendors


async def seed_rfqs(db: AsyncSession):
    rfqs = [
        RFQ(
            rfq_number="RFQ-2024-001",
            title="Laptop Procurement Q4",
            department="IT",
            product="Laptop",
            quantity=500,
            budget=6000000,
            required_delivery_date=datetime.utcnow().date() + timedelta(days=15),
            payment_terms="Net 30",
            additional_requirements="3 year warranty, pre-installed Windows 11 Pro",
            status="closed",
        ),
        RFQ(
            rfq_number="RFQ-2024-002",
            title="Office Furniture Renewal",
            department="Operations",
            product="Office Chair",
            quantity=200,
            budget=1200000,
            required_delivery_date=datetime.utcnow().date() + timedelta(days=30),
            payment_terms="Net 45",
            additional_requirements="Ergonomic design, 5 year warranty",
            status="open",
        ),
        RFQ(
            rfq_number="RFQ-2024-003",
            title="Software License Renewal",
            department="IT",
            product="Enterprise Software License",
            quantity=100,
            budget=2800000,
            required_delivery_date=datetime.utcnow().date() + timedelta(days=7),
            payment_terms="Net 30",
            additional_requirements="Annual license, premium support",
            status="awarded",
        ),
    ]
    db.add_all(rfqs)
    await db.commit()
    for r in rfqs:
        await db.refresh(r)
    return rfqs


async def seed_quotations(db: AsyncSession, rfqs, vendors):
    quotations = [
        Quotation(
            rfq_id=rfqs[0].id,
            vendor_id=vendors[0].id,
            quotation_number="QT-2024-001",
            file_path="/uploads/qt_abc_2024_001.pdf",
            extracted_data='{"vendor_name":"ABC Technologies","quotation_number":"QT-2024-001","currency":"INR","items":[{"name":"Laptop","quantity":500,"unit_price":10000,"discount":500000}],"subtotal":4950000,"tax":891000,"shipping":0,"total":5841000,"delivery_days":10,"payment_terms":"Net 30","warranty":"3 years","risks":[]}',
            subtotal=4950000,
            tax=891000,
            shipping=0,
            total=5841000,
            delivery_days=10,
            payment_terms="Net 30",
            warranty="3 years",
            status="completed",
        ),
        Quotation(
            rfq_id=rfqs[0].id,
            vendor_id=vendors[1].id,
            quotation_number="QT-2024-002",
            file_path="/uploads/qt_global_2024_002.pdf",
            extracted_data='{"vendor_name":"Global Systems","quotation_number":"QT-2024-002","currency":"INR","items":[{"name":"Laptop","quantity":500,"unit_price":9500,"discount":0}],"subtotal":4750000,"tax":855000,"shipping":250000,"total":5855000,"delivery_days":35,"payment_terms":"100% Advance","warranty":"1 year","risks":["100% advance payment required","Long delivery time"]}',
            subtotal=4750000,
            tax=855000,
            shipping=250000,
            total=5855000,
            delivery_days=35,
            payment_terms="100% Advance",
            warranty="1 year",
            status="completed",
        ),
        Quotation(
            rfq_id=rfqs[0].id,
            vendor_id=vendors[2].id,
            quotation_number="QT-2024-003",
            file_path="/uploads/qt_techworld_2024_003.pdf",
            extracted_data='{"vendor_name":"TechWorld Solutions","quotation_number":"QT-2024-003","currency":"INR","items":[{"name":"Laptop","quantity":500,"unit_price":10200,"discount":250000}],"subtotal":4860000,"tax":874800,"shipping":50000,"total":5784800,"delivery_days":12,"payment_terms":"Net 45","warranty":"3 years","risks":[]}',
            subtotal=4860000,
            tax=874800,
            shipping=50000,
            total=5784800,
            delivery_days=12,
            payment_terms="Net 45",
            warranty="3 years",
            status="completed",
        ),
    ]
    db.add_all(quotations)
    await db.commit()
    for q in quotations:
        await db.refresh(q)
    return quotations


async def seed_scores(db: AsyncSession, rfqs, quotations, vendors):
    scores = [
        VendorScore(
            quotation_id=quotations[0].id,
            vendor_id=vendors[0].id,
            rfq_id=rfqs[0].id,
            price_score=92.0,
            delivery_score=95.0,
            quality_score=90.0,
            warranty_score=100.0,
            payment_score=90.0,
            reliability_score=94.0,
            final_score=91.2,
            tco=5841000,
            risk_score=15,
            risk_level="Low",
            recommendation_rank=1,
            delivery_days=10,
            payment_terms="Net 30",
        ),
        VendorScore(
            quotation_id=quotations[1].id,
            vendor_id=vendors[1].id,
            rfq_id=rfqs[0].id,
            price_score=83.33,
            delivery_score=30.0,
            quality_score=75.0,
            warranty_score=50.0,
            payment_score=10.0,
            reliability_score=78.0,
            final_score=85.0,
            tco=5855000,
            risk_score=78,
            risk_level="High",
            recommendation_rank=3,
            delivery_days=35,
            payment_terms="100% Advance",
        ),
        VendorScore(
            quotation_id=quotations[2].id,
            vendor_id=vendors[2].id,
            rfq_id=rfqs[0].id,
            price_score=88.0,
            delivery_score=88.0,
            quality_score=85.0,
            warranty_score=100.0,
            payment_score=70.0,
            reliability_score=88.0,
            final_score=89.0,
            tco=5784800,
            risk_score=25,
            risk_level="Low",
            recommendation_rank=2,
            delivery_days=12,
            payment_terms="Net 45",
        ),
    ]
    db.add_all(scores)
    await db.commit()
    return scores


async def seed_purchase_orders(db: AsyncSession, rfqs, vendors, scores):
    pos = [
        PurchaseOrder(
            po_number="PO-2024-001",
            rfq_id=rfqs[0].id,
            vendor_id=vendors[0].id,
            quotation_id=scores[0].quotation_id,
            items='[{"name":"Laptop","quantity":500,"price":5841000}]',
            subtotal=5841000,
            tax=891000,
            total_amount=6732000,
            delivery_days=10,
            payment_terms="Net 30",
            status="approved",
            approved_by=2,
            approved_at=datetime.utcnow(),
        ),
        PurchaseOrder(
            po_number="PO-2024-002",
            rfq_id=rfqs[2].id,
            vendor_id=vendors[0].id,
            quotation_id=None,
            items='[{"name":"Enterprise Software License","quantity":100,"price":2800000}]',
            subtotal=2800000,
            tax=504000,
            total_amount=3304000,
            delivery_days=7,
            payment_terms="Net 30",
            status="pending",
            approved_by=None,
            approved_at=None,
        ),
    ]
    db.add_all(pos)
    await db.commit()
    for po in pos:
        await db.refresh(po)
    return pos


async def seed_inventory(db: AsyncSession, pos):
    inventories = [
        Inventory(
            po_id=pos[0].id,
            product_name="Laptop",
            quantity=500,
            expected_delivery_date=datetime.utcnow().date() + timedelta(days=10),
            status="inbound",
        ),
        Inventory(
            po_id=pos[1].id,
            product_name="Enterprise Software License",
            quantity=100,
            expected_delivery_date=datetime.utcnow().date() + timedelta(days=7),
            status="pending",
        ),
    ]
    db.add_all(inventories)
    await db.commit()
    return inventories


async def seed_finance(db: AsyncSession, pos, vendors):
    finances = [
        Finance(
            po_id=pos[0].id,
            vendor_id=vendors[0].id,
            amount=6732000,
            due_date=datetime.utcnow().date() + timedelta(days=30),
            status="draft",
            payment_terms="Net 30",
        ),
        Finance(
            po_id=pos[1].id,
            vendor_id=vendors[0].id,
            amount=3304000,
            due_date=datetime.utcnow().date() + timedelta(days=30),
            status="draft",
            payment_terms="Net 30",
        ),
    ]
    db.add_all(finances)
    await db.commit()
    return finances


async def seed_audit_logs(db: AsyncSession, users, rfqs):
    logs = [
        AuditLog(action="created", entity_type="rfq", entity_id=rfqs[0].id, user_id=users[0].id, details=json.dumps({"rfq_number": rfqs[0].rfq_number})),
        AuditLog(action="uploaded", entity_type="quotation", entity_id=1, user_id=users[2].id, details=json.dumps({"vendor": "ABC Technologies"})),
        AuditLog(action="analyzed", entity_type="rfq", entity_id=rfqs[0].id, user_id=users[1].id, details=json.dumps({"recommendation": "ABC Technologies"})),
        AuditLog(action="approved", entity_type="purchase_order", entity_id=1, user_id=users[1].id, details=json.dumps({"po_number": "PO-2024-001"})),
    ]
    db.add_all(logs)
    await db.commit()


async def main():
    db_path = "starai.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")

    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        print("Seeding users...")
        users = await seed_users(db)

        print("Seeding vendors...")
        vendors = await seed_vendors(db)

        print("Seeding RFQs...")
        rfqs = await seed_rfqs(db)

        print("Seeding quotations...")
        quotations = await seed_quotations(db, rfqs, vendors)

        print("Seeding scores...")
        scores = await seed_scores(db, rfqs, quotations, vendors)

        print("Seeding purchase orders...")
        pos = await seed_purchase_orders(db, rfqs, vendors, scores)

        print("Seeding inventory...")
        await seed_inventory(db, pos)

        print("Seeding finance...")
        await seed_finance(db, pos, vendors)

        print("Seeding audit logs...")
        await seed_audit_logs(db, users, rfqs)

    print("Database seeded successfully!")
    print("\nDemo accounts:")
    print("  admin@starai.com / admin123")
    print("  manager@starai.com / manager123")
    print("  procurement@starai.com / proc123")


if __name__ == "__main__":
    asyncio.run(main())
