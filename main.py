import sys
from subprocess import call

if len(sys.argv) < 2:
    print("No input folder specified.")
    exit()

input_folder = sys.argv[1]

# TODO make this dynamic somehow
ground_truth = [
    "ELAMISLUBA",
    # "BB0021535",
    "NIMI",
    # "ANBARJAFARI",
    # "GHOLAMREZA",
    "KEHTIV KUNI",
    # "05.08.2021",
    "VÄLJAANDMISE KOHT JA KUUPÄEV",
    # "PPA, 05.08.2016",
    "LOA LIIK",
    # "ELAMISLUBA TÖÖTAMISEKS",
    "MÄRKUSED",
    # "RESIDENCE PERMIT",
    # "FOR EMPLOYMENT",
    # "KUNI/UNTIL 31.08.2021",
    # "400688",
    "RESIDENCE PERMIT"
]

deblur_with = [
    ("SRN-Deblur", False),
]
extract_with = [
    ("text_extractor", False),
    ("text_extractor_2", True),
    ("text_extractor_manual", False),
]
ocr_with = [
    ("crnn", False),
    ("crnn.pytorch", False),
    ("tesseract", False),
    ("tesseract_with_custom_dict", False),
]

for value in deblur_with:
    d_script, run = value

    if not run:
        continue

    deblur_path = "_deblurring/" + d_script
    deblur_file = deblur_path + "/main.py"

    print("Running deblurring script - " + deblur_file)

    res = call(["python", "main.py", "../../" + input_folder], cwd=deblur_path)

for d_value in deblur_with:
    d_script, _ = d_value
    d_result = "../../_deblurring/" + d_script + "/res"

    for e_value in extract_with:
        e_script, run = e_value

        if not run:
            continue

        extraction_path = "_extraction/" + e_script
        extraction_file = extraction_path + "/main.py"

        print("Running extraction script - " + extraction_file)

        call(["python", "main.py", d_result, d_script] + ground_truth, cwd=extraction_path)

for d_value in deblur_with:
    d_script, _ = d_value
    for e_value in extract_with:
        e_script, _ = e_value
        e_result = "../../_extraction/" + e_script + "/res/" + d_script

        for o_value in ocr_with:
            o_script, run = o_value

            if not run:
                continue

            ocr_path = "_ocr/" + o_script
            ocr_file = ocr_path + "/main.py"
            output_path = d_script + "/" + e_script

            print("Running OCR script - " + ocr_file)

            res = call(["python", "main.py", e_result, output_path], cwd=ocr_path)
