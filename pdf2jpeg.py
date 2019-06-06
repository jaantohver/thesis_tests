import ghostscript

pdf_input_path = "/Users/jaan/Projects/kool/thesis/thesis_tests/pdf_utils/test.pdf"
jpeg_output_path = "/Users/jaan/Projects/kool/thesis/thesis_tests/pdf_utils/images/test%d.jpeg"


def pdf2jpeg(pdf_input_path, jpeg_output_path):
    args = ["pdf2jpeg",  # actual value doesn't matter
            "-dNOPAUSE",
            "-sDEVICE=jpeg",
            "-r144",
            "-sOutputFile=" + jpeg_output_path,
            pdf_input_path]

    ghostscript.Ghostscript(*args)

pdf2jpeg(pdf_input_path, jpeg_output_path)
