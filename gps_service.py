"""Dịch vụ giả lập phần cứng GPS của YummyApp."""


class GPSSignalLostError(Exception):
    """Ngoại lệ khi thiết bị không nhận được tín hiệu GPS."""


def get_current_location():
    """Trả về tọa độ GPS mẫu; trong test có thể được thay bằng mock."""
    return 10.0, 105.0
