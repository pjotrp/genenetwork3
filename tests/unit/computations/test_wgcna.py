"""module contains python code for wgcna"""
from unittest import TestCase
from gn3.computations.wgcna import dump_wgcna_data
from gn3.computations.wgcna import compose_wgcna_cmd


class TestWgcna(TestCase):
    """test class for wgcna"""

    def test_compose_wgcna_cmd(self):
        """test for composing wgcna cmd"""
        wgcna_cmd = compose_wgcna_cmd("/wgcna.r", "/tmp/wgcna.json")
        self.assertEqual(wgcna_cmd, f"Rscript /wgcna.r  /tmp/wgcna.json")

    def test_create_json_data(self):
        """test for writing the data to a csv file"""
        # # All the traits we have data for (should not contain duplicates)
        # All the strains we have data for (contains duplicates)

        trait_sample_data = {"1425642_at": {"129S1/SvImJ": 7.142, "A/J": 7.31, "AKR/J": 7.49,
                                            "B6D2F1": 6.899, "BALB/cByJ": 7.172, "BALB/cJ": 7.396},
                             "1457784_at": {"129S1/SvImJ": 7.071, "A/J": 7.05, "AKR/J": 7.313,
                                            "B6D2F1": 6.999, "BALB/cByJ": 7.293, "BALB/cJ": 7.117},
                             "1444351_at": {"129S1/SvImJ": 7.221, "A/J": 7.246, "AKR/J": 7.754,
                                            "B6D2F1": 6.866, "BALB/cByJ": 6.752, "BALB/cJ": 7.269}

                             }

        expected_input = {
            "trait_sample_data": trait_sample_data,
            "TOMtype": "unsigned",
            "minModuleSize": 30
        }

        _results = dump_wgcna_data(expected_input)
