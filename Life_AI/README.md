# LIFE AI - Đường ống tạo và sàng lọc phân tử

Đây là một dự án mô phỏng nền tảng khám phá thuốc dựa trên AI, được xây dựng để tự động hóa quy trình đề xuất, sàng lọc và xếp hạng các phân tử hóa học tiềm năng. Hệ thống được thiết kế như một dịch vụ web với các agent thông minh để thực hiện các tác vụ một cách tự động và có thể kiểm toán được.

## Chức năng chính

- **Luồng làm việc Agentic:** Hệ thống sử dụng nhiều agent (Planner, Generator, Ranker) để tự động điều phối quy trình làm việc.
- **Xử lý tác vụ bất đồng bộ:** Các yêu cầu phân tử được xử lý trong nền, cho phép API phản hồi ngay lập tức mà không cần chờ đợi.
- **Tích hợp công cụ hóa học:** Sử dụng `RDKit` để thực hiện các phép toán hóa học phức tạp như xác thực SMILES và tính toán thuộc tính phân tử.
- **Sàng lọc và chấm điểm có thể cấu hình:** Cho phép người dùng định nghĩa các bộ lọc (ví dụ: quy tắc Lipinski) và logic chấm điểm để xếp hạng các ứng viên.
- **Giao diện API RESTful:** Cung cấp một bộ API rõ ràng để bắt đầu một lần chạy, kiểm tra trạng thái, và truy xuất kết quả cũng như dấu vết xử lý.
- **Đột biến phân tử đa dạng:** Generator hỗ trợ nhiều loại đột biến bao gồm: swap halogen (F↔Cl, Br↔Cl), add/remove methyl, thêm nhóm chức, chuyển đổi vòng thơm/không thơm.
- **Kiểm tra tính duy nhất:** Tự động loại bỏ các phân tử trùng lặp trong quá trình tạo và sàng lọc.
- **Phân tích thất bại chi tiết:** Báo cáo chi tiết về lý do phân tử không đạt tiêu chuẩn (MW quá cao, LogP quá cao, v.v.).
- **Thống kê tổng hợp:** Cung cấp summary với thống kê đầy đủ về quá trình xử lý.

## Cấu trúc thư mục

Dự án được tổ chức theo cấu trúc module hóa để dễ dàng bảo trì và mở rộng.

```
.
├── app/
│   ├── __init__.py
│   ├── api.py          # Định nghĩa FastAPI app và các API endpoints.
│   ├── worker.py       # Chứa logic xử lý tác vụ nền (dây chuyền xử lý).
│   ├── schemas.py      # Định nghĩa các mô hình dữ liệu Pydantic (cấu trúc đầu vào).
│   ├── agents/         # Chứa các agent "thông minh" của hệ thống.
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── generator.py
│   │   └── ranker.py
│   └── tools/          # Chứa các công cụ khoa học (ví dụ: hóa học, sàng lọc).
│       ├── __init__.py
│       ├── chemistry.py
│       └── screening.py
├── main.py             # Điểm vào để khởi chạy máy chủ web.
├── requirements.txt    # Danh sách các thư viện Python cần thiết.
└── README.md           # Tệp tài liệu này.
```

## Hướng dẫn cài đặt và chạy chương trình

### 1. Yêu cầu
- Python 3.8+
- `pip` và `venv`

### 2. Cài đặt

**a. Tạo và kích hoạt môi trường ảo:**
Mở terminal trong thư mục gốc của dự án và chạy:
```sh
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows (PowerShell)
.venv\Scripts\Activate.ps1
# Trên macOS/Linux
source .venv/bin/activate
```

**b. Cài đặt các thư viện cần thiết:**
```sh
pip install -r requirements.txt
```
*Lưu ý: Tệp `requirements.txt` đã được cấu hình để cài đặt phiên bản `numpy` tương thích với `rdkit`.*

### 3. Khởi động máy chủ

Sử dụng `uvicorn` để chạy máy chủ. Tùy chọn `--reload` sẽ tự động khởi động lại máy chủ khi có thay đổi trong mã nguồn, rất hữu ích cho việc phát triển.
```sh
uvicorn app.api:app --reload
```
Sau khi chạy, máy chủ sẽ hoạt động tại địa chỉ `http://127.0.0.1:8000`.

### 4. Tương tác với API

Sử dụng PowerShell trên Windows để gửi yêu cầu và nhận kết quả đã được định dạng đẹp.

**a. Bắt đầu một lần chạy mới:**

