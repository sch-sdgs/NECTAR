from nectar.nectar_class import nectar
import os


def test_is_done():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    n = nectar(dir_path + "/resources/test_config")

    assert n.is_done("S1000000-02") == False


def test_is_done():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    n = nectar(dir_path + "/resources/test_config")

    assert n.is_done("S1000001-02") == True
