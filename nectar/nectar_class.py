from producers.StarLims import StarLimsApi
import ConfigParser
import os
import errno
import subprocess
import glob


#remote jobs with ssh key
#https://stackoverflow.com/questions/5327465/using-an-ssh-keyfile-with-fabric

class nectar():
    def __init__(self, config):
        """
        initialse nectar instance, with the config file containing all information needed for nectar sample file transfer

        :param config:
        """
        self.config = config

        configP = ConfigParser.ConfigParser()
        configP.readfp(open(config))

        self.ip = configP.get('nectar config', 'ip')
        self.port = configP.get('nectar config', 'port')
        self.username = configP.get('nectar config', 'username')
        self.query = configP.get('nectar config', 'query')
        self.database = configP.get('nectar config', 'database')
        self.destination = configP.get('nectar config','destination')

    def mkdir_p(self, path):
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

    def is_done(self, container):
        """
        check the database file to see if sample has been sent

        :param container: container id of sample
        :return: Boolean
        """
        if os.path.isfile(self.database) == False:
            print os.path.split(self.database)[0]
            self.mkdir_p(os.path.split(self.database)[0])
            open(self.database, 'a').close()

        with open(self.database, "r") as f:
            for line in f:
                database_container, database_red = line.rstrip("\n").split("\t")
                if database_container == container:
                    return True

        return False

    def get_nectar_samples(self):
        """
        get nectar sample info from starlims

        :return: dictionary of sample info
        """
        s = StarLimsApi.get_nectar_project(self.query)
        return s

    def get_file_list_for_sample(self, containerid, worklist, year):
        """
        gets list of file for transfer for a sample

        :param containerid:
        :param worklist:
        :param year:
        """
        file_extensions = ["_Aligned_Sorted_Clipped_PCRDuped_IndelsRealigned.bam",
                           "_Variants.vcf",
                           "_coverage_summary.txt",
                           "_variants_LessLQsPolys.xlsx",
                           "_gaps_in_sequencing.txt",
                           "_coverage_depth_bases_full_small_panel.txt",
                           "_provenance.txt",
                           "_analysis_log.txt",
                           "_qc.json",
                           "_samtools_stats_all.txt",
                           "_samtools_stats_rmdup.txt",
                           ]

        all_files = []

        for ext in file_extensions:
            files = glob.glob("/".join(["/results/Analysis/HiSeq", year, worklist, containerid, "*" + ext]))
            if len(files) == 0:
                files = glob.glob("/".join(["/results/Analysis/HiSeq", year, worklist, containerid, "*", "*" + ext]))
            if len(files) == 0:
                files = glob.glob(
                    "/".join(["/results/Analysis/HiSeq", year, worklist, containerid, "*", "Results", "*" + ext]))
            all_files.append(files[0])

        return all_files

    def transfer_sample(self, file_list):

        self.mkdir_p(self.destination)

        for file in file_list:
            command = ["rsync","-prc",file,self.username+"@"+self.ip+":"+self.destination]






print nectar("/home/bioinfo/config").get_file_list_for_sample("S1103728-02", "1701491", "2017")
