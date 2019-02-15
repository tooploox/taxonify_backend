import unittest

from aquascope.util.taxonomy_dictionary_utils import add


class TestAddListToDictionary(unittest.TestCase):
    def test_add_normal_list_to_empty(self):
        dictionary = {}
        elements = ["1", "2", "3"]
        expected_dict = {
            "1": {
                "2": {
                    "3": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_single_elem_list(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = ["1"]
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            },
            "1": {}
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_subelem_already_present(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = ["A", "B"]
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_elem_already_present(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = ["A", "B", "C"]
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_list_with_nan(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = ["1", float('NaN'), "2"]
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            },
            "1": {}
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_empty_list_to_empty(self):
        dictionary = {}
        elements = []
        expected_dict = {}
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_empty_list_to_non_empty(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = []
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_normal_list_to_non_empty_and_no_match(self):
        dictionary = {
            "A": {
                "B": {
                    "C": {}
                }
            }
        }
        elements = ["1", "2", "3"]
        expected_dict = {
            "A": {
                "B": {
                    "C": {}
                }
            },
            "1": {
                "2": {
                    "3": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_normal_list_to_non_empty_and_partial_match(self):
        dictionary = {
            "1": {
                "2": {
                    "C": {
                        "D": {}
                    }
                }
            }
        }
        elements = ["1", "2", "3", "4", "5"]
        expected_dict = {
            "1": {
                "2": {
                    "C": {
                        "D": {}
                    },
                    "3": {
                        "4": {
                            "5": {}
                        }
                    }
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_capitalization(self):
        dictionary = {
            "alpha": {
                "Beta": {
                    "Charlie": {}
                }
            }
        }
        elements = ["alpha", "Beta", "cHaRlIe Daniel", "delta"]
        expected_dict = {
            "Alpha": {
                "Beta": {
                    "Charlie daniel": {
                        "Delta": {}
                    }
                }
            },
            "alpha": {
                "Beta": {
                    "Charlie": {},
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)
