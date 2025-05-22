import pandas as pd
import numpy as np

# --- Configuration for Data Generation ---
num_months = 36  # Generate data for 3 years
start_date = '2022-01-01'

# Initial values
initial_subscribed_facilities = 10
initial_operational_capacity = 5
initial_satisfaction = 4.5
initial_reputation_proxy = 50 # (0-100 scale)
initial_marketing_spend = 500
initial_sales_team_size = 2

# Growth/Trend factors
avg_signups_per_salesperson = 1.5
marketing_effectiveness_on_signups = 0.01
reputation_effectiveness_on_signups = 0.005
churn_base_rate = 0.01
satisfaction_impact_on_churn = -0.005 # Negative: higher satisfaction -> lower churn impact
strain_impact_on_satisfaction = -0.2 # Higher strain reduces satisfaction
capacity_investment_trigger_growth_pct = 0.05 # Invest if facilities grow by 5%
capacity_investment_base_per_10_facilities = 100
capacity_units_per_investment_unit = 0.002
value_realization_for_reputation = 0.5 # Per net new facility
reputation_decay_rate = 0.02

# Generate MonthYear sequence
dates = pd.to_datetime(pd.date_range(start=start_date, periods=num_months, freq='MS'))

# --- Initialize lists to store data ---
data_list = []

# --- Seed initial values for the loop ---
current_subscribed_facilities = initial_subscribed_facilities
current_operational_capacity = initial_operational_capacity
current_satisfaction = initial_satisfaction
current_reputation_proxy = initial_reputation_proxy
current_marketing_spend = initial_marketing_spend
current_sales_team_size = initial_sales_team_size

# --- Simulate month by month ---
for i in range(num_months):
    # For the very first month, set facilities_at_start_of_month for churn calculation
    if i == 0:
        facilities_at_start_of_month = initial_subscribed_facilities
    else:
        facilities_at_start_of_month = data_list[-1]['Active_Subscribed_Facilities']

    # 1. New Facility Signups
    base_signups_from_sales = current_sales_team_size * avg_signups_per_salesperson
    marketing_boost = current_marketing_spend * marketing_effectiveness_on_signups
    reputation_boost = current_reputation_proxy * reputation_effectiveness_on_signups
    new_facility_signups = int(np.round(max(0, base_signups_from_sales + marketing_boost + reputation_boost + np.random.normal(0, 1))))

    # 2. Churned Facilities
    churn_increase_due_to_low_satisfaction = (5 - current_satisfaction) * abs(satisfaction_impact_on_churn) * 5 # Amplified effect
    actual_churn_rate = churn_base_rate + churn_increase_due_to_low_satisfaction
    churned_facilities = int(np.round(max(0, facilities_at_start_of_month * actual_churn_rate + np.random.normal(0, 0.5))))
    churned_facilities = min(churned_facilities, facilities_at_start_of_month + new_facility_signups) # Cannot churn more than available

    # 3. Active Subscribed Facilities (STOCK UPDATE LOGIC)
    if i == 0:
        active_subscribed_facilities_end_of_month = initial_subscribed_facilities + new_facility_signups - churned_facilities
    else:
        active_subscribed_facilities_end_of_month = data_list[-1]['Active_Subscribed_Facilities'] + new_facility_signups - churned_facilities
    active_subscribed_facilities_end_of_month = max(0, active_subscribed_facilities_end_of_month)

    # 4. Operational Capacity & Investment
    capacity_investment_spend = 0
    # Invest if facility count grows significantly OR if capacity is much lower than needed by signups
    if (active_subscribed_facilities_end_of_month > facilities_at_start_of_month * (1 + capacity_investment_trigger_growth_pct)) or \
       (current_operational_capacity < new_facility_signups * 0.8 and i > 0): # Needs some history for the second condition
        capacity_investment_spend = (active_subscribed_facilities_end_of_month // 10) * capacity_investment_base_per_10_facilities + np.random.randint(0, 200)
        current_operational_capacity += capacity_investment_spend * capacity_units_per_investment_unit
    current_operational_capacity = max(1, current_operational_capacity + np.random.normal(0, 0.05)) # Small organic change/noise, min 1

    # 5. Strain Proxy
    strain_proxy = new_facility_signups / max(1, current_operational_capacity)

    # 6. Customer Satisfaction
    satisfaction_change_due_to_strain = strain_proxy * strain_impact_on_satisfaction
    # Mean reversion towards a higher base if strain is low
    mean_reversion_effect = (4.0 - current_satisfaction) * 0.1 if strain_proxy < 1.5 else 0
    current_satisfaction += satisfaction_change_due_to_strain + mean_reversion_effect
    current_satisfaction = np.clip(current_satisfaction + np.random.normal(0, 0.05), 1, 5)

    # 7. Service Reputation Proxy
    net_new_facilities_this_month = new_facility_signups - churned_facilities
    reputation_build = net_new_facilities_this_month * value_realization_for_reputation
    reputation_decay = current_reputation_proxy * reputation_decay_rate
    current_reputation_proxy += reputation_build - reputation_decay
    current_reputation_proxy = np.clip(current_reputation_proxy + np.random.normal(0, 1), 0, 100)

    # 8. Support Tickets
    support_tickets_opened = int(max(5, active_subscribed_facilities_end_of_month * 0.25 + strain_proxy * 10 + (5 - current_satisfaction) * 5 + np.random.normal(0, 5)))

    # 9. Marketing Spend & Sales Team (simplified growth)
    if i % 6 == 0 and i > 0: # Review marketing every 6 months
        current_marketing_spend = max(300, current_marketing_spend + np.random.randint(-50, 150) + (active_subscribed_facilities_end_of_month // 50) * 50)
    if active_subscribed_facilities_end_of_month > (current_sales_team_size**2 * 15) and i > 0: # Threshold to add salesperson
        current_sales_team_size = max(initial_sales_team_size, current_sales_team_size + 1)
    current_marketing_spend = max(200, current_marketing_spend)
    current_sales_team_size = max(1, current_sales_team_size)

    data_list.append({
        'MonthYear': dates[i], # Store as datetime object directly
        'New_Facility_Signups': new_facility_signups,
        'Active_Subscribed_Facilities': active_subscribed_facilities_end_of_month,
        'Churned_Facilities': churned_facilities,
        'Operational_Capacity_Units': round(current_operational_capacity, 2),
        'Average_Customer_Satisfaction_Score': round(current_satisfaction, 2),
        'Service_Reputation': round(current_reputation_proxy, 1),
    })

df_dynamic_performance = pd.DataFrame(data_list)

# Save to CSV
csv_file_path_dynamic = 'monthly_business_performance_dynamic.csv'
df_dynamic_performance.to_csv(csv_file_path_dynamic, index=False, date_format='%Y-%m-%d')

print(f"'{csv_file_path_dynamic}' created successfully with dynamic stock-flow logic.")