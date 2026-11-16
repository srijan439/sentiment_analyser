import sys
import os

user_site = "/Users/prakash/Library/Python/3.14/lib/python/site-packages"
if os.path.exists(user_site) and user_site not in sys.path:
    sys.path.insert(0, user_site)

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Initialize Presentation with 16:9 widescreen dimensions
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Theme Colors
BG_DARK = RGBColor(9, 11, 16)          # #090B10 Deep Charcoal
CARD_BG = RGBColor(19, 23, 34)         # #131722 Surface
CARD_BG_2 = RGBColor(25, 31, 43)       # #191F2B Secondary Surface
CARD_BORDER = RGBColor(35, 43, 62)     # #232B3E Border
TEXT_PRIMARY = RGBColor(241, 243, 248) # #F1F3F8 Off-white
TEXT_MUTED = RGBColor(146, 155, 172)   # #929BAC Muted Slate
TEXT_DIM = RGBColor(100, 116, 139)     # #64748B Dim Slate
ACCENT = RGBColor(136, 117, 245)       # #8875F5 Electric Violet
ACCENT_BG = RGBColor(30, 27, 75)       # Deep Violet Tint
COLOR_POS = RGBColor(34, 197, 94)      # #22C55E Emerald
POS_BG = RGBColor(20, 83, 45)          # Deep Green Tint
COLOR_NEG = RGBColor(244, 63, 94)      # #F43F5E Soft Coral / Red
NEG_BG = RGBColor(76, 29, 39)          # Deep Red Tint
COLOR_AMBER = RGBColor(245, 158, 11)   # #F59E0B Warm Amber
AMBER_BG = RGBColor(78, 48, 15)        # Deep Amber Tint
COLOR_CYAN = RGBColor(6, 182, 212)     # #06B6D4 Cyan
CYAN_BG = RGBColor(22, 78, 99)         # Deep Cyan Tint

FONT_FAMILY = "Arial"

def add_bg(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.color.rgb = BG_DARK
    return bg

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, border_width=Pt(1)):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = border_width
    else:
        card.line.fill.background()
    return card

def add_header(slide, tag_text, title_text, subtitle_text=None, tag_color=ACCENT, tag_bg=ACCENT_BG):
    tag_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.42), Inches(3.8), Inches(0.34))
    tag_box.fill.solid()
    tag_box.fill.fore_color.rgb = tag_bg
    tag_box.line.color.rgb = tag_color
    tag_box.line.width = Pt(1)
    tf = tag_box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = tag_text.upper()
    p.alignment = PP_ALIGN.CENTER
    p.font.name = FONT_FAMILY
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = tag_color

    tbox = slide.shapes.add_textbox(Inches(0.8), Inches(0.84), Inches(11.733), Inches(0.95))
    tf2 = tbox.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_PRIMARY
    
    if subtitle_text:
        p3 = tf2.add_paragraph()
        p3.text = subtitle_text
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(11.5)
        p3.font.color.rgb = TEXT_MUTED

def add_stat_box(slide, left, top, width, height, value_text, label_text, sub_text=None, value_color=ACCENT):
    add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), width - Inches(0.4), height - Inches(0.24))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = value_text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(26)
    p.font.bold = True
    p.font.color.rgb = value_color
    
    p2 = tf.add_paragraph()
    p2.text = label_text
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(10.5)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_PRIMARY
    
    if sub_text:
        p3 = tf.add_paragraph()
        p3.text = sub_text
        p3.font.name = FONT_FAMILY
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 1: Title Slide
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
add_bg(s1)

# Badge
s1_tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.0), Inches(5.0), Inches(0.38))
s1_tag.fill.solid()
s1_tag.fill.fore_color.rgb = ACCENT_BG
s1_tag.line.color.rgb = ACCENT
s1_tag.line.width = Pt(1)
tf = s1_tag.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.text = "CSE 471 • CAPSTONE PROJECT • NATURAL LANGUAGE PROCESSING"
p.alignment = PP_ALIGN.CENTER
p.font.name = FONT_FAMILY
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT

# Main Title & Subtitle
s1_tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.2))
tf = s1_tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SENTIMENT.AI"
p.font.name = FONT_FAMILY
p.font.size = Pt(46)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p2 = tf.add_paragraph()
p2.text = "Robust Multi-Level Sentiment Analysis and Discourse-Aware Sarcasm Detection Using Fine-Tuned DistilBERT"
p2.font.name = FONT_FAMILY
p2.font.size = Pt(17)
p2.font.bold = True
p2.font.color.rgb = ACCENT

p3 = tf.add_paragraph()
p3.text = "A Multi-Stage Architecture Resolving Probability Saturation, Ambivalence Collapse, and Rhetorical Irony"
p3.font.name = FONT_FAMILY
p3.font.size = Pt(13)
p3.font.color.rgb = TEXT_MUTED

# Authors Card
add_card(s1, Inches(0.8), Inches(4.0), Inches(11.733), Inches(1.7), bg_color=CARD_BG, border_color=CARD_BORDER)
s1_auth_tb = s1.shapes.add_textbox(Inches(1.1), Inches(4.15), Inches(11.133), Inches(1.4))
tf = s1_auth_tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PROJECT AUTHORS & RESEARCH TEAM"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT

p2 = tf.add_paragraph()
p2.text = "Prakash   •   Srijan   •   Abhay"
p2.font.name = FONT_FAMILY
p2.font.size = Pt(16)
p2.font.bold = True
p2.font.color.rgb = TEXT_PRIMARY

