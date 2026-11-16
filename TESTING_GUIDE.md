# 🧪 Sentiment Analysis Testing & Quality Assurance Guide

This guide provides test datasets, edge-case benchmarks, and systematic verification steps to evaluate the **SENTIMENT.AI** DistilBERT inference engine and dashboard interface.

---

## 📁 Included Test Documents

| File | Format | Purpose | Usage |
|---|---|---|---|
| [`test_samples.txt`](file:///Users/prakash/Desktop/cse471/sentiment_analyser/test_samples.txt) | Plain text (`.txt`) | 25 diverse reviews and sentences | Drag-and-drop into the **Batch Processing** tab or copy lines into Single Analysis |
| [`test_benchmark.csv`](file:///Users/prakash/Desktop/cse471/sentiment_analyser/test_benchmark.csv) | CSV (`.csv`) | 15 categorized benchmark samples with expected sentiment & test objectives | Systematic edge-case evaluation (negations, idioms, slang) |

---

## 🚀 How to Run the Tests

### Test 1: Single Text Analysis (Live & Manual)

1. Launch the server (if not already running):
   ```bash
   python app/app.py
   ```
2. Open **[http://localhost:8501](http://localhost:8501)**.
3. Test the built-in presets by clicking any of the 6 benchmark chips:
   - **Highly Positive**: Verifies high confidence (>95%) on strong positive vocabulary.
   - **Harsh Criticism**: Verifies high confidence (>95%) on scathing critiques.
   - **Sarcastic Praise**: Tests how the transformer evaluates irony (`"Oh brilliant..."`).
   - **Mixed Feelings**: Tests contrastive clauses (`"The cinematography was breathtaking, but..."`).
   - **Strongly Negative**: Tests deep disappointment and critique.
   - **Casual Slang**: Tests modern vernacular (`"lowkey fire", "fr"`).
4. **Keyboard Shortcut**: Press <kbd>Cmd</kbd> + <kbd>Enter</kbd> (or <kbd>Ctrl</kbd> + <kbd>Enter</kbd>) to trigger instant analysis.
5. **Live Typing**: Toggle the **Live Typing** switch to ON, then type a sentence to verify debounced real-time predictions.
6. **Token Salience**: Notice the **Key Sentiment Drivers** tags beneath the probabilities—they show which specific words pushed the score positive or negative.

---

### Test 2: Batch Processing with `test_samples.txt`

1. Click on the **Batch Processing** tab in the top navigation bar.
2. Drag and drop [`test_samples.txt`](file:///Users/prakash/Desktop/cse471/sentiment_analyser/test_samples.txt) directly into the dashed upload area (or click to browse and select it).
3. The 25 sample lines will populate the editor automatically.
4. Click **Execute Batch Analysis**.
5. **Verify the Results**:
   - Total Processed count updates to `25`.
   - Positive and Negative count cards display accurate ratios.
   - Total runtime is calculated in milliseconds (typically ~100–300ms for 25 items on MPS/CPU).
6. **Filter Results**:
   - Click **Positive Only** to verify only positive rows are displayed.
   - Click **Negative Only** to verify only negative rows are displayed.
   - Click **All Results** to reset the view.
7. **Export**:
   - Click **Export CSV** to download `sentiment_batch_results.csv` with confidence scores and latencies.

---

### Test 3: Linguistic Edge-Case Benchmarks

Use samples from [`test_benchmark.csv`](file:///Users/prakash/Desktop/cse471/sentiment_analyser/test_benchmark.csv) to test transformer comprehension:

| Category | Test Sentence | Expected Result | Why It's a Challenge |
|---|---|---|---|
| **Contrastive 'But'** | *"The cinematography was breathtaking, but the plot was disjointed and flat."* | **Negative** (or low confidence) | The contrastive clause ("but...") usually determines the ultimate sentiment of a sentence. |
| **Double Negation** | *"I honestly cannot believe how not bad this turned out to be!"* | **Positive** | "not bad" is positive; double negation can confuse simple dictionary/lexicon analyzers, but transformers resolve it. |
| **Inverted Idiom** | *"The camera work failed to disappoint, delivering mesmerizing visuals."* | **Positive** | "Failed to disappoint" means it succeeded and was good. |
| **Expectation Flip** | *"I walked into the theater expecting trash, but I was pleasantly surprised."* | **Positive** | Starts with negative keyword ("trash") but concludes positively ("pleasantly surprised"). |
| **Minimal Token Length** | *"meh."* | **Negative / Neutral** | Extremely short input testing subword tokenizer handling on single colloquial expressions. |

---

### Test 4: Model Insights & History

1. **Model Insights Tab**:
   - Click the **Model Insights** tab.
   - Verify the 4 KPI cards load dynamically from `/api/model-info`:
     - Test Accuracy: `91.22%`
     - F1-Score: `91.24%`
     - Precision: `91.01%`
     - Recall: `91.47%`
   - Review the Confusion Matrix (11,370 TN, 1,130 FP, 1,066 FN, 11,434 TP) and active compute device.
2. **History Tab**:
   - Click the **History** tab.
   - Verify your recent analyses are logged with timestamps and latencies.
   - Click **Load** next to any previous prediction to reload that text back into the Single Analysis editor.
   - Click **Export JSON** to verify the history downloads properly.

---

### Test 5: Direct REST API Testing (Terminal / curl)

You can also test the backend endpoints directly using `curl`:

#### Single Prediction Endpoint
```bash
curl -X POST http://localhost:8501/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "An absolute cinematic masterpiece with breathtaking direction."}'
```

#### Batch Endpoint
```bash
curl -X POST http://localhost:8501/api/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great experience!", "Terrible service.", "It was okay."]}'
```

#### Model Info Endpoint
```bash
curl http://localhost:8501/api/model-info
```

#### Interactive Swagger UI
Open **[http://localhost:8501/docs](http://localhost:8501/docs)** to test all API routes directly from the interactive OpenAPI documentation interface.
