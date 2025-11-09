import unittest
from allowance.cli import main

class TestCLI(unittest.TestCase):
    
    def test_command_parsing(self):
        # Test that the CLI correctly parses commands
        result = main(['allowance', 'command_name'])
        self.assertEqual(result, expected_output)

    def test_command_execution(self):
        # Test that the CLI executes commands correctly
        result = main(['allowance', 'command_name', 'arg1', 'arg2'])
        self.assertEqual(result, expected_output)

    def test_invalid_command(self):
        # Test that the CLI handles invalid commands gracefully
        with self.assertRaises(SystemExit):
            main(['allowance', 'invalid_command'])

if __name__ == '__main__':
    unittest.main()