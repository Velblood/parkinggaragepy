from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from mock import GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage, ParkingGarageError


class TestParkingGarage(TestCase):

    @patch.object(GPIO, "input")
    def test_check_occupancy(self, mock_distance_sensor: Mock):
        mock_distance_sensor.return_value = True
        system = ParkingGarage()
        occupied = system.check_occupancy(system.INFRARED_PIN1)
        self.assertTrue(occupied)

    def test_check_occupancy_raises_error(self):
        system = ParkingGarage()
        self.assertRaises(ParkingGarageError, system.check_occupancy, -1)

    @patch.object(GPIO, "input")
    def test_number_occupied_spots(self, mock_distance_sensor: Mock):
        mock_distance_sensor.side_effect = [True, False, True]
        system = ParkingGarage()
        number = system.get_number_occupied_spots()
        self.assertEqual(2, number)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_parking_fee_same_minutes(self, mock_time: Mock):
        system = ParkingGarage()
        mock_time.return_value = datetime(2024, 11, 6, 16, 0)
        fee = system.calculate_parking_fee(datetime(2024, 11, 6, 14, 0))
        self.assertEqual(5, fee)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_parking_fee_different_minutes(self, mock_time: Mock):
        system = ParkingGarage()
        mock_time.return_value = datetime(2024, 11, 6, 16, 0)
        fee = system.calculate_parking_fee(datetime(2024, 11, 6, 14, 1))
        self.assertEqual(5, fee)

    @patch.object(ParkingGarage, "change_servo_angle")
    def test_open_garage_door(self, mock_serve: Mock):
        system = ParkingGarage()
        system.open_garage_door()
        mock_serve.assert_called_with(12)
        self.assertTrue(system.open_garage_door)

    @patch.object(GPIO, "output")
    def test_open_red_light(self, mock_light: Mock):
        system = ParkingGarage()
        system.turn_on_red_light()
        mock_light.assert_called_with(system.LED_PIN, False)
        self.assertTrue(system.red_light_on)
