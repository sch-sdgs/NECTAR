from producers.StarLims import StarLimsApi
import ConfigParser
import os
import errno
import subprocess
import glob

class nectar():

    def __init__(self,config):
        self.config = config

        configP = ConfigParser.ConfigParser()
        configP.readfp(open(config))

        self.ip = configP.get('nectar config', 'ip')
        self.port = configP.get('nectar config', 'port')
        self.username = configP.get('nectar config', 'username')
        self.query = configP.get('nectar config', 'query')
        self.database = configP.get('nectar config', 'database')

    def mkdir_p(self,path):
        """
        emulates unix mkdir -p

        :param path: path to create
        """
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def is_done(self,container):
        """
        check the database file to see if sample has been sent

        :param container: container id of sample
        :return: Boolean
        """
        if os.path.isfile(self.database) == False:
            print os.path.split(self.database)[0]
            self.mkdir_p(os.path.split(self.database)[0])
            open(self.database, 'a').close()


        with open(self.database,"r") as f:
            for line in f:
                database_container, database_red = line.rstrip("\n").split("\t")
                if database_container == container:
                    return True

        return False

    def get_nectar_samples(self):
        s = StarLimsApi.get_nectar_project(self.query)
        return s

    def get_file_list_for_sample(self,containerid,worklist,year):
        """
        gets list of file for transfer for a sample

        :param containerid:
        :param worklist:
        :param year:
        """
        file_extensions = ["_Aligned_Sorted_Clipped_PCRDuped_IndelsRealigned.bam",
                          "_Variants.vcf",
                          "_coverage_summary.txt",
                          "_variants_LessLQsPolys.xlsx"
                          ]

        all_files = []

        for ext in file_extensions:
            files = glob.glob("/".join(["/results/Analysis/HiSeq",year,worklist,containerid,"*"+ext]))
            if len(files) == 0:
                files = glob.glob("/".join(["/results/Analysis/HiSeq", year, worklist, containerid,"*", "*" + ext]))
            if len(files) == 0:
                files = glob.glob("/".join(["/results/Analysis/HiSeq", year, worklist, containerid, "*", "Results", "*" + ext]))
            all_files.append(files[0])

        return all_files


    def transfer_sample(self,containerid):
        pass


    def run_local_checksum(self,file_path):
        pass

    def run_remote_checksum(self,file_path):
        pass

print nectar("/home/bioinfo/config").get_file_list_for_sample("S1103728-02","1701491","2017")


