[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*Hình ảnh khoa học lai mở: điểm ảnh đơn, sự kiện, khung hình và phổ trong một ngăn xếp nghiên cứu dễ bảo trì.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager là không gian nghiên cứu và thiết kế cho một bộ dò khoa học hỗn hợp. Ý tưởng kết hợp bộ dò điểm ảnh đơn có dải động cao, thời gian của camera sự kiện, chi tiết của camera khung hình và phép đo phổ tùy chọn trong một mô hình dữ liệu đồng bộ.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## Khái niệm hệ thống

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **Nhánh điểm ảnh đơn:** đường bộ dò trung tâm và TIA nhiễu thấp cho cường độ tuyệt đối, dải động cao, đo phổ hoặc đo mã hóa.
- **Nhánh sự kiện:** tương phản thời gian bất đồng bộ từ camera sự kiện thương mại trước, sau đó là giao diện FPGA mở khi thực tế.
- **Nhánh khung hình:** mô-đun màn trập toàn cục cho chi tiết ảnh, hiệu chuẩn và kiểm tra trực quan.
- **Lớp hợp nhất:** luồng có dấu thời gian với phơi sáng, gain, hồ sơ hiệu chuẩn, trigger và siêu dữ liệu mẫu.

## Bo mạch cảm biến V1

![Bản render KiCad HybridImager V1](../hardware/v1-weiqi-sensor/artifacts/hybridimager-v1-kicad-render-full.png)

Bản nháp bo mạch đầu tiên là carrier cảm biến thưa kiểu **Weiqi** được tạo bằng KiCad, có 21 vị trí bộ dò điểm ảnh đơn thay vì chỉ một bucket trung tâm. Nó có pad tín hiệu theo từng vị trí, đường hồi tiếp đất rõ ràng, ba placeholder AFE, một placeholder định thời QFN, SMA sync in/out, header nguồn/sync và header mở rộng 2x20.

Gói rà soát: [`hardware/v1-weiqi-sensor/`](../hardware/v1-weiqi-sensor/) chứa bo KiCad, dataset, BOM, DRC sạch, STEP, Gerber, file khoan và render toàn cảnh.

## Nội dung hiện tại

| Khu vực | Vị trí |
| --- | --- |
| Bài viết ý tưởng | `publications/hybrid_camera_concept.pdf` |
| Khảo sát camera mở | `publications/open_camera_project_survey.pdf` |
| Bo cảm biến thưa V1 | `hardware/v1-weiqi-sensor/` |
| Ghi chú nghiên cứu | `references/` |
| Sơ đồ xác định | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| Kế hoạch phần cứng | `hardware/board_architecture.md` |
| Kế hoạch tái tạo | `algorithms/reconstruction_plan.md` |
| Ngữ cảnh trước đó | `copied-context/` |
| Bản sao dự án mở | `external/` dưới dạng git submodule |

## Bắt đầu nhanh

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

Nếu đã clone:

```bash
git submodule update --init --recursive
make survey
```

## Nền tảng nghiên cứu

Lộ trình điểm ảnh đơn mở mạnh nhất là **ONE-PIX** cùng **ONE-PIX_hardware**. Với thị giác sự kiện, bản dựng đầu tiên thực tế dùng camera sự kiện thương mại với **OpenEB**, **jAER**, **v2e** và **E2VID**. Với phần cứng khung hình, các tham chiếu mở hữu ích là **OneInchEye**, **Antmicro OV9281**, **AXIOM Beta** và **Seeed reCamera**.

Dự án không giả định ASIC cảm biến sự kiện tùy chỉnh trong giai đoạn đầu. Nó bắt đầu bằng đồng bộ cấp bo mạch mở, định dạng dữ liệu mở, tái tạo có thể lặp lại và tham chiếu cơ khí/PCB có thể tái sử dụng.

## Ghi chú CAD và phần cứng

Gói xuất Shapr3D khuyến nghị cho công việc cơ khí có thể chỉnh sửa:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

Dùng STEP làm định dạng trao đổi chính, Parasolid làm bản sao solid độ trung thực cao, DXF cho biên dạng 2D và tấm phẳng, còn STL/3MF chỉ cho in hoặc xem trước mesh.

## Lệnh build

```bash
make figures
make paper
make survey
make all
make clean
```

## Trích dẫn

Nếu dùng HybridImager trong nghiên cứu, hãy trích dẫn kho mã này. GitHub đọc [CITATION.cff](../CITATION.cff) và hiển thị bảng **Cite this repository** trên trang kho mã.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## Trạng thái

Đây là không gian nghiên cứu giai đoạn đầu, không phải sản phẩm hình ảnh đã được chứng nhận. Mục tiêu trước mắt là một pipeline thí nghiệm dễ bảo trì cho quang học và kính hiển vi: xây bằng mô-đun sẵn có, đồng bộ sạch, tái tạo lặp lại và chỉ tích hợp phần cứng tùy chỉnh sau khi hợp đồng dữ liệu ổn định.

Xây ít hơn. Ghi hình nhiều hơn.
