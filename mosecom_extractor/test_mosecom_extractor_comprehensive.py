#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import subprocess
import sys
import os
from unittest.mock import patch, MagicMock

# Add the current directory to Python path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mosecom_extractor


class TestMosecomExtractorFunctions(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Sample HTML content for testing based on actual page structure
        self.sample_html = '''
        <html>
        <body>
            <h3>Последние полученные данные                    </h3>
            <div id="trl-one" class="tabs-red-line">
                <span id="pdktext" class="active">доли</span>
                <span >мг/м<sup>3</sup></span>
            </div>
            <div id="cft" class="clear-content content-for-tab">
                <div class="content-tab active">
                    <div class="item-block m-flip lm4 count-green">
                        <div class="m-flip__content">
                            <div class="front">
                                <div class="norma">
                                    <div class="text-norma">
                                        CO                                    </div>
                                    <div class="info-icon"></div>
                                </div>
                                <div class="center-mode">
                                    <div class="item-type">
                                        <span class="first-type">
                                            Оксид углерода                                        </span>
                                        <span class="total-type">
                                            <span class="this-count ">
                                                0,047                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="item-block m-flip lm4 count-green">
                        <div class="m-flip__content">
                            <div class="front">
                                <div class="norma">
                                    <div class="text-norma">
                                        NO2                                    </div>
                                    <div class="info-icon"></div>
                                </div>
                                <div class="center-mode">
                                    <div class="item-type">
                                        <span class="first-type">
                                            Диоксид азота                                        </span>
                                        <span class="total-type">
                                            <span class="this-count ">
                                                0,078                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="dinamic">
        </body>
        </html>
        '''
    
    def test_parse_current_data_short_names(self):
        """Test parsing current data with short names."""
        data = mosecom_extractor.parse_current_data(self.sample_html, name_type='short', measure_unit='parts')
        
        self.assertEqual(len(data), 2)
        self.assertIn(('CO', '0.047'), data)
        self.assertIn(('NO2', '0.078'), data)
    
    def test_parse_current_data_long_names(self):
        """Test parsing current data with long names."""
        data = mosecom_extractor.parse_current_data(self.sample_html, name_type='long', measure_unit='parts')
        
        self.assertEqual(len(data), 2)
        self.assertIn(('Оксид углерода', '0.047'), data)
        self.assertIn(('Диоксид азота', '0.078'), data)
    
    def test_parse_current_data_duplicates_removed(self):
        """Test that duplicate entries are removed."""
        html_with_duplicates = '''
        <html>
        <body>
            <h3>Последние полученные данные                    </h3>
            <div id="trl-one" class="tabs-red-line">
                <span id="pdktext" class="active">доли</span>
                <span >мг/м<sup>3</sup></span>
            </div>
            <div id="cft" class="clear-content content-for-tab">
                <div class="content-tab active">
                    <div class="item-block m-flip lm4 count-green">
                        <div class="m-flip__content">
                            <div class="front">
                                <div class="norma">
                                    <div class="text-norma">
                                        CO                                    </div>
                                    <div class="info-icon"></div>
                                </div>
                                <div class="center-mode">
                                    <div class="item-type">
                                        <span class="first-type">
                                            Оксид углерода                                        </span>
                                        <span class="total-type">
                                            <span class="this-count ">
                                                0,047                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="item-block m-flip lm4 count-green">
                        <div class="m-flip__content">
                            <div class="front">
                                <div class="norma">
                                    <div class="text-norma">
                                        NO2                                    </div>
                                    <div class="info-icon"></div>
                                </div>
                                <div class="center-mode">
                                    <div class="item-type">
                                        <span class="first-type">
                                            Диоксид азота                                        </span>
                                        <span class="total-type">
                                            <span class="this-count ">
                                                0,078                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="item-block m-flip lm4 count-green">
                        <div class="m-flip__content">
                            <div class="front">
                                <div class="norma">
                                    <div class="text-norma">
                                        CO                                    </div>
                                    <div class="info-icon"></div>
                                </div>
                                <div class="center-mode">
                                    <div class="item-type">
                                        <span class="first-type">
                                            Оксид углерода                                        </span>
                                        <span class="total-type">
                                            <span class="this-count ">
                                                0,050                                            </span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="dinamic">
        </body>
        </html>
        '''
        
        data = mosecom_extractor.parse_current_data(html_with_duplicates, name_type='short', measure_unit='parts')
        
        # Should still only have 2 entries, not 3
        self.assertEqual(len(data), 2)
        # Should have the first value, not the duplicate
        self.assertIn(('CO', '0.047'), data)
        self.assertIn(('NO2', '0.078'), data)
    
    def test_format_output_all_data(self):
        """Test formatting output for all data."""
        data = [('CO', '0.047'), ('NO2', '0.078')]
        output = mosecom_extractor.format_output(data)
        
        expected = "CO : 0.047\nNO2 : 0.078"
        self.assertEqual(output, expected)
    
    def test_format_output_specific_gas(self):
        """Test formatting output for specific gas type."""
        data = [('CO', '0.047'), ('NO2', '0.078')]
        output = mosecom_extractor.format_output(data, gas_type='CO')
        
        self.assertEqual(output, '0.047')
    
    def test_format_output_specific_gas_not_found(self):
        """Test formatting output for non-existent gas type."""
        data = [('CO', '0.047'), ('NO2', '0.078')]
        output = mosecom_extractor.format_output(data, gas_type='SO2')
        
        self.assertEqual(output, '')
    
    def test_parse_historical_data(self):
        """Test that historical data parsing returns empty list."""
        data = mosecom_extractor.parse_historical_data(self.sample_html)
        self.assertEqual(data, [])


class TestMosecomExtractorIntegration(unittest.TestCase):
    
    def run_script(self, args=None):
        """Run the mosecom_extractor.py script with given arguments and return output."""
        if args is None:
            args = []
        
        cmd = [sys.executable, 'mosecom_extractor.py'] + args
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, '', 'Timeout'
    
    def test_default_behavior(self):
        """Test default behavior of the script."""
        returncode, stdout, stderr = self.run_script()
        
        # Should execute successfully (may fail due to network, but shouldn't crash)
        # We're testing the structure, not the network connectivity
        self.assertIn(returncode, [0, 1], f"Script exited with unexpected code: {returncode}")
    
    def test_help_option(self):
        """Test --help option."""
        returncode, stdout, stderr = self.run_script(['--help'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        self.assertIn("usage:", stdout, "Help output doesn't contain usage information")
    
    def test_long_name_option_structure(self):
        """Test that --long-name option produces different output structure."""
        # We can't test the exact content due to network dependency,
        # but we can test that it runs without error
        returncode, stdout, stderr = self.run_script(['--long-name'])
        
        # Should execute successfully (may fail due to network, but shouldn't crash on argument parsing)
        self.assertIn(returncode, [0, 1], f"Script exited with unexpected code: {returncode}")


if __name__ == '__main__':
    unittest.main()