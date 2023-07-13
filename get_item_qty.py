
from PyPDF2 import PdfReader
import os


def pdf_to_dict(fname):
    reader = PdfReader(fname)
    text = ''
    for page in reader.pages:
        text = f"{text}\n{page.extract_text()}"
    lines = text.split("\n")
    data = lines[lines.index('Items')+5: lines.index('Item')]
    cleaned_data = []
    for _ in range(len(data)):
        if is_sub_word(cleaned_data, data, _):
            cleaned_data[-1] = f"{cleaned_data[-1]} {data[_]}"
        else:
            cleaned_data.append(data[_])
    output = dict(zip(
        [cleaned_data[_] for _ in range(0, len(cleaned_data), 3)]  # names
        , [cleaned_data[_] for _ in range(1, len(cleaned_data), 3)]  # qty
    ))
    return output


def is_numeric(n):
    try:
        float(n)
        return True
    except ValueError:
        return False


def is_sub_word(cleaned_data, data, idx):
    return idx > 0 and not (is_numeric(cleaned_data[-1]) or is_numeric(data[idx]))


def merge_dict(d1, d2):
    d = d1.copy()
    for k, v in d2.items():
        d[k] = f"{d[k]} + {v}" if k in d else v
    return d


def main(dir_path):
    output = {}
    files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".pdf")]
    print(f"Found files ", files)
    for file in files:
        print(f"Parsing file {file}")
        output = merge_dict(output, pdf_to_dict(file))

    # pretty print output
    for k, v in {key: output[key] for key in sorted(output.keys())}.items():
        print(k, v, sep=" - ")


if __name__ == "__main__":
    dir_name = "pdfs"
    dir_path = os.path.join(os.getcwd(), dir_name)
    main(dir_path)
