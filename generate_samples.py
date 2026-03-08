"""
Script to generate sample Excel files for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


def create_sample_sales_data():
    """Create sample sales data with marketing correlation"""
    np.random.seed(42)
    
    months = pd.date_range(start='2023-01-01', periods=24, freq='M')
    
    # Generate correlated data
    marketing_spend = np.random.uniform(1000, 5000, 24)
    marketing_spend = np.sort(marketing_spend) + np.random.normal(0, 200, 24)  # Trend with noise
    
    # Sales correlates with marketing (coefficient ~2.5)
    base_sales = 3000
    sales = base_sales + 2.5 * marketing_spend + np.random.normal(0, 500, 24)
    
    # Employees grow over time
    employees = np.linspace(10, 30, 24).astype(int) + np.random.randint(-2, 3, 24)
    
    # Customer satisfaction
    satisfaction = 4.0 + 0.3 * np.random.random(24) + 0.0001 * marketing_spend
    satisfaction = np.clip(satisfaction, 3.5, 5.0)
    
    # Revenue = Sales * Average order value (with some variation)
    avg_order_value = 10 + np.random.uniform(-1, 1, 24)
    revenue = sales * avg_order_value
    
    # Profit margin varies
    profit_margin = 0.15 + 0.1 * np.random.random(24)
    profit = revenue * profit_margin
    
    data = pd.DataFrame({
        'Month': months.strftime('%Y-%m'),
        'Marketing_Spend': np.round(marketing_spend, 2),
        'Sales': np.round(sales, 2),
        'Employees': employees,
        'Customer_Satisfaction': np.round(satisfaction, 2),
        'Revenue': np.round(revenue, 2),
        'Profit': np.round(profit, 2)
    })
    
    return data


def create_sample_inventory_data():
    """Create sample inventory and supply chain data"""
    np.random.seed(123)
    
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    weeks = 52
    
    data_rows = []
    
    for week in range(1, weeks + 1):
        for product in products:
            # Stock level
            base_stock = 100 + np.random.randint(-20, 20)
            
            # Demand
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * week / 52)
            demand = int(50 * seasonal_factor + np.random.randint(-10, 10))
            
            # Price
            base_price = 20 + products.index(product) * 10
            price = base_price * (1 + 0.1 * np.random.random())
            
            # Lead time
            lead_time = 3 + np.random.randint(0, 5)
            
            # Stockout risk
            stockout_risk = max(0, min(100, 100 * (demand / base_stock)))
            
            data_rows.append({
                'Week': week,
                'Product': product,
                'Stock_Level': base_stock,
                'Demand': demand,
                'Price': round(price, 2),
                'Lead_Time_Days': lead_time,
                'Stockout_Risk': round(stockout_risk, 1)
            })
    
    return pd.DataFrame(data_rows)


def create_sample_hr_data():
    """Create sample HR and workforce data"""
    np.random.seed(456)
    
    quarters = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    
    # Generate correlated HR metrics
    headcount = [100, 105, 112, 118, 125, 130, 138, 145]
    
    data_rows = []
    
    for i, quarter in enumerate(quarters):
        # Training hours correlate with productivity
        training_hours = 20 + 2 * i + np.random.randint(-3, 3)
        
        # Productivity correlates with training
        productivity = 70 + 0.8 * training_hours + np.random.randint(-5, 5)
        
        # Turnover inversely correlates with satisfaction
        satisfaction = 3.5 + 0.05 * training_hours + np.random.uniform(-0.2, 0.2)
        turnover = max(5, 25 - 4 * satisfaction + np.random.randint(-2, 2))
        
        # Hiring cost
        hiring_cost = 5000 + 100 * turnover + np.random.randint(-500, 500)
        
        data_rows.append({
            'Quarter': quarter,
            'Headcount': headcount[i],
            'Training_Hours_Per_Employee': round(training_hours, 1),
            'Productivity_Score': round(productivity, 1),
            'Employee_Satisfaction': round(satisfaction, 2),
            'Turnover_Rate': round(turnover, 1),
            'Hiring_Cost': round(hiring_cost, 2)
        })
    
    return pd.DataFrame(data_rows)


def generate_all_samples():
    """Generate all sample Excel files"""
    # Create samples directory
    os.makedirs('samples', exist_ok=True)
    
    # Sales data
    sales_df = create_sample_sales_data()
    sales_df.to_excel('samples/sales_data.xlsx', index=False)
    print("Created: samples/sales_data.xlsx")
    
    # Inventory data
    inventory_df = create_sample_inventory_data()
    inventory_df.to_excel('samples/inventory_data.xlsx', index=False)
    print("Created: samples/inventory_data.xlsx")
    
    # HR data
    hr_df = create_sample_hr_data()
    hr_df.to_excel('samples/hr_data.xlsx', index=False)
    print("Created: samples/hr_data.xlsx")
    
    print("\nAll sample files generated successfully!")


if __name__ == "__main__":
    generate_all_samples()
