from pydoc import classname
import re
input_file = "mae.bbl"
output_file = "mae.bib"
cite_match = r"\\bibitem{.*}"
cite_find = re.compile(r'{(.*)}')
block_find = r"\\newblock (.*)"
journal_find = r"\\newblock {\\em (.*)}, .*"
year_find = r"\\newblock .*, (.*)."
booktitle_find = r"\\newblock In {\\em (.*)}, .*."
only_year = r"\\newblock (.*)."

journal_templete = """@article{{{cite},
  title={{{title}}},
  author={{{author}}},
  journal={{{journal}}},
  year={{{year}}}
}}
"""
booktitle_templete = """@article{{{cite},
  title={{{title}}},
  author={{{author}}},
  booktitle={{{booktitle}}},
  year={{{year}}}
}}
"""
year_templete = """@article{{{cite},
  title={{{title}}},
  author={{{author}}},
  year={{{year}}}
}}
"""

data_list = []
with open(input_file) as f:
    line = f.readline()
    idx = 0
    data_dict = {}
    while line:
        if re.match(cite_match, line):
            idx = 0
            data_dict = {}
            data_dict['cite'] = re.findall(cite_find, line)[0]
            line = f.readline()
            print("cite:", data_dict["cite"])

            data_dict["author"] = ""
            while not re.match(block_find, line):
                data_dict["author"] += line
                line = f.readline()
            data_dict["author"] = data_dict["author"][:-2].replace(","," and")
            print("author:", data_dict["author"])

            data_dict["title"] = line
            line = f.readline()
            while not re.match(block_find, line):
                data_dict["title"] += line
                line = f.readline()
            data_dict["title"] = re.findall(
                block_find, data_dict["title"])[0][:-1]
            print("title:", data_dict["title"])

            if re.match(journal_find, line):
                data_dict["journal"] = re.findall(journal_find, line)[0]
                data_dict["year"] = re.findall(year_find, line)[0]
                data_dict["booktitle"] = ""
                print("journal:", data_dict["journal"])
                print("year", data_dict["year"])
            elif re.match(booktitle_find, line):
                data_dict["booktitle"] = re.findall(
                    booktitle_find, line)[0]
                data_dict["year"] = re.findall(year_find, line)[0]
                data_dict["journal"] = ""
                print("booktitle:", data_dict["booktitle"])
                print("year", data_dict["year"])
            elif re.match(only_year, line):
                data_dict["journal"] = ""
                data_dict["booktitle"] = ""
                data_dict["year"] = re.findall(only_year, line)[0]
                print("year", data_dict["year"])
            else:
                print(line)
                print("error")
                exit()

            data_list += [data_dict]
        line = f.readline()

with open(output_file, "w+") as f:
    for data_dict in data_list:
        if data_dict["journal"] != "":
            f.write(journal_templete.format(
                cite=data_dict["cite"], title=data_dict["title"], author=data_dict["author"], journal=data_dict["journal"], year=data_dict["year"]))
        elif data_dict["booktitle"] != "":
            f.write(booktitle_templete.format(cite=data_dict["cite"], title=data_dict["title"],
                    author=data_dict["author"], booktitle=data_dict["booktitle"], year=data_dict["year"]))
        else:
            f.write(year_templete.format(
                cite=data_dict["cite"], title=data_dict["title"], author=data_dict["author"], year=data_dict["year"]))

