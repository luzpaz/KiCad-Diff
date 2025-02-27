import time
import os
import shutil
import sys
import settings
from scms.generic import scm as generic_scm
from xml.parsers.expat import ParserCreate
from dateutil.parser import isoparse


class scm(generic_scm):
    @staticmethod
    def get_boards(diff1, diff2, prjct_name, kicad_project_path, prjct_path):
        """Given two SVN revisions, write out two kicad_pcb files to their respective
        directories (named after the revision number). Returns the date and time of both commits"""

        if not diff1 == prjct_name:
            artifact1, *tail = diff1.split(" |")
        else:
            artifact1 = "local"

        if not diff2 == prjct_name:
            artifact2, *tail = diff2.split(" |")
        else:
            artifact2 = "local"

        # Using this to fix the path when there is no subproject
        prj_path = kicad_project_path + "/"
        if kicad_project_path == ".":
            prj_path = ""

        if (not diff1 == prjct_name) and (not diff2 == prjct_name):

            cmd = [
                "svn",
                "diff",
                "--summarize",
                "-r",
                artifact1 + ":" + artifact2,
                prj_path + prjct_name,
            ]

            print("")
            print("Getting Boards")
            print(' '.join(cmd))

            stdout, stderr = settings.run_cmd(prjct_path, cmd)
            changed, *boardName = stdout

            if changed != "M":
                print("\nThere is no difference in .kicad_pcb file in selected commits")

        outputDir1 = os.path.join(
            prjct_path, settings.plot_dir, kicad_project_path, artifact1
        )
        if not os.path.exists(outputDir1):
            os.makedirs(outputDir1)

        outputDir2 = os.path.join(
            prjct_path, settings.plot_dir, kicad_project_path, artifact2
        )
        if not os.path.exists(outputDir2):
            os.makedirs(outputDir2)

        svnPath = os.path.join(kicad_project_path, "/")

        print("")
        print("Setting artifacts paths")
        print("svnPath      :", svnPath)

        if not diff1 == prjct_name:
            svnArtifact1 = ["svn", "cat", "-r", artifact1, svnPath]
            print("SVN artifact1: ", ' '.join(svnArtifact1))
        else:
            print("SVN artifact1: ", diff1)

        if not diff2 == prjct_name:
            svnArtifact2 = ["svn", "cat", "-r", artifact2, svnPath]
            print("SVN artifact2: ", ' '.join(svnArtifact2))

        else:
            print("SVN artifact2: ", diff2)

        if not diff1 == prjct_name:
            stdout, stderr = settings.run_cmd(prjct_path, svnArtifact1)
            with open(os.path.join(outputDir1, prjct_name), "w") as fout1:
                fout1.write(stdout)
        else:
            shutil.copyfile(prjct_name, os.path.join(outputDir1, prjct_name))

        if not diff2 == prjct_name:
            stdout, stderr = settings.run_cmd(prjct_path, svnArtifact2)
            with open(os.path.join(outputDir2, prjct_name), "w") as fout2:
                fout2.write(stdout)
        else:
            shutil.copyfile(prjct_name, os.path.join(outputDir2, prjct_name))

        print("")
        print("Check datetime")

        if not diff1 == prjct_name:
            svnDateTime1 = ["svn", "log", "-r", artifact1]
            print(' '.join(svnDateTime1))

        if not diff2 == prjct_name:
            svnDateTime2 = ["svn", "log", "-r", artifact2]
            print(' '.join(svnDateTime2))

        if not diff1 == prjct_name:
            stdout, stderr = settings.run_cmd(prjct_path, svnDateTime1)
            dateTime = stdout

            cmt = (dateTime.splitlines()[1]).split("|")
            _, SVNdate1, SVNtime1, SVNutc, *_ = cmt[2].split(" ")
        else:
            artifact1 = prjct_name
            modTimesinceEpoc = os.path.getmtime(prjct_name)
            SVNdate1 = time.strftime("%Y-%m-%d", time.localtime(modTimesinceEpoc))
            SVNtime1 = time.strftime("%H:%M:%S", time.localtime(modTimesinceEpoc))

        if not diff2 == prjct_name:
            stdout, stderr = settings.run_cmd(prjct_path, svnDateTime2)
            dateTime = stdout

            cmt = (dateTime.splitlines()[1]).split("|")
            _, SVNdate2, SVNtime2, SVNutc, *_ = cmt[2].split(" ")
        else:
            artifact2 = prjct_name
            modTimesinceEpoc = os.path.getmtime(prjct_name)
            SVNdate2 = time.strftime("%Y-%m-%d", time.localtime(modTimesinceEpoc))
            SVNtime2 = time.strftime("%H:%M:%S", time.localtime(modTimesinceEpoc))

        times = SVNdate1 + " " + SVNtime1 + " " + SVNdate2 + " " + SVNtime2

        return artifact1, artifact2, times

    @staticmethod
    def get_artefacts(prjct_path, kicad_project_path, board_file):
        """Returns list of revisions from a directory"""

        cmd = [
            "svn",
            "log",
            "--xml",
            "-r",
            "HEAD:0",
            os.path.join(kicad_project_path, board_file),
        ]
        print("")
        print("Getting Artifacts")
        print(cmd)

        stdout, _ = settings.run_cmd(prjct_path, cmd)
        parser = SvnLogHandler()
        parser.parseString(stdout)
        artifacts = [board_file] + parser.lines

        return artifacts

    @staticmethod
    def get_kicad_project_path(prjct_path):
        """Returns the root folder of the repository"""

        cmd = ["svn", "info", "--show-item", "wc-root"]

        stdout, _ = settings.run_cmd(prjct_path, cmd)
        repo_root_path = stdout.strip()

        kicad_project_path = os.path.relpath(prjct_path, repo_root_path)

        return repo_root_path, kicad_project_path


class SvnLogHandler:
    def __init__(self):
        self.parser = ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.EndElementHandler = self.endElement
        self.parser.CharacterDataHandler = self.characters
        self.lines = []
        self.current_line = ""
        self.save = False

    def parseString(self, data):
        self.parser.Parse(data)

    def startElement(self, name, attrs):
        if name == "logentry":
            self.current_line = "r" + attrs.get("revision")

        else:
            self.save = name == "date" or name == "msg"
        if self.save:
            self.save = name
            self.current_line += " | "

    def endElement(self, name):
        if name == "logentry":
            self.lines.append(self.current_line)

    def characters(self, content):
        if self.save and len(content):
            if self.save == "date":
                self.current_line += isoparse(content).strftime("%Y-%m-%d %H:%M")
            else:
                self.current_line += content
            self.save = False
