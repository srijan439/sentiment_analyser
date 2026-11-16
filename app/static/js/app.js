/**
 * SENTIMENT.AI — Enterprise Dashboard Client Application
 * Handles Real-time Inference, Batch Processing, Model Insights, and Audio Feedback.
 */

document.addEventListener('DOMContentLoaded', () => {
  // ── Global Application State ──
  const state = {
    activeTab: 'single',
    liveMode: false,
    debounceTimer: null,
    isAnalyzing: false,
    history: JSON.parse(localStorage.getItem('sentiment_ai_history') || '[]'),
    batchResults: [],
    batchFilter: 'all',
  };

  // ── DOM References ──
  const singleText = document.getElementById('single-text');
  const analyzeBtn = document.getElementById('analyze-btn');
  const clearBtn = document.getElementById('clear-btn');
  const liveToggle = document.getElementById('live-mode-toggle');
  const charCount = document.getElementById('char-count');
  const wordCount = document.getElementById('word-count');
  const resultContainer = document.getElementById('result-container');
  const resultsMetaPill = document.getElementById('results-meta-pill');
  const resultsLatencyText = document.getElementById('results-latency-text');
  const soundToggleBtn = document.getElementById('sound-toggle-btn');
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const batchText = document.getElementById('batch-text');
  const batchAnalyzeBtn = document.getElementById('batch-analyze-btn');
  const batchFile = document.getElementById('batch-file');
  const dropZone = document.getElementById('drop-zone');
  const batchResultsWrap = document.getElementById('batch-results-wrapper');
  const exportCsvBtn = document.getElementById('export-csv-btn');
  const historyList = document.getElementById('history-list');
  const clearHistoryBtn = document.getElementById('clear-history-btn');
  const exportHistoryBtn = document.getElementById('export-history-btn');
  const historyCounter = document.getElementById('history-counter');

  // ── Sound Feedback Engine ──
  function updateSoundButton() {
    if (!soundToggleBtn) return;
    const isMuted = window.soundEngine ? window.soundEngine.isMuted() : false;
    soundToggleBtn.innerHTML = isMuted
      ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
           <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
           <line x1="23" y1="9" x2="17" y2="15"></line>
           <line x1="17" y1="9" x2="23" y2="15"></line>
         </svg>`
      : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
           <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
           <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
           <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
         </svg>`;
    soundToggleBtn.title = isMuted ? 'Audio feedback: Muted' : 'Audio feedback: Active';
  }
  updateSoundButton();

  soundToggleBtn?.addEventListener('click', () => {
    if (window.soundEngine) {
      const active = window.soundEngine.toggleMute();
      updateSoundButton();
      showToast(active ? 'Audio feedback enabled' : 'Audio feedback muted');
    }
  });

  // ── Theme Management (Dark by Default) ──
  function updateThemeButton(theme) {
    if (!themeToggleBtn) return;
    themeToggleBtn.innerHTML = theme === 'dark'
      ? `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
           <circle cx="12" cy="12" r="5"></circle>
           <line x1="12" y1="1" x2="12" y2="3"></line>
           <line x1="12" y1="21" x2="12" y2="23"></line>
           <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
           <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
           <line x1="1" y1="12" x2="3" y2="12"></line>
           <line x1="21" y1="12" x2="23" y2="12"></line>
           <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
           <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
         </svg>`
      : `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
           <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
         </svg>`;
  }

  const savedTheme = localStorage.getItem('sentiment_ai_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeButton(savedTheme);

  themeToggleBtn?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('sentiment_ai_theme', next);
    updateThemeButton(next);
    window.soundEngine?.playClick();
    showToast(`Switched to ${next} theme`);
  });

  // ── Segmented Control Tabs Navigation ──
  document.querySelectorAll('.segment-tab').forEach(btn => {
    btn.addEventListener('click', () => {
      window.soundEngine?.playClick();
      const target = btn.dataset.tab;

      document.querySelectorAll('.segment-tab').forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const panel = document.getElementById(`tab-${target}`);
      if (panel) panel.classList.add('active');
      state.activeTab = target;

      if (target === 'insights') {
        fetchModelInsights();
      } else if (target === 'history') {
        renderHistory();
      }
    });
  });

  // ── Text Editor Word & Char Counting ──
  function updateTextCounts() {
    const text = singleText ? singleText.value : '';
    const chars = text.length;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    if (charCount) charCount.textContent = `${chars} character${chars === 1 ? '' : 's'}`;
    if (wordCount) wordCount.textContent = `${words} word${words === 1 ? '' : 's'}`;
  }

  singleText?.addEventListener('input', () => {
    updateTextCounts();
    if (state.liveMode) {
      clearTimeout(state.debounceTimer);
      state.debounceTimer = setTimeout(() => {
        if (singleText.value.trim().length >= 3) {
          runSinglePrediction(true);
        }
      }, 350);
    }
  });

  // Keyboard shortcut: Cmd + Enter (or Ctrl + Enter)
  singleText?.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      runSinglePrediction();
    } else if (e.key === 'Escape') {
      clearBtn?.click();
    }
  });

  // ── Clear Action ──
  clearBtn?.addEventListener('click', () => {
    window.soundEngine?.playClick();
    if (singleText) singleText.value = '';
    updateTextCounts();
    resetResultToEmptyState();
    singleText?.focus();
    showToast('Input cleared');
  });

  // ── Live Analysis Toggle ──
  liveToggle?.addEventListener('change', (e) => {
    state.liveMode = e.target.checked;
    window.soundEngine?.playClick();
    if (state.liveMode && singleText.value.trim().length >= 3) {
      runSinglePrediction(true);
    }
    showToast(state.liveMode ? 'Real-time analysis active' : 'Manual evaluation mode');
  });

  // ── Preset Benchmark Chips ──
  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      window.soundEngine?.playClick();
      const text = btn.dataset.text;
      if (singleText && text) {
        singleText.value = text;
        updateTextCounts();
        runSinglePrediction();
      }
    });
  });

  // ── Analyze Button Click ──
  analyzeBtn?.addEventListener('click', () => runSinglePrediction());

  // ── Single Prediction Execution ──
  async function runSinglePrediction(isLive = false) {
    const text = singleText ? singleText.value.trim() : '';
    if (!text) {
      showToast('Please enter text to analyze', 'warning');
      singleText?.focus();
      return;
    }

    if (!isLive) {
      window.soundEngine?.playClick();
      setAnalyzeLoading(true);
    }

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Prediction request failed');
      }

      const data = await response.json();
      renderSingleResult(data);

      // Audio feedback
      if (data.sarcasm && data.sarcasm.is_sarcastic) {
        window.soundEngine?.playSarcasm();
      } else if (data.label_category === 'positive') {
        window.soundEngine?.playPositive();
      } else if (data.label_category === 'neutral') {
        window.soundEngine?.playNeutral();
      } else {
        window.soundEngine?.playNegative();
      }
      window.soundEngine?.haptic(20);

      // Save to history log
      saveToHistory(data);
    } catch (err) {
      console.error(err);
      showToast(`Error: ${err.message}`, 'error');
    } finally {
      if (!isLive) {
        setAnalyzeLoading(false);
      }
    }
  }

  function setAnalyzeLoading(loading) {
    state.isAnalyzing = loading;
    if (!analyzeBtn) return;
    if (loading) {
      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
          <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
          <path d="M12 2a10 10 0 0 1 10 10"></path>
        </svg>
        <span>Computing...</span>
      `;
    } else {
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
        <span>Analyze Sentiment</span>
        <kbd class="btn-kbd">⌘↵</kbd>
      `;
    }
  }

  function resetResultToEmptyState() {
    if (resultsMetaPill) resultsMetaPill.style.display = 'none';
    if (!resultContainer) return;
    resultContainer.innerHTML = `
      <div class="empty-state-view">
        <div class="empty-graphic">
          <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="4" y="8" width="40" height="32" rx="8" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3 3"/>
            <path d="M12 24C15 20 18 28 21 24C24 20 27 28 30 24C33 20 36 26 36 24" stroke="var(--accent)" stroke-width="2" stroke-linecap="round"/>
            <circle cx="21" cy="24" r="2" fill="var(--accent)"/>
            <circle cx="30" cy="24" r="2" fill="var(--positive)"/>
          </svg>
        </div>
        <h3 class="empty-title">Awaiting Text Input</h3>
        <p class="empty-description">
          Enter text in the editor or select a preset benchmark on the left to run inference with the fine-tuned DistilBERT transformer.
        </p>
        <div class="model-spec-chips">
          <span class="spec-chip">DistilBERT-Base</span>
          <span class="spec-chip">66.3M Parameters</span>
          <span class="spec-chip">Sub-15ms Latency</span>
        </div>
      </div>
    `;
  }

  // ── Render Results with Premium SaaS Presentation ──
  function renderSingleResult(data) {
    if (!resultContainer) return;

    // Update Header Meta Pill
    if (resultsMetaPill && resultsLatencyText) {
      resultsMetaPill.style.display = 'inline-flex';
      resultsLatencyText.textContent = `${data.time_ms} ms`;
    }

    const isPos = data.label_category === 'positive';
    const isNeg = data.label_category === 'negative';
    const isNeutral = data.label_category === 'neutral';
    const isSarcastic = data.sarcasm && data.sarcasm.is_sarcastic;
    const heroClass = isSarcastic ? 'sarcastic' : (data.label_category || (data.confidence_pct < 60 ? 'neutral' : (isPos ? 'positive' : 'negative')));
    const labelTitle = isSarcastic ? 'Sarcastic Mockery' : (data.label.includes('Sentiment') ? data.label : `${data.label} Sentiment`);
    const subLabelText = isSarcastic 
      ? 'DistilBERT Lexical Dissonance Engine' 
      : (data.segments && data.segments.length > 1 ? 'DistilBERT Multi-Clause Evaluator' : 'DistilBERT Sequence Classifier');

    const ambivalencePct = data.ambivalence_pct !== undefined ? data.ambivalence_pct : Math.max(0, Math.round((100 - Math.abs(data.positive_pct - data.negative_pct)) * 10) / 10);
    const explanation = data.explanation || (isPos ? 'The model detected favorable sentiment.' : 'The model detected critical sentiment.');

    // Sarcasm & Irony Intelligence Box
    const sarcasmHtml = isSarcastic ? `
      <div class="sarcasm-callout-box">
        <div class="sarcasm-callout-header">
          <div class="sarcasm-header-left">
            <span class="sarcasm-badge-tag">🎭 SARCASTIC MOCKERY & IRONY</span>
          </div>
          <span class="sarcasm-badge-score">${data.sarcasm.sarcasm_pct}% Sarcasm Index</span>
        </div>
        <div class="sarcasm-callout-body">
          <p class="sarcasm-narrative">
            Hyperbolic superlative praise is employed as an ironic rhetorical device to satirize critical flaws. The true emotional polarity is negative critique.
          </p>
          <div class="sarcasm-trope-group">
            <div class="sarcasm-trope-title">DETECTED RHETORICAL TROPES & LEXICAL CLASH:</div>
            <div class="sarcasm-chips-wrap">
              ${(data.sarcasm.markers || []).map(m => `<span class="sarcasm-chip marker"><span class="chip-type">Rhetoric</span> "${escapeHtml(m.matches[0])}"</span>`).join('')}
              ${(data.sarcasm.ironic_praise || []).map(p => `<span class="sarcasm-chip praise"><span class="chip-type">Ironic Praise</span> "${escapeHtml(p)}"</span>`).join('')}
              ${(data.sarcasm.critique_tokens || []).slice(0, 4).map(c => `<span class="sarcasm-chip critique"><span class="chip-type">Critical Target</span> "${escapeHtml(c)}"</span>`).join('')}
            </div>
          </div>
        </div>
      </div>
    ` : '';

    // Aspect Polarity Matrix (Favorable Dimensions vs. Critical Shortcomings)
    const hasAspects = data.aspects && data.aspects.has_mixed_aspects;
    const aspectMatrixHtml = hasAspects ? `
      <div class="aspect-matrix-container">
        <div class="aspect-matrix-header">
          <span>DIMENSIONAL POLARITY COMPARISON</span>
          <span class="aspect-matrix-sub">Visual Brilliance vs. Narrative / Execution</span>
        </div>
        <div class="aspect-grid-two-col">
          <div class="aspect-col favorable">
            <div class="aspect-col-title">
              <span class="aspect-status-dot pos"></span>
              <span>FAVORABLE DIMENSIONS</span>
            </div>
            <div class="aspect-cards-list">
              ${data.aspects.favorable_aspects.map(a => `
                <div class="aspect-card-item pos">
                  <div class="aspect-card-label">${escapeHtml(a.title)}</div>
                  <div class="aspect-card-keywords">${a.keywords.map(k => `<code>${escapeHtml(k)}</code>`).join(' ')}</div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="aspect-col critical">
            <div class="aspect-col-title">
              <span class="aspect-status-dot neg"></span>
              <span>CRITICAL SHORTCOMINGS</span>
            </div>
            <div class="aspect-cards-list">
              ${data.aspects.critical_aspects.map(a => `
                <div class="aspect-card-item neg">
                  <div class="aspect-card-label">${escapeHtml(a.title)}</div>
                  <div class="aspect-card-keywords">${a.keywords.map(k => `<code>${escapeHtml(k)}</code>`).join(' ')}</div>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    ` : '';

    // Emotional Trajectory Arc Timeline
    const arcHtml = data.segments && data.segments.length > 1 ? `
      <div class="arc-timeline-container">
        <div class="arc-timeline-header">
          <span>EMOTIONAL TRAJECTORY ARC</span>
          <span class="arc-timeline-sub">${data.segments.length} Clause Milestones</span>
        </div>
        <div class="arc-steps-track">
          ${data.segments.map((seg, idx) => `
            <div class="arc-step-node ${seg.label.toLowerCase()}" title="Clause ${idx + 1}: ${seg.label} (${seg.label === 'Positive' ? seg.positive_pct : seg.negative_pct}%)">
              <span class="arc-node-badge ${seg.label.toLowerCase()}">#${idx + 1}</span>
              <span class="arc-node-label">${seg.label}</span>
              <span class="arc-node-pct">${seg.label === 'Positive' ? seg.positive_pct : seg.negative_pct}%</span>
            </div>
          `).join('<div class="arc-step-arrow">→</div>')}
        </div>
      </div>
    ` : '';

    // Clause-by-clause sentiment flow
    const segmentsHtml = data.segments && data.segments.length > 1 ? `
      <div class="segments-container">
        <div class="segments-header">
          <span>CLAUSE-BY-CLAUSE SENTIMENT FLOW</span>
          <span class="segments-header-meta">${data.segments.length} Segments Analyzed</span>
        </div>
        <div class="segments-list">
          ${data.segments.map(seg => `
            <div class="segment-card ${seg.label.toLowerCase()}">
              <div class="segment-badge ${seg.label.toLowerCase()}">
                <span class="segment-dot ${seg.label.toLowerCase()}"></span>
                <span>${seg.label}</span>
                <span class="segment-conf">${seg.label === 'Positive' ? seg.positive_pct : seg.negative_pct}%</span>
              </div>
              <div class="segment-text">"${escapeHtml(seg.text)}"</div>
            </div>
          `).join('')}
        </div>
      </div>
    ` : '';

    // Salience Highlights
    const salienceHtml = data.salient_words && data.salient_words.length > 0 ? `
      <div class="salience-container">
        <div class="salience-header">
          <span>KEY SENTIMENT DRIVERS</span>
          <span style="font-size:10px; font-weight:500; font-family:var(--font-mono); color:var(--text-muted);">Leave-One-Out Token Salience</span>
        </div>
        <div class="salience-chips-wrap">
          ${data.salient_words.map(w => `
            <span class="salience-token ${w.polarity}">
              <span>${escapeHtml(w.word)}</span>
              ${w.is_ironic ? `<span class="ironic-chip-pill">ironic</span>` : ''}
              <span class="salience-weight">${w.importance > 0 ? '+' : ''}${w.importance}</span>
            </span>
          `).join('')}
        </div>
      </div>
    ` : '';

    resultContainer.innerHTML = `
      <div class="results-card-content">
        
        <!-- Dominant Sentiment Hero Card -->
        <div class="dominant-sentiment-banner ${heroClass}">
          <div class="dominant-sentiment-left">
            <div class="dominant-sentiment-badge ${heroClass}">
              ${isPos ? `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              ` : isNeutral ? `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="8" y1="12" x2="16" y2="12"></line>
                </svg>
              ` : `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              `}
            </div>
            <div>
              <h3 class="dominant-title-text ${heroClass}">${labelTitle}</h3>
              <span class="dominant-sub-label">${subLabelText}</span>
            </div>
          </div>

          <div class="dominant-confidence-right">
            <div class="dominant-conf-value ${heroClass}">${data.confidence_pct}%</div>
            <div class="dominant-conf-sub">Confidence</div>
          </div>
        </div>

        <!-- Horizontal Probability Meter -->
        <div class="probability-visualization-box">
          <div class="prob-meter-labels">
            <span style="color:var(--positive);">Positive: ${data.positive_pct}%</span>
            <span style="color:var(--negative);">Negative: ${data.negative_pct}%</span>
          </div>
          <div class="prob-meter-track" role="progressbar" aria-valuenow="${data.positive_pct}" aria-valuemin="0" aria-valuemax="100">
            <div class="prob-meter-fill-pos" style="width: ${data.positive_pct}%;"></div>
            <div class="prob-meter-fill-neg" style="width: ${data.negative_pct}%;"></div>
          </div>
          <div class="prob-meter-ticks">
            <span>0%</span>
            <span>25%</span>
            <span>50%</span>
            <span>75%</span>
            <span>100%</span>
          </div>
        </div>

        <!-- 3 Breakdown Metric Cards -->
        <div class="probability-cards-grid">
          <div class="prob-stat-card pos">
            <span class="prob-stat-label">Positive</span>
            <span class="prob-stat-value">${data.positive_pct}%</span>
          </div>
          <div class="prob-stat-card neutral">
            <span class="prob-stat-label">Ambivalence</span>
            <span class="prob-stat-value">${ambivalencePct}%</span>
          </div>
          <div class="prob-stat-card neg">
            <span class="prob-stat-label">Negative</span>
            <span class="prob-stat-value">${data.negative_pct}%</span>
          </div>
        </div>

        <!-- Natural Language Explanation -->
        <div class="explanation-callout">
          ${explanation}
        </div>

        <!-- Sarcasm & Irony Intelligence Box (if detected) -->
        ${sarcasmHtml}

        <!-- Aspect-Level Dimensional Separation (for Mixed/Ambivalent reviews) -->
        ${aspectMatrixHtml}

        <!-- Emotional Trajectory Arc Timeline -->
        ${arcHtml}

        <!-- Segment Breakdown -->
        ${segmentsHtml}

        <!-- Salience Token Drivers -->
        ${salienceHtml}

        <!-- Telemetry & Hardware Metadata Footer -->
        <div class="telemetry-footer-bar">
          <div class="telemetry-items">
            <span class="telemetry-item">Latency: <strong>${data.time_ms}ms</strong></span>
            <span class="telemetry-item">Tokens: <strong>${data.token_count}</strong></span>
            <span class="telemetry-item">Device: <strong>${data.device}</strong></span>
          </div>
          <button type="button" class="copy-result-btn" id="copy-result-btn">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            <span>Copy</span>
          </button>
        </div>

      </div>
    `;

    document.getElementById('copy-result-btn')?.addEventListener('click', () => {
      const summary = `SENTIMENT.AI Analysis:\nSentiment: ${data.label} (${data.confidence_pct}% confidence)\nPositive: ${data.positive_pct}% | Negative: ${data.negative_pct}%\nLatency: ${data.time_ms}ms (${data.device})`;
      navigator.clipboard.writeText(summary).then(() => {
        showToast('Classification summary copied to clipboard');
      });
    });
  }

  // ── History Management ──
  function updateHistoryCounter() {
    if (historyCounter) {
      historyCounter.textContent = state.history.length;
    }
  }

  function saveToHistory(item) {
    const historyItem = {
      id: Date.now(),
      text: item.text,
      label: item.label,
      confidence_pct: item.confidence_pct,
      positive_pct: item.positive_pct,
      negative_pct: item.negative_pct,
      time_ms: item.time_ms,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    state.history.unshift(historyItem);
    if (state.history.length > 50) state.history.pop();
    localStorage.setItem('sentiment_ai_history', JSON.stringify(state.history));
    updateHistoryCounter();
  }

  function renderHistory() {
    if (!historyList) return;
    updateHistoryCounter();

    if (state.history.length === 0) {
      historyList.innerHTML = `
        <div style="text-align:center; padding: 48px 24px; color:var(--text-muted);">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:12px; color:var(--text-disabled);">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <p style="font-weight:600; color:var(--text-secondary); margin-bottom:4px;">No evaluation history</p>
          <p style="font-size:12px;">Run a single or batch text evaluation to automatically record predictions.</p>
        </div>
      `;
      return;
    }

    historyList.innerHTML = state.history.map(item => `
      <div class="history-card-item">
        <div class="history-main-content">
          <p class="history-text-snippet" title="${escapeHtml(item.text)}">${escapeHtml(item.text)}</p>
          <div class="history-meta-line">
            ${item.timestamp} · Latency ${item.time_ms}ms · Pos ${item.positive_pct}% · Neg ${item.negative_pct}%
          </div>
        </div>
        <div class="history-controls">
          <span class="sentiment-badge ${item.label === 'Positive' ? 'positive' : 'negative'}">
            ${item.label} ${item.confidence_pct}%
          </span>
          <button type="button" class="btn-secondary" style="padding: 4px 10px; font-size: 11px;" onclick="loadHistoryItem('${item.id}')">
            Load
          </button>
        </div>
      </div>
    `).join('');
  }

  window.loadHistoryItem = (id) => {
    const item = state.history.find(h => String(h.id) === String(id));
    if (item) {
      document.querySelector('[data-tab="single"]')?.click();
      if (singleText) {
        singleText.value = item.text;
        updateTextCounts();
        runSinglePrediction();
        showToast('Loaded into text editor');
      }
    }
  };

  clearHistoryBtn?.addEventListener('click', () => {
    window.soundEngine?.playClick();
    state.history = [];
    localStorage.removeItem('sentiment_ai_history');
    renderHistory();
    showToast('Inference history cleared');
  });

  exportHistoryBtn?.addEventListener('click', () => {
    if (state.history.length === 0) {
      showToast('No history records to export', 'warning');
      return;
    }
    const blob = new Blob([JSON.stringify(state.history, null, 2)], { type: 'application/json' });
    downloadBlob(blob, 'sentiment_ai_history.json');
    showToast('Downloaded history as JSON');
  });

  // ── Batch Processing ──
  dropZone?.addEventListener('click', () => batchFile?.click());

  dropZone?.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone?.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone?.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleBatchFileInput(e.dataTransfer.files[0]);
    }
  });

  batchFile?.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleBatchFileInput(e.target.files[0]);
    }
  });

  function handleBatchFileInput(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (batchText) batchText.value = e.target.result;
      showToast(`Loaded ${file.name}`);
      window.soundEngine?.playClick();
    };
    reader.readAsText(file);
  }

  batchAnalyzeBtn?.addEventListener('click', async () => {
    const raw = batchText ? batchText.value.trim() : '';
    if (!raw) {
      showToast('Enter lines of text or upload a file', 'warning');
      return;
    }

    const lines = raw.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
    if (lines.length === 0) {
      showToast('No valid non-empty lines found', 'warning');
      return;
    }

    window.soundEngine?.playClick();
    batchAnalyzeBtn.disabled = true;
    batchAnalyzeBtn.innerHTML = `
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
        <circle cx="12" cy="12" r="10" stroke-opacity="0.25"></circle>
        <path d="M12 2a10 10 0 0 1 10 10"></path>
      </svg>
      <span>Executing Batch...</span>
    `;

    try {
      const response = await fetch('/api/batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texts: lines }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || 'Batch classification failed');
      }

      const data = await response.json();
      state.batchResults = data.results;
      renderBatchResults(data);
      window.soundEngine?.playPositive();
      window.soundEngine?.haptic(40);
      showToast(`Processed ${data.summary.total} texts in ${data.summary.total_time_ms}ms`);
    } catch (err) {
      console.error(err);
      showToast(`Error: ${err.message}`, 'error');
    } finally {
      batchAnalyzeBtn.disabled = false;
      batchAnalyzeBtn.innerHTML = `
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
          <polyline points="2 17 12 22 22 17"></polyline>
          <polyline points="2 12 12 17 22 12"></polyline>
        </svg>
        <span>Execute Batch Analysis</span>
      `;
    }
  });

  function renderBatchResults(data) {
    if (batchResultsWrap) batchResultsWrap.style.display = 'block';

    const sum = data.summary;
    const totalEl = document.getElementById('batch-stat-total');
    const posEl = document.getElementById('batch-stat-pos');
    const negEl = document.getElementById('batch-stat-neg');
    const timeEl = document.getElementById('batch-stat-time');

    if (totalEl) totalEl.textContent = sum.total;
    if (posEl) posEl.textContent = `${sum.positive_count} (${sum.positive_ratio}%)`;
    if (negEl) negEl.textContent = `${sum.negative_count} (${sum.negative_ratio}%)`;
    if (timeEl) timeEl.textContent = `${sum.total_time_ms}ms`;

    renderBatchTable(data.results);
  }

  function renderBatchTable(results) {
    const tableBody = document.getElementById('batch-table-body');
    if (!tableBody) return;

    const filtered = state.batchFilter === 'all'
      ? results
      : results.filter(r => r.label.toLowerCase() === state.batchFilter);

    tableBody.innerHTML = filtered.map(r => `
      <tr>
        <td style="font-family:var(--font-mono); font-size:11px; color:var(--text-muted);">${r.id}</td>
        <td style="color:var(--text-primary); font-size:13px;">${escapeHtml(r.snippet)}</td>
        <td>
          <span class="sentiment-badge ${r.label === 'Positive' ? 'positive' : 'negative'}">
            ${r.label}
          </span>
        </td>
        <td style="font-family:var(--font-mono); font-weight:600; color:var(--text-primary);">${r.confidence_pct}%</td>
        <td style="font-family:var(--font-mono); color:var(--positive);">${r.positive_pct}%</td>
        <td style="font-family:var(--font-mono); color:var(--negative);">${r.negative_pct}%</td>
      </tr>
    `).join('');
  }

  document.querySelectorAll('.batch-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      window.soundEngine?.playClick();
      document.querySelectorAll('.batch-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.batchFilter = btn.dataset.filter;
      renderBatchTable(state.batchResults);
    });
  });

  exportCsvBtn?.addEventListener('click', () => {
    if (state.batchResults.length === 0) return;
    window.soundEngine?.playClick();

    const headers = ['ID', 'Text', 'Sentiment', 'Confidence', 'Positive_Pct', 'Negative_Pct', 'Latency_ms'];
    const rows = state.batchResults.map(r => [
      r.id,
      `"${r.text.replace(/"/g, '""')}"`,
      r.label,
      r.confidence,
      r.positive_pct,
      r.negative_pct,
      r.time_ms,
    ]);

    const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    downloadBlob(blob, 'sentiment_batch_results.csv');
    showToast('Downloaded batch results as CSV');
  });

  // ── Model Insights & Metrics Fetcher ──
  async function fetchModelInsights() {
    try {
      const response = await fetch('/api/model-info');
      if (!response.ok) return;
      const data = await response.json();

      const accEl = document.getElementById('info-accuracy');
      const f1El = document.getElementById('info-f1');
      const precEl = document.getElementById('info-precision');
      const recEl = document.getElementById('info-recall');
      const devEl = document.getElementById('info-device');
      const paramsEl = document.getElementById('info-params');

      if (accEl) accEl.textContent = `${data.metrics.test_accuracy}%`;
      if (f1El) f1El.textContent = `${data.metrics.test_f1}%`;
      if (precEl) precEl.textContent = `${data.metrics.test_precision}%`;
      if (recEl) recEl.textContent = `${data.metrics.test_recall}%`;
      if (devEl) devEl.textContent = data.device;
      if (paramsEl) paramsEl.textContent = data.parameters;

      // Populate Confusion Matrix
      const cm = data.metrics.confusion_matrix;
      if (cm && cm.length === 2) {
        const tn = document.getElementById('cm-tn');
        const fp = document.getElementById('cm-fp');
        const fn = document.getElementById('cm-fn');
        const tp = document.getElementById('cm-tp');
        if (tn) tn.textContent = cm[0][0].toLocaleString();
        if (fp) fp.textContent = cm[0][1].toLocaleString();
        if (fn) fn.textContent = cm[1][0].toLocaleString();
        if (tp) tp.textContent = cm[1][1].toLocaleString();
      }
    } catch (e) {
      console.error('Failed to fetch model insights:', e);
    }
  }

  // ── Helper Utilities ──
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function downloadBlob(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast-item';
    toast.innerHTML = `
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--accent);">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
      <span>${escapeHtml(message)}</span>
    `;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(8px)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, 2600);
  }

  // ── Initial Boot ──
  updateTextCounts();
  updateHistoryCounter();
  fetchModelInsights();
});
