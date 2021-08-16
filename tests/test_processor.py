from datetime import datetime
from unittest import TestCase, mock

from goodwe.processor import GoodWeXSProcessor, InvalidDataException


class TestProcessor(TestCase):
    def test_process_data(self):
        validator = mock.Mock()
        validator.return_value = True

        with open('sample/inverter_data', 'rb') as f:
            mock_data = f.read()

        processor = GoodWeXSProcessor(validator)
        data = processor.process_data(mock_data)

        self.assertEqual(data.date, datetime(year=2021, month=8, day=8, hour=10, minute=49, second=52))
        self.assertEqual(data.volts_dc, 99.8)
        self.assertEqual(data.current_dc, 1.8)
        self.assertEqual(data.volts_ac, 234.7)
        self.assertEqual(data.current_ac, 0.7)
        self.assertEqual(data.frequency_ac, 50.02)
        self.assertEqual(data.generation_today, 0.3),
        self.assertEqual(data.generation_total, 201.4)
        self.assertEqual(data.rssi, 70)
        self.assertEqual(data.operational_hours, 895)
        self.assertEqual(data.temperature, 30.3)
        self.assertEqual(data.power, 189)
        self.assertEqual(data.status, 'Normal')

    def test_process_data_invalid_data(self):
        validator = mock.Mock()
        validator.return_value = False

        processor = GoodWeXSProcessor(validator)
        self.assertRaises(InvalidDataException, processor.process_data, b'')
