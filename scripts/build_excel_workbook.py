import os
import sys
import shutil

# Ensure local lib has openpyxl and et_xmlfile
script_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(script_dir, 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference, Series

def create_workbook():
    print("Building comprehensive Excel workbook: paper/expanded_experimental_results.xlsx...")
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)

    # Styling definitions
    font_family = 'Calibri'
    title_font = Font(name=font_family, size=15, bold=True, color='1A365D')
    section_font = Font(name=font_family, size=12, bold=True, color='2B5C8F')
    header_font = Font(name=font_family, size=10, bold=True, color='FFFFFF')
    bold_font = Font(name=font_family, size=10, bold=True, color='000000')
    regular_font = Font(name=font_family, size=10, color='222222')
    italic_note_font = Font(name=font_family, size=9, italic=True, color='555555')
    bold_note_font = Font(name=font_family, size=9, bold=True, color='1A365D')

    header_fill = PatternFill(start_color='1A365D', end_color='1A365D', fill_type='solid')
    header_fill_accent = PatternFill(start_color='2B5C8F', end_color='2B5C8F', fill_type='solid')
    zebra_fill = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
    white_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    summary_fill = PatternFill(start_color='EDF2F7', end_color='EDF2F7', fill_type='solid')
    highlight_fill = PatternFill(start_color='FEFCBF', end_color='FEFCBF', fill_type='solid')

    thin_border_side = Side(style='thin', color='CBD5E0')
    border_all = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    thick_bottom = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=Side(style='medium', color='1A365D'))

    align_center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    align_left = Alignment(horizontal='left', vertical='center', wrap_text=True)
    align_right = Alignment(horizontal='right', vertical='center', wrap_text=False)

    def style_table_header(ws, row_idx, headers, fill=header_fill):
        for col_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=h)
            cell.font = header_font
            cell.fill = fill
            cell.alignment = align_center
            cell.border = border_all
        ws.row_dimensions[row_idx].height = 28

    def auto_fit_cols(ws, min_col=1, max_col=None, min_w=12, max_w=48):
        if max_col is None:
            max_col = ws.max_column
        for col in range(min_col, max_col + 1):
            col_letter = get_column_letter(col)
            max_len = 0
            for row in range(1, ws.max_row + 1):
                v = ws.cell(row=row, column=col).value
                if v is not None:
                    s = str(v)
                    # Don't let long titles or notes blow up the column width
                    if len(s) > 75 or '\n' in s:
                        continue
                    max_len = max(max_len, len(s))
            w = max(min_w, min(max_len + 3, max_w))
            ws.column_dimensions[col_letter].width = w

    base_results = 'hindi-lexical-sensitivity/results/runs/scaleup_rerun/'
    base_data = 'hindi-lexical-sensitivity/data/final/'

    # =========================================================================
    # 1. Dataset Overview and Category Distribution
    # =========================================================================
    print("  Creating sheet 1: Dataset Overview and Category Distribution...")
    ws1 = wb.create_sheet(title="Dataset Overview & Distribution")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1['A1'] = "1. Dataset Overview, Experimental Cohorts & Category Distribution"
    ws1['A1'].font = title_font
    ws1['A2'] = "Authoritative Source: data/final/COMPLETE_2000_ROW_RECONCILIATION.csv & PRIMARY_BENCHMARK_ADJUDICATED.csv"
    ws1['A2'].font = italic_note_font
    
    # Section A: Overview of Cohorts
    ws1['A4'] = "A. Experimental Cohort Definitions and Sample Sizes"
    ws1['A4'].font = section_font
    
    headers1_a = ["Cohort Name", "Sample Size (Pairs)", "Evaluations (Sentences)", "Adjudication Status", "Description & Role in Research"]
    style_table_header(ws1, 5, headers1_a)
    
    cohort_data = [
        ["Primary Benchmark", 1679, 3358, "100% Adjudicated / Verified", "Authoritative core benchmark across 3 tracks (1,005 spelling, 362 synonym, 312 context). Fully audited."],
        ["Template Sensitivity Benchmark", 1957, 3914, "Audited / Verified", "Primary benchmark (N=1,679) plus 278 template variants across 278 template frames. NOT an independent dataset."],
        ["Auxiliary Multiword Probe", 12, 24, "Audited / Verified", "Edge-case probe investigating multiword syntactic ripples (verbal agreement, case marker insertion, repeated targets)."],
        ["Historical Preliminary Pilot", 200, 400, "Historical (Frozen)", "Original preliminary exploratory pilot retained in results/runs/historical_pilot_200/ for historical context only."],
        ["Audited Curated Raw Pool", 2000, 4000, "Complete Reconciliation", "Full audited pool: 1,679 Primary + 278 Template-only + 12 Auxiliary-only + 31 Excluded (quality/duplicate failed)."]
    ]
    
    for r_idx, row in enumerate(cohort_data, start=6):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        for c_idx, val in enumerate(row, start=1):
            c = ws1.cell(row=r_idx, column=c_idx, value=val)
            c.font = regular_font if c_idx != 1 else bold_font
            c.fill = fill
            c.border = border_all
            if c_idx in [2, 3]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx == 4:
                c.alignment = align_center
            else:
                c.alignment = align_left
        ws1.row_dimensions[r_idx].height = 22

    # Section B: Track Distribution Table
    ws1['A13'] = "B. Experimental Track Distribution by Cohort"
    ws1['A13'].font = section_font

    headers1_b = ["Cohort", "Experimental Track", "Pair Count (N)", "Track Proportion (%)", "Evaluation Count (2xN)", "Linguistic Characteristics"]
    style_table_header(ws1, 14, headers1_b)

    track_data = [
        ["Primary Benchmark", "REALISTIC_SPELLING_ERROR", 1005, 0.5986, 2010, "Authentic Devanagari typos (matra inversions, ligature splits, consonant confusions)"],
        ["Primary Benchmark", "SYNONYM_SUBSTITUTION", 362, 0.2156, 724, "Semantic preservation with lexical variation (high human acceptability)"],
        ["Primary Benchmark", "VALID_WORD_CONTEXT", 312, 0.1858, 624, "Valid-word contextual contrasts (grammatical vs. incongruous word choice)"],
        ["Primary Benchmark", "TOTAL PRIMARY", 1679, 1.0000, 3358, "100% human-verified and linguistically adjudicated benchmark"],
        ["Template Sensitivity", "REALISTIC_SPELLING_ERROR", 1260, 0.6438, 2520, "1,005 primary spelling + 255 template-derived spelling error variants"],
        ["Template Sensitivity", "SYNONYM_SUBSTITUTION", 385, 0.1967, 770, "362 primary synonym + 23 template-derived synonym variants"],
        ["Template Sensitivity", "VALID_WORD_CONTEXT", 312, 0.1594, 624, "312 primary contextual contrasts (no additional template variants)"],
        ["Template Sensitivity", "TOTAL TEMPLATE", 1957, 1.0000, 3914, "Primary benchmark + 278 template variants across 278 syntactic frames"],
        ["Auxiliary Multiword Probe", "Gender/Number Agreement Ripple", 6, 0.5000, 12, "Lexical substitution triggering verbal/adjectival agreement changes across context"],
        ["Auxiliary Multiword Probe", "Repeated-Target Ambiguity", 4, 0.3333, 8, "Target word appears multiple times in sentence; tests alignment robustness"],
        ["Auxiliary Multiword Probe", "Postpositional Case Insertion", 1, 0.0833, 2, "Grammatical alteration requiring case marker insertion (altering length geometry)"],
        ["Auxiliary Multiword Probe", "Collocational Light-Verb Change", 1, 0.0833, 2, "Lexical change altering light verb collocation (e.g. bhojan karna vs khana khana)"],
        ["Auxiliary Multiword Probe", "TOTAL AUXILIARY", 12, 1.0000, 24, "Edge-case minimal pairs evaluated under 4-category taxonomy"],
        ["Historical Preliminary Pilot", "VALID_WORD_CONTEXT", 142, 0.7100, 284, "Initial exploratory cohort; retained intact for historical provenance"],
        ["Historical Preliminary Pilot", "SYNONYM_SUBSTITUTION", 38, 0.1900, 76, "Initial exploratory cohort; retained intact for historical provenance"],
        ["Historical Preliminary Pilot", "REALISTIC_SPELLING_ERROR", 20, 0.1000, 40, "Initial exploratory cohort; retained intact for historical provenance"],
        ["Historical Preliminary Pilot", "TOTAL HISTORICAL PILOT", 200, 1.0000, 400, "Historical preliminary pilot benchmark"]
    ]

    for r_idx, row in enumerate(track_data, start=15):
        is_total = "TOTAL" in str(row[1])
        fill = summary_fill if is_total else (zebra_fill if r_idx % 2 == 0 else white_fill)
        fnt = bold_font if is_total else regular_font
        for c_idx, val in enumerate(row, start=1):
            c = ws1.cell(row=r_idx, column=c_idx, value=val)
            c.font = fnt
            c.fill = fill
            c.border = border_all
            if c_idx in [3, 5]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx == 4:
                c.alignment = align_right
                c.number_format = '0.00%'
            else:
                c.alignment = align_left
        ws1.row_dimensions[r_idx].height = 20

    # Section C: Native Chart
    chart1 = BarChart()
    chart1.type = "col"
    chart1.style = 10
    chart1.title = "Primary vs. Template Benchmark Track Counts"
    chart1.y_axis.title = "Minimal Pairs (N)"
    chart1.x_axis.title = "Experimental Track"
    chart1.height = 12
    chart1.width = 18

    # Primary tracks are rows 15-17; Template tracks are rows 19-21
    # Let's create a compact chart reference table
    ws1['A34'] = "Track"
    ws1['B34'] = "Primary Benchmark (N)"
    ws1['C34'] = "Template Sensitivity (N)"
    chart_summary_rows = [
        ["Spelling Error", 1005, 1260],
        ["Synonym Substitution", 362, 385],
        ["Valid Word Context", 312, 312]
    ]
    for idx, r in enumerate(chart_summary_rows, start=35):
        ws1.cell(row=idx, column=1, value=r[0])
        ws1.cell(row=idx, column=2, value=r[1])
        ws1.cell(row=idx, column=3, value=r[2])

    data_ref = Reference(ws1, min_col=2, min_row=34, max_col=3, max_row=37)
    cats_ref = Reference(ws1, min_col=1, min_row=35, max_row=37)
    chart1.add_data(data_ref, titles_from_data=True)
    chart1.set_categories(cats_ref)
    ws1.add_chart(chart1, "E34")

    # Source notes
    ws1['A40'] = "Scientific & Provenance Notes:"
    ws1['A40'].font = bold_note_font
    ws1['A41'] = "1. Strict Cohort Separation: The Primary Benchmark (N=1,679) contains zero template repetitions. The Template Sensitivity Benchmark (N=1,957) explicitly includes the Primary Benchmark plus 278 template variants; it must not be treated as an independent dataset."
    ws1['A41'].font = italic_note_font
    ws1['A42'] = "2. Reconciliation Integrity: All 2,000 raw rows are accounted for: 1,679 primary + 278 template-only + 12 auxiliary-only + 31 excluded (failed quality audit / duplicate checks)."
    ws1['A42'].font = italic_note_font

    ws1.auto_filter.ref = "A14:F31"
    ws1.freeze_panes = 'A6'
    auto_fit_cols(ws1)

    # =========================================================================
    # 2. Tokenization and Fragmentation
    # =========================================================================
    print("  Creating sheet 2: Tokenization and Fragmentation...")
    ws2 = wb.create_sheet(title="Tokenization & Fragmentation")
    ws2.views.sheetView[0].showGridLines = True

    ws2['A1'] = "2. Subword Tokenization Dynamics & Target Word Fragmentation (N = 1,679)"
    ws2['A1'].font = title_font
    ws2['A2'] = "Source: results/runs/scaleup_rerun/dashboard_data/tokenization_summary.csv"
    ws2['A2'].font = italic_note_font

    headers2 = [
        "Model Checkpoint", "Experimental Track", "Pair Count (N)", "Mean Orig Tokens", 
        "Mean Cont Tokens", "Token Delta (Δ)", "Length Ratio", "Mean Orig Target Subwords", 
        "Mean Cont Target Subwords", "Single-Subword Orig Target (%)", "Single-Subword Cont Target (%)", 
        "Single-Subword Collapse (Δ pp)"
    ]
    style_table_header(ws2, 4, headers2)

    tok_df = pd.read_csv(os.path.join(base_results, 'dashboard_data/tokenization_summary.csv'))
    
    for r_idx, row in tok_df.iterrows():
        row_num = r_idx + 5
        fill = zebra_fill if row_num % 2 == 0 else white_fill
        
        m_name = "XLM-RoBERTa" if "xlm" in row['model_name'].lower() else "MuRIL"
        track = row['track']
        n_pairs = int(row['pair_count'])
        m_orig_tok = float(row['mean_orig_tokens'])
        m_cont_tok = float(row['mean_cont_tokens'])
        delta_tok = float(row['mean_delta_tokens'])
        len_ratio = float(row['mean_length_ratio'])
        m_orig_tgt = float(row['mean_orig_target_subwords'])
        m_cont_tgt = float(row['mean_cont_target_subwords'])
        pct_orig_single = float(row['pct_single_subword_orig_target']) / 100.0
        pct_cont_single = float(row['pct_single_subword_cont_target']) / 100.0
        collapse_pp = (pct_cont_single - pct_orig_single) * 100.0

        vals = [
            m_name, track, n_pairs, m_orig_tok, m_cont_tok, delta_tok, len_ratio,
            m_orig_tgt, m_cont_tgt, pct_orig_single, pct_cont_single, collapse_pp
        ]

        for c_idx, val in enumerate(vals, start=1):
            c = ws2.cell(row=row_num, column=c_idx, value=val)
            c.font = bold_font if c_idx in [1, 2, 12] else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx == 3:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [4, 5, 8, 9]:
                c.alignment = align_right
                c.number_format = '0.00'
            elif c_idx in [6, 7]:
                c.alignment = align_right
                c.number_format = '+0.00;-0.00;0.00'
            elif c_idx in [10, 11]:
                c.alignment = align_right
                c.number_format = '0.0%'
            elif c_idx == 12:
                c.alignment = align_right
                c.number_format = '+0.0;-0.0;0.0'
            else:
                c.alignment = align_left
        ws2.row_dimensions[row_num].height = 22

    # Chart on sheet 2: Single-Subword Coverage Collapse
    chart2 = BarChart()
    chart2.type = "col"
    chart2.style = 11
    chart2.title = "Target Single-Subword Coverage Collapse Under Spelling Noise"
    chart2.y_axis.title = "Single-Subword Target Share (%)"
    chart2.height = 12
    chart2.width = 18

    # We plot cols 10 and 11 for rows 5 and 8 (spelling error rows)
    # Let's create a tidy chart block
    ws2['A13'] = "Model (Spelling Errors)"
    ws2['B13'] = "Original Canonical Target (%)"
    ws2['C13'] = "Perturbed Target (%)"
    ws2['A14'] = "XLM-RoBERTa"
    ws2['B14'] = 0.623
    ws2['C14'] = 0.064
    ws2['A15'] = "MuRIL"
    ws2['B15'] = 0.917
    ws2['C15'] = 0.201

    ws2['B14'].number_format = '0.0%'
    ws2['C14'].number_format = '0.0%'
    ws2['B15'].number_format = '0.0%'
    ws2['C15'].number_format = '0.0%'

    data2 = Reference(ws2, min_col=2, min_row=13, max_col=3, max_row=15)
    cats2 = Reference(ws2, min_col=1, min_row=14, max_row=15)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats2)
    ws2.add_chart(chart2, "E13")

    ws2['A18'] = "Linguistic & Structural Insights:"
    ws2['A18'].font = bold_note_font
    ws2['A19'] = "1. Catastrophic Target Fragmentation: Authentic Devanagari spelling errors (swapping a matra or splitting a ligature) destroy subword vocabulary matches, causing a 71.6 percentage point drop in MuRIL (91.7% to 20.1%) and a 55.9 percentage point drop in XLM-R (62.3% to 6.4%)."
    ws2['A19'].font = italic_note_font
    ws2['A20'] = "2. Localized Token Inflation: Full sentence token inflation (+1.13 in MuRIL, +1.04 in XLM-R) is driven entirely by fragmentation at the target word locus, demonstrating that context tokens remain stable."
    ws2['A20'].font = italic_note_font

    ws2.auto_filter.ref = "A4:L10"
    ws2.freeze_panes = 'A5'
    auto_fit_cols(ws2)

    # =========================================================================
    # 3. MuRIL PLL Results
    # =========================================================================
    print("  Creating sheet 3: MuRIL PLL Results...")
    ws3 = wb.create_sheet(title="MuRIL PLL Results")
    ws3.views.sheetView[0].showGridLines = True

    ws3['A1'] = "3. MuRIL Pseudo-Log-Likelihood (PLL) Scoring Results (google/muril-base-cased)"
    ws3['A1'].font = title_font
    ws3['A2'] = "Source: results/runs/scaleup_rerun/analysis/descriptive_statistics.csv (Evaluated N = 1,679 minimal pairs)"
    ws3['A2'].font = italic_note_font

    headers_pll = [
        "Track Scope", "Pair Count (N)", "Mean ΔMeanLogP", "Median Δ", "Std Dev", 
        "IQR", "Q25", "Q75", "Min Δ", "Max Δ", "Orig Preferred (N)", "Orig Preferred (%)", 
        "Cont Preferred (N)", "Cont Preferred (%)", "Linguistic Interpretation"
    ]
    style_table_header(ws3, 4, headers_pll)

    desc_df = pd.read_csv(os.path.join(base_results, 'analysis/descriptive_statistics.csv'))
    muril_desc = desc_df[(desc_df['model_name'] == 'google/muril-base-cased') & (desc_df['include_rejected'] == False)]

    # Add ALL_TRACKS summary row
    muril_comb = pd.read_csv(os.path.join(base_results, 'analysis/combined_pair_level_results.csv'))
    muril_all_pairs = muril_comb[muril_comb['model_name'] == 'google/muril-base-cased']

    interp_map = {
        'REALISTIC_SPELLING_ERROR': 'Severe plausibility penalty; 83.2% original preference confirms sensitivity to orthographic noise',
        'VALID_WORD_CONTEXT': 'Strong contextual sensitivity; 94.2% original preference against incongruous contextual substitutions',
        'SYNONYM_SUBSTITUTION': 'Near-preservation of semantic plausibility; 58.8% original preference reflects stylistic/frequency nuances'
    }

    row_pos = 5
    for _, r in muril_desc.iterrows():
        track = r['track']
        n = int(r['n_pairs'])
        m_delta = float(r['delta_meanlp_mean'])
        med_delta = float(r['delta_meanlp_median'])
        sd_delta = float(r['delta_meanlp_std'])
        iqr_delta = float(r['delta_meanlp_iqr'])
        q25 = float(r['delta_meanlp_q25'])
        q75 = float(r['delta_meanlp_q75'])
        min_d = float(r['delta_meanlp_min'])
        max_d = float(r['delta_meanlp_max'])
        orig_pref_n = int(r['delta_meanlp_n_negative'])
        orig_pref_pct = orig_pref_n / n
        cont_pref_n = int(r['delta_meanlp_n_positive'])
        cont_pref_pct = cont_pref_n / n
        note = interp_map.get(track, "")

        row_vals = [track, n, m_delta, med_delta, sd_delta, iqr_delta, q25, q75, min_d, max_d, orig_pref_n, orig_pref_pct, cont_pref_n, cont_pref_pct, note]
        fill = zebra_fill if row_pos % 2 == 0 else white_fill

        for c_idx, val in enumerate(row_vals, start=1):
            c = ws3.cell(row=row_pos, column=c_idx, value=val)
            c.font = bold_font if c_idx == 1 else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx == 2 or c_idx in [11, 13]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [3, 4, 5, 6, 7, 8, 9, 10]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx in [12, 14]:
                c.alignment = align_right
                c.number_format = '0.0%'
            else:
                c.alignment = align_left
        ws3.row_dimensions[row_pos].height = 22
        row_pos += 1

    # Overall Primary Benchmark row
    all_n = len(muril_all_pairs)
    all_m = float(muril_all_pairs['delta_mean_log_prob'].mean())
    all_med = float(muril_all_pairs['delta_mean_log_prob'].median())
    all_sd = float(muril_all_pairs['delta_mean_log_prob'].std())
    all_iqr = float(muril_all_pairs['delta_mean_log_prob'].quantile(0.75) - muril_all_pairs['delta_mean_log_prob'].quantile(0.25))
    all_q25 = float(muril_all_pairs['delta_mean_log_prob'].quantile(0.25))
    all_q75 = float(muril_all_pairs['delta_mean_log_prob'].quantile(0.75))
    all_min = float(muril_all_pairs['delta_mean_log_prob'].min())
    all_max = float(muril_all_pairs['delta_mean_log_prob'].max())
    all_orig_n = int((muril_all_pairs['delta_mean_log_prob'] < 0).sum())
    all_orig_pct = all_orig_n / all_n
    all_cont_n = int((muril_all_pairs['delta_mean_log_prob'] > 0).sum())
    all_cont_pct = all_cont_n / all_n

    all_row = ["ALL_TRACKS (PRIMARY)", all_n, all_m, all_med, all_sd, all_iqr, all_q25, all_q75, all_min, all_max, all_orig_n, all_orig_pct, all_cont_n, all_cont_pct, "Global primary benchmark summary (N=1,679 minimal pairs)"]
    for c_idx, val in enumerate(all_row, start=1):
        c = ws3.cell(row=row_pos, column=c_idx, value=val)
        c.font = bold_font
        c.fill = summary_fill
        c.border = thick_bottom
        if c_idx in [2, 11, 13]:
            c.alignment = align_right
            c.number_format = '#,##0'
        elif c_idx in [3, 4, 5, 6, 7, 8, 9, 10]:
            c.alignment = align_right
            c.number_format = '+0.0000;-0.0000;0.0000'
        elif c_idx in [12, 14]:
            c.alignment = align_right
            c.number_format = '0.0%'
        else:
            c.alignment = align_left
    ws3.row_dimensions[row_pos].height = 24

    # Chart on sheet 3
    chart3 = BarChart()
    chart3.type = "col"
    chart3.style = 12
    chart3.title = "MuRIL Plausibility Shift (ΔMeanLogP) by Track"
    chart3.y_axis.title = "Signed ΔMeanLogP"
    chart3.height = 12
    chart3.width = 18

    data3 = Reference(ws3, min_col=3, min_row=4, max_col=4, max_row=7)
    cats3 = Reference(ws3, min_col=1, min_row=5, max_row=7)
    chart3.add_data(data3, titles_from_data=True)
    chart3.set_categories(cats3)
    ws3.add_chart(chart3, "B11")

    ws3.auto_filter.ref = "A4:O8"
    ws3.freeze_panes = 'A5'
    auto_fit_cols(ws3)

    # =========================================================================
    # 4. XLM-R PLL Results
    # =========================================================================
    print("  Creating sheet 4: XLM-R PLL Results...")
    ws4 = wb.create_sheet(title="XLM-R PLL Results")
    ws4.views.sheetView[0].showGridLines = True

    ws4['A1'] = "4. XLM-RoBERTa Pseudo-Log-Likelihood (PLL) Scoring Results (FacebookAI/xlm-roberta-base)"
    ws4['A1'].font = title_font
    ws4['A2'] = "Source: results/runs/scaleup_rerun/analysis/descriptive_statistics.csv (Evaluated N = 1,679 minimal pairs)"
    ws4['A2'].font = italic_note_font

    style_table_header(ws4, 4, headers_pll)

    xlm_desc = desc_df[(desc_df['model_name'] == 'FacebookAI/xlm-roberta-base') & (desc_df['include_rejected'] == False)]
    xlm_all_pairs = muril_comb[muril_comb['model_name'] == 'FacebookAI/xlm-roberta-base']

    interp_map_xlm = {
        'REALISTIC_SPELLING_ERROR': 'Significant plausibility penalty (76.4% original preferred); less severe than MuRIL',
        'VALID_WORD_CONTEXT': 'Robust contextual sensitivity (82.7% original preferred) against incongruous substitutions',
        'SYNONYM_SUBSTITUTION': 'Near-perfect interchangeability (mean Δ = -0.0098; 50.6% preference indicates near-parity)'
    }

    row_pos = 5
    for _, r in xlm_desc.iterrows():
        track = r['track']
        n = int(r['n_pairs'])
        m_delta = float(r['delta_meanlp_mean'])
        med_delta = float(r['delta_meanlp_median'])
        sd_delta = float(r['delta_meanlp_std'])
        iqr_delta = float(r['delta_meanlp_iqr'])
        q25 = float(r['delta_meanlp_q25'])
        q75 = float(r['delta_meanlp_q75'])
        min_d = float(r['delta_meanlp_min'])
        max_d = float(r['delta_meanlp_max'])
        orig_pref_n = int(r['delta_meanlp_n_negative'])
        orig_pref_pct = orig_pref_n / n
        cont_pref_n = int(r['delta_meanlp_n_positive'])
        cont_pref_pct = cont_pref_n / n
        note = interp_map_xlm.get(track, "")

        row_vals = [track, n, m_delta, med_delta, sd_delta, iqr_delta, q25, q75, min_d, max_d, orig_pref_n, orig_pref_pct, cont_pref_n, cont_pref_pct, note]
        fill = zebra_fill if row_pos % 2 == 0 else white_fill

        for c_idx, val in enumerate(row_vals, start=1):
            c = ws4.cell(row=row_pos, column=c_idx, value=val)
            c.font = bold_font if c_idx == 1 else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx == 2 or c_idx in [11, 13]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [3, 4, 5, 6, 7, 8, 9, 10]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx in [12, 14]:
                c.alignment = align_right
                c.number_format = '0.0%'
            else:
                c.alignment = align_left
        ws4.row_dimensions[row_pos].height = 22
        row_pos += 1

    # XLM Overall Primary Benchmark row
    all_n_x = len(xlm_all_pairs)
    all_m_x = float(xlm_all_pairs['delta_mean_log_prob'].mean())
    all_med_x = float(xlm_all_pairs['delta_mean_log_prob'].median())
    all_sd_x = float(xlm_all_pairs['delta_mean_log_prob'].std())
    all_iqr_x = float(xlm_all_pairs['delta_mean_log_prob'].quantile(0.75) - xlm_all_pairs['delta_mean_log_prob'].quantile(0.25))
    all_q25_x = float(xlm_all_pairs['delta_mean_log_prob'].quantile(0.25))
    all_q75_x = float(xlm_all_pairs['delta_mean_log_prob'].quantile(0.75))
    all_min_x = float(xlm_all_pairs['delta_mean_log_prob'].min())
    all_max_x = float(xlm_all_pairs['delta_mean_log_prob'].max())
    all_orig_n_x = int((xlm_all_pairs['delta_mean_log_prob'] < 0).sum())
    all_orig_pct_x = all_orig_n_x / all_n_x
    all_cont_n_x = int((xlm_all_pairs['delta_mean_log_prob'] > 0).sum())
    all_cont_pct_x = all_cont_n_x / all_n_x

    all_row_x = ["ALL_TRACKS (PRIMARY)", all_n_x, all_m_x, all_med_x, all_sd_x, all_iqr_x, all_q25_x, all_q75_x, all_min_x, all_max_x, all_orig_n_x, all_orig_pct_x, all_cont_n_x, all_cont_pct_x, "Global primary benchmark summary (N=1,679 minimal pairs)"]
    for c_idx, val in enumerate(all_row_x, start=1):
        c = ws4.cell(row=row_pos, column=c_idx, value=val)
        c.font = bold_font
        c.fill = summary_fill
        c.border = thick_bottom
        if c_idx in [2, 11, 13]:
            c.alignment = align_right
            c.number_format = '#,##0'
        elif c_idx in [3, 4, 5, 6, 7, 8, 9, 10]:
            c.alignment = align_right
            c.number_format = '+0.0000;-0.0000;0.0000'
        elif c_idx in [12, 14]:
            c.alignment = align_right
            c.number_format = '0.0%'
        else:
            c.alignment = align_left
    ws4.row_dimensions[row_pos].height = 24

    # Chart on sheet 4
    chart4 = BarChart()
    chart4.type = "col"
    chart4.style = 13
    chart4.title = "XLM-RoBERTa Plausibility Shift (ΔMeanLogP) by Track"
    chart4.y_axis.title = "Signed ΔMeanLogP"
    chart4.height = 12
    chart4.width = 18

    data4 = Reference(ws4, min_col=3, min_row=4, max_col=4, max_row=7)
    cats4 = Reference(ws4, min_col=1, min_row=5, max_row=7)
    chart4.add_data(data4, titles_from_data=True)
    chart4.set_categories(cats4)
    ws4.add_chart(chart4, "B11")

    ws4.auto_filter.ref = "A4:O8"
    ws4.freeze_panes = 'A5'
    auto_fit_cols(ws4)

    # =========================================================================
    # 5. Cross-Model Comparison
    # =========================================================================
    print("  Creating sheet 5: Cross-Model Comparison...")
    ws5 = wb.create_sheet(title="Cross-Model Comparison")
    ws5.views.sheetView[0].showGridLines = True

    ws5['A1'] = "5. Cross-Model Comparison: MuRIL vs. XLM-RoBERTa Plausibility Concordance (N = 1,679)"
    ws5['A1'].font = title_font
    ws5['A2'] = "Source: results/runs/scaleup_rerun/analysis/model_comparison.csv"
    ws5['A2'].font = italic_note_font

    headers5 = [
        "Track Scope", "Pair Count (N)", "Direction Both Negative (N)", "Direction Both Positive (N)", 
        "XLM Neg / MuRIL Pos (N)", "XLM Pos / MuRIL Neg (N)", "Directional Agreement Rate (%)", 
        "Spearman Rank rs (ΔMeanLogP)", "p-value (rs)", "95% CI Lower", "95% CI Upper", "Methodological Note"
    ]
    style_table_header(ws5, 4, headers5)

    comp_df = pd.read_csv(os.path.join(base_results, 'analysis/model_comparison.csv'))

    for r_idx, r in comp_df.iterrows():
        row_num = r_idx + 5
        is_all = r['track_scope'] == 'ALL_TRACKS'
        fill = summary_fill if is_all else (zebra_fill if row_num % 2 == 0 else white_fill)
        fnt = bold_font if is_all else regular_font

        row_vals = [
            r['track_scope'], int(r['n_pairs']), int(r['direction_both_negative']), 
            int(r['direction_both_positive']), int(r['direction_xlm_neg_muril_pos']), 
            int(r['direction_xlm_pos_muril_neg']), float(r['direction_agreement_rate']), 
            float(r['spearman_r_delta_meanlp']), float(r['p_value']), 
            float(r['ci_95_lo']), float(r['ci_95_hi']), r['note']
        ]

        for c_idx, val in enumerate(row_vals, start=1):
            c = ws5.cell(row=row_num, column=c_idx, value=val)
            c.font = fnt
            c.fill = fill
            c.border = border_all
            if c_idx in [2, 3, 4, 5, 6]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx == 7:
                c.alignment = align_right
                c.number_format = '0.00%'
            elif c_idx in [8, 10, 11]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx == 9:
                c.alignment = align_right
                c.number_format = '< 1e-15' if val < 1e-10 else '0.0000'
            else:
                c.alignment = align_left
        ws5.row_dimensions[row_num].height = 22

    # Chart on sheet 5
    chart5 = BarChart()
    chart5.type = "col"
    chart5.style = 14
    chart5.title = "Directional Plausibility Agreement & Rank Correlation"
    chart5.y_axis.title = "Rate / Correlation"
    chart5.height = 12
    chart5.width = 18

    data5 = Reference(ws5, min_col=7, min_row=4, max_col=8, max_row=8)
    cats5 = Reference(ws5, min_col=1, min_row=5, max_row=8)
    chart5.add_data(data5, titles_from_data=True)
    chart5.set_categories(cats5)
    ws5.add_chart(chart5, "B11")

    ws5['A17'] = "Analytical Findings:"
    ws5['A17'].font = bold_note_font
    ws5['A18'] = "1. Global Concordance: Overall directional agreement across all 1,679 pairs is 73.67% with Spearman rs = +0.5496 (p < 10^-15, 95% CI [0.5153, 0.5821])."
    ws5['A18'].font = italic_note_font
    ws5['A19'] = "2. Decoupling on Synonyms: Agreement drops to 60.22% (rs = +0.2271) on synonyms, demonstrating that stylistic preferences diverge between the multilingual generalist and Indic specialist."
    ws5['A19'].font = italic_note_font

    ws5.auto_filter.ref = "A4:L8"
    ws5.freeze_panes = 'A5'
    auto_fit_cols(ws5)

    # =========================================================================
    # 6. Explanation Stability
    # =========================================================================
    print("  Creating sheet 6: Explanation Stability...")
    ws6 = wb.create_sheet(title="Explanation Stability")
    ws6.views.sheetView[0].showGridLines = True

    ws6['A1'] = "6. Visible-Target Explanation Stability under Devanagari Spelling Perturbations (N = 1,005)"
    ws6['A1'].font = title_font
    ws6['A2'] = "Source: results/runs/scaleup_rerun/dashboard_data/stability_summary.csv"
    ws6['A2'].font = italic_note_font

    headers6 = [
        "Model Checkpoint", "Explanation Method", "Evaluated Subset", "Pair Count (N)", 
        "Stage 6 Masked ρ (Artifact)", "Stage 6 Masked Cosine", "Visible-Target Mean ρ", 
        "Visible-Target Median ρ", "Visible-Target Mean Cosine", "Visible-Target Median Cosine", 
        "Methodological Finding & Alignment Note"
    ]
    style_table_header(ws6, 4, headers6)

    stab_df = pd.read_csv(os.path.join(base_results, 'dashboard_data/stability_summary.csv'))

    for r_idx, r in stab_df.iterrows():
        row_num = r_idx + 5
        m_name = "XLM-RoBERTa" if "xlm" in r['model_name'].lower() else "MuRIL"
        method = "Attention" if r['method'] == 'attention' else "Integrated Gradients"
        subset = r['subset'].replace('_', ' ').title()
        n = int(r['pair_count'])
        s6_rho = float(r['stage6_masked_target_stability_rho'])
        s6_cos = float(r['stage6_masked_target_cosine'])
        vt_m_rho = float(r['visible_target_stability_rho_mean'])
        vt_med_rho = float(r['visible_target_stability_rho_median'])
        vt_m_cos = float(r['visible_target_cosine_mean'])
        vt_med_cos = float(r['visible_target_cosine_median'])
        note = r['methodological_note']

        is_pooled = 'Pooled' in subset
        fill = summary_fill if is_pooled else (zebra_fill if row_num % 2 == 0 else white_fill)
        fnt = bold_font if is_pooled else regular_font

        row_vals = [m_name, method, subset, n, s6_rho, s6_cos, vt_m_rho, vt_med_rho, vt_m_cos, vt_med_cos, note]

        for c_idx, val in enumerate(row_vals, start=1):
            c = ws6.cell(row=row_num, column=c_idx, value=val)
            c.font = fnt
            c.fill = fill
            c.border = border_all
            if c_idx == 4:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [5, 6, 7, 8, 9, 10]:
                c.alignment = align_right
                c.number_format = '0.0000'
            else:
                c.alignment = align_left
        ws6.row_dimensions[row_num].height = 22

    # Chart on sheet 6
    chart6 = BarChart()
    chart6.type = "col"
    chart6.style = 10
    chart6.title = "Visible-Target Explanation Stability: Attention vs. Integrated Gradients"
    chart6.y_axis.title = "Metric Value"
    chart6.height = 12
    chart6.width = 18

    # Compare cols 7 and 9 for rows 5, 8, 11, 14 (pooled rows)
    # Build chart block
    ws6['A19'] = "Configuration"
    ws6['B19'] = "Mean Rank Stability (ρ)"
    ws6['C19'] = "Mean Cosine Similarity"
    ws6['A20'] = "XLM-R Attention"
    ws6['B20'] = 0.6258
    ws6['C20'] = 0.9353
    ws6['A21'] = "XLM-R IG"
    ws6['B21'] = 0.3319
    ws6['C21'] = 0.8890
    ws6['A22'] = "MuRIL Attention"
    ws6['B22'] = 0.8027
    ws6['C22'] = 0.9518
    ws6['A23'] = "MuRIL IG"
    ws6['B23'] = 0.2560
    ws6['C23'] = 0.9818

    data6 = Reference(ws6, min_col=2, min_row=19, max_col=3, max_row=23)
    cats6 = Reference(ws6, min_col=1, min_row=20, max_row=23)
    chart6.add_data(data6, titles_from_data=True)
    chart6.set_categories(cats6)
    ws6.add_chart(chart6, "E19")

    ws6['A25'] = "Methodological Resolution:"
    ws6['A25'].font = bold_note_font
    ws6['A26'] = "1. The Stage 6 Masked-Target Artifact: In Stage 6, masking the target word in both sentences completely removed the spelling perturbation at the target locus, yielding an illusory perfect stability (rho = 1.0000, cosine = 1.0000)."
    ws6['A26'].font = italic_note_font
    ws6['A27'] = "2. The Stage 7 Visible-Target Protocol: Keeping the target visible exposes the actual model attribution dynamics: Attention achieves 1.9x to 3.1x higher rank stability than IG, while IG preserves high directional cosine similarity."
    ws6['A27'].font = italic_note_font

    ws6.auto_filter.ref = "A4:K16"
    ws6.freeze_panes = 'A5'
    auto_fit_cols(ws6)

    # =========================================================================
    # 7. Strict Single-Subword Stability
    # =========================================================================
    print("  Creating sheet 7: Strict Single-Subword Stability...")
    ws7 = wb.create_sheet(title="Strict Single-Subword Stability")
    ws7.views.sheetView[0].showGridLines = True

    ws7['A1'] = "7. Strict Single-Subword Stability Analysis (Exact 1:1 Token Alignment)"
    ws7['A1'].font = title_font
    ws7['A2'] = "Source: results/runs/scaleup_rerun/stability/stability_pair_level.csv (Filtered for strict single-subword pairs)"
    ws7['A2'].font = italic_note_font

    # Section A: Summary
    ws7['A4'] = "A. Summary Comparison of Strict Single-Subword Cohort"
    ws7['A4'].font = section_font

    headers7_a = ["Model Checkpoint", "Explanation Method", "Eligible Pairs (N)", "Mean Rank ρ", "Median Rank ρ", "Mean Cosine", "Median Cosine", "Alignment Validity"]
    style_table_header(ws7, 5, headers7_a)

    strict_summary = [
        ["XLM-RoBERTa", "Attention", 52, 0.6306, 0.7746, 0.9349, 0.9598, "Exact 1:1 token alignment (target = 1 subword in both original and perturbed)"],
        ["XLM-RoBERTa", "Integrated Gradients", 52, 0.4210, 0.5442, 0.9026, 0.9313, "Exact 1:1 token alignment (target = 1 subword in both original and perturbed)"],
        ["MuRIL", "Attention", 197, 0.8053, 0.9000, 0.9725, 0.9861, "Exact 1:1 token alignment (target = 1 subword in both original and perturbed)"],
        ["MuRIL", "Integrated Gradients", 197, 0.3471, 0.4000, 0.9868, 0.9885, "Exact 1:1 token alignment (target = 1 subword in both original and perturbed)"]
    ]

    for r_idx, row in enumerate(strict_summary, start=6):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        for c_idx, val in enumerate(row, start=1):
            c = ws7.cell(row=r_idx, column=c_idx, value=val)
            c.font = bold_font if c_idx in [1, 2] else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx == 3:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [4, 5, 6, 7]:
                c.alignment = align_right
                c.number_format = '0.0000'
            else:
                c.alignment = align_left
        ws7.row_dimensions[r_idx].height = 22

    # Section B: Pair-Level Sample Records
    ws7['A12'] = "B. Sample Strict Single-Subword Pair Records (First 25 Pairs)"
    ws7['A12'].font = section_font

    headers7_b = ["Pair ID", "Model", "Method", "Target Original", "Target Contrast", "Visible-Target Rank ρ", "Visible-Target Cosine", "Original Tokens", "Contrast Tokens"]
    style_table_header(ws7, 13, headers7_b)

    stab_rel = pd.read_csv(os.path.join(base_results, 'dashboard_data/stability_faithfulness_relationship.csv'))
    pri_bench = pd.read_csv(os.path.join(base_data, 'PRIMARY_BENCHMARK_ADJUDICATED.csv'))
    strict_pairs = stab_rel[stab_rel['subset'] == 'strict_single_subword'].merge(
        pri_bench[['pair_id', 'target_original', 'target_contrast']], on='pair_id', how='left'
    )
    sample_strict = strict_pairs.head(25)

    for r_idx, (_, r) in enumerate(sample_strict.iterrows(), start=14):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        m_short = "XLM-R" if "xlm" in r['model_name'].lower() else "MuRIL"
        vals = [
            r['pair_id'], m_short, r['method'], str(r.get('target_original', '')), str(r.get('target_contrast', '')),
            float(r['visible_target_stability_rho']), float(r['visible_target_cosine_similarity']),
            1, 1
        ]
        for c_idx, val in enumerate(vals, start=1):
            c = ws7.cell(row=r_idx, column=c_idx, value=val)
            c.font = regular_font
            c.fill = fill
            c.border = border_all
            if c_idx in [6, 7]:
                c.alignment = align_right
                c.number_format = '0.0000'
            elif c_idx in [8, 9]:
                c.alignment = align_right
                c.number_format = '#,##0'
            else:
                c.alignment = align_left
        ws7.row_dimensions[r_idx].height = 20

    chart7 = BarChart()
    chart7.type = "col"
    chart7.style = 11
    chart7.title = "Strict Single-Subword Stability Metrics"
    chart7.y_axis.title = "Value"
    chart7.height = 12
    chart7.width = 18

    # Chart reference block
    ws7['K5'] = "Condition"
    ws7['L5'] = "Mean Rank ρ"
    ws7['M5'] = "Mean Cosine"
    for idx, r_src in enumerate(range(6, 10), start=6):
        ws7.cell(row=idx, column=11, value=f"{ws7.cell(row=r_src, column=1).value[:5]} {ws7.cell(row=r_src, column=2).value[:3]}")
        ws7.cell(row=idx, column=12, value=ws7.cell(row=r_src, column=4).value)
        ws7.cell(row=idx, column=13, value=ws7.cell(row=r_src, column=6).value)
        ws7.cell(row=idx, column=12).number_format = '0.0000'
        ws7.cell(row=idx, column=13).number_format = '0.0000'

    data7 = Reference(ws7, min_col=12, min_row=5, max_col=13, max_row=9)
    cats7 = Reference(ws7, min_col=11, min_row=6, max_row=9)
    chart7.add_data(data7, titles_from_data=True)
    chart7.set_categories(cats7)
    ws7.add_chart(chart7, "K12")

    ws7.auto_filter.ref = "A5:H9"
    ws7.freeze_panes = 'A6'
    auto_fit_cols(ws7)

    # =========================================================================
    # 8, 9, 10. Faithfulness (10%, 20%, 30% Erasure)
    # =========================================================================
    faith_df = pd.read_csv(os.path.join(base_results, 'dashboard_data/faithfulness_summary.csv'))

    fractions_info = [
        (0.10, "Faithfulness - 10% Erasure", "8. Explanation Faithfulness under 10% Context Token Erasure (f = 0.10)", 8),
        (0.20, "Faithfulness - 20% Erasure", "9. Explanation Faithfulness under 20% Context Token Erasure (f = 0.20)", 9),
        (0.30, "Faithfulness - 30% Erasure", "10. Explanation Faithfulness under 30% Context Token Erasure (f = 0.30)", 10),
    ]

    headers_faith = [
        "Model Checkpoint", "Explanation Method", "Evaluated Subset", "Evaluated Sentences (N)", 
        "Mean Masked Tokens (k)", "Mean Top-k Logit Drop", "Median Top Drop", 
        "Mean Bottom-k Drop (Control)", "Median Bottom Drop", "Mean Random-k Drop", 
        "Median Random Drop", "Mean Faithfulness Gap", "Median Faithfulness Gap", 
        "Win Rate vs. Bottom Control (%)", "Win Rate vs. Random (%)", "Theoretical & Causal Interpretation"
    ]

    for f_val, sheet_title, page_title, sheet_num in fractions_info:
        print(f"  Creating sheet {sheet_num}: {sheet_title}...")
        ws_f = wb.create_sheet(title=sheet_title)
        ws_f.views.sheetView[0].showGridLines = True

        ws_f['A1'] = page_title
        ws_f['A1'].font = title_font
        ws_f['A2'] = f"Source: results/runs/scaleup_rerun/dashboard_data/faithfulness_summary.csv (Evaluated at fraction f = {f_val:.2f})"
        ws_f['A2'].font = italic_note_font

        style_table_header(ws_f, 4, headers_faith)

        sub_f = faith_df[abs(faith_df['fraction'] - f_val) < 0.001]

        row_pos = 5
        for _, r in sub_f.iterrows():
            m_name = "XLM-RoBERTa" if "xlm" in r['model_name'].lower() else "MuRIL"
            method = "Attention" if r['method'] == 'attention' else "Integrated Gradients"
            subset = r['subset'].replace('_', ' ').title()
            n_sent = int(r['n_evaluated_sentences'])
            k_tok = float(r['k_tokens_mean'])
            top_m = float(r['top_k_logit_drop_mean'])
            top_med = float(r['top_k_logit_drop_median'])
            bot_m = float(r['bottom_k_logit_drop_mean'])
            bot_med = float(r['bottom_k_logit_drop_median'])
            rnd_m = float(r['random_k_logit_drop_mean'])
            rnd_med = float(r['random_k_logit_drop_median'])
            gap_m = float(r['faithfulness_gap_mean'])
            gap_med = float(r['faithfulness_gap_median'])
            win_bot = float(r['win_rate_vs_bottom'])
            win_rnd = float(r['win_rate_vs_random'])

            if m_name == "XLM-RoBERTa" and method == "Attention":
                c_interp = "Consistently positive faithfulness gap; attention routes discrete causal features effectively."
            elif m_name == "MuRIL" and method == "Integrated Gradients":
                c_interp = "Operates near or below chance; continuous path integrals mismatch discrete token replacement."
            else:
                c_interp = "Standard discrete erasure behavior."

            is_pooled = 'All' in subset
            fill = summary_fill if is_pooled else (zebra_fill if row_pos % 2 == 0 else white_fill)
            fnt = bold_font if is_pooled else regular_font

            vals = [
                m_name, method, subset, n_sent, k_tok, top_m, top_med, bot_m, bot_med, 
                rnd_m, rnd_med, gap_m, gap_med, win_bot, win_rnd, c_interp
            ]

            for c_idx, val in enumerate(vals, start=1):
                c = ws_f.cell(row=row_pos, column=c_idx, value=val)
                c.font = fnt
                c.fill = fill
                c.border = border_all
                if c_idx == 4:
                    c.alignment = align_right
                    c.number_format = '#,##0'
                elif c_idx == 5:
                    c.alignment = align_right
                    c.number_format = '0.00'
                elif c_idx in [6, 7, 8, 9, 10, 11, 12, 13]:
                    c.alignment = align_right
                    c.number_format = '+0.0000;-0.0000;0.0000'
                elif c_idx in [14, 15]:
                    c.alignment = align_right
                    c.number_format = '0.00%'
                else:
                    c.alignment = align_left
            ws_f.row_dimensions[row_pos].height = 22
            row_pos += 1

        # Chart on faithfulness sheet
        chart_f = BarChart()
        chart_f.type = "col"
        chart_f.style = 11
        chart_f.title = f"Faithfulness Win Rates vs. Bottom Control (f = {f_val:.2f})"
        chart_f.y_axis.title = "Win Rate (%)"
        chart_f.height = 12
        chart_f.width = 18

        # Chart summary block
        ws_f['A13'] = "Model & Method"
        ws_f['B13'] = "Win Rate vs. Bottom (%)"
        ws_f['C13'] = "Mean Faithfulness Gap"
        
        # Populate from pooled rows (5, 7, 9, 11)
        r_map = [5, 7, 9, 11]
        for idx, r_src in enumerate(r_map, start=14):
            ws_f.cell(row=idx, column=1, value=f"{ws_f.cell(row=r_src, column=1).value} {ws_f.cell(row=r_src, column=2).value}")
            ws_f.cell(row=idx, column=2, value=ws_f.cell(row=r_src, column=14).value)
            ws_f.cell(row=idx, column=3, value=ws_f.cell(row=r_src, column=12).value)
            ws_f.cell(row=idx, column=2).number_format = '0.0%'
            ws_f.cell(row=idx, column=3).number_format = '+0.0000;-0.0000;0.0000'

        data_f = Reference(ws_f, min_col=2, min_row=13, max_col=2, max_row=17)
        cats_f = Reference(ws_f, min_col=1, min_row=14, max_row=17)
        chart_f.add_data(data_f, titles_from_data=True)
        chart_f.set_categories(cats_f)
        ws_f.add_chart(chart_f, "E13")

        ws_f.auto_filter.ref = f"A4:P{row_pos-1}"
        ws_f.freeze_panes = 'A5'
        auto_fit_cols(ws_f)

    # =========================================================================
    # 11. Stability–Faithfulness Correlations
    # =========================================================================
    print("  Creating sheet 11: Stability–Faithfulness Correlations...")
    ws11 = wb.create_sheet(title="Stability-Faithfulness Corrs")
    ws11.views.sheetView[0].showGridLines = True

    ws11['A1'] = "11. Stability–Faithfulness Correlation Matrix (RQ5; N = 1,005 Spelling Pairs)"
    ws11['A1'].font = title_font
    ws11['A2'] = "Source: results/runs/scaleup_rerun/dashboard_data/stability_faithfulness_relationship.csv"
    ws11['A2'].font = italic_note_font

    headers11 = [
        "Model Checkpoint", "Explanation Method", "Evaluated Subset", "Sample Size (N)", 
        "Spearman Rank rs", "p-value (rs)", "Pearson Linear r", "p-value (r)", 
        "Empirical Statistical Interpretation", "Linguistic & XAI Nuance"
    ]
    style_table_header(ws11, 4, headers11)

    table6_data = [
        ["XLM-RoBERTa", "Attention", "Pooled (All-Scorable)", 953, 0.0607, 0.0612, 0.0564, 0.0816, "Non-Significant (p > 0.05)", "No consistent positive association between stability and faithfulness"],
        ["XLM-RoBERTa", "Attention", "Strict Single-Subword", 52, 0.2472, 0.0773, 0.2949, 0.0338, "Non-Significant Rank (p > 0.05)", "Spearman rank non-significant; linear Pearson r significant positive at p < 0.05"],
        ["XLM-RoBERTa", "Integrated Gradients", "Pooled (All-Scorable)", 953, 0.0632, 0.0510, 0.0495, 0.1270, "Non-Significant (p > 0.05)", "Attribution stability does not track causal faithfulness under feature erasure"],
        ["XLM-RoBERTa", "Integrated Gradients", "Strict Single-Subword", 52, 0.1647, 0.2434, 0.1464, 0.3005, "Non-Significant (p > 0.05)", "No significant rank or linear association under exact 1:1 token alignment"],
        ["MuRIL", "Attention", "Pooled (All-Scorable)", 808, -0.0442, 0.2099, -0.0790, 0.0248, "Weak Inverse Linear (r < 0, p < 0.05)", "Weak negative Pearson correlation; rank correlation non-significant"],
        ["MuRIL", "Attention", "Strict Single-Subword", 197, -0.1924, 0.0067, -0.1129, 0.1141, "Weak Inverse Rank (rs < 0, p < 0.01)", "Statistically significant weak negative rank correlation under exact alignment"],
        ["MuRIL", "Integrated Gradients", "Pooled (All-Scorable)", 808, 0.0214, 0.5442, 0.0290, 0.4108, "Non-Significant (p > 0.05)", "Continuous gradient stability does not predict discrete masking faithfulness"],
        ["MuRIL", "Integrated Gradients", "Strict Single-Subword", 197, 0.0344, 0.6316, -0.0037, 0.9592, "Non-Significant (p > 0.05)", "Near-zero correlation across both rank and linear formulations"]
    ]

    for r_idx, row in enumerate(table6_data, start=5):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        for c_idx, val in enumerate(row, start=1):
            c = ws11.cell(row=r_idx, column=c_idx, value=val)
            c.font = bold_font if c_idx in [1, 2, 9] else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx == 4:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [5, 7]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx in [6, 8]:
                c.alignment = align_right
                c.number_format = '0.0000'
            else:
                c.alignment = align_left
        ws11.row_dimensions[r_idx].height = 22

    # Chart on sheet 11
    chart11 = BarChart()
    chart11.type = "col"
    chart11.style = 12
    chart11.title = "Stability vs. Faithfulness Correlations (Spearman rs vs. Pearson r)"
    chart11.y_axis.title = "Correlation Coefficient"
    chart11.height = 12
    chart11.width = 18

    # Chart reference block
    ws11['A15'] = "Condition"
    ws11['B15'] = "Spearman rs"
    ws11['C15'] = "Pearson r"
    for idx, r_src in enumerate(range(5, 13), start=16):
        ws11.cell(row=idx, column=1, value=f"{ws11.cell(row=r_src, column=1).value[:5]} {ws11.cell(row=r_src, column=2).value[:3]} ({ws11.cell(row=r_src, column=3).value[:6]})")
        ws11.cell(row=idx, column=2, value=ws11.cell(row=r_src, column=5).value)
        ws11.cell(row=idx, column=3, value=ws11.cell(row=r_src, column=7).value)
        ws11.cell(row=idx, column=2).number_format = '+0.0000;-0.0000;0.0000'
        ws11.cell(row=idx, column=3).number_format = '+0.0000;-0.0000;0.0000'

    data11 = Reference(ws11, min_col=2, min_row=15, max_col=3, max_row=23)
    cats11 = Reference(ws11, min_col=1, min_row=16, max_row=23)
    chart11.add_data(data11, titles_from_data=True)
    chart11.set_categories(cats11)
    ws11.add_chart(chart11, "E15")

    ws11['A26'] = "Core Scientific & Statistical Conclusion (RQ5):"
    ws11['A26'].font = bold_note_font
    ws11['A27'] = "1. Overall Empirical Interpretation: Across all evaluated configurations, there is no consistent positive association between explanation stability and faithfulness. Some weak negative associations occur for MuRIL Attention (pooled Pearson r = -0.0790, p = 0.0248; strict single-subword Spearman rho = -0.1924, p = 0.0067), while other combinations are non-significant (p > 0.05)."
    ws11['A27'].font = italic_note_font
    ws11['A28'] = "2. Scientific Nuance: We do NOT claim that these results mathematically prove independence across all neural architectures, establish causal isolation, or rule out all sample-size limitations. Rather, they demonstrate empirically that explanation stability under spelling noise cannot serve as a reliable proxy for causal explanation faithfulness."
    ws11['A28'].font = italic_note_font

    ws11.auto_filter.ref = "A4:J12"
    ws11.freeze_panes = 'A5'
    auto_fit_cols(ws11)

    # =========================================================================
    # 12. Template Sensitivity
    # =========================================================================
    print("  Creating sheet 12: Template Sensitivity...")
    ws12 = wb.create_sheet(title="Template Sensitivity")
    ws12.views.sheetView[0].showGridLines = True

    ws12['A1'] = "12. Secondary Template Sensitivity Benchmark Analysis (N = 1,957 Minimal Pairs Across 278 Frames)"
    ws12['A1'].font = title_font
    ws12['A2'] = "Source: results/runs/scaleup_rerun/template_sensitivity/analysis/ (Contains Primary Benchmark N=1,679 + 278 template variants; NOT independent)"
    ws12['A2'].font = italic_note_font

    # Section A: Track Breakdown Table
    ws12['A4'] = "A. Template Sensitivity Benchmark Descriptive Statistics by Track"
    ws12['A4'].font = section_font

    headers12 = [
        "Model Checkpoint", "Experimental Track", "Pair Count (N)", "Mean ΔMeanLogP", 
        "Median Δ", "Std Dev", "IQR", "Min Δ", "Max Δ", "Orig Preferred (N)", 
        "Orig Preferred (%)", "Cont Preferred (N)", "Cont Preferred (%)"
    ]
    style_table_header(ws12, 5, headers12)

    tpl_desc = pd.read_csv(os.path.join(base_results, 'template_sensitivity/analysis/descriptive_statistics.csv'))
    tpl_desc = tpl_desc[tpl_desc['include_rejected'] == False]

    for r_idx, (_, r) in enumerate(tpl_desc.iterrows(), start=6):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        m_name = "XLM-RoBERTa" if "xlm" in r['model_name'].lower() else "MuRIL"
        track = r['track']
        n = int(r['n_pairs'])
        m_d = float(r['delta_meanlp_mean'])
        med_d = float(r['delta_meanlp_median'])
        sd_d = float(r['delta_meanlp_std'])
        iqr_d = float(r['delta_meanlp_iqr'])
        min_d = float(r['delta_meanlp_min'])
        max_d = float(r['delta_meanlp_max'])
        orig_n = int(r['delta_meanlp_n_negative'])
        orig_pct = orig_n / n
        cont_n = int(r['delta_meanlp_n_positive'])
        cont_pct = cont_n / n

        vals = [m_name, track, n, m_d, med_d, sd_d, iqr_d, min_d, max_d, orig_n, orig_pct, cont_n, cont_pct]
        for c_idx, val in enumerate(vals, start=1):
            c = ws12.cell(row=r_idx, column=c_idx, value=val)
            c.font = bold_font if c_idx in [1, 2] else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx in [3, 10, 12]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx in [4, 5, 6, 7, 8, 9]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx in [11, 13]:
                c.alignment = align_right
                c.number_format = '0.0%'
            else:
                c.alignment = align_left
        ws12.row_dimensions[r_idx].height = 22

    # Section B: Cross-Model Comparison Table on Template Cohort
    ws12['A14'] = "B. Cross-Model Agreement on Template Sensitivity Benchmark (N = 1,957)"
    ws12['A14'].font = section_font

    headers12_b = ["Track Scope", "Pair Count (N)", "Direction Both Negative (N)", "Direction Both Positive (N)", "Directional Agreement (%)", "Spearman Rank rs", "p-value (rs)", "95% CI Lower", "95% CI Upper"]
    style_table_header(ws12, 15, headers12_b)

    tpl_comp = pd.read_csv(os.path.join(base_results, 'template_sensitivity/analysis/model_comparison.csv'))
    for r_idx, (_, r) in enumerate(tpl_comp.iterrows(), start=16):
        is_all = r['track_scope'] == 'ALL_TRACKS'
        fill = summary_fill if is_all else (zebra_fill if r_idx % 2 == 0 else white_fill)
        fnt = bold_font if is_all else regular_font

        vals = [
            r['track_scope'], int(r['n_pairs']), int(r['direction_both_negative']), int(r['direction_both_positive']),
            float(r['direction_agreement_rate']), float(r['spearman_r_delta_meanlp']), float(r['p_value']),
            float(r['ci_95_lo']), float(r['ci_95_hi'])
        ]
        for c_idx, val in enumerate(vals, start=1):
            c = ws12.cell(row=r_idx, column=c_idx, value=val)
            c.font = fnt
            c.fill = fill
            c.border = border_all
            if c_idx in [2, 3, 4]:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx == 5:
                c.alignment = align_right
                c.number_format = '0.00%'
            elif c_idx in [6, 8, 9]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx == 7:
                c.alignment = align_right
                c.number_format = '< 1e-15' if val < 1e-10 else '0.0000'
            else:
                c.alignment = align_left
        ws12.row_dimensions[r_idx].height = 22

    # Section C: Cohort Comparison Table: Primary vs. Template
    ws12['A22'] = "C. Cohort Comparison: Primary Benchmark (N=1,679) vs. Template Benchmark (N=1,957)"
    ws12['A22'].font = section_font

    headers12_c = ["Metric", "Primary Benchmark (N=1,679)", "Template Sensitivity Benchmark (N=1,957)", "Difference / Consistency Assessment"]
    style_table_header(ws12, 23, headers12_c)

    cohort_comp_rows = [
        ["Total Evaluated Minimal Pairs", 1679, 1957, "+278 template variants across 278 frames"],
        ["Cross-Model Directional Agreement Rate", 0.7367, 0.7128, "Highly consistent (-2.39 pp difference)"],
        ["Cross-Model Spearman Rank Correlation (rs)", 0.5496, 0.5344, "Highly consistent (p < 10^-15 across both)"],
        ["MuRIL Spelling Error Preference Rate", 0.8318, 0.8190, "Consistent harsh penalty on orthographic errors"],
        ["XLM-R Spelling Error Preference Rate", 0.7642, 0.7079, "Consistent moderate penalty on orthographic errors"],
        ["XLM-R Synonym Mean Delta MeanLogP", -0.0098, -0.0026, "Consistent near-zero delta (semantic preservation)"]
    ]

    for r_idx, row in enumerate(cohort_comp_rows, start=24):
        fill = zebra_fill if r_idx % 2 == 0 else white_fill
        for c_idx, val in enumerate(row, start=1):
            c = ws12.cell(row=r_idx, column=c_idx, value=val)
            c.font = bold_font if c_idx == 1 else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx in [2, 3]:
                c.alignment = align_right
                if isinstance(val, int):
                    c.number_format = '#,##0'
                elif isinstance(val, float) and val > 0.01:
                    c.number_format = '0.00%'
                else:
                    c.number_format = '+0.0000;-0.0000;0.0000'
            else:
                c.alignment = align_left
        ws12.row_dimensions[r_idx].height = 20

    chart12 = BarChart()
    chart12.type = "col"
    chart12.style = 10
    chart12.title = "Primary (N=1,679) vs. Template (N=1,957) Concordance Metrics"
    chart12.y_axis.title = "Value"
    chart12.height = 12
    chart12.width = 18

    data12 = Reference(ws12, min_col=2, min_row=23, max_col=3, max_row=28)
    cats12 = Reference(ws12, min_col=1, min_row=25, max_row=28)
    chart12.add_data(data12, titles_from_data=True)
    chart12.set_categories(cats12)
    ws12.add_chart(chart12, "E23")

    ws12.auto_filter.ref = "A5:M11"
    ws12.freeze_panes = 'A6'
    auto_fit_cols(ws12)

    # =========================================================================
    # 13. Auxiliary Multiword Probe
    # =========================================================================
    print("  Creating sheet 13: Auxiliary Multiword Probe...")
    ws13 = wb.create_sheet(title="Auxiliary Multiword Probe")
    ws13.views.sheetView[0].showGridLines = True

    ws13['A1'] = "13. Auxiliary Multiword Probe Analysis (Fine-Grained 4-Category Taxonomy; N = 12 Minimal Pairs)"
    ws13['A1'].font = title_font
    ws13['A2'] = "Source: data/final/AUXILIARY_MULTIWORD_PROBE.csv & results/runs/scaleup_rerun/auxiliary_probe/analysis/"
    ws13['A2'].font = italic_note_font

    # Section A: 4-Category Taxonomy Breakdown
    ws13['A4'] = "A. Fine-Grained 4-Category Taxonomy Distribution"
    ws13['A4'].font = section_font

    headers13_a = ["Fine-Grained Category Name", "Pair Count (N)", "Proportion (%)", "Linguistic Phenomenon & Alignment Challenge"]
    style_table_header(ws13, 5, headers13_a)

    tax_rows = [
        ["Gender/number agreement changes", 6, 0.5000, "Lexical substitution triggers grammatical agreement ripples in surrounding adjectives/verbs (e.g. sahas dikhaya -> veerta dikhayi)."],
        ["Repeated-target ambiguities", 4, 0.3333, "Sentences where the target token occurs multiple times (e.g. ki... ki), creating token alignment ambiguity."],
        ["Postpositional case insertion", 1, 0.0833, "Lexical substitution requiring insertion of a case marker (door -> faasle par), altering length geometry."],
        ["Collocational light-verb change", 1, 0.0833, "Lexical change altering light verb collocation (bhojan karna -> khana khana), shifting syntactic frame geometry."],
        ["TOTAL AUXILIARY PROBE", 12, 1.0000, "12 challenging edge-case minimal pairs evaluated separately to prevent confounding primary benchmark."]
    ]

    for r_idx, row in enumerate(tax_rows, start=6):
        is_tot = "TOTAL" in row[0]
        fill = summary_fill if is_tot else (zebra_fill if r_idx % 2 == 0 else white_fill)
        fnt = bold_font if is_tot else regular_font
        for c_idx, val in enumerate(row, start=1):
            c = ws13.cell(row=r_idx, column=c_idx, value=val)
            c.font = fnt
            c.fill = fill
            c.border = border_all
            if c_idx == 2:
                c.alignment = align_right
                c.number_format = '#,##0'
            elif c_idx == 3:
                c.alignment = align_right
                c.number_format = '0.0%'
            else:
                c.alignment = align_left
        ws13.row_dimensions[r_idx].height = 22

    # Section B: Full Itemized Table
    ws13['A13'] = "B. Complete Itemized Records for All 12 Minimal Pairs"
    ws13['A13'].font = section_font

    headers13_b = [
        "Pair ID", "Taxonomy Category", "Target Orig", "Target Cont", 
        "Original Sentence", "Contrast Sentence", 
        "MuRIL ΔMeanLogP", "XLM-R ΔMeanLogP", "Directional Agreement"
    ]
    style_table_header(ws13, 14, headers13_b)

    aux_comb = pd.read_csv(os.path.join(base_results, 'auxiliary_probe/analysis/combined_pair_level_results.csv'))
    aux_pairs = pd.read_csv(os.path.join(base_data, 'AUXILIARY_MULTIWORD_PROBE.csv'))

    category_map = {
        'HC_0069': 'Gender/number agreement changes',
        'HC_0113': 'Gender/number agreement changes',
        'HC_1060': 'Repeated-target ambiguities',
        'HC_1067': 'Repeated-target ambiguities',
        'HC_1081': 'Repeated-target ambiguities',
        'HC_1190': 'Repeated-target ambiguities',
        'HC_1863': 'Gender/number agreement changes',
        'HC_1874': 'Gender/number agreement changes',
        'HC_1878': 'Gender/number agreement changes',
        'HC_1919': 'Postpositional case insertion',
        'HC_1934': 'Collocational light-verb change',
        'HC_1943': 'Gender/number agreement changes'
    }

    item_row = 15
    for _, p_row in aux_pairs.iterrows():
        p_id = p_row['pair_id']
        cat = category_map.get(p_id, "Multiword Ripple")
        t_orig = p_row['target_original']
        t_cont = p_row['target_contrast']
        s_orig = p_row['original_sentence']
        s_cont = p_row['contrast_sentence']

        sub_m = aux_comb[(aux_comb['pair_id'] == p_id) & (aux_comb['model_name'] == 'google/muril-base-cased')]
        sub_x = aux_comb[(aux_comb['pair_id'] == p_id) & (aux_comb['model_name'] == 'FacebookAI/xlm-roberta-base')]

        m_delta = float(sub_m['delta_mean_log_prob'].values[0]) if len(sub_m) > 0 else 0.0
        x_delta = float(sub_x['delta_mean_log_prob'].values[0]) if len(sub_x) > 0 else 0.0
        agree = (m_delta < 0 and x_delta < 0) or (m_delta > 0 and x_delta > 0)

        vals = [p_id, cat, t_orig, t_cont, s_orig, s_cont, m_delta, x_delta, "AGREE" if agree else "DISAGREE"]
        fill = zebra_fill if item_row % 2 == 0 else white_fill

        for c_idx, val in enumerate(vals, start=1):
            c = ws13.cell(row=item_row, column=c_idx, value=val)
            c.font = bold_font if c_idx in [1, 9] else regular_font
            c.fill = fill
            c.border = border_all
            if c_idx in [7, 8]:
                c.alignment = align_right
                c.number_format = '+0.0000;-0.0000;0.0000'
            elif c_idx == 9:
                c.alignment = align_center
            else:
                c.alignment = align_left
        ws13.row_dimensions[item_row].height = 20
        item_row += 1

    ws13['A29'] = "Summary Metrics & Linguistic Findings:"
    ws13['A29'].font = bold_note_font
    ws13['A30'] = "1. Directional Agreement: On these 12 multiword edge cases, directional agreement drops to 41.67% (5 out of 12 pairs), compared to 73.67% on the primary benchmark."
    ws13['A30'].font = italic_note_font
    ws13['A31'] = "2. Attribution Challenges: Multiword ripples alter surrounding context words (e.g., gender marking on verbs), creating distributed causal features that single-token attribution and standard alignment protocols cannot isolate cleanly."
    ws13['A31'].font = italic_note_font

    chart13 = BarChart()
    chart13.type = "col"
    chart13.style = 13
    chart13.title = "MuRIL vs. XLM-R Plausibility Shifts on Auxiliary Probe"
    chart13.y_axis.title = "Signed ΔMeanLogP"
    chart13.height = 12
    chart13.width = 18

    data13 = Reference(ws13, min_col=7, min_row=14, max_col=8, max_row=26)
    cats13 = Reference(ws13, min_col=1, min_row=15, max_row=26)
    chart13.add_data(data13, titles_from_data=True)
    chart13.set_categories(cats13)
    ws13.add_chart(chart13, "K14")

    ws13.auto_filter.ref = "A14:I26"
    ws13.freeze_panes = 'A6'
    auto_fit_cols(ws13)

    # Save to paper/ and copy to research_paper/
    out_path_paper = 'hindi-lexical-sensitivity/paper/expanded_experimental_results.xlsx'
    out_path_rp = 'hindi-lexical-sensitivity/research_paper/expanded_experimental_results.xlsx'

    os.makedirs(os.path.dirname(out_path_paper), exist_ok=True)
    wb.save(out_path_paper)
    print(f"Workbook successfully saved to: {out_path_paper} ({os.path.getsize(out_path_paper)} bytes)")

    try:
        os.makedirs(os.path.dirname(out_path_rp), exist_ok=True)
        shutil.copyfile(out_path_paper, out_path_rp)
        print(f"Workbook successfully mirrored to: {out_path_rp}")
    except Exception as e:
        print(f"Note: Could not mirror to research_paper/: {e}")

if __name__ == '__main__':
    create_workbook()
