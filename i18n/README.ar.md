[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# HybridImager

*تصوير علمي هجين ومفتوح: بكسل واحد، وأحداث، وإطارات، وقياس طيفي ضمن حزمة بحثية قابلة للصيانة.*

[![Website](https://img.shields.io/badge/Website-lazying.art-111827?style=for-the-badge&logo=googlechrome&logoColor=white)](https://lazying.art)
[![Concept Paper](https://img.shields.io/badge/PDF-Concept%20Paper-334155?style=for-the-badge&logo=latex&logoColor=white)](../publications/hybrid_camera_concept.pdf)
[![Survey](https://img.shields.io/badge/PDF-Open%20Camera%20Survey-0f766e?style=for-the-badge&logo=readthedocs&logoColor=white)](../publications/open_camera_project_survey.pdf)
[![GitHub Sponsors](https://img.shields.io/badge/Sponsor-lachlanchen-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)

HybridImager مساحة بحث وتصميم لكاشف علمي مختلط. يجمع المفهوم بين كاشف بكسل واحد عالي المجال الديناميكي، وتوقيت كاميرا الأحداث، وملمس كاميرا الإطارات، وقياسات طيفية اختيارية ضمن نموذج بيانات متزامن واحد.

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://img.shields.io/badge/Donate-LazyingArt-0EA5E9?style=for-the-badge&logo=kofi&logoColor=white)](https://chat.lazying.art/donate) | [![PayPal](https://img.shields.io/badge/PayPal-RongzhouChen-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen) | [![Stripe](https://img.shields.io/badge/Stripe-Donate-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## مفهوم النظام

![Hybrid board layout](../figures/hybrid_board_layout.png)

- **فرع البكسل الواحد:** مسار كاشف ومضخم TIA منخفض الضجيج للكثافة المطلقة، والمجال الديناميكي العالي، والقياسات الطيفية أو المرمزة.
- **فرع الأحداث:** تباين زمني غير متزامن من كاميرات أحداث تجارية أولا، ثم واجهات FPGA مفتوحة عندما يصبح ذلك عمليا.
- **فرع الإطارات:** وحدات إطارات ذات غالق عام للملمس، والمعايرة، والفحص البشري.
- **طبقة الدمج:** تدفقات ذات طابع زمني مع التعريض، والكسب، وملف المعايرة، والمشغل، وبيانات النمط.

## لوحة المستشعر V1

![عرض KiCad لـ HybridImager V1](../hardware/v1-weiqi-sensor/artifacts/hybridimager-v1-kicad-render-full.png)

المسودة الأولى للوحة هي حاملة مستشعرات متناثرة بنمط **Weiqi** مولدة في KiCad، وفيها 21 موقع كاشف بكسل واحد بدلا من bucket مركزي واحد فقط. تتضمن Pads إشارة لكل موقع، ومسار أرضي واضحا، وثلاثة مواضع AFE، وموضع توقيت QFN، وSMA للمزامنة دخولا وخروجا، وموصل طاقة/مزامنة، وموصل توسعة 2x20.

حزمة المراجعة: [`hardware/v1-weiqi-sensor/`](../hardware/v1-weiqi-sensor/) تحتوي لوحة KiCad، ومجموعة البيانات، وBOM، وDRC نظيفا، وSTEP، وGerbers، وملفات الحفر، وعروض الرؤية الكاملة.

## المحتوى الحالي

| المجال | الموقع |
| --- | --- |
| ورقة المفهوم | `publications/hybrid_camera_concept.pdf` |
| مسح مشاريع الكاميرات المفتوحة | `publications/open_camera_project_survey.pdf` |
| لوحة مستشعر متناثرة V1 | `hardware/v1-weiqi-sensor/` |
| مصفوفة ALS-PT19 مصطفة V2 | `hardware/v2-als-pt19-32x32/` |
| ملاحظات البحث | `references/` |
| الرسوم الحتمية | `figures/hybrid_board_layout.*`, `figures/hybrid_signal_chain.*` |
| خطة العتاد | `hardware/board_architecture.md` |
| خطة إعادة البناء | `algorithms/reconstruction_plan.md` |
| سياق سابق | `copied-context/` |
| مرايا المشاريع المفتوحة | `external/` كوحدات git فرعية |

## البدء السريع

```bash
git clone --recurse-submodules https://github.com/lachlanchen/HybridImager.git
cd HybridImager
make all
```

إذا كان المستودع مستنسخا مسبقا:

```bash
git submodule update --init --recursive
make survey
```

## خط الأساس البحثي

أقوى مسار مفتوح للبكسل الواحد هو **ONE-PIX** مع **ONE-PIX_hardware**. ولرؤية الأحداث، يبدأ البناء الواقعي بكاميرات أحداث تجارية مع **OpenEB** و **jAER** و **v2e** و **E2VID**. أما عتاد الإطارات، فأفضل المراجع المفتوحة هي **OneInchEye** و **Antmicro OV9281** و **AXIOM Beta** و **Seeed reCamera**.

لا يفترض المشروع تصنيع ASIC مخصص لحساس الأحداث في المرحلة الأولى. يبدأ بالمزامنة المفتوحة على مستوى اللوحة، وصيغ البيانات المفتوحة، وإعادة البناء القابلة للتكرار، ومراجع ميكانيكية ومراجع PCB قابلة لإعادة الاستخدام.

## ملاحظات CAD والعتاد

حزمة التصدير المفضلة من Shapr3D للعمل الميكانيكي القابل للتحرير:

```text
STEP + native .shapr + Parasolid + DXF from sketch + 3MF/STL preview
```

استخدم STEP كصيغة تبادل رئيسية، وParasolid كنسخة صلبة احتياطية عالية الدقة، وDXF للمخططات ثنائية الأبعاد والصفائح، وSTL/3MF للطباعة أو معاينة الشبكات فقط.

## أوامر البناء

```bash
make figures
make paper
make survey
make all
make clean
```

## الاستشهاد

إذا استخدمت HybridImager في بحثك، فاستشهد بالمستودع. يقرأ GitHub ملف [CITATION.cff](../CITATION.cff) ويعرض لوحة **Cite this repository** في صفحة المستودع.

```bibtex
@software{chen_hybridimager_2026,
  author = {Chen, Lachlan},
  title = {HybridImager: Open Hybrid Scientific Imaging Research Workspace},
  year = {2026},
  url = {https://github.com/lachlanchen/HybridImager}
}
```

## الحالة

هذه مساحة بحث مبكرة وليست منتجا تصويريا معتمدا. الهدف المباشر هو خط تجارب قابل للصيانة للأنظمة البصرية والمجهرية: البناء بوحدات متاحة، والمزامنة النظيفة، وإعادة البناء القابلة للتكرار، ثم دمج العتاد المخصص فقط بعد استقرار عقد البيانات.

ابن أقل. صوّر أكثر.
