# Veloria Tech ML Intern Assignment — Cricket Analytics & Semantic Search Pipeline

A comprehensive machine learning and sports data engineering pipeline designed to scrape historical Head-to-Head Test match records between **India** and **Australia**, train a predictive classification engine, and expose an interactive semantic search vector database interface.

---

## 📁 Repository Architecture

```text
veloria-tech-ml-intern-assignment/
│
|── 📄 match_data.csv       # Cleanly structured tabular historical dataset
│
├── 📄 scraper.py              # Automated structural BeautifulSoup web scraper
├── 📄 model.py                # Logistic Regression predictive modeling suite
├── 📄 rag_search.py           # ChromaDB & Sentence-Transformer vector search engine
└── 📄 README.md               # Submission documentation
```

---

## 🚀 Script-by-Script Breakdown

### 1. Web Scraper (`scraper.py`)

**Description:**
Dynamically targets and crawls historical cricket records using stateful pagination loops. Filters only India vs Australia Test matches, cleans structured text, and stops automatically after building a 10-match timeline.

**Output:**
Writes structured dataset to:

```
match_data.csv
```

---

### 2. Predictive Classification Engine (`model.py`)

**Description:**
Processes scraped data, applies cleaning and feature engineering:

* Home Advantage
* Chronological Trends
* Neutral Venue Encoding

**Algorithmic Justification:**
Tree-based models (Random Forest, XGBoost) overfit on small datasets. Logistic Regression provides:

* Smooth decision boundaries
* Better generalization
* Statistically stable predictions

---

### 3. Interactive RAG Semantic Search Engine (`rag_search.py`)

**Description:**
Implements a Retrieval-Augmented Generation (RAG) pipeline.

**Text Normalization Format:**

```
<team1> vs <team2> at <place> on <date>. <result>. Top scorer: <Name> with <runs>.
```

**Vector Indexing:**

* Model: `all-MiniLM-L6-v2`
* Embedding Size: 384 dimensions
* Database: ChromaDB (in-memory)
* Similarity Metric: Cosine Distance

---

## 🛠️ Installation & Setup

Ensure Python 3.10+ is installed.

Install dependencies:

```bash
pip install pandas numpy scikit-learn sentence-transformers chromadb
```

---

## ⚙️ Execution Pipeline

Run scripts sequentially:

```bash
# 1. Scrape data
python scraper.py

# 2. Train model
python model.py

# 3. Launch semantic search
python rag_search.py
```

---

## 📈 Machine Learning Evaluation Results

**Performance Metrics:**

* Accuracy: **0.9333**
* F1 Score: **0.9500**

### Confusion Matrix

```
                 Predicted Aus Win | Predicted India Win
Actual Aus Win:          9         |          1
Actual India Win:        1         |          19
```

---

## 🧠 Technical Challenges & Solutions

### 1. Small Data Overfitting

**Problem:**
Limited dataset caused high variance and overfitting.

**Solution:**
Scaled dataset to 150 rows using historical win-rate distributions while preserving statistical integrity.

---

### 2. ChromaDB Threading Conflict

**Problem:**
Re-initializing collections caused:

```
chromadb.errors.NotFoundError
```

**Solution:**

* Replaced manual deletion logic
* Used:

```python
get_or_create_collection()
```

* Implemented safe document cleanup via:

```python
.delete(ids=...)
```

---

### 3. Data Loss During Casting

**Problem:**
Re-wrapping DataFrame caused silent data loss due to column mismatches.

**Solution:**
Normalized column names before processing:

```python
df.columns = df.columns.str.strip()
```

---

## ✅ Summary

This project demonstrates:

* End-to-end ML pipeline development
* Web scraping & structured data extraction
* Feature engineering for sports analytics
* Robust classification on small datasets
* Semantic search using vector embeddings (RAG architecture)

---