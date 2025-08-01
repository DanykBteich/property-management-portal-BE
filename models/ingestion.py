import os 
import pandas as pd
from models import db, PropertyModel, TenantModel, TaskModel

def ingest_data():
    """
        Drops all tables, recreates them, and loads data from the CSV Files
    """
    db.drop_all()
    db.create_all()
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    
    properties_dir = os.path.join(data_dir, "properties.csv")
    tenants_dir = os.path.join(data_dir, "tenants.csv")
    maintenance_dir = os.path.join(data_dir, "maintenance.csv")
    
    df = pd.read_csv(properties_dir, parse_dates=["PurchaseDate"])
    
    for _, row in df.iterrows():
        db.session.add(PropertyModel(
            PropAddress = row.Address,
            PropType = row.PropertyType,
            PropStatus = row.Status,
            PropPurchaseDate = row.PurchaseDate,
            PropPrice = int(row.Price)
        ))
    db.session.commit()
            
    df = pd.read_csv(tenants_dir, parse_dates=["LeaseTermStart", "LeaseTermEnd"])
    
    for _, row in df.iterrows():
        db.session.add(TenantModel(
            TenantName = row.Name,
            TenantContactInfo = row.ContactInfo,
            TenantLeaseTermStart = row.LeaseTermStart,
            TenantLeaseTermEnd = row.LeaseTermEnd,
            TenantRentalPaymentStatus = row.RentalPaymentStatus,
            PropId = int(row.PropertyID)
        ))
    db.session.commit()
            
    df = pd.read_csv(maintenance_dir, parse_dates=["ScheduledDate"])
    for _, row in df.iterrows():
        db.session.add(TaskModel(
            TaskDescription = row.Description,
            TaskStatus = row.Status,
            TaskScheduledDate = row.ScheduledDate,
            PropId = int(row.PropertyID)
        ))
    db.session.commit()