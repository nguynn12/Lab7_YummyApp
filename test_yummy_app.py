"""Unit tests cho YummyApp, gồm các ca kiểm thử mocking dịch vụ ngoài."""

import unittest
from unittest.mock import patch

import gps_service
from yummy_app import YummyApp


class TestEasyLevel(unittest.TestCase):
    """Kiểm thử cơ bản chức năng tính tiền giỏ hàng."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 2}), 100_000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95_000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": 0}), 0.0)

    def test_calculate_total_ignores_unknown_item(self):
        self.assertEqual(self.app.calculate_order_total({"cake": 2}), 0.0)

    def test_calculate_total_ignores_negative_quantity(self):
        self.assertEqual(self.app.calculate_order_total({"pho": -1}), 0.0)


class TestMediumLevel(unittest.TestCase):
    """Kiểm thử xác thực và áp dụng mã khuyến mãi."""

    def test_promo_online_valid_code(self):
        app = YummyApp(network_status="online")
        self.assertEqual(app.apply_promo_code(100_000, "GIAM10"), 90_000)

    def test_promo_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100_000, "GIAM10")

    def test_special_promo_allowed_on_os_15(self):
        app = YummyApp(os_version=15)
        self.assertEqual(app.apply_promo_code(100_000, "NEW_OS_ONLY"), 80_000)

    def test_special_promo_rejected_on_os_14(self):
        app = YummyApp(os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100_000, "NEW_OS_ONLY")

    def test_unknown_promo_code_raises_value_error(self):
        with self.assertRaises(ValueError):
            YummyApp().apply_promo_code(100_000, "NOT_A_CODE")


class TestHardLevel(unittest.TestCase):
    """Kiểm thử GPS bằng mock, không phụ thuộc phần cứng thật."""

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_inside_known_area_returns_restaurants(self, mock_location):
        mock_location.return_value = (10.0, 105.0)
        result = YummyApp().get_nearby_restaurants()
        self.assertEqual(
            result,
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_location.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_outside_known_area_returns_empty_list(self, mock_location):
        mock_location.return_value = (20.0, 110.0)
        self.assertEqual(YummyApp().get_nearby_restaurants(), [])

    @patch("yummy_app.gps_service.get_current_location")
    def test_gps_signal_lost_returns_message(self, mock_location):
        mock_location.side_effect = gps_service.GPSSignalLostError
        self.assertEqual(
            YummyApp().get_nearby_restaurants(),
            "Khong the xac dinh vi tri.",
        )


class TestGPSService(unittest.TestCase):
    """Kiểm tra giá trị mẫu mặc định của module GPS."""

    def test_default_location(self):
        self.assertEqual(gps_service.get_current_location(), (10.0, 105.0))


if __name__ == "__main__":
    unittest.main()
