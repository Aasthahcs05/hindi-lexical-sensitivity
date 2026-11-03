import os, sys, re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        print(f"Total pages rendered: {num_pages}")
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Suppress headers/footers on page 1 (cover) if desired, or show clean header
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 11 * inch - 36, "Research Context & Claude Master Review Brief | Beyond Tokenization (Devanagari Hindi MLMs)")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)
        
        # Footer
        footer_text = f"Authoritative Project Reference & Evidence Brief  |  Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 30, footer_text)
        self.drawString(54, 30, "GitHub: Aasthahcs05/hindi-lexical-sensitivity (main)")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 42, 8.5 * inch - 54, 42)
        
        self.restoreState()

def build_brief_pdf():
    pdf_filename = "Research_Context_and_Claude_Brief_Updated.pdf"
    print(f"Generating master brief PDF: {pdf_filename}...")
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0f172a")    # Slate 900
    c_navy = colors.HexColor("#1e3a8a")       # Blue 900
    c_accent = colors.HexColor("#2563eb")     # Blue 600
    c_text = colors.HexColor("#334155")       # Slate 700
    c_bg_light = colors.HexColor("#f8fafc")   # Slate 50
    c_callout_bg = colors.HexColor("#eff6ff") # Blue 50
    c_callout_border = colors.HexColor("#3b82f6") # Blue 500
    c_warn_bg = colors.HexColor("#fefce8")    # Amber 50
    c_warn_border = colors.HexColor("#eab308")# Amber 500
    c_success_bg = colors.HexColor("#f0fdf4") # Green 50
    c_success_border = colors.HexColor("#22c55e") # Green 500
    
    # Paragraph Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_navy,
        spaceAfter=4,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_navy,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_text,
        spaceAfter=5
    )
    
    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_text,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    callout_text_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=0
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_text,
        alignment=0
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=c_primary,
        alignment=0
    )
    
    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=c_navy,
        alignment=1,
        spaceBefore=3,
        spaceAfter=8
    )

    story = []
    
    # -------------------------------------------------------------------------
    # COVER / HEADER BLOCK
    # -------------------------------------------------------------------------
    story.append(Paragraph("RESEARCH CONTEXT & CLAUDE MASTER REVIEW BRIEF", title_style))
    story.append(Paragraph("A Complete, Verified Handoff Document for Academic Paper Writing and Comprehensive Review<br/><b>Paper Title:</b> <i>Beyond Tokenization: Spelling Perturbations, Explanation Stability and Faithfulness in Devanagari Hindi Masked Language Models</i>", subtitle_style))
    
    # Executive Metadata Table
    meta_data = [
        [Paragraph("<b>DATASET SCOPE</b>", table_header_style), Paragraph("<b>MODELS & SETUP</b>", table_header_style)],
        [
            Paragraph("• <b>Primary Benchmark:</b> 1,679 accepted pairs (3,358 evaluations)<br/>• <b>Template Sensitivity:</b> 1,957 pairs (3,914 evaluations)<br/>• <b>Auxiliary Multiword:</b> 12 pairs (24 evaluations)<br/>• <b>Historical Pilot:</b> 200 pairs (archived baseline)", table_cell_style),
            Paragraph("• <b>MuRIL:</b> <code>google/muril-base-cased</code> (WordPiece, 197k vocab)<br/>• <b>XLM-RoBERTa:</b> <code>FacebookAI/xlm-roberta-base</code> (BPE, 250k vocab)<br/>• <b>Zero-Shot Inference:</b> Pretrained, frozen weights, evaluation mode<br/>• <b>Explainability:</b> Layer-11 Attention & Integrated Gradients (M=20)", table_cell_style)
        ],
        [Paragraph("<b>COMPLETED & VERIFIED EXPERIMENTS</b>", table_header_style), Paragraph("<b>REPOSITORY & SOURCE OF TRUTH</b>", table_header_style)],
        [
            Paragraph("• Stage 1 Curation & 2,000-row reconciliation<br/>• Stage 2 Subword tokenization & alignment dynamics<br/>• Stage 3 PLL scoring & MeanLogP length-normalization<br/>• Stage 4 Attribution (Attention vs Integrated Gradients)", table_cell_style),
            Paragraph("• Stage 5 Explanation Stability (Visible-Target Protocol)<br/>• Stage 6 Faithfulness Interventions (2,010 sentences, 10/20/30% masking)<br/>• Stage 7 Stability–Faithfulness Decoupling (RQ5 resolved)<br/>• <b>GitHub:</b> <code>Aasthahcs05/hindi-lexical-sensitivity</code> (main)", table_cell_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[3.5*inch, 3.5*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('BACKGROUND', (0,2), (-1,2), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))
    
    # Status Banner Callout
    banner_p = Paragraph(
        "<b>AUTHORITATIVE STATUS NOTE:</b> This document completely supersedes the preliminary brief PDF (where sample size was listed as 1,980 and Stages 5 & 6 were marked 'pending'). In the current audited repository (<code>Aasthahcs05/hindi-lexical-sensitivity</code>), <b>all experimental stages (Stages 1 through 7) are 100% completed, statistically audited, verified against canonical CSVs, and synchronized</b>. All five paper tables, all eight publication figures, and the research manuscript reflect the verified Primary Benchmark ($N=1,679$).",
        callout_text_style
    )
    t_banner = Table([[banner_p]], colWidths=[7.0*inch])
    t_banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_success_bg),
        ('BOX', (0,0), (-1,-1), 1.0, c_success_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_banner)
    story.append(Spacer(1, 8))
    
    # -------------------------------------------------------------------------
    # 1. EXECUTIVE RESEARCH OVERVIEW & PREMISE
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Executive Research Overview", h1_style))
    story.append(Paragraph(
        "This study provides the first systematic empirical investigation into how lexical contrasts, semantic synonyms, and authentic spelling variations in <b>Devanagari Hindi</b> affect subword tokenization, masked language model scoring, and the reliability of model explanations. Devanagari is an abugida script structured into syllables (<i>aksharas</i>), vowel diacritics (<i>matras</i>), and ligature conjuncts. Small orthographic variations break syllabic boundaries, causing canonical subword entries to fracture into tiny fragments.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Central Experimental Sequence:</b><br/>"
        "Lexical / Spelling Perturbation &rarr; Subword Fragmentation &rarr; Contextual Predictability (PLL) &rarr; Feature Attribution Generation (Attention & Integrated Gradients) &rarr; Explanation Stability (Visible-Target Protocol) &rarr; Explanation Faithfulness (Erasure Interventions) &rarr; <b>Stability–Faithfulness Decoupling (The Core Finding)</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Core Explainability Dilemma:</b> In XAI literature, explanation stability (invariance under noise) is frequently assumed to imply explanation quality or faithfulness. We rigorously test this assumption in Hindi MLMs and discover that <b>stability is empirically decoupled from, and can even negatively correlate with, causal faithfulness</b>.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------------------
    # 2. RESEARCH QUESTIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Research Questions (RQ1 – RQ5)", h1_style))
    rq_items = [
        "<b>RQ1 (Subword Fragmentation):</b> How do spelling errors, synonyms, and context substitutions affect target-word subword fertility in MuRIL and XLM-RoBERTa?",
        "<b>RQ2 (Model Plausibility / Scoring):</b> To what extent do lexical perturbations degrade target pseudo-log-likelihood (PLL / MeanLogP)?",
        "<b>RQ3 (Cross-Model Concordance):</b> How consistently do MuRIL (Indic-specialized) and XLM-R (general multilingual) agree on directional preference across perturbation types?",
        "<b>RQ4 (Stability & Faithfulness):</b> How stable are Attention and Integrated Gradients explanations across spelling variations, and do highlighted context tokens causally govern predictions under erasure?",
        "<b>RQ5 (Decoupling Relationship):</b> Does explanation stability predict or correlate with explanation faithfulness, or are they orthogonal?"
    ]
    for rq in rq_items:
        story.append(Paragraph(f"• {rq}", bullet_style))
    story.append(Spacer(1, 6))

    # -------------------------------------------------------------------------
    # 3. DATASET ACCOUNTING & RECONCILIATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Dataset Accounting & Reconciliation (2,000 Candidate Rows)", h1_style))
    story.append(Paragraph(
        "The project underwent an exhaustive 2,000-row linguistic and cryptographic audit (<code>data/final/COMPLETE_2000_ROW_RECONCILIATION.csv</code>). The preliminary 1,980 count from earlier drafts was reconciled to remove 16 strict duplicates, 15 malformed entries, and to cleanly isolate synthetic template repetitions:",
        body_style
    ))
    
    ds_table_data = [
        [Paragraph("<b>Cohort / Dataset Name</b>", table_header_style), Paragraph("<b>Sample Size</b>", table_header_style), Paragraph("<b>Composition / Category Breakdown</b>", table_header_style), Paragraph("<b>Primary Scientific Use</b>", table_header_style)],
        [
            Paragraph("<b>Primary Adjudicated Benchmark</b>", table_cell_bold),
            Paragraph("<b>N = 1,679</b>", table_cell_bold),
            Paragraph("Spelling: 1,005 (59.9%)<br/>Synonym: 362 (21.6%)<br/>Valid Context: 312 (18.6%)", table_cell_style),
            Paragraph("<b>Gold-standard benchmark</b> used for all primary paper tables, figures, and hypothesis tests.", table_cell_style)
        ],
        [
            Paragraph("<b>Template Sensitivity Benchmark</b>", table_cell_bold),
            Paragraph("N = 1,957", table_cell_style),
            Paragraph("Spelling: 1,260<br/>Synonym: 385<br/>Valid Context: 312", table_cell_style),
            Paragraph("Includes 278 template variants across 278 syntactic frames to test template invariance.", table_cell_style)
        ],
        [
            Paragraph("<b>Auxiliary Multiword Probe</b>", table_cell_bold),
            Paragraph("N = 12", table_cell_style),
            Paragraph("Synonym: 8, Context: 3, Spelling: 1", table_cell_style),
            Paragraph("Isolated probe for multi-token target spans and grammatical agreement edge cases.", table_cell_style)
        ],
        [
            Paragraph("<b>Excluded Candidate Rows</b>", table_cell_bold),
            Paragraph("N = 31", table_cell_style),
            Paragraph("16 strict duplicate pairs<br/>15 malformed / empty rows", table_cell_style),
            Paragraph("Excluded from all experiments to preserve statistical validity.", table_cell_style)
        ],
        [
            Paragraph("<b>Historical Preliminary Pilot</b>", table_cell_bold),
            Paragraph("N = 200", table_cell_style),
            Paragraph("Context: 142, Synonym: 38, Spelling: 20", table_cell_style),
            Paragraph("Preserved in <code>results/runs/historical_pilot_200/</code> as historical baseline.", table_cell_style)
        ]
    ]
    t_ds = Table(ds_table_data, colWidths=[1.8*inch, 0.9*inch, 2.1*inch, 2.2*inch])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), c_bg_light),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 4. EXPERIMENTAL PIPELINE & METHODOLOGICAL INNOVATIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Experimental Pipeline & Methodological Breakthroughs", h1_style))
    pipeline_points = [
        "<b>Stage 1 (Curation & Offset Mapping):</b> Exact target-span character offsets mapped to tokenizer subwords across all 3,358 sentences with 100% alignment success.",
        "<b>Stage 2 (Tokenization Dynamics):</b> Measures fertility and single-subword collapse. Spelling noise fractures words into smaller subwords.",
        "<b>Stage 3 (Pseudo-Log-Likelihood):</b> Evaluates bidirectional contextual predictability. Uses length-normalized <code>MeanLogP = (1/|S|) &sum; log P(w_t | S_{\\t})</code> to eliminate sentence length confounding. Raw cross-model PLL comparisons are explicitly forbidden.",
        "<b>Stage 4 (Feature Attribution):</b> Compares two distinct paradigms: (1) <i>Final-Layer Self-Attention (Layer 11)</i> averaged across heads, and (2) <i>Layer Integrated Gradients (M=20 Riemann steps)</i> from zero-embedding baseline.",
        "<b>Stage 5 (The Masked-Target Artifact & Visible-Target Protocol):</b> A crucial discovery. Masking target tokens during stability checks produces trivial, artificial stability (&rho; &approx; 1.0) because contexts become identical. We introduced the <b>Visible-Target Protocol</b>, keeping target spellings visible to measure true attribution shifts.",
        "<b>Stage 6 (Faithfulness Context Erasure):</b> Measures causal impact by erasing top-k, bottom-k, and random-k context tokens across budgets f &isin; {0.10, 0.20, 0.30} on 2,010 sentences. Target remains visible during context erasure.",
        "<b>Stage 7 (Decoupling Analysis / RQ5):</b> Correlates pair-level stability with faithfulness gap. Disproves the assumption that stable explanations are faithful."
    ]
    for p in pipeline_points:
        story.append(Paragraph(f"• {p}", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 5. THE FIVE CANONICAL PAPER TABLES
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Authoritative Quantitative Result Tables", h1_style))
    story.append(Paragraph(
        "These five tables represent the verified numerical ground truth across all 1,679 primary benchmark pairs and 1,005 spelling pairs, updated and synchronized directly from <code>results/runs/scaleup_rerun/</code>:",
        body_style
    ))
    
    # Table 1: Tokenization
    story.append(Paragraph("<b>Table 1: Single-Subword Coverage for Spelling Pairs (N = 1,005 pairs)</b>", h2_style))
    t1_data = [
        [Paragraph("<b>Model</b>", table_header_style), Paragraph("<b>Original Coverage</b>", table_header_style), Paragraph("<b>Perturbed Coverage</b>", table_header_style), Paragraph("<b>Change (pp)</b>", table_header_style), Paragraph("<b>Mean Subwords (Orig &rarr; Pert)</b>", table_header_style)],
        [Paragraph("<b>MuRIL</b> (WordPiece, 197k)", table_cell_bold), Paragraph("91.7% (922/1,005)", table_cell_style), Paragraph("20.1% (202/1,005)", table_cell_style), Paragraph("<b>−71.6 pp</b>", table_cell_bold), Paragraph("1.12 &rarr; 2.25 (+1.13)", table_cell_style)],
        [Paragraph("<b>XLM-RoBERTa</b> (BPE, 250k)", table_cell_bold), Paragraph("62.3% (626/1,005)", table_cell_style), Paragraph("6.4% (64/1,005)", table_cell_style), Paragraph("<b>−55.9 pp</b>", table_cell_bold), Paragraph("1.63 &rarr; 2.67 (+1.04)", table_cell_style)]
    ]
    t1 = Table(t1_data, colWidths=[2.1*inch, 1.3*inch, 1.3*inch, 1.0*inch, 1.3*inch])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light)
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    # Table 2: Scoring
    story.append(Paragraph("<b>Table 2: Mean &Delta;S (&Delta;MeanLogP) by Model and Pair Category (N = 1,679 pairs)</b>", h2_style))
    t2_data = [
        [Paragraph("<b>Model</b>", table_header_style), Paragraph("<b>Perturbation Track</b>", table_header_style), Paragraph("<b>Sample Size (N)</b>", table_header_style), Paragraph("<b>Mean &Delta;S</b>", table_header_style), Paragraph("<b>Preferred Original (%)</b>", table_header_style), Paragraph("<b>Statistical Significance</b>", table_header_style)],
        [Paragraph("XLM-RoBERTa", table_cell_style), Paragraph("Valid-Word Context", table_cell_style), Paragraph("312", table_cell_style), Paragraph("<b>−1.0831</b>", table_cell_bold), Paragraph("85.6%", table_cell_style), Paragraph("p < 10⁻¹⁵, d_z = −0.61", table_cell_style)],
        [Paragraph("XLM-RoBERTa", table_cell_style), Paragraph("Synonym Substitution", table_cell_style), Paragraph("362", table_cell_style), Paragraph("<b>−0.0098</b>", table_cell_bold), Paragraph("50.6%", table_cell_style), Paragraph("p = 0.468, nonsignificant", table_cell_style)],
        [Paragraph("XLM-RoBERTa", table_cell_style), Paragraph("Realistic Spelling Error", table_cell_style), Paragraph("1,005", table_cell_style), Paragraph("<b>−0.8864</b>", table_cell_bold), Paragraph("76.4%", table_cell_style), Paragraph("p < 10⁻¹⁵, d_z = −0.48", table_cell_style)],
        [Paragraph("MuRIL", table_cell_style), Paragraph("Valid-Word Context", table_cell_style), Paragraph("312", table_cell_style), Paragraph("<b>−1.8470</b>", table_cell_bold), Paragraph("92.3%", table_cell_style), Paragraph("p < 10⁻¹⁵, d_z = −0.92", table_cell_style)],
        [Paragraph("MuRIL", table_cell_style), Paragraph("Synonym Substitution", table_cell_style), Paragraph("362", table_cell_style), Paragraph("<b>−0.1787</b>", table_cell_bold), Paragraph("59.4%", table_cell_style), Paragraph("p = 0.003, d_z = −0.16", table_cell_style)],
        [Paragraph("MuRIL", table_cell_style), Paragraph("Realistic Spelling Error", table_cell_style), Paragraph("1,005", table_cell_style), Paragraph("<b>−1.2045</b>", table_cell_bold), Paragraph("91.0%", table_cell_style), Paragraph("p < 10⁻¹⁵, d_z = −0.69", table_cell_style)]
    ]
    t2 = Table(t2_data, colWidths=[1.2*inch, 1.6*inch, 0.8*inch, 1.0*inch, 1.1*inch, 1.3*inch])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), c_bg_light),
    ]))
    story.append(t2)
    story.append(Spacer(1, 6))

    # Table 3: Stability
    story.append(Paragraph("<b>Table 3: Pooled Explanation Stability (N = 1,005 Spelling Pairs, Visible-Target Protocol)</b>", h2_style))
    t3_data = [
        [Paragraph("<b>Model</b>", table_header_style), Paragraph("<b>Explanation Method</b>", table_header_style), Paragraph("<b>Mean Rank &rho; (Spearman)</b>", table_header_style), Paragraph("<b>Mean Cosine Similarity</b>", table_header_style), Paragraph("<b>Strict Single-Subword &rho;</b>", table_header_style)],
        [Paragraph("<b>XLM-RoBERTa</b>", table_cell_bold), Paragraph("Attention (Layer 11)", table_cell_style), Paragraph("<b>0.6258</b>", table_cell_bold), Paragraph("0.9353", table_cell_style), Paragraph("0.6306 (N = 52)", table_cell_style)],
        [Paragraph("<b>XLM-RoBERTa</b>", table_cell_bold), Paragraph("Integrated Gradients (M=20)", table_cell_style), Paragraph("<b>0.3319</b>", table_cell_bold), Paragraph("0.8890", table_cell_style), Paragraph("0.3541 (N = 52)", table_cell_style)],
        [Paragraph("<b>MuRIL</b>", table_cell_bold), Paragraph("Attention (Layer 11)", table_cell_style), Paragraph("<b>0.8027</b>", table_cell_bold), Paragraph("0.9518", table_cell_style), Paragraph("0.8053 (N = 197)", table_cell_style)],
        [Paragraph("<b>MuRIL</b>", table_cell_bold), Paragraph("Integrated Gradients (M=20)", table_cell_style), Paragraph("<b>0.2560</b>", table_cell_bold), Paragraph("0.9818", table_cell_style), Paragraph("0.2489 (N = 197)", table_cell_style)]
    ]
    t3 = Table(t3_data, colWidths=[1.5*inch, 1.8*inch, 1.4*inch, 1.1*inch, 1.2*inch])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
    ]))
    story.append(t3)
    story.append(Spacer(1, 6))

    # Table 4: Faithfulness
    story.append(Paragraph("<b>Table 4: Faithfulness Intervention Summary (N = 2,010 Sentences, 3-Fraction Avg)</b>", h2_style))
    t4_data = [
        [Paragraph("<b>Model</b>", table_header_style), Paragraph("<b>Explanation Method</b>", table_header_style), Paragraph("<b>Mean Gap (&Delta;Top &minus; &Delta;Bottom)</b>", table_header_style), Paragraph("<b>Win Rate (% Top &gt; Bottom)</b>", table_header_style), Paragraph("<b>Faithfulness Interpretation</b>", table_header_style)],
        [Paragraph("<b>XLM-RoBERTa</b>", table_cell_bold), Paragraph("Attention (Layer 11)", table_cell_style), Paragraph("<b>+3.02</b>", table_cell_bold), Paragraph("<b>65.6%</b>", table_cell_bold), Paragraph("Highly Faithful (Top-k degrades prediction)", table_cell_style)],
        [Paragraph("<b>XLM-RoBERTa</b>", table_cell_bold), Paragraph("Integrated Gradients", table_cell_style), Paragraph("<b>+2.54</b>", table_cell_bold), Paragraph("<b>62.4%</b>", table_cell_bold), Paragraph("Moderately Faithful", table_cell_style)],
        [Paragraph("<b>MuRIL</b>", table_cell_bold), Paragraph("Attention (Layer 11)", table_cell_style), Paragraph("<b>−1.31</b>", table_cell_bold), Paragraph("<b>39.6%</b>", table_cell_bold), Paragraph("Unfaithful (Bottom-k causes larger drop)", table_cell_style)],
        [Paragraph("<b>MuRIL</b>", table_cell_bold), Paragraph("Integrated Gradients", table_cell_style), Paragraph("<b>−0.63</b>", table_cell_bold), Paragraph("<b>48.7%</b>", table_cell_bold), Paragraph("Chance-level Faithfulness", table_cell_style)]
    ]
    t4 = Table(t4_data, colWidths=[1.4*inch, 1.7*inch, 1.4*inch, 1.1*inch, 1.4*inch])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
    ]))
    story.append(t4)
    story.append(Spacer(1, 6))

    # Table 5: Correlations (RQ5)
    story.append(Paragraph("<b>Table 5: Stability–Faithfulness Correlations (N = 1,005 Spelling Pairs, f = 0.20)</b>", h2_style))
    t5_data = [
        [Paragraph("<b>Model & Method</b>", table_header_style), Paragraph("<b>Cohort</b>", table_header_style), Paragraph("<b>Spearman &rho;</b>", table_header_style), Paragraph("<b>p-value (&rho;)</b>", table_header_style), Paragraph("<b>95% CI (&rho;, Fisher z)</b>", table_header_style), Paragraph("<b>Pearson r</b>", table_header_style), Paragraph("<b>p-value (r)</b>", table_header_style)],
        [Paragraph("XLM-R Attention", table_cell_style), Paragraph("Pooled (1,005)", table_cell_style), Paragraph("+0.0711", table_cell_style), Paragraph("0.0241*", table_cell_style), Paragraph("[+0.0093, +0.1324]", table_cell_style), Paragraph("+0.0564", table_cell_style), Paragraph("0.0816", table_cell_style)],
        [Paragraph("XLM-R IG", table_cell_style), Paragraph("Pooled (1,005)", table_cell_style), Paragraph("+0.0705", table_cell_style), Paragraph("0.0255*", table_cell_style), Paragraph("[+0.0087, +0.1318]", table_cell_style), Paragraph("+0.0495", table_cell_style), Paragraph("0.1270", table_cell_style)],
        [Paragraph("MuRIL Attention", table_cell_style), Paragraph("Pooled (1,005)", table_cell_style), Paragraph("−0.0714", table_cell_style), Paragraph("0.0235*", table_cell_style), Paragraph("[−0.1327, −0.0096]", table_cell_style), Paragraph("−0.0790", table_cell_style), Paragraph("0.0248*", table_cell_style)],
        [Paragraph("MuRIL IG", table_cell_style), Paragraph("Pooled (1,005)", table_cell_style), Paragraph("+0.0218", table_cell_style), Paragraph("0.4902", table_cell_style), Paragraph("[−0.0401, +0.0835]", table_cell_style), Paragraph("+0.0290", table_cell_style), Paragraph("0.4108", table_cell_style)],
        [Paragraph("<b>MuRIL Attention</b>", table_cell_bold), Paragraph("<b>Strict (N=197)</b>", table_cell_bold), Paragraph("<b>−0.1924</b>", table_cell_bold), Paragraph("<b>0.0067**</b>", table_cell_bold), Paragraph("<b>[−0.3235, −0.0541]</b>", table_cell_bold), Paragraph("−0.1129", table_cell_style), Paragraph("0.1141", table_cell_style)],
        [Paragraph("<b>XLM-R Attention</b>", table_cell_bold), Paragraph("<b>Strict (N=52)</b>", table_cell_bold), Paragraph("+0.2472", table_cell_style), Paragraph("0.0773", table_cell_style), Paragraph("[−0.0279, +0.4862]", table_cell_style), Paragraph("<b>+0.2949</b>", table_cell_bold), Paragraph("<b>0.0338*</b>", table_cell_bold)]
    ]
    t5 = Table(t5_data, colWidths=[1.3*inch, 1.0*inch, 0.9*inch, 0.8*inch, 1.2*inch, 0.8*inch, 1.0*inch])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
        ('BACKGROUND', (0,3), (-1,3), c_bg_light),
        ('BACKGROUND', (0,5), (-1,5), colors.HexColor("#fef2f2")),
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor("#f0fdf4")),
    ]))
    story.append(t5)
    story.append(Paragraph("<i>Note: * p < 0.05, ** p < 0.01. Strict single-subword 95% CI [-0.3235, -0.0541] strictly excludes zero. In pooled cohorts, nominal p < 0.05 is driven by high power (N=1,005); practical effect sizes are negligible (|&rho;| < 0.08, R² < 0.006), proving empirical decoupling.</i>", body_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # 6. PUBLICATION FIGURES & VISUAL EVIDENCE
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("6. Publication Figures Manifest & Visual Evidence", h1_style))
    story.append(Paragraph(
        "Below are all eight master publication figures generated from <code>results/runs/scaleup_rerun/figures/</code>. Each figure is displayed with its visual description, axes, sample size, and analytical takeaway for Claude:",
        body_style
    ))
    
    fig_dir = r"results\runs\scaleup_rerun\figures"
    
    figures_info = [
        {
            "id": "Figure 1",
            "file": "fig1_delta_meanlp_by_track.png",
            "title": "Figure 1: Distribution of Plausibility Shifts (&Delta;MeanLogP) by Track",
            "caption": "Figure 1: Violin and boxplot distributions of &Delta;MeanLogP across Valid-Word Context (N=312), Synonym Substitution (N=362), and Spelling Error (N=1,005) for MuRIL vs. XLM-RoBERTa (Total N=1,679).",
            "takeaway": "<b>Takeaway:</b> Valid-word context substitutions produce the steepest plausibility penalties (-1.85 in MuRIL, -1.08 in XLM-R), followed by spelling errors (-1.20 in MuRIL, -0.89 in XLM-R). Synonyms exhibit near-zero drop, proving both models recognize semantic equivalence while heavily penalizing orthographic and syntactic dissonance.",
            "width": 6.8 * inch,
            "height": 2.82 * inch
        },
        {
            "id": "Figure 2",
            "file": "fig2_token_delta_vs_meanlp.png",
            "title": "Figure 2: Sentence Token Inflation vs. Plausibility Shifts (&Delta;MeanLogP)",
            "caption": "Figure 2: Scatter plot of sentence-level token count change (&Delta;Tokens) vs. &Delta;MeanLogP with linear regression fits faceted by model (N=1,679 pairs).",
            "takeaway": "<b>Takeaway:</b> Sentence token inflation strongly tracks score drops in both models. However, token inflation is driven almost entirely by target-word subword fragmentation rather than context lengthening.",
            "width": 6.8 * inch,
            "height": 2.82 * inch
        },
        {
            "id": "Figure 3",
            "file": "fig3_target_token_delta_vs_meanlp.png",
            "title": "Figure 3: Target-Word Subword Fragmentation vs. Plausibility Shifts",
            "caption": "Figure 3: Target subword delta (&Delta;Target Tokens) vs. &Delta;MeanLogP across experimental tracks (N=1,679 pairs).",
            "takeaway": "<b>Takeaway:</b> In the spelling error track, target words undergo extreme fracturing (+1 to +3 tokens), correlating with sharp log-probability declines. Synonym substitutions remain primarily single-subword with zero fragmentation.",
            "width": 6.8 * inch,
            "height": 2.82 * inch
        },
        {
            "id": "Figure 4",
            "file": "fig4_model_comparison_scatter.png",
            "title": "Figure 4: Cross-Model Plausibility Correlation (MuRIL vs. XLM-RoBERTa)",
            "caption": "Figure 4: Correlation between MuRIL &Delta;MeanLogP and XLM-RoBERTa &Delta;MeanLogP across all 1,679 pairs faceted by perturbation track.",
            "takeaway": "<b>Takeaway:</b> Strong cross-model concordance across all tracks (Spearman r_s = +0.5496, p < 10⁻¹⁵, 95% CI [0.5153, 0.5821]). Concordance is highest in spelling errors (r_s = +0.5513) and valid context (r_s = +0.5280).",
            "width": 4.5 * inch,
            "height": 4.5 * inch
        },
        {
            "id": "Figure 5",
            "file": "fig5_direction_agreement.png",
            "title": "Figure 5: Cross-Model Directional Agreement Rates",
            "caption": "Figure 5: Percentage of sentence pairs where MuRIL and XLM-RoBERTa agree on preference direction (Total N=1,679).",
            "takeaway": "<b>Takeaway:</b> Global directional agreement is 73.67%, rising to 83.18% on spelling errors and 84.62% on context substitutions, demonstrating that both models share core directional priors on Hindi orthographic acceptability.",
            "width": 5.8 * inch,
            "height": 3.19 * inch
        },
        {
            "id": "Figure 6",
            "file": "fig6_explanation_stability.png",
            "title": "Figure 6: Explanation Stability Across Models and Methods (N = 1,005)",
            "caption": "Figure 6 (Paper Fig. 3): Mean Rank Stability (Spearman &rho;) and Directional Stability (Cosine Similarity) for Attention vs. Integrated Gradients in MuRIL and XLM-RoBERTa.",
            "takeaway": "<b>Takeaway:</b> Attention achieves much higher rank stability than Integrated Gradients (&rho; = 0.80 vs 0.26 in MuRIL; &rho; = 0.63 vs 0.33 in XLM-R). However, Integrated Gradients achieves high vector cosine similarity (0.89 - 0.98), reflecting continuous geometric preservation rather than discrete rank preservation.",
            "width": 6.8 * inch,
            "height": 2.97 * inch
        },
        {
            "id": "Figure 7",
            "file": "fig7_faithfulness_interventions.png",
            "title": "Figure 7: Faithfulness Erasure Interventions Across Budgets (N = 2,010)",
            "caption": "Figure 7 (Paper Fig. 4): Faithfulness Gaps (&Delta;Top - &Delta;Bottom) and Win Rates (%) across context erasure fractions (10%, 20%, 30%) for Attention vs. IG.",
            "takeaway": "<b>Takeaway:</b> XLM-RoBERTa demonstrates genuine faithfulness with win rates of 63.5% - 67.5% and positive gaps (+2.44 to +3.81). MuRIL fails faithfulness tests, yielding win rates below chance (39.6% - 48.7%) and negative gaps, indicating that erasing its bottom-k tokens harms prediction more than top-k.",
            "width": 6.8 * inch,
            "height": 2.82 * inch
        },
        {
            "id": "Figure 8",
            "file": "fig8_stability_vs_faithfulness.png",
            "title": "Figure 8: Stability vs. Faithfulness Decoupling Scatter Plots (N = 1,005)",
            "caption": "Figure 8 (Paper Fig. 2): Pair-level scatter plots of Visible-Target Stability (Rank &rho;) vs. Faithfulness Gap at 20% masking, faceted by model and explanation method.",
            "takeaway": "<b>Takeaway:</b> Visual proof of decoupling. Observations form a diffuse, horizontal cloud across all models and methods. High stability does not produce higher faithfulness, conclusively disproving stability as an unvalidated proxy for explanation quality.",
            "width": 6.8 * inch,
            "height": 2.94 * inch
        }
    ]
    
    for fig in figures_info:
        img_path = os.path.join(fig_dir, fig["file"])
        if os.path.exists(img_path):
            story.append(Paragraph(f"<b>{fig['title']}</b>", h2_style))
            story.append(Spacer(1, 2))
            story.append(RLImage(img_path, width=fig["width"], height=fig["height"]))
            story.append(Paragraph(fig["caption"], caption_style))
            story.append(Paragraph(fig["takeaway"], body_style))
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(f"<i>[Image file not found: {fig['file']}]</i>", body_style))
    
    # -------------------------------------------------------------------------
    # 7. MAJOR SCIENTIFIC DISCOVERIES & IMPLICATIONS
    # -------------------------------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("7. Core Scientific Discoveries & Conceptual Narrative", h1_style))
    
    discoveries = [
        ("Discovery 1: Subword Collapse in Devanagari MLMs",
         "Spelling errors in Hindi do not behave like typos in English. Because Devanagari relies on vowel matras and ligature halants, swapping a short/long vowel or omitting a conjunct marker destroys the canonical subword entry. MuRIL single-subword coverage collapses by <b>-71.6 pp</b> (91.7% to 20.1%) and XLM-RoBERTa collapses by <b>-55.9 pp</b> (62.3% to 6.4%). This subword fracturing penalizes model log-likelihood (-1.20 in MuRIL, -0.89 in XLM-R)."),
        
        ("Discovery 2: The Masked-Target Stability Artifact (Methodological Breakthrough)",
         "In prior literature, explanation stability was often computed by masking the target token in both original and perturbed sentences. We discovered that this introduces a fatal artifact: because the surrounding context is identical, masking the target makes both sentences identical, producing artificial perfect stability (&rho; = 1.0, cos = 1.0). We solved this by developing the <b>Visible-Target Scoring Protocol</b>, keeping target spellings visible. This reveals genuine stability (&rho; = 0.26 - 0.80) and exposes the real sensitivity of attention routing."),
        
        ("Discovery 3: The Stability–Faithfulness Decoupling (The Core Paper Finding)",
         "A prevailing dogma in XAI is that stable explanations are better explanations. Our empirical evidence decisively refutes this. MuRIL Attention displays the highest stability of all tested configurations (&rho; = 0.8027, cos = 0.9518), yet it is <b>unfaithful</b> under causal token erasure (win rate 39.6%, negative gap -1.31). Conversely, XLM-R Attention has lower stability (&rho; = 0.6258) but high faithfulness (win rate 65.6%, gap +3.02). Across 1,005 pairs, correlation effect sizes are negligible (|&rho;| < 0.08, R² < 0.006)."),
        
        ("Discovery 4: Negative Correlation in Clean Targets",
         "When restricting analysis to strict single-subword targets (N=197 in MuRIL), MuRIL Attention stability is <b>statistically significantly negatively correlated</b> with faithfulness (&rho; = -0.1924, p = 0.0067, 95% CI [-0.3235, -0.0541]). This proves that optimizing explanations for noise invariance can actively favor unfaithful features."),
        
        ("Discovery 5: Axiomatic Gradient vs. Internal Attention Trade-Off",
         "Integrated Gradients satisfies mathematical axioms (completeness, implementation invariance) in continuous embedding space, maintaining high cosine similarity (&ge; 0.89). However, under discrete token erasure interventions, attention weights provide substantially better rank stability and practical faithfulness in XLM-R.")
    ]
    
    for d_title, d_desc in discoveries:
        story.append(Paragraph(f"<b>{d_title}</b>", h2_style))
        story.append(Paragraph(d_desc, body_style))
        story.append(Spacer(1, 4))
        
    # -------------------------------------------------------------------------
    # 8. METHODOLOGICAL SAFEGUARDS & DO-NOT-CLAIM RULES
    # -------------------------------------------------------------------------
    story.append(Paragraph("8. Methodological Safeguards & 'Do-Not-Claim' Rules", h1_style))
    story.append(Paragraph(
        "Claude must strictly adhere to the following academic safeguards when drafting or evaluating paper sections:",
        body_style
    ))
    safeguards = [
        "<b>Do NOT treat PLL as sentence probability:</b> Pseudo-log-likelihood is an unnormalized sum of bidirectional conditional probabilities, not an autoregressive sequence likelihood.",
        "<b>Do NOT claim subword fragmentation causes PLL drops without qualification:</b> Token fragmentation strongly correlates with PLL drops, but vocabulary unigram frequency and out-of-vocabulary effects are significant confounds.",
        "<b>Do NOT claim attention is an inherently faithful explanation:</b> Attention reflects internal model routing. It is faithful in XLM-R but unfaithful in MuRIL.",
        "<b>Do NOT conflate stability with faithfulness:</b> Always treat stability (invariance under input noise) and faithfulness (causal impact under erasure) as separate, empirically decoupled properties.",
        "<b>Do NOT attribute model differences solely to pretraining corpus size:</b> MuRIL (197k WordPiece, Indic-focused) and XLM-R (250k BPE, multilingual) differ in tokenizer architecture, vocabulary coverage, and objective weights.",
        "<b>Acknowledge the zero-embedding baseline limitation:</b> The zero/pad baseline in Integrated Gradients is an out-of-distribution embedding point, which may introduce baseline artifacts."
    ]
    for sg in safeguards:
        story.append(Paragraph(f"• {sg}", bullet_style))
    story.append(Spacer(1, 8))

    # -------------------------------------------------------------------------
    # 9. SECTION-BY-SECTION PAPER BLUEPRINT FOR CLAUDE
    # -------------------------------------------------------------------------
    story.append(Paragraph("9. Academic Paper Blueprint & Instructions for Claude", h1_style))
    blueprint = [
        "<b>Title & Abstract:</b> Emphasize Devanagari orthographic sensitivity, the N=1,679 primary benchmark, token collapse (-71.6 pp in MuRIL, -55.9 pp in XLM-R), and the empirical decoupling of stability and faithfulness.",
        "<b>1. Introduction:</b> Motivate the study through the lens of non-Latin abugida scripts. Contrast Latin character substitutions with Devanagari syllabic disruptions. Formulate RQ1 to RQ5 and highlight the Visible-Target Protocol.",
        "<b>2. Related Work:</b> Survey Indic NLP (IndicBERT, MuRIL), subword tokenization vulnerabilities, PLL scoring, and the XAI debate (Jain & Wallace vs. Wiegreffe & Pinter; Jacovi & Goldberg).",
        "<b>3. Dataset Construction & Annotation:</b> Document the 2,000-row candidate reconciliation into 1,679 Primary, 1,957 Template, 12 Multiword, and 31 Excluded rows. Detail the 4-part orthographic error typology.",
        "<b>4. Methodology:</b> Formalize MeanLogP scoring, Layer-11 Mean Attention, Layer Integrated Gradients (M=20), the Visible-Target Protocol, and discrete erasure interventions (Top-k vs. Bottom-k / Random-k at 10%, 20%, 30%).",
        "<b>5. Empirical Results:</b> Organize strictly around RQ1–RQ5 utilizing Tables 1–5 and Figures 1–8. Emphasize the exact numbers and p-values.",
        "<b>6. Discussion:</b> Analyze why stability and faithfulness decouple. Explain why MuRIL's high attention stability reflects rigid attention sinks rather than faithful reasoning.",
        "<b>7. Limitations:</b> Document the zero-embedding baseline in IG, discrete masking distribution shifts, and scope limited to masked language models in Hindi.",
        "<b>8. Conclusion:</b> Summarize that explanation stability cannot serve as a proxy for explanation faithfulness in explainable NLP benchmarks."
    ]
    for bp in blueprint:
        story.append(Paragraph(f"• {bp}", bullet_style))
    story.append(Spacer(1, 10))
    
    # Ready-to-paste box
    prompt_box = Paragraph(
        "<b>COPY-READY INSTRUCTION TO PASTE TO CLAUDE:</b><br/>"
        "<i>\"I am uploading my research paper draft alongside the master Research Context & Claude Review Brief PDF. The project is fully completed, audited, and synchronized at https://github.com/Aasthahcs05/hindi-lexical-sensitivity (main). The authoritative dataset is the Primary Adjudicated Benchmark (N=1,679 pairs; 1,005 spelling, 362 synonym, 312 context). All five tables, all eight figures, and Stages 1–7 are 100% complete and verified. Please evaluate and refine the paper according to the Master Brief, preserving the core finding that explanation stability is decoupled from explanation faithfulness, maintaining exact numerical fidelity, and adhering to all methodological safeguards.\"</i>",
        callout_text_style
    )
    t_pbox = Table([[prompt_box]], colWidths=[7.0*inch])
    t_pbox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_callout_bg),
        ('BOX', (0,0), (-1,-1), 1.0, c_callout_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_pbox)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master brief PDF generated successfully: {pdf_filename} (Size: {os.path.getsize(pdf_filename)} bytes)")

if __name__ == "__main__":
    build_brief_pdf()
