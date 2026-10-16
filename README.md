# YummyApp Lab 7: Mocking và CI/CD

Bộ này chuẩn bị mã ứng dụng, bộ kiểm thử mocking, workflow GitHub Actions và ghi chú ôn tập theo đề. Chưa có thông tin cá nhân, repo GitHub hoặc log do bạn tự tạo.

## Chạy trên máy

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
mkdir -p logs
coverage run -m unittest discover -s . -p "test_*.py" > logs/local_test.log 2>&1
coverage report -m >> logs/local_test.log
```

Trên Windows PowerShell, tạo thư mục log bằng:

```powershell
New-Item -ItemType Directory -Force logs
```

Chạy riêng linter:

```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

Bộ test có 4 ca giỏ hàng ban đầu, 4 ca khuyến mãi và 3 ca GPS mocking theo đề, cộng thêm các ca biên. Trong môi trường dựng bộ này, 15 test đã chạy thành công, coverage tổng đạt 99% và linter qua các nhóm lỗi được cấu hình. Hãy tự chạy lại để tạo log cá nhân.

## Kết nối GitHub và ghi minh chứng

1. Tạo repo của bạn và thay `main` trong workflow nếu nhánh chính có tên khác.
2. Cấu hình Git bằng tên theo định dạng yêu cầu của giảng viên, gắn với MSSV và email của bạn. Commit/push bằng tài khoản của bạn.
3. Để minh họa Break the Build mà không làm hỏng `main`, tạo nhánh thử nghiệm, tạo Pull Request về `main`, rồi đưa vào đó một lỗi cú pháp có chủ đích. Lưu log/ảnh CI đỏ. Sau đó sửa cú pháp, push lại và lưu minh chứng CI xanh.
4. Tải raw log của lần Actions chạy xanh vào `logs/github_actions_run.log`.
5. Sau khi có commit thật, xuất lịch sử vào `logs/git_history.log` bằng:

```bash
git log --graph --pretty=format:"%h - %an (%ad) : %s" > logs/git_history.log
```

6. Tự vẽ sơ đồ CI, tự kẻ bảng 7 test case, và tự viết tay 6 câu lý thuyết trên giấy theo đề. Ghi họ tên, MSSV, ngày làm và chữ ký thật; chụp/scan vào PDF. Ghi chú gợi ý ở `docs/goi_y_viet_tay.md` chỉ để học và tự diễn đạt.
7. Hoàn thiện báo cáo có link repo và ảnh chụp Actions; thêm log và PDF viết tay. Đổi tên ZIP theo đúng mẫu MSSV_HoTen_Lab7.zip.

**Chưa phải bộ hồ sơ nộp cuối:** ZIP này không có commit cá nhân, log GitHub Actions, ảnh chụp workflow, thông tin sinh viên hoặc trang viết tay có chữ ký. Không dùng các tệp giả để thay minh chứng thật.
