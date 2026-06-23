#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import subprocess
import sys
import os

class TestMosecomExtractor(unittest.TestCase):
    
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
        
        # Should execute successfully
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        
        # Should have output
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should contain expected format
        self.assertIn(" : ", stdout, "Output doesn't match expected format 'Величина : значение'")
        
        # Should contain some expected substances
        expected_substances = ["CO", "NO2", "H2S", "PM10", "CH4", "NO"]
        found_substances = 0
        for substance in expected_substances:
            if substance in stdout:
                found_substances += 1
        
        # Should find at least some of the expected substances
        self.assertGreater(found_substances, 0, f"Didn't find expected substances in output: {stdout}")
    
    def test_long_name_option(self):
        """Test --long-name option."""
        returncode, stdout, stderr = self.run_script(['--long-name'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should contain long names instead of short names
        long_names = ["Оксид углерода", "Диоксид азота", "Сероводород", "Взвешенные частицы PM10", "Метан", "Оксид азота"]
        found_long_names = 0
        for name in long_names:
            if name in stdout:
                found_long_names += 1
        
        self.assertGreater(found_long_names, 0, f"Didn't find expected long names in output: {stdout}")
    
    def test_gas_type_option(self):
        """Test --gas-type option."""
        # Test with CO
        returncode, stdout, stderr = self.run_script(['--gas-type', 'CO'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should contain only a numeric value (or empty)
        # Remove whitespace and newlines
        value = stdout.strip()
        self.assertTrue(value == '' or self._is_numeric(value), 
                       f"Expected numeric value for --gas-type CO, got: '{value}'")
    
    def test_gas_type_with_long_name(self):
        """Test --gas-type with long name when --long-name is used."""
        returncode, stdout, stderr = self.run_script(['--gas-type', 'Диоксид азота', '--long-name'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        
        # Should contain only a numeric value (or empty)
        value = stdout.strip()
        self.assertTrue(value == '' or self._is_numeric(value), 
                       f"Expected numeric value for --gas-type 'Диоксид азота', got: '{value}'")
    
    def test_measure_mg_m3_option(self):
        """Test --measure-mg-m3 option."""
        returncode, stdout, stderr = self.run_script(['--measure-mg-m3'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should still contain the expected format
        self.assertIn(" : ", stdout, "Output doesn't match expected format 'Величина : значение'")
    
    def test_current_data_option(self):
        """Test --current-data option."""
        returncode, stdout, stderr = self.run_script(['--current-data'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should be same as default behavior
        default_returncode, default_stdout, _ = self.run_script()
        self.assertEqual(returncode, default_returncode, "Return codes differ between default and --current-data")
    
    def test_help_option(self):
        """Test --help option."""
        returncode, stdout, stderr = self.run_script(['--help'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        self.assertIn("usage:", stdout, "Help output doesn't contain usage information")
    
    def test_url_option(self):
        """Test --url option with default URL."""
        returncode, stdout, stderr = self.run_script([
            '--url', 'https://mosecom.mos.ru/m1-6-moskvorechye-saburovo/'
        ])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
    
    def test_combination_of_options(self):
        """Test combination of --long-name and --measure-mg-m3."""
        returncode, stdout, stderr = self.run_script(['--long-name', '--measure-mg-m3'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        self.assertTrue(len(stdout.strip()) > 0, "Script produced no output")
        
        # Should contain long names
        long_names = ["Оксид углерода", "Диоксид азота", "Сероводород", "Взвешенные частицы PM10", "Метан", "Оксид азота"]
        found_long_names = 0
        for name in long_names:
            if name in stdout:
                found_long_names += 1
        
        self.assertGreater(found_long_names, 0, f"Didn't find expected long names in combined output: {stdout}")
    
    def test_historical_data_option(self):
        """Test --historical-data option (should return empty as it's not implemented)."""
        returncode, stdout, stderr = self.run_script(['--historical-data'])
        
        self.assertEqual(returncode, 0, f"Script failed with stderr: {stderr}")
        # Historical data is not implemented, so should return empty or minimal output
        # This is expected behavior as noted in the script comments
    
    def _is_numeric(self, value):
        """Check if a string represents a numeric value."""
        try:
            float(value)
            return True
        except ValueError:
            return False

if __name__ == '__main__':
    unittest.main()