import glob
import os

MD_PATTERN = "|-|-|-|:-|"
IGNORED_EXTS = [".txt", ".a", ".o", ".out", ".exe"]
LANGUAGES = {
    ".c": "C",
    ".cpp": "C++",
    ".csx": "C#",
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".rs": "Rust",
    ".zig": "Zig",
}


def main():
    sites = [
        Website("LeetCode"),
        Website("Baekjoon"),
        Website("AdventOfCode"),
    ]
    Markdown(sites)


class Website:
    def __init__(self, folder):
        self.__folder: str = folder
        self.__files: list[str] = []
        self.__lang_count: dict[str, int] = {}
        self.__recent = ""

        # actions
        self.__filter_files()
        self.__count_files()
        self.__find_recent()

    def get_stats(self) -> tuple[str, int, str, str]:
        # total files count
        total_file_count = 0
        for count in self.__lang_count.values():
            total_file_count += count

        # most used language (convert file type to language name)
        most_used_language = ""
        if len(self.__lang_count) != 0:
            most_used_language = max(
                self.__lang_count, key=(lambda key: self.__lang_count[key])
            )
            if most_used_language in LANGUAGES.keys():
                most_used_language = LANGUAGES[most_used_language]
            else:
                most_used_language = "Other"

        return self.__folder, total_file_count, most_used_language, self.__recent

    def __filter_files(self):
        for dirpath, _, filenames in os.walk(self.__folder):
            for file in filenames:
                # remove files without a file extension or files that start with a dot
                if file.find(".") == -1 and file.startswith("."):
                    pass

                # remove files that should be ignored
                elif file[file.find(".") :] in IGNORED_EXTS:
                    pass

                # add files to self.files
                else:
                    dir: str = dirpath.replace("\\", "/") + "/"
                    self.__files.append(
                        (dir[1:] if dir.startswith("/") else dir) + file
                    )

    def __count_files(self):
        for file in self.__files:
            file_ext = file[file.find(".") :]
            if file_ext in self.__lang_count.keys():
                self.__lang_count[file_ext] += 1
            else:
                self.__lang_count[file_ext] = 1

    def __find_recent(self):
        if len(self.__files) != 0:
            self.__recent = max(self.__files, key=os.path.getmtime).removeprefix(
                self.__folder + "/"
            )


class Markdown:
    def __init__(self, sites):
        self.__file = "README.md"
        self.__sites: list[Website] = sites
        self.__updated_content = []

        # actions
        self.__update_md()
        self.__write_md()

    def __update_md(self):
        # add existing content till found '|' (which is the start of a markdown table)
        with open(self.__file, "r", encoding="utf-8") as md:
            lines = md.readlines()

            for line, text in enumerate(lines):
                if text.startswith(MD_PATTERN):
                    break
                else:
                    self.__updated_content.append(text)
        md.close()

        # add new table
        self.__updated_content.append(MD_PATTERN + "\n")
        for site in self.__sites:
            folder, total_file_count, most_used_language, recent = site.get_stats()
            self.__updated_content.append(
                f"|[{folder}]({folder})|{total_file_count}|{most_used_language}|[{recent}]({folder}/{recent.replace(' ', '%20')})|\n"
            )

    def __write_md(self):
        with open(self.__file, "w") as md:
            md.writelines(self.__updated_content)
        md.close()


main()
