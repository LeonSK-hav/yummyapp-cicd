import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# ==============================================================================
# CAP DO 1: Bo test co ban cho san (Moi chi dat 35% Coverage)
# ==============================================================================
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ==============================================================================
# CAP DO 2 (TIET 3): SINH VIEN TU TAY LAP TRINH TEST CASE DUOI DAY
# ==============================================================================
class TestMediumLevel(unittest.TestCase):
    """Kiem thu chuc nang ap dung ma khuyen mai apply_promo_code"""

    def test_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        res = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(res, 90000.0)

    def test_promo_offline_connection_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_promo_invalid_code_value_error(self):
        app = YummyApp(network_status="online", os_version=15)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "INVALID_CODE")

    def test_promo_new_os_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        res = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(res, 80000.0)

    def test_promo_old_os_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


class TestHardLevel(unittest.TestCase):
    """Kiem thu chuc nang tim nha hang voi Mocking GPS Service"""

    def setUp(self):
        self.app = YummyApp()

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_in_range(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        expected = ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"]
        self.assertEqual(self.app.get_nearby_restaurants(), expected)

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_out_of_range(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_restaurants_gps_lost_error(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError
        res = self.app.get_nearby_restaurants()
        self.assertEqual(res, "Khong the xac dinh vi tri.")


if __name__ == '__main__':
    unittest.main()