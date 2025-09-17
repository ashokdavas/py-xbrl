"""
This unittest tests the parsing of locally saved instance documents.
"""

import sys
import unittest
import xml.etree.ElementTree as ET
from xbrl.cache import HttpCache
from xbrl.instance import parse_ixbrl, parse_xbrl, XbrlInstance, _parse_unit_elements
import logging


# abs_file_path: str = str(os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)))

class InstanceTest(unittest.TestCase):
    """
    Unit test for taxonomy.test_parse_taxonomy()
    """

    def test_parse_xbrl_document(self):
        """ Integration test for instance.parse_xbrl_instance() """
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        cache_dir: str = './cache/'
        cache: HttpCache = HttpCache(cache_dir)

        instance_doc_url: str = './tests/data/example.xml'
        inst: XbrlInstance = parse_xbrl(instance_doc_url, cache)
        print(inst)
        self.assertEqual(len(inst.facts), 1)

    def test_parse_ixbrl_document(self):
        """ Integration test for instance.parse_ixbrl_instance() """
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        cache_dir: str = './cache/'
        cache: HttpCache = HttpCache(cache_dir)

        instance_doc_url: str = './tests/data/example.html'
        inst: XbrlInstance = parse_ixbrl(instance_doc_url, cache)
        print(inst)
        self.assertEqual(len(inst.facts), 3)

    def test_pure_unit_added_by_default(self):
        """ Test that pure unit is automatically added when not defined """
        # Create test XML with no pure unit defined
        xml_content = '''
        <root xmlns:xbrli="http://www.xbrl.org/2003/instance">
            <xbrli:unit id="usd">
                <xbrli:measure>iso4217:USD</xbrli:measure>
            </xbrli:unit>
        </root>
        '''
        
        # Parse the XML
        root = ET.fromstring(xml_content)
        unit_elements = root.findall('xbrli:unit', {'xbrli': 'http://www.xbrl.org/2003/instance'})
        
        # Call the function
        unit_dict = _parse_unit_elements(unit_elements)
        
        # Verify pure unit was added
        self.assertIn('pure', unit_dict)
        self.assertEqual(unit_dict['pure'].unit_id, 'pure')
        self.assertEqual(unit_dict['pure'].unit, 'xbrli:pure')

    def test_existing_pure_unit_preserved(self):
        """ Test that existing pure unit definition is not overridden """
        # Create test XML with pure unit already defined
        xml_content = '''
        <root xmlns:xbrli="http://www.xbrl.org/2003/instance">
            <xbrli:unit id="pure">
                <xbrli:measure>custom:pure</xbrli:measure>
            </xbrli:unit>
        </root>
        '''
        
        # Parse the XML
        root = ET.fromstring(xml_content)
        unit_elements = root.findall('xbrli:unit', {'xbrli': 'http://www.xbrl.org/2003/instance'})
        
        # Call the function
        unit_dict = _parse_unit_elements(unit_elements)
        
        # Verify existing pure unit was preserved
        self.assertIn('pure', unit_dict)
        self.assertEqual(unit_dict['pure'].unit, 'custom:pure')


if __name__ == '__main__':
    unittest.main()
