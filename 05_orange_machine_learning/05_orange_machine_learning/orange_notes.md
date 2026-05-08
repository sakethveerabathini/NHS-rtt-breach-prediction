The machine learning stage was implemented using Orange Data Mining to predict RTT breaches.

---

### Data Input
- Imported dataset from SQL output (`rtt_ml_dataset.csv`)
- Dataset includes engineered features such as:
  - current_pct
  - total_waiting
  - p92_wait_time
  - pct_change_last_month
  - waiting_list_change

---

### Feature Selection
- Target Variable:
  - will_breach_next_month (1 = breach, 0 = safe)

- Features used:
  - current_pct  
  - total_waiting  
  - p92_wait_time  
  - pct_change_last_month  
  - waiting_list_change  

- Ignored fields:
  - provider_code  
  - treatment_function  
  - record_date  

---

### Data Preprocessing
- Applied **Impute widget** to handle missing values  
- Ensured consistent input for machine learning models  

---

### Model Training
- Models applied:
  - Random Forest (primary model)
  - Logistic Regression
  - Decision Tree  

- Used **Test & Score** to evaluate model performance  

---

### Model Evaluation
- Evaluated using:
  - ROC Curve  
  - Confusion Matrix  

- Random Forest showed the best performance and was selected for prediction  

---

### Prediction Process
- March 2025 data used as input  
- Trained model applied to predict April 2025 breaches  

- Output:
  - 1 → Likely to breach  
  - 0 → Likely safe  

---

### Output Files
- Workflow file: `rtt_prediction.ows`  
- Workflow screenshot: `orange_workflow.png`  
- Prediction output: `predicted_april_2025.csv`  

---

### Key Insight
The model uses historical performance trends and waiting list changes to predict future RTT breaches, enabling proactive healthcare planning.