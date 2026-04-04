#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import db

# Sample plans data
sample_plans = [
    {
        "name": "Basic Plan",
        "description": "Perfect for light users with essential OTT services",
        "price": 9.99,
        "features": [
            "Access to 50+ channels",
            "HD streaming",
            "Mobile app access",
            "Basic customer support"
        ]
    },
    {
        "name": "Premium Plan",
        "description": "Comprehensive entertainment package for families",
        "price": 19.99,
        "features": [
            "Access to 200+ channels",
            "4K streaming",
            "Multiple device support",
            "Priority customer support",
            "Offline downloads"
        ]
    },
    {
        "name": "Ultimate Plan",
        "description": "Complete entertainment experience with all premium features",
        "price": 29.99,
        "features": [
            "Access to 500+ channels",
            "8K streaming",
            "Unlimited devices",
            "24/7 premium support",
            "Offline downloads",
            "Exclusive content",
            "Early access to new releases"
        ]
    }
]

def add_sample_plans():
    try:
        # Check if plans already exist
        existing_plans = db.plans.count_documents({})
        if existing_plans > 0:
            print(f"Database already has {existing_plans} plans. Skipping sample data insertion.")
            return

        # Insert sample plans
        result = db.plans.insert_many(sample_plans)
        print(f"Successfully inserted {len(result.inserted_ids)} sample plans")

        # Print the inserted plans
        for plan in db.plans.find():
            print(f"Plan: {plan['name']} - ${plan['price']}")

    except Exception as e:
        print(f"Error adding sample plans: {e}")

if __name__ == "__main__":
    add_sample_plans()