# E-commerce Behavioral Analytics & A/B Test Simulation
#### Identifying funnel drop-offs and improving purchase conversion through experiment design

(*Work In Progress)

## 1. Project Overview

This project analyzes large-scale e-commerce behavioral log data to identify conversion bottlenecks and design an A/B test strategy for improving purchase conversion.

Rather than stopping at descriptive analytics, this project follows a practical business workflow:

> raw data audit → funnel analysis → item/category analysis → A/B test design → statistical simulation → business recommendation

The objective is to transform behavioral data into actionable product and growth strategies.

---

## 2. Raw Data Summary

Initial raw data audit results:

| Data | Summary |
|---|---:|
| Event rows | 2,756,101 |
| Unique visitors | 1,407,580 |
| Unique items in events | 235,061 |
| Event period | 2015-05-03 to 2015-09-18 |
| Item property rows | 20,275,902 |
| Category tree rows | 1,669 |

Event distribution:

| Event Type | Count |
|---|---:|
| view | 2,664,312 |
| addtocart | 69,332 |
| transaction | 22,457 |

User-level funnel:

| Funnel Stage | Unique Visitors |
|---|---:|
| View | 1,404,179 |
| Add to Cart | 37,722 |
| Purchase | 11,719 |

Approximate user-level conversion rates:

| Conversion Step | Rate |
|---|---:|
| View → Add to Cart | 2.69% |
| Add to Cart → Purchase | 28.04% |
| View → Purchase | 0.83% |

---

## 3. Key Analytical Direction

The initial audit suggests that the largest conversion bottleneck occurs before users add products to cart.

This means the highest-impact optimization opportunity may not be the checkout page, but the product discovery and product detail experience.

Potential business hypotheses:

- Product pages may not create enough purchase intent.
- Some item categories may naturally convert better than others.
- High traffic does not always mean high purchase conversion.
- A/B tests should focus on cart-entry triggers and product page UX.

---

## 4. Project Structure

```text
ECOMMERCE_AB_TEST_PROJECT/
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_raw_data_audit.ipynb
│   ├── 02_event_funnel_analysis.ipynb
│   ├── 03_item_category_analysis.ipynb
│   ├── 04_ab_test_design_simulation.ipynb
│   └── 05_business_recommendation.ipynb
│
├── outputs/
│   ├── charts/
│   └── tables/
│
├── src/
│   └── utils.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 5. Analysis Workflow

### 1. Raw Data Audit

Notebook: `01_raw_data_audit.ipynb`

Main tasks:

- Validate row counts and schema
- Check data types
- Convert timestamps
- Detect missing values
- Detect duplicate rows
- Summarize event distribution

### 2. Funnel Analysis

Notebook: `02_event_funnel_analysis.ipynb`

Main tasks:

- Define user funnel stages
- Measure conversion rates
- Analyze drop-off points
- Time-series trend analysis

### 3. Item & Category Analysis

Notebook: `03_item_category_analysis.ipynb`

Main tasks:

- Merge behavioral logs with item categories
- Compare item-level conversion
- Identify high-performing categories
- Detect underperforming segments

### 4. A/B Test Design & Simulation

Notebook: `04_ab_test_design_simulation.ipynb`

Main tasks:

- Define baseline conversion
- Set uplift scenarios
- Sample size estimation
- Two-proportion z-test
- Expected revenue impact simulation

### 5. Business Recommendation

Notebook: `05_business_recommendation.ipynb`

Main tasks:

- Summarize findings
- Prioritize experiments
- Recommend actionable growth strategies

---

## 6. Streamlit Dashboard

The Streamlit dashboard is designed for business stakeholders.

Planned pages:

1. Executive Summary  
2. Funnel Analysis  
3. Item & Category Insights  
4. A/B Test Simulation  
5. Business Action Plan

Run locally:

```bash
streamlit run app/streamlit_app.py
```

---

## 7. Tech Stack

- Python
- pandas
- NumPy
- SciPy
- Statsmodels
- Matplotlib
- Plotly
- Streamlit
- Jupyter Notebook
- PyArrow
- tqdm

---

## 8. Repository Policy

Raw data files are excluded from the repository due to file size.

Excluded paths:

data/raw/  
data/processed/  
outputs/

---

## 9. Author

Ji-Eun Son
