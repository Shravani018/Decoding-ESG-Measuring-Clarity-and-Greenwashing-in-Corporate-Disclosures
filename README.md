# Decoding ESG: Measuring Clarity and Greenwashing in Corporate Disclosures

**Authors:** Vishwas Khandelwal, Shravani Mahadeshwar, Padma Priya Botsa  
**Under the Guidance of:** Prof. Dr. Lucas Böttcher  
**Program:** Master in Applied Data Science (Batch 2025)  
**Institution:** Frankfurt School of Finance and Management  

---

## 📘 Project Overview

Environmental, Social, and Governance (ESG) reporting has become a cornerstone of modern corporate communication. However, while ESG scores and quantitative performance metrics are widely studied, the **linguistic quality and credibility** of these disclosures remain largely unexplored.

This project analyzes **how** companies communicate ESG information — not just **what** they report — using **Natural Language Processing (NLP)** and **probabilistic topic modeling** techniques.

We examine **10 years (2015–2025)** of SEC 10-K filings from **S&P 50 companies** to measure clarity, factuality, and credibility in ESG communication.

---

## 🎯 Objectives

1. **Identify and categorize** dominant ESG themes using *Guided Latent Dirichlet Allocation (Guided LDA)*.  
2. **Quantify linguistic clarity** via a *Concreteness Score* measuring factual vs. vague language.  
3. **Develop the Greenwashing Risk Index (GRI)** to assess the balance between ESG emphasis and linguistic clarity.  
4. **Provide an empirical framework** for assessing credibility and transparency in corporate ESG reporting.

---

## 🧩 Methodology

### 1. Guided Latent Dirichlet Allocation (Guided LDA)
- Uncovers hidden ESG themes while incorporating prior knowledge through seed words.
- Analyzes each document as a mixture of ESG-related topics.
- Provides interpretable topic distributions for Environmental, Social, and Governance pillars.

### 2. Concreteness and Vagueness Scoring
- Measures linguistic clarity by comparing factual (numeric, measurable) terms vs. vague or hedge words.
- Higher scores indicate clearer, evidence-based communication.

### 3. Token Count and ESG Proportions
- Quantifies text share dedicated to Environmental (E), Social (S), and Governance (G) pillars.

### 4. Greenwashing Risk Index (GRI)
- Evaluates the ratio of ESG content to linguistic clarity.
- **High GRI:** More emphasis with less clarity → potential greenwashing.  
- **Low GRI:** Balanced, credible reporting.

### 5. Topic Coherence Evaluation
- Ensures semantic consistency of topics using *Coherence Scores*.

| ESG Pillar | Coherence Score | Interpretation |
|-------------|-----------------|----------------|
| Environmental | 0.4339 | Distinct but overlapping financial–environmental themes |
| Social | 0.4402 | Balanced coverage of employee and governance-linked reporting |
| Governance | 0.4918 | Strong coherence around compliance and financial control |

---

## 🧠 Key Results and Insights

- **ESG Content Distribution:**  
  - Environmental → 22.4%  
  - Social → 31.1%  
  - Governance → 46.4% (most dominant)  

- **Concreteness Score:** 65.61% → Indicates majority of ESG language is factual and measurable.  
- **Average ESG Content:** 1.46% of total 10-K text.  
- **Average GRI:** 2.3% → Suggests balanced and credible ESG communication overall.  
- **Topic Trends:**  
  - *Environmental:* Climate and Emission Compliance  
  - *Social:* Diversity, Inclusion, and Executive Governance  
  - *Governance:* Board Leadership and Internal Control  

---

## 📊 Data Source and Coverage

- **Source:** SEC **EDGAR** database via the `edgar` Python library.  
- **Dataset:** 10-K filings for all **S&P 50 companies (2015–2025)**.  
- **Metadata:** Ticker, Filing Date, Report Date, Accession Number, Report Text.  
- **Validation:** ESG keyword flag applied for completeness check (not filtering).  
- **Note:** Berkshire Hathaway filings unavailable → analyzed **S&P 49 companies**.  

---

## ⚙️ Tools & Technologies

- **Programming Language:** Python  
- **Libraries:** `guidedlda`, `pandas`, `nltk`, `regex`, `matplotlib`, `edgar`  
- **Modeling:** Guided LDA Topic Modeling  
- **Linguistic Analysis:** Concreteness and Vagueness Scoring using NLP  
- **Evaluation:** Topic Coherence Metrics  

---

## 📈 Limitations & Future Work

- 2025 filings incomplete for most companies.  
- Analysis limited to **10-K filings** (excludes voluntary CSR reports).  
- Future improvements:
  - Extend to global markets (non-SEC filings).  
  - Incorporate transformer-based models (e.g., BERT, BERTopic).  
  - Link linguistic metrics (GRI, clarity) with **actual ESG performance data**.

---

---

## 📜 References

1. Loughran, T. & McDonald, B. (2021). *Measuring Textual Disclosure of Sustainability and CSR in 10-K Filings*. *Journal of Accounting Research.*  
2. Li, Y., Chen, H., & Wang, Q. (2023). *ESG Disclosures in U.S. Public Filings: An Empirical Text Analysis.* SSRN Preprint. [https://ssrn.com/abstract/4402165](https://ssrn.com/abstract/4402165)  
3. Yu, J. & Zhang, L. (2022). *Quantifying ESG Reporting in Corporate Annual Filings.* *Sustainability Accounting Journal*, 11(3), 45–60.  

---

## 🤖 AI Assistance Disclosure

Some portions of this project (language refinement, code comments, report formatting) were supported by **AI tools** including *ChatGPT (GPT-5 by OpenAI)* and *Claude Sonnet (Claude 4.5 by Anthropic)*.  
All AI-assisted outputs were **reviewed and validated** by the authors to ensure technical accuracy and alignment with project objectives.

---

## 🔗 Links

- 📄 **Code Repository:** [GitHub – Vikh110/Decoding-ESG-Measuring-Clarity-and-Greenwashing-in-Corporate-Disclosures](https://github.com/Vikh110/Decoding-ESG-Measuring-Clarity-and-Greenwashing-in-Corporate-Disclosures)
- 📑 **Data Source:** [SEC EDGAR Database](https://www.sec.gov/edgar)
- 📊 **Presentation:** `Presentation.pptx` (included in repo)
- 🧾 **Full Report:** `Micropublication.docx` (included in repo)

---

**© 2025 | Frankfurt School of Finance and Management | Applied Data Science Program**

