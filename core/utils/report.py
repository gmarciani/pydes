"""
Utility classes that realize reports for experiments.
"""


from collections import OrderedDict
import os


class SimpleReport(object):
    """
    The simplest report for an experiment.
    """

    def __init__(self, title):
        """
        Creates a new report.
        :param title: (string) the title of the report.
        """
        self.title = title
        self.params = OrderedDict()

    def add(self, section_title, param_title, param_value):
        """
        Adds a new parameter to the report.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param param_title: (string) the name of the new parameter.
        :param param_value: (object) the value of the new parameter.
        :return: (void)
        """
        if section_title not in self.params:
            self.params[section_title] = []
        self.params[section_title].append((param_title, param_value))

    def add_all(self, section_title, obj):
        """
        Add all object public attributes.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param obj: the object to scan for attributes.
        :return: (void)
        """
        for attr in obj.__dict__:
            if not attr.startswith("__") and not attr.startswith("_") and not callable(getattr(obj, attr)):
                value = obj.__dict__[attr]
                if isinstance(value, float):
                    self.add(section_title, attr, round(value, 3))
                else:
                    self.add(section_title, attr, value)

    def add_all_attrs(self, section_title, obj, *attrs):
        """
        Add all object attributes.
        :param section_title: (string) the title of the section for the new
        parameter.
        :param obj: the object to scan for attributes.
        :param attrs: the attributes to add.
        :return: (void)
        """
        for attr in attrs:
            if attr in obj.__dict__ and not callable(getattr(obj, attr)):
                value = obj.__dict__[attr]
                if isinstance(value, float):
                    self.add(section_title, attr, round(value, 3))
                else:
                    self.add(section_title, attr, value)

    def get(self, section_title, param_title):
        """
        Retrieve the value of the given parameter.
        :param section_title: the title of the section.
        :param param_title: the name of the arameter.
        :return: the value of the parameter, if present; None, otherwise.
        """
        for elem in self.params[section_title]:
            if elem[0] == param_title:
                return elem[1]
        return None

    def save(self, filename):
        """
        Saves the report onto a file.
        :param filename: (string) the absolute file path.
        """
        #os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w+') as resfile:
            resfile.write(str(self))

    def save_csv(self, filename):
        """
        Saves the report onto a CSV file.
        :param filename: (string) the absolute file path.
        """
        #os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w+") as resfile:
            resfile.write("report_name,")
            for section in self.params:
                headers = ["{}.{}".format(section, p[0]) for p in self.params[section]]
                resfile.write(",".join(headers))
                resfile.write(",")
            resfile.write("\n")
            resfile.write("{},".format(self.title))
            for section in self.params:
                values = [str(p[1]) for p in self.params[section]]
                resfile.write(",".join(values))
                resfile.write(",")
            resfile.write("\n")

    def append_csv(self, filename):
        """
        Append the report onto a CSV file.
        :param filename: (string) the absolute file path.
        """
        with open(filename, "a+") as resfile:
            resfile.write("{},".format(self.title))
            for section in self.params:
                values = [str(p[1]) for p in self.params[section]]
                resfile.write(",".join(values))
                resfile.write(",")
            resfile.write("\n")

    def __str__(self):
        title_separator = '=' * 60

        s = '\n{}\n{:^60}\n{}\n'.format(title_separator, self.title, title_separator)

        for section in self.params.items():
            s += '\n{:^60}\n'.format(section[0])
            for p in section[1]:
                s += '{:.<30}{:.>30}\n'.format(str(p[0]), str(p[1]))

        return s


if __name__ == "__main__":
    for i in range(3):
        report_title = "SIMULATION-{}".format(i)
        report = SimpleReport(report_title)
        report.add("sec_1", "param_1", 10 * i)
        report.add("sec_1", "param_2", 20 * i)
        report.add("sec_2", "param_1", 30 * i)
        report.add("sec_2", "param_2", 40 * i)
        report.add("sec_3", "param_1", 50 * i)
        report.add("sec_3", "param_2", 60 * i)
        report.save(report_title)
        report.save_csv("{}.csv".format(report_title))

    filename = "simulation_overall.csv"
    for i in range(3):
        report_title = "SIMULATION-{}".format(i)
        report = SimpleReport(report_title)
        report.add("sec_1", "param_1", 10 * i)
        report.add("sec_1", "param_2", 20 * i)
        report.add("sec_2", "param_1", 30 * i)
        report.add("sec_2", "param_2", 40 * i)
        report.add("sec_3", "param_1", 50 * i)
        report.add("sec_3", "param_2", 60 * i)
        if i == 0:
            report.save_csv("{}.csv".format(filename))
        else:
            report.append_csv("{}.csv".format(filename))