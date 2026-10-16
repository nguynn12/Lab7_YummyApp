# Ghi chú học tập cho phần viết tay Lab 7

Đây là ghi chú để hiểu ý, không phải trang minh chứng để nộp. Hãy tự viết lại bằng cách diễn đạt của bạn, trên giấy, và ký tên thật.

## Ma trận 7 ca mocking cần có

| Test case | Hàm được gọi | Mock | Kết quả cần assert |
|---|---|---|---|
| Mã GIAM10 hợp lệ, online | `apply_promo_code` | Không cần mock | Tổng 100.000 còn 90.000 |
| Mất mạng | `apply_promo_code` | `network_status="offline"` | Ném `ConnectionError` |
| Mã NEW_OS_ONLY trên OS 15 | `apply_promo_code` | `os_version=15` | Tổng 100.000 còn 80.000 |
| Mã NEW_OS_ONLY trên OS 14 | `apply_promo_code` | `os_version=14` | Ném `ValueError` |
| GPS trong vùng | `get_nearby_restaurants` | GPS trả `(10.0, 105.0)` | Trả về 2 nhà hàng mẫu |
| GPS ngoài vùng | `get_nearby_restaurants` | GPS trả `(20.0, 110.0)` | Trả về danh sách rỗng |
| Mất tín hiệu GPS | `get_nearby_restaurants` | GPS ném `GPSSignalLostError` | Trả thông báo không xác định được vị trí |

## Gợi ý trả lời 6 câu hỏi

### 2.1 Vì sao Linter chạy trước test?
Linter kiểm tra một số lỗi cú pháp và lỗi code có thể phát hiện tĩnh, nên chạy sớm để dừng nhanh. Nếu có lỗi, CI báo thất bại ngay, không tốn thời gian chạy các bước test tiếp theo. Đây là fail-fast.

### 2.2 `--fail-under=80` báo build thất bại thế nào?
Coverage tính tỷ lệ dòng lệnh đã được chạy. Nếu kết quả thấp hơn 80%, lệnh `coverage report` trả mã thoát khác 0. Shell của GitHub Actions coi lệnh có mã thoát khác 0 là thất bại, nên job và workflow bị đánh đỏ. Nếu đạt ngưỡng, lệnh trả mã 0 và job có thể tiếp tục.

### 2.3 `coverage report -m` thêm gì?
`-m` hiển thị số dòng chưa được chạy cho từng file. Kỹ sư có thể tìm đúng nhánh chưa được test để bổ sung ca kiểm thử, thay vì chỉ nhìn tỷ lệ tổng.

### 3.1 Flaky test và sai lệch môi trường khác nhau thế nào?
Flaky test lúc pass, lúc fail dù code và điều kiện test gần như không đổi; nguyên nhân thường là timing, race condition, thứ tự test hoặc tài nguyên không ổn định. Sai lệch môi trường xảy ra khi test chạy trong điều kiện khác nhau, như phiên bản Python, biến môi trường, mạng, thời gian hay thiết bị. Mock GPS giúp loại bỏ phụ thuộc vào GPS/mạng thật. Khi tự viết, hãy dùng một ví dụ cụ thể và giải thích dấu hiệu phân biệt.

### 3.2 Vì sao ghim phiên bản?
Ghim phiên bản giúp máy lập trình viên và CI cài cùng bộ thư viện. Nếu để phiên bản tự do, lần chạy sau có thể tải bản mới với thay đổi API hoặc hành vi, làm build khác đi và khó tái hiện lỗi. Nâng cấp nên được kiểm thử và review có chủ đích.

### 3.3 Sáu bước nâng cấp thư viện qua PR
1. Tạo nhánh riêng từ `main`.
2. Đọc release notes, thay đổi tương thích và yêu cầu phụ thuộc.
3. Cập nhật phiên bản trong `requirements.txt` hoặc lockfile.
4. Chạy linter, unit/integration tests và quality gate.
5. Mở PR, ghi lý do, thay đổi, kết quả test và rủi ro; yêu cầu review.
6. Sửa theo review, bảo đảm CI xanh rồi merge theo quy trình; theo dõi sau merge và revert nếu có lỗi.

## Nhớ về workflow

- `push` và `pull_request` là trigger.
- `runs-on` chọn runner; `steps` là các bước trên runner.
- `actions/checkout` lấy mã nguồn; `actions/setup-python` cài Python.
- Linter phát hiện một số lỗi tĩnh; unittest kiểm tra hành vi; coverage đo các dòng code đã chạy.
- `--fail-under=80` là quality gate; lệnh thất bại làm workflow đỏ.
- Artifact HTML giúp xem chi tiết dòng nào chưa được test.
