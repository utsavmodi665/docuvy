# Docuvy Rebrand & Merge Feature TODO

## Approved Plan Status: Implementation Started ✅

### Phase 1: Project Setup & Branding [5/6]
- [x] Updated TODO.md with detailed step tracking
- [ ] Create static/logo.svg (gradient Docuvy logo)
- [x] Update main.py: Full rebrand (name, CSS colors/fonts/rounded/shadows, layout, logo) → created main_docuvy.py
- [x] Add tabs: "Convert" | "Merge to PDF"
- [x] Style: hero header, upload card, gradient buttons (#2563EB→#7C3AED), minimal design


### Phase 2: Merge Functionality [3/3]
- [x] Add merge_pdfs() and to_pdf_if_needed() in converter.py
- [x] Extend convert_file dispatcher for "merge_to_pdf"
- [x] Implement Merge tab UI logic in main.py (auto-convert → merge → download)



### Phase 3: Polish & Test [0/4]
- [ ] Update requirements.txt if needed (none expected)
- [ ] Test all features: single/batch convert, merge mixed formats
- [ ] Graceful errors (LibreOffice, unsupported files)
- [ ] Mark complete, attempt_completion

### Run Command
```
streamlit run main.py
```

**Next Step**: Test with `streamlit run main_docuvy.py` then rename to main.py if good [Phase 3]



