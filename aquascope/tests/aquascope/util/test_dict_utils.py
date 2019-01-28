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
            "a": {
                "b": {
                    "c": {}
                }
            }
        }
        elements = ["1"]
        expected_dict = {
            "a": {
                "b": {
                    "c": {}
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
            "a": {
                "b": {
                    "c": {}
                }
            }
        }
        elements = []
        expected_dict = {
            "a": {
                "b": {
                    "c": {}
                }
            }
        }
        add(dictionary, elements)
        self.assertDictEqual(dictionary, expected_dict)

    def test_add_normal_list_to_non_empty_and_no_match(self):
        dictionary = {
            "a": {
                "b": {
                    "c": {}
                }
            }
        }
        elements = ["1", "2", "3"]
        expected_dict = {
            "a": {
                "b": {
                    "c": {}
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
                    "c": {
                        "d": {}
                    }
                }
            }
        }
        elements = ["1", "2", "3", "4", "5"]
        expected_dict = {
            "1": {
                "2": {
                    "c": {
                        "d": {}
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
