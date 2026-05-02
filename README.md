# E-commerce Behavioral Analytics & A/B Test Simulation  
#### Turning behavioral log data into conversion growth strategies through funnel analytics and experiment design

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)]()
[![Status](https://img.shields.io/badge/Project-Completed-brightgreen.svg)]()

### 🚀 Streamlit Dashboard: [Click Here to Explore the Live App](https://ecommerce-ab-test.streamlit.app/)

---

## 1. Project Overview

This project analyzes large-scale e-commerce behavioral event log data to identify where users drop off in the purchase journey and how conversion can be improved through A/B testing.

Rather than stopping at descriptive analytics, the project follows a practical product analytics workflow:

> **raw data audit → funnel diagnosis → item/category opportunity analysis → A/B test simulation → business action plan**

The final goal is simple:

> **Find where conversion is leaking, prioritize what to improve first, and design experiments with measurable business impact.**

---

## 2. Why This Project Matters

In e-commerce, even a small improvement in conversion rate can create significant business value.

Examples:

- Better CTA button wording
- Improved product detail page layout
- Stronger trust signals: reviews, delivery, returns
- Better recommendation placement
- Smarter exposure of high-converting categories

Instead of relying on intuition, this project uses data to answer:

> **Which change should be tested first?**

---

## 3. Core Findings

### User-Level Funnel

| Funnel Stage | Unique Users |
|---|---:|
| View Product | 1,404,179 |
| Add to Cart | 37,722 |
| Purchase | 11,719 |

### Conversion Rates

| Conversion Step | Rate |
|---|---:|
| View → Add to Cart | **2.69%** |
| Add to Cart → Purchase | **28.04%** |
| View → Purchase | **0.83%** |

### Key Insight

The largest conversion bottleneck occurs **before users add products to cart**.

This means the first optimization priority is **not checkout**, but:

- Product detail page UX
- CTA button design / wording
- Promotion messaging
- Recommendation modules
- Trust-building information

---

## 4. Final Business Action Plan

### Action 1. Optimize High-Traffic / Low-Conversion Categories

Target categories with many visitors but weak conversion.

Recommended tests:

- CTA redesign
- Better price / benefit communication
- Review visibility improvement
- Shipping / return reassurance

### Action 2. Expand Low-Traffic / High-Conversion Categories

Some categories convert well but lack exposure.

Recommended tests:

- Recommendation slots
- Search ranking boost
- Homepage banner exposure
- Promotional traffic allocation

### Action 3. Measure the Right Metrics

**Primary Metric**

> View → Add to Cart Conversion Rate

**Guardrail Metric**

> View → Purchase Conversion Rate

---

## 5. Analytical Workflow

### 01. Raw Data Audit

Notebook: `01_raw_data_audit.ipynb`

- Validate schema and row counts
- Timestamp conversion
- Missing values / duplicates
- Event distribution audit

### 02. Funnel Analysis

Notebook: `02_event_funnel_analysis.ipynb`

- User journey funnel definition
- Step conversion rates
- Drop-off diagnosis
- Daily / monthly trends

### 03. Item & Category Analysis

Notebook: `03_item_category_analysis.ipynb`

- Category mapping merge
- High-performing categories
- Opportunity matrix
- Optimization vs expansion candidates

### 04. A/B Test Design & Simulation

Notebook: `04_ab_test_design_simulation.ipynb`

- Baseline metric setup
- Uplift scenarios
- Sample size estimation
- Two-proportion z-test
- Monte Carlo simulation
- Expected impact per 100K users

### 05. Business Recommendation

Notebook: `05_business_recommendation.ipynb`

- Prioritized roadmap
- Final experiment plan
- Decision rules for rollout

---

## 6. Streamlit Dashboard

An interactive dashboard was built for business stakeholders.

### Main Pages

1. Project Guide
2. Executive Summary
3. Funnel Analysis
4. Item & Category Insights
5. A/B Test Simulation
6. Business Action Plan
7. Data & Repository Notes

### Run Locally

```bash
python -m streamlit run app/streamlit_app.py
```

---

## 7. Project Structure

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
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 8. Tech Stack

- Python
- pandas
- NumPy
- SciPy
- Statsmodels
- Matplotlib
- Streamlit
- Jupyter Notebook
- PyArrow
- tqdm

---

## 9. Repository Policy

Raw data files are excluded from GitHub due to file size.

Excluded paths:

```text
data/raw/
data/processed/
outputs/
```

---

## 10. Author

**Ji-Eun Son**