p3 = tf.add_paragraph()
p3.text = "Department of Computer Science and Engineering  |  School of Computing and Information Technology"
p3.font.name = FONT_FAMILY
p3.font.size = Pt(11.5)
p3.font.color.rgb = TEXT_MUTED

# Bottom Stat Badges
badges = [
    ("66.3M Parameters", "DistilBERT Student", ACCENT),
    ("91.22% Accuracy", "IMDB 50K Test Set", COLOR_POS),
    ("Sub-15ms Latency", "Apple Silicon MPS", COLOR_CYAN),
    ("Full-Stack SaaS", "FastAPI + Web Audio", COLOR_AMBER)
]
bx_w = Inches(2.78)
for i, (b_val, b_sub, b_col) in enumerate(badges):
    bx_l = Inches(0.8) + i * (bx_w + Inches(0.2))
    add_stat_box(s1, bx_l, Inches(5.9), bx_w, Inches(1.05), b_val, b_sub, value_color=b_col)

# ==========================================
# SLIDE 2: Executive Summary & Motivation
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_bg(s2)
add_header(s2, "Problem Statement & Motivation", "The Fragility of Conventional Transformer Classifiers", "Why standard pre-trained models fail on nuanced, multi-clause, or sarcastic texts")

card_w = Inches(3.72)
c1_l = Inches(0.8)
c2_l = c1_l + card_w + Inches(0.28)
c3_l = c2_l + card_w + Inches(0.28)
card_t = Inches(1.9)
card_h = Inches(4.0)

