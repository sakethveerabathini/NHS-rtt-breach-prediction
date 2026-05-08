# Feature Engineering

Feature engineering was performed in SQL to prepare the dataset for machine learning prediction.

## Features Created
- current_pct
- total_waiting
- p92_wait_time
- pct_change_last_month
- waiting_list_change

## Target Variable
- will_breach_next_month

## Logic
Historical NHS RTT data was transformed into a predictive dataset by calculating:
- month-over-month performance changes
- waiting list growth trends
- future breach indicators

The target variable predicts whether a pathway will breach the RTT target in the following month.