Gửi một yêu cầu `POST` đến `/runs` với các thông số của bạn. Lệnh này sẽ trả về một đối tượng, bạn có thể lấy `run_id` từ thuộc tính `Content`.
```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body '{
      "objective": "Generate drug-like molecules; maximize QED; keep ≤ 1 rule violation.",
      "seeds": ["CCO", "c1ccccc1"],
      "filters": { "MW": 500, "LogP": 5, "HBD": 5, "HBA": 10, "TPSA": 140 },
      "max_violations": 1,
      "rounds": 2,
      "candidates_per_round": 20
    }'

# Lấy run_id từ kết quả
$run_id = ($response.Content | ConvertFrom-Json).run_id
Write-Host "Đã bắt đầu lần chạy với ID: $run_id"
```
Hãy sao chép ID này để sử dụng trong các bước tiếp theo.

**b. Kiểm tra trạng thái:**

Thay thế `$run_id` bằng ID bạn nhận được.
```powershell
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/status").Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**c. Lấy dấu vết xử lý:**
```powershell
# Hiển thị đầy đủ
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/trace").Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Hoặc lưu vào file để xem chi tiết
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/trace").Content | Out-File "trace.json"
notepad trace.json
```

**d. Lấy kết quả cuối cùng:**

Sau khi trạng thái chuyển thành `"completed"`, bạn có thể lấy danh sách các phân tử tốt nhất.

```powershell
# Cách 1: Hiển thị JSON đầy đủ trong terminal (Khuyến nghị)
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Cách 2: Lưu vào file để xem chi tiết
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | Out-File "results.json"
notepad results.json

# Cách 3: Xem từng phân tử riêng biệt
$results = (Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json
$results.results | ForEach-Object { 
    Write-Host "=== Molecule ===" -ForegroundColor Green
    $_ | ConvertTo-Json -Depth 5
    Write-Host ""
}
```

**e. Lấy thống kê tổng hợp (Summary):**

Endpoint mới để xem thống kê chi tiết bao gồm failure breakdown (phân tích nguyên nhân thất bại).
```powershell
# Hiển thị summary đầy đủ
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/summary").Content | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Hoặc hiển thị dạng danh sách dễ đọc
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/summary").Content | ConvertFrom-Json | Format-List
```

Kết quả summary sẽ hiển thị:
- `total_passed`: Tổng số phân tử đã vượt qua sàng lọc
- `total_failure_breakdown`: Chi tiết lý do thất bại (MW_too_high, LogP_too_high, HBD_too_high, HBA_too_high, TPSA_too_high)
- `final_selected`: Số phân tử cuối cùng được chọn (top_k)

### 5. Xử lý kết quả dài trong PowerShell

**Lưu ý:** PowerShell mặc định cắt bớt output dài. Nếu kết quả bị hiển thị không đầy đủ (như `...`), hãy sử dụng một trong các phương pháp sau:

**Phương pháp 1 - Thêm `-Depth 10` (Nhanh nhất):**
```powershell
# Thay vì
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json

# Sử dụng
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

**Phương pháp 2 - Lưu vào file JSON (Dễ đọc nhất):**
```powershell
# Lưu tất cả endpoints vào file
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | Out-File "results.json"
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/trace").Content | Out-File "trace.json"
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/summary").Content | Out-File "summary.json"

# Mở file để xem
notepad results.json
```

**Phương pháp 3 - Tăng buffer size (Cho tất cả lệnh):**
```powershell
# Chạy lệnh này một lần ở đầu session
$PSDefaultParameterValues['Out-String:Width'] = 300

# Sau đó tất cả lệnh sẽ hiển thị rộng hơn
(Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json
```

**Phương pháp 4 - Xem từng phần tử (Cho arrays lớn):**
```powershell
# Lưu kết quả vào biến
$data = (Invoke-WebRequest -Uri "http://127.0.0.1:8000/runs/$run_id/results").Content | ConvertFrom-Json

# Xem từng phân tử
$data.results[0] | ConvertTo-Json -Depth 5  # Phân tử đầu tiên
$data.results[1] | ConvertTo-Json -Depth 5  # Phân tử thứ hai

# Hoặc xem tất cả từng cái một
$data.results | ForEach-Object { $_ | ConvertTo-Json -Depth 5; Write-Host "`n---`n" }
```

## Hướng phát triển

- **Tích hợp cơ sở dữ liệu:** Thay thế biến `runs` trong bộ nhớ bằng một cơ sở dữ liệu bền vững như `SQLite` hoặc `PostgreSQL` để lưu trữ kết quả lâu dài.
- **Tăng cường trí thông minh cho Agent:** Tích hợp các mô hình ngôn ngữ lớn (LLM) để `GeneratorAgent` có thể tạo ra các phân tử một cách sáng tạo hơn, hoặc để `PlannerAgent` có thể tự động đề xuất kế hoạch từ một mục tiêu cấp cao.
```