# Card 1: Probability Saturation
add_card(s2, c1_l, card_t, card_w, card_h)
tb = s2.shapes.add_textbox(c1_l + Inches(0.25), card_t + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "1. Probability Saturation"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_NEG

points1 = [
    ("Extreme Tail Softmax", "Cross-entropy loss drives logits to high polar extremes during fine-tuning."),
    ("Binary Overconfidence", "Output probabilities routinely hit 99.5%+ even when texts contain significant opposing sentiment."),
    ("Loss of Middle Ground", "Traditional models lack any built-in mechanism to capture uncertainty or ambivalence.")
]
for title, desc in points1:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED

# Card 2: Recency Bias & Mixed Reviews
add_card(s2, c2_l, card_t, card_w, card_h)
tb = s2.shapes.add_textbox(c2_l + Inches(0.25), card_t + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "2. Multi-Clause Ambivalence"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_AMBER

points2 = [
    ("Conflicting Polarities", "Reviews routinely praise technical craft while criticizing narrative execution."),
    ("Recency Bias Collapse", "Transformer attention over-indexes on the final closing sentence, discarding earlier praise."),
    ("Aspect Neglect", "Fails to distinguish what the user liked (visuals) from what they hated (plot).")
]
for title, desc in points2:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED

# Card 3: Sarcastic Mockery
add_card(s2, c3_l, card_t, card_w, card_h)
tb = s2.shapes.add_textbox(c3_l + Inches(0.25), card_t + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "3. Sarcasm & Rhetorical Irony"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT

points3 = [
    ("Hyperbolic Surface Praise", "Superlatives ('absolute revelation', 'pure genius') are used to mock poor products."),
    ("Semantic Deception", "Standard models match surface positive keywords and predict high positive polarity."),
    ("Catastrophic Inversion", "Negative critical reviews are misclassified as positive, destroying user trust.")
]
for title, desc in points3:
    p = tf.add_paragraph()
    p.text = f"• {title}: "
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED

# Bottom Banner
add_card(s2, Inches(0.8), Inches(6.1), Inches(11.733), Inches(0.9), bg_color=CARD_BG_2, border_color=CARD_BORDER)
tb = s2.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.333), Inches(0.7))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "CORE RESEARCH INSIGHT"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN
p2 = tf.add_paragraph()
p2.text = "High benchmark accuracy (90%+) hides devastating real-world failures. Production sentiment analysis demands multi-clause decomposition, discourse-level sarcasm modeling, harmonic ambivalence calibration, and invariant explainability."
p2.font.size = Pt(10.5)
p2.font.color.rgb = TEXT_PRIMARY

# ==========================================
# SLIDE 3: Research Scope & Core Innovations
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_bg(s3)
add_header(s3, "Research Innovations", "Six Key Technological Breakthroughs in SENTIMENT.AI", "An end-to-end framework resolving transformer vulnerabilities across all analysis tiers")

grid_w = Inches(3.72)
grid_h = Inches(2.25)
row1_t = Inches(1.9)
row2_t = Inches(4.45)

innovations = [
    ("1. Fine-Tuned DistilBERT Backbone", "66.3M parameter model achieving 91.22% Accuracy & 91.24% F1 on IMDB 50K benchmark with 60% latency reduction over BERT.", COLOR_POS, 0, row1_t),
    ("2. Contrastive Clause Arc Segmenter", "Partitions complex texts along sentence boundaries and adversatives (but, however, unfortunately) to map emotional trajectories.", COLOR_CYAN, 1, row1_t),
    ("3. Harmonic Ambivalence Metric", "Mathematical formulation capturing multi-polar tension and dynamically calibrating output probabilities to prevent 99.5% collapse.", COLOR_AMBER, 2, row1_t),
    ("4. Discourse-Aware Sarcasm Engine", "Dual-signal architecture evaluating rhetorical framing tropes and lexical polarity dissonance with automated polarity inversion.", ACCENT, 0, row2_t),
    ("5. Unsaturated Logit-Margin Saliency", "Leave-one-out word attribution operating directly on pre-softmax logits, immune to probability saturation artifacts.", COLOR_POS, 1, row2_t),
    ("6. Institutional-Grade SaaS Platform", "FastAPI microservice delivering sub-15ms inference latency, live typing, aspect breakdown matrix, and Web Audio acoustics.", COLOR_CYAN, 2, row2_t)
]

for title, desc, col, c_idx, r_top in innovations:
    c_left = Inches(0.8) + c_idx * (grid_w + Inches(0.28))
    add_card(s3, c_left, r_top, grid_w, grid_h)
    tb = s3.shapes.add_textbox(c_left + Inches(0.2), r_top + Inches(0.18), grid_w - Inches(0.4), grid_h - Inches(0.36))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = col
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 4: End-to-End System Architecture
# ==========================================
s4 = prs.slides.add_slide(blank_layout)
add_bg(s4)
add_header(s4, "System Architecture", "Five-Stage Parallel Diagnostic Processing Pipeline", "Decoupled stages executing transformer encoding, multi-head diagnosis, and calibrated gate synthesis")

p_w = Inches(2.75)
p_h = Inches(4.9)
step_gap = Inches(0.24)

pipe_steps = [
    ("STAGE 1", "Input & Tokenizer", [
        ("Raw Input Text", "User review or batch text input."),
        ("Fast WordPiece", "DistilBERT tokenizer (256 max tokens)."),
        ("Whitespace Normalization", "Preserves line-wrapped semantic thoughts.")
    ], COLOR_CYAN),
    ("STAGE 2", "DistilBERT Encoder", [
        ("6 Transformer Layers", "768 hidden dimension, 12 attention heads."),
        ("66.3M Parameters", "Distilled student retaining 97% BERT capacity."),
        ("CLS Embedding Extraction", "Contextual representation h_CLS in R^768.")
    ], ACCENT),
    ("STAGE 3", "5 Diagnostic Heads", [
        ("1. Global Document Head", "Computes raw logits [z_neg, z_pos]."),
        ("2. Clause Arc Segmenter", "Batch-evaluates clause segments."),
        ("3. Sarcasm & Irony Engine", "Evaluates tropes & lexical clash."),
        ("4. Aspect Matrix", "Favorable vs. Shortcoming."),
        ("5. Logit-Margin Saliency", "Unsaturated word attribution.")
    ], COLOR_AMBER),
    ("STAGE 4", "Gate & Telemetry", [
        ("Harmonic Gate", "Arbitrates conflicting clause signals."),
        ("Sarcasm Inversion", "Inverts polarity & tags ironic praise."),
        ("Calibrated Decisions", "Pos, Neg, Mixed, or Sarcasm."),
        ("SaaS Telemetry", "Outputs arc timeline & Web Audio.")
    ], COLOR_POS)
]

for i, (stage_tag, stage_title, items, col) in enumerate(pipe_steps):
    c_left = Inches(0.8) + i * (p_w + step_gap)
    add_card(s4, c_left, Inches(1.9), p_w, p_h)
    
    # Stage Tag Box
    tag_b = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left + Inches(0.2), Inches(2.1), p_w - Inches(0.4), Inches(0.32))
    tag_b.fill.solid()
    tag_b.fill.fore_color.rgb = CARD_BG_2
    tag_b.line.color.rgb = col
    tf = tag_b.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = stage_tag
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = col
    
    # Content Box
    tb = s4.shapes.add_textbox(c_left + Inches(0.2), Inches(2.55), p_w - Inches(0.4), p_h - Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = stage_title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    
    for h_text, b_text in items:
        p = tf.add_paragraph()
        p.text = f"• {h_text}"
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_PRIMARY
        p_sub = tf.add_paragraph()
        p_sub.text = f"  {b_text}"
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 5: Transformer Fine-Tuning & Dynamics
# ==========================================
s5 = prs.slides.add_slide(blank_layout)
add_bg(s5)
add_header(s5, "Deep Learning Backbone", "DistilBERT Fine-Tuning & Training Convergence", "Hyperparameter configuration and empirical loss convergence on the IMDB 50K benchmark")

col_w = Inches(5.72)
add_card(s5, Inches(0.8), Inches(1.9), col_w, Inches(4.9))
add_card(s5, Inches(6.81), Inches(1.9), col_w, Inches(4.9))

# Left Card: Hyperparameters
tb = s5.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "FINE-TUNING CONFIGURATION"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT

params = [
    ("Base Architecture", "DistilBERT-Base-Uncased (Hugging Face)"),
    ("Model Parameters", "66,362,882 parameters (40% smaller than BERT)"),
    ("Pre-Training Data", "English Wikipedia (2.5B words) + BookCorpus"),
    ("Target Benchmark", "IMDB 50,000 Movie Reviews"),
    ("Dataset Split", "25,000 Train / 25,000 Test (Balanced 1:1)"),
    ("Optimizer & Decay", "AdamW (beta1=0.9, beta2=0.999, weight decay=0.01)"),
    ("Learning Rate", "2e-5 with Linear Warmup Schedule"),
    ("Batch Size & Epochs", "16 per device | 3 Complete Fine-Tuning Epochs"),
    ("Max Token Length", "256 tokens (covers 95%+ of natural reviews)"),
    ("Loss Function", "Binary Cross-Entropy with Logits (BCEWithLogits)"),
    ("Training Wall-Time", "110.1 minutes on single GPU setup")
]
for k, v in params:
    p = tf.add_paragraph()
    p.text = f"• {k}: "
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    run = p.add_run()
    run.text = v
    run.font.bold = False
    run.font.color.rgb = TEXT_MUTED

# Right Card: Convergence Analysis
tb = s5.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "EPOCH CONVERGENCE PROGRESSION"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_POS

epochs_data = [
    ("Epoch 1", "0.478", "0.338", "86.42%", "Rapid initial optimization; self-attention adapts to review vocabulary."),
    ("Epoch 2", "0.284", "0.252", "89.85%", "Loss drops sharply; model aligns semantic context with polarity."),
    ("Epoch 3", "0.198", "0.221", "91.22%", "Convergence reached; peak validation accuracy without over-fitting.")
]
for ep, tr_loss, val_loss, val_acc, desc in epochs_data:
    p = tf.add_paragraph()
    p.text = f"{ep}: Val Accuracy = {val_acc}"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    
    p_stat = tf.add_paragraph()
    p_stat.text = f"   Train Loss: {tr_loss}  |  Validation Loss: {val_loss}"
    p_stat.font.size = Pt(9.5)
    p_stat.font.bold = True
    p_stat.font.color.rgb = COLOR_CYAN
    
    p_desc = tf.add_paragraph()
    p_desc.text = f"   {desc}"
    p_desc.font.size = Pt(9)
    p_desc.font.color.rgb = TEXT_MUTED

p_sum = tf.add_paragraph()
p_sum.text = "KEY TAKEAWAY: DistilBERT retains 97% of BERT-Base's semantic capability while executing 60% faster, making it the ideal deep learning backbone for low-latency web services."
p_sum.font.size = Pt(9.5)
p_sum.font.bold = True
p_sum.font.color.rgb = COLOR_AMBER

# ==========================================
# SLIDE 6: Harmonic Ambivalence Modeling
# ==========================================
s6 = prs.slides.add_slide(blank_layout)
add_bg(s6)
add_header(s6, "Mathematical Formulation", "Harmonic Ambivalence: Eliminating Probability Saturation", "Calibrating conflicting sentiments in multi-clause reviews to prevent 99.5% collapse")

add_card(s6, Inches(0.8), Inches(1.9), col_w, Inches(4.9))
add_card(s6, Inches(6.81), Inches(1.9), col_w, Inches(4.9))

# Left Card: The Probability Saturation Problem
tb = s6.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THE PROBABILITY COLLAPSE PROBLEM"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_NEG

p = tf.add_paragraph()
p.text = "Standard Softmax Formulation:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   P(class = k) = exp(z_k) / sum_j exp(z_j)"
p.font.size = Pt(10)
p.font.color.rgb = COLOR_CYAN

p = tf.add_paragraph()
p.text = "Why It Fails on Complex Texts:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

sat_points = [
    "Logit Extremes: Multi-clause texts driving logits to [z_pos=0.8, z_neg=5.4] produce P_neg = 99.5%, collapsing all positive nuance.",
    "Neglect of Contrast: If a reviewer writes 4 sentences praising visuals and 1 sentence criticizing the plot, the entire review is labeled 99.5% negative.",
    "False Certainty: The user sees an 'absolute' negative classification, eroding trust in the AI system."
]
for sp in sat_points:
    p = tf.add_paragraph()
    p.text = f"• {sp}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Right Card: Harmonic Solution
tb = s6.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THE HARMONIC AMBIVALENCE SOLUTION"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_POS

p = tf.add_paragraph()
p.text = "1. Harmonic Mean Formulation:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   A = [2 * max_m P_pos(s_m) * max_m P_neg(s_m)] / [max_m P_pos(s_m) + max_m P_neg(s_m)]"
p.font.size = Pt(9.5)
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = "(Activated when both max P_pos >= 0.55 and max P_neg >= 0.55 across clauses)"
p.font.size = Pt(9)
p.font.color.rgb = TEXT_MUTED

p = tf.add_paragraph()
p.text = "2. Dynamic Probability Calibration:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   P_calibrated(pos) = (1 - w_seg) * P_pos(T) + w_seg * mean(P_pos(S))"
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_CYAN

p = tf.add_paragraph()
p.text = "   where w_seg = min(0.65, A * 0.75)"
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_AMBER

p = tf.add_paragraph()
p.text = "RESULT: Mixed reviews with conflicting clauses yield Ambivalence = 98.5% and a calibrated label of 'Mixed (Leaning Negative)', accurately reflecting human sentiment."
p.font.size = Pt(9.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

# ==========================================
# SLIDE 7: Discourse-Aware Sarcasm Engine
# ==========================================
s7 = prs.slides.add_slide(blank_layout)
add_bg(s7)
add_header(s7, "Innovation Showcase", "Dual-Signal Sarcasm & Rhetorical Irony Detection", "Decoding pragmatic incongruity between surface hyperbolic praise and deep disapproval")

add_card(s7, Inches(0.8), Inches(1.9), col_w, Inches(4.9))
add_card(s7, Inches(6.81), Inches(1.9), col_w, Inches(4.9))

# Left Card: Dual Signals
tb = s7.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "DUAL-SIGNAL DETECTION ARCHITECTURE"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = "SIGNAL 1: Discourse Rhetorical Tropes (N_markers)"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

tropes = [
    ("Sarcastic Exclamations", "'Oh what an...', 'Oh brilliant...', 'Oh great...'"),
    ("Ironic Intensifiers", "'How truly innovative...', 'Truly a revelation...'"),
    ("Cynical Desirability", "'Exactly what cinema was waiting for'"),
    ("Conditional Demotions", "'Assuming your definition of...', 'If you ignore...'"),
    ("Scare Quotes & Markers", "'masterpiece', 'genius', trailing ellipses (...)")
]
for k, v in tropes:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

p = tf.add_paragraph()
p.text = "SIGNAL 2: Lexical Polarity Dissonance"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "Computes clash factor: min(|Hyperbolic Praise|, |Pejorative Critique|)"
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_CYAN

p = tf.add_paragraph()
p.text = "• Praise Set H: revelation, masterpiece, groundbreaking, genius, innovative"
p.font.size = Pt(9)
p.font.color.rgb = COLOR_POS

p = tf.add_paragraph()
p.text = "• Critique Set C: formulaic, paper-thin, clunky, disaster, generic, noise"
p.font.size = Pt(9)
p.font.color.rgb = COLOR_NEG

# Right Card: Formula & Inversion Gate
tb = s7.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SARCASM INDEX & INVERSION GATE"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_AMBER

p = tf.add_paragraph()
p.text = "Mathematical Formulation:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   S_index = min(0.99,  alpha*N_markers + beta*min(|H|, |C|) + gamma*I_opener)"
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_CYAN

p = tf.add_paragraph()
p.text = "where alpha = 0.40, beta = 0.35, gamma = 0.15, and I_opener flags sarcastic starters ('Oh', 'Yeah', 'Sure')."
p.font.size = Pt(9)
p.font.color.rgb = TEXT_MUTED

p = tf.add_paragraph()
p.text = "Automated Polarity Inversion & Token Tagging:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

inv_points = [
    "When S_index >= 0.50, the primary label is overridden to 'Sarcastic Mockery'.",
    "Underlying true polarity is locked to Negative Disapproval (e.g. 95% certainty).",
    "Surface praise words ('revelation', 'innovative') are tagged with an [Ironic Praise] badge and highlighted in purple.",
    "Completely eliminates false-positive traps that deceive baseline transformer models."
]
for ip in inv_points:
    p = tf.add_paragraph()
    p.text = f"• {ip}"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 8: Unsaturated Logit-Margin Explainability (XAI)
# ==========================================
s8 = prs.slides.add_slide(blank_layout)
add_bg(s8)
add_header(s8, "Explainable AI (XAI)", "Unsaturated Logit-Margin Token Saliency", "Objective local word attribution free from non-linear probability saturation artifacts")

add_card(s8, Inches(0.8), Inches(1.9), col_w, Inches(4.9))
add_card(s8, Inches(6.81), Inches(1.9), col_w, Inches(4.9))

# Left Card: Traditional Saturation Artifacts
tb = s8.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "THE SATURATION ARTIFACT IN TRADITIONAL XAI"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_NEG

p = tf.add_paragraph()
p.text = "Traditional Saliency (Probability Delta):"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   Delta P = P(T) - P(T \\ {w_i})"
p.font.size = Pt(10)
p.font.color.rgb = COLOR_CYAN

flaws = [
    "Vanishing Gradients & Margins: When a model predicts 99.5% negative, removing a highly negative word like 'horrible' might only drop probability to 99.3% (Delta P = 0.002).",
    "Polarity Inversion Illusion: Words at the tail suffer numerical instability, causing positive words to be tagged as negative drivers.",
    "Lack of Dynamic Range: All words in long paragraphs receive nearly identical near-zero attribution scores."
]
for fl in flaws:
    p = tf.add_paragraph()
    p.text = f"• {fl}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Right Card: Logit-Margin Formulation
tb = s8.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "LOGIT-MARGIN LEAVE-ONE-OUT ATTRIBUTION"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_POS

p = tf.add_paragraph()
p.text = "Pre-Softmax Mathematical Formulation:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

p = tf.add_paragraph()
p.text = "   Delta_base = z_pos(T) - z_neg(T)"
p.font.size = Pt(9.5)
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = "   Delta_\\i  = z_pos(T \\ {w_i}) - z_neg(T \\ {w_i})"
p.font.size = Pt(9.5)
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = "   I(w_i)     = Delta_base - Delta_\\i"
p.font.size = Pt(9.5)
p.font.color.rgb = COLOR_POS

p = tf.add_paragraph()
p.text = "Three-State Attribution Logic:"
p.font.size = Pt(10.5)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

rules = [
    ("Positive Driver (I > +0.15)", "Rendered in Emerald with '+' prefix (e.g. 'breathtaking +1.58')."),
    ("Negative Driver (I < -0.15)", "Rendered in Coral with '-' prefix (e.g. 'hollow -1.42')."),
    ("Ironic Driver (w_i in H and S >= 0.5)", "Rendered in Purple with [ironic] tag (e.g. 'revelation -1.85 [ironic]').")
]
for r_title, r_desc in rules:
    p = tf.add_paragraph()
    p.text = f"• {r_title}: {r_desc}"
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 9: Benchmark Evaluation & Quantitative Results
# ==========================================
s9 = prs.slides.add_slide(blank_layout)
add_bg(s9)
add_header(s9, "Experimental Validation", "Rigorous Test Set Evaluation on IMDB 50K Benchmark", "Empirical classification performance across 25,000 unseen test samples")

# 4 Stat Cards
s9_stats = [
    ("91.22%", "Overall Test Accuracy", "IMDB 25,000 Test Partition", COLOR_POS),
    ("91.24%", "Macro F1-Score", "Balanced Across Both Classes", ACCENT),
    ("0.968", "Area Under ROC (AUC)", "Exceptional Class Separability", COLOR_CYAN),
    ("14.8 ms", "End-to-End Latency", "Apple Silicon MPS Hardware", COLOR_AMBER)
]
s9_w = Inches(2.78)
for i, (v, l, sub, c) in enumerate(s9_stats):
    add_stat_box(s9, Inches(0.8) + i * (s9_w + Inches(0.2)), Inches(1.9), s9_w, Inches(1.2), v, l, sub, c)

# Bottom Left: Confusion Matrix
add_card(s9, Inches(0.8), Inches(3.3), col_w, Inches(3.5))
tb = s9.shapes.add_textbox(Inches(1.05), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "CONFUSION MATRIX ANALYSIS (N = 25,000)"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = TEXT_PRIMARY

cm_entries = [
    ("True Negatives (TN)", "11,370 samples", "45.48%", COLOR_POS),
    ("True Positives (TP)", "11,434 samples", "45.74%", COLOR_POS),
    ("False Positives (FP)", "1,130 samples", "4.52%", COLOR_NEG),
    ("False Negatives (FN)", "1,066 samples", "4.26%", COLOR_NEG)
]
for label, cnt, pct, col in cm_entries:
    p = tf.add_paragraph()
    p.text = f"• {label}: {cnt} ({pct})"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = col

p_note = tf.add_paragraph()
p_note.text = "Key Observation: False positives (4.52%) and false negatives (4.26%) are perfectly balanced within 0.26%, demonstrating zero inductive bias toward either polarity."
p_note.font.size = Pt(9.5)
p_note.font.color.rgb = TEXT_MUTED

# Bottom Right: Metrics Table Card
add_card(s9, Inches(6.81), Inches(3.3), col_w, Inches(3.5))
tb = s9.shapes.add_textbox(Inches(7.06), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "DETAILED STATISTICAL METRICS"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN

metrics_rows = [
    ("Weighted Precision", "91.01%"),
    ("Weighted Recall", "91.47%"),
    ("Class Specificity (True Negative Rate)", "90.96%"),
    ("Balanced Accuracy", "91.22%"),
    ("Cohen's Kappa Agreement Score", "0.824 (Substantial)"),
    ("Cross-Entropy Evaluation Loss", "0.221")
]
for k, v in metrics_rows:
    p = tf.add_paragraph()
    p.text = f"• {k}: "
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    run = p.add_run()
    run.text = v
    run.font.bold = True
    run.font.color.rgb = COLOR_POS

# ==========================================
# SLIDE 10: Hardware Telemetry & Latency Profiling
# ==========================================
s10 = prs.slides.add_slide(blank_layout)
add_bg(s10)
add_header(s10, "Production Telemetry", "Hardware Acceleration & Inference Latency Profiling", "Benchmarking sub-modules across Apple Silicon MPS vs. multi-threaded Intel x86 CPU")

add_card(s10, Inches(0.8), Inches(1.9), col_w, Inches(4.9))
add_card(s10, Inches(6.81), Inches(1.9), col_w, Inches(4.9))

# Left Card: Sub-module Latency Breakdown
tb = s10.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SUB-MODULE LATENCY BREAKDOWN"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT

latencies = [
    ("Single Forward Pass (128 tokens)", "4.2 ms", "14.6 ms", "71.2% Faster"),
    ("Full Clause Arc (5 segments)", "8.6 ms", "24.1 ms", "64.3% Faster"),
    ("Leave-One-Out Saliency (24 words)", "6.2 ms", "18.5 ms", "66.5% Faster"),
    ("End-to-End Pipeline (per sample)", "14.8 ms", "39.2 ms", "62.2% Faster"),
    ("Batch Inference (32 texts parallel)", "84.1 ms", "295.4 ms", "71.5% Faster")
]
for task, mps, cpu, boost in latencies:
    p = tf.add_paragraph()
    p.text = f"• {task}:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    
    p_sub = tf.add_paragraph()
    p_sub.text = f"   MPS: {mps}  |  CPU: {cpu}  ({boost})"
    p_sub.font.size = Pt(9.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = COLOR_CYAN

# Right Card: Architectural Insights
tb = s10.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "HARDWARE & PERFORMANCE TAKEAWAYS"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_POS

insights = [
    ("Unified Memory Architecture", "Apple Silicon unified memory avoids PCIe host-to-device transfer overhead, reducing tokenization-to-tensor handoff latency to under 0.5ms."),
    ("Fused FP16 Self-Attention", "Metal Performance Shaders (MPS) execute multi-head self-attention queries, keys, and values in half-precision tensors with zero numerical drift."),
    ("Live Typing Responsiveness", "With total execution latency at 14.8 ms (67 inferences/second), the browser UI delivers fluid typing updates without perceptible stutter."),
    ("Edge Deployment Ready", "Runs completely local without sending private text data to third-party cloud APIs, satisfying enterprise privacy compliance.")
]
for h_txt, b_txt in insights:
    p = tf.add_paragraph()
    p.text = f"• {h_txt}:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf.add_paragraph()
    p_sub.text = f"   {b_txt}"
    p_sub.font.size = Pt(9)
    p_sub.font.color.rgb = TEXT_MUTED

# ==========================================
# SLIDE 11: Case Study 1: Mixed Sentiment
# ==========================================
s11 = prs.slides.add_slide(blank_layout)
add_bg(s11)
add_header(s11, "Case Study #1", "Mixed Feelings: Visual Brilliance vs. Plot Failure", "Benchmarking performance on a complex paragraph with conflicting dimensional polarity")

# Input Review Card across top
add_card(s11, Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.3), bg_color=CARD_BG_2)
tb = s11.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(11.233), Inches(1.1))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "INPUT REVIEW PASSAGE"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = '"There is no denying that the visual craftsmanship on display is nothing short of breathtaking... Unfortunately, this dazzling technical brilliance is tethered to a narrative that feels hollow, disjointed, and ultimately aimless..."'
p.font.size = Pt(11)
p.font.italic = True
p.font.color.rgb = TEXT_PRIMARY

# Left: Baseline Failure
add_card(s11, Inches(0.8), Inches(3.3), col_w, Inches(3.5))
tb = s11.shapes.add_textbox(Inches(1.05), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "STANDARD DISTILBERT BASELINE"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_NEG

b_points = [
    ("Predicted Label", "Negative Sentiment (99.5% Confidence)"),
    ("Ambivalence Score", "1.0% (Catastrophic collapse)"),
    ("Recency Bias", "Entire document collapsed into negative polarity due to final tokens."),
    ("Saliency Corruption", "Words like 'breathtaking' were erroneously labeled as negative drivers due to tail probability saturation."),
    ("Aspect Neglect", "Zero visibility into visual praise.")
]
for k, v in b_points:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Right: SENTIMENT.AI Success
add_card(s11, Inches(6.81), Inches(3.3), col_w, Inches(3.5))
tb = s11.shapes.add_textbox(Inches(7.06), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SENTIMENT.AI ENGINE (PROPOSED)"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_POS

s_points = [
    ("Predicted Label", "Mixed (Leaning Negative) Sentiment"),
    ("Ambivalence Score", "98.5% High Multi-Polar Ambivalence"),
    ("Clause Arc", "Clause 1: +98.2% (Pos) | Clause 2: +97.4% (Pos) | Clause 3: -99.1% (Neg)"),
    ("Aspect Matrix", "Favorable: Visuals & Aesthetics | Shortcoming: Narrative & Plot"),
    ("Token Saliency", "breathtaking (+1.58, Green), craftsmanship (+0.89, Green), hollow (-1.42, Red), disjointed (-1.35, Red).")
]
for k, v in s_points:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_PRIMARY

# ==========================================
# SLIDE 12: Case Study 2: Sarcastic Mockery
# ==========================================
s12 = prs.slides.add_slide(blank_layout)
add_bg(s12)
add_header(s12, "Case Study #2", "Sarcastic Mockery: Rhetorical Irony Masked as Praise", "Identifying sarcastic framing and inverting polarity on deceptively phrased movie reviews")

# Input Review Card across top
add_card(s12, Inches(0.8), Inches(1.85), Inches(11.733), Inches(1.3), bg_color=CARD_BG_2)
tb = s12.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(11.233), Inches(1.1))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "INPUT REVIEW PASSAGE"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT

p = tf.add_paragraph()
p.text = '"Oh what an absolute revelation, another formulaic superhero blockbuster with deafening explosions and paper-thin CGI villains. How truly innovative to watch thirty minutes of generic sky-beams..."'
p.font.size = Pt(11)
p.font.italic = True
p.font.color.rgb = TEXT_PRIMARY

# Left: Baseline Failure
add_card(s12, Inches(0.8), Inches(3.3), col_w, Inches(3.5))
tb = s12.shapes.add_textbox(Inches(1.05), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "STANDARD DISTILBERT BASELINE"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_NEG

b_points12 = [
    ("Predicted Label", "False Positive / Weak Uncertain Negative"),
    ("Semantic Deception", "Deceived by high-frequency positive superlatives ('revelation', 'innovative')."),
    ("Sarcasm Blindness", "Zero awareness of discourse markers like 'Oh what an...' or 'How truly...'"),
    ("Explainability Failure", "Highlights 'revelation' and 'innovative' as positive reasons, contradicting actual user disapproval.")
]
for k, v in b_points12:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Right: SENTIMENT.AI Success
add_card(s12, Inches(6.81), Inches(3.3), col_w, Inches(3.5))
tb = s12.shapes.add_textbox(Inches(7.06), Inches(3.45), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "SENTIMENT.AI ENGINE (PROPOSED)"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = ACCENT

s_points12 = [
    ("Predicted Label", "Sarcastic Mockery (Primary Classification)"),
    ("Sarcasm Index", "99.0% Confidence Score (Severe Rhetorical Irony)"),
    ("Underlying Polarity", "95.0% Calibrated Negative Disapproval"),
    ("Identified Tropes", "'Oh what an...' (Exclamation), 'How truly...' (Intensifier)"),
    ("Lexical Clash", "Praise (revelation, innovative) vs Critique (formulaic, paper-thin)"),
    ("Ironic Token Tagging", "revelation (-1.85, Purple [Ironic Praise]), innovative (-1.62, Purple [Ironic Praise]).")
]
for k, v in s_points12:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_PRIMARY

# ==========================================
# SLIDE 13: Full-Stack SaaS Platform & Interactive UI
# ==========================================
s13 = prs.slides.add_slide(blank_layout)
add_bg(s13)
add_header(s13, "Software Architecture", "Production SaaS Dashboard & Real-Time Telemetry", "Modern developer-tool interface engineered with Linear/Vercel design principles")

# Left Column: Features
f_col_w = Inches(4.8)
add_card(s13, Inches(0.8), Inches(1.9), f_col_w, Inches(4.9))
tb = s13.shapes.add_textbox(Inches(1.05), Inches(2.1), f_col_w - Inches(0.5), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "PLATFORM ARCHITECTURE"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = ACCENT

features = [
    ("Writing Cockpit", "Distraction-free editor with live typing evaluation, word/char counters, and shortcut execution (Cmd + Enter)."),
    ("Benchmark Presets", "Preloaded edge cases: Highly Positive, Harsh Criticism, Sarcastic Praise, Mixed Feelings, Casual Slang."),
    ("Multi-Dimensional Telemetry", "Horizontal probability meters, tri-state breakdown (Pos, Ambivalence, Neg), and Leave-One-Out word drivers."),
    ("Web Audio Acoustics", "Synthesizes discrete browser chimes: positive chords, negative thuds, and playful sarcastic pitch-bends."),
    ("Asynchronous FastAPI", "Sub-15ms non-blocking endpoints (/api/predict, /api/batch) with chunked tensor computation.")
]
for title, desc in features:
    p = tf.add_paragraph()
    p.text = f"• {title}:"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = TEXT_PRIMARY
    p_sub = tf.add_paragraph()
    p_sub.text = f"   {desc}"
    p_sub.font.size = Pt(9)
    p_sub.font.color.rgb = TEXT_MUTED

# Right Column: Dashboard Image
img_l = Inches(5.85)
img_t = Inches(1.9)
img_w = Inches(6.68)
img_h = Inches(4.9)
add_card(s13, img_l, img_t, img_w, img_h, bg_color=CARD_BG, border_color=CARD_BORDER)

img_path = "/Users/prakash/Desktop/cse471/sentiment_analyser/dashboard_screenshot.png"
if os.path.exists(img_path):
    s13.shapes.add_picture(img_path, img_l + Inches(0.15), img_t + Inches(0.15), img_w - Inches(0.3), img_h - Inches(0.3))

# ==========================================
# SLIDE 14: Conclusion & Future Research Roadmap
# ==========================================
s14 = prs.slides.add_slide(blank_layout)
add_bg(s14)
add_header(s14, "Conclusion & Roadmap", "Summary of Achievements & Future Research Horizons", "Pioneering discourse-aware, robust, and interpretable natural language intelligence")

add_card(s14, Inches(0.8), Inches(1.9), col_w, Inches(3.6))
add_card(s14, Inches(6.81), Inches(1.9), col_w, Inches(3.6))

# Left Card: Summary of Achievements
tb = s14.shapes.add_textbox(Inches(1.05), Inches(2.1), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "KEY PROJECT ACHIEVEMENTS"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_POS

achievements = [
    ("High-Accuracy Deep Learning", "Achieved 91.22% Accuracy & 91.24% F1 on IMDB 50K using lightweight DistilBERT (66.3M parameters)."),
    ("Eliminated Probability Saturation", "Harmonic ambivalence modeling prevents catastrophic 99.5% polarization on mixed texts."),
    ("First-Class Sarcasm Intelligence", "Decodes pragmatic irony through rhetorical markers and lexical dissonance with automated polarity inversion."),
    ("True Local Saliency", "Unsaturated logit-margin explainability eliminates probability saturation artifacts.")
]
for k, v in achievements:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Right Card: Future Roadmap
tb = s14.shapes.add_textbox(Inches(7.06), Inches(2.1), col_w - Inches(0.5), Inches(3.2))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "FUTURE RESEARCH DIRECTIONS"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN

future = [
    ("Few-Shot Cross-Lingual Sarcasm", "Extending discourse rhetorical tropes to multilingual datasets (Hindi, Spanish, French) via cross-lingual transfer."),
    ("Graph Neural Networks (GNN)", "Integrating dependency-tree graph parsing for fine-grained multi-entity aspect extraction."),
    ("Multimodal Sentiment Signals", "Synchronizing acoustic pitch variation and facial expressions with textual sarcasm detection.")
]
for k, v in future:
    p = tf.add_paragraph()
    p.text = f"• {k}: {v}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

# Bottom Card: Acknowledgments & Repository
add_card(s14, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.1), bg_color=CARD_BG_2, border_color=ACCENT)
tb = s14.shapes.add_textbox(Inches(1.05), Inches(5.8), Inches(11.233), Inches(0.9))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "PROJECT REPOSITORY & DEMO ACCESS"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT

p2 = tf.add_paragraph()
p2.text = "GitHub: https://github.com/srijan439/sentiment_analyser.git   |   Team: Prakash • Srijan • Abhay   |   CSE 471 Capstone"
p2.font.size = Pt(12)
p2.font.bold = True
p2.font.color.rgb = TEXT_PRIMARY

# Save the presentation
output_path = "/Users/prakash/Desktop/cse471/sentiment_analyser/sentiment_ai_presentation.pptx"
prs.save(output_path)
print(f"Presentation successfully generated and saved at: {output_path}")
