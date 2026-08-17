#!/usr/bin/env python3
"""Generate localized versions of the Nugget Wallpaper landing page."""
import json, os

BASE = 'https://nuggetwallpaper.github.io'

# language config: dir, self path, label, mwallx language code for links
LANGS = {
    'en':    dict(path='/',        label='English',   code='EN',   dir='',    mlang='en',   nav=('About', 'Catalog', 'Install', 'FAQ')),
    'zh-CN': dict(path='/zh-CN/',  label='简体中文',   code='中文', dir='',    mlang='zh-HK', nav=('关于', '目录', '安装', '常见问题')),
    'hi':    dict(path='/hi/',     label='हिन्दी',    code='HI',   dir='',    mlang='hi',   nav=('परिचय', 'कैटलॉग', 'इंस्टॉल', 'FAQ')),
    'es':    dict(path='/es/',     label='Español',   code='ES',   dir='',    mlang='es',   nav=('Acerca de', 'Catálogo', 'Instalar', 'FAQ')),
    'fr':    dict(path='/fr/',     label='Français',  code='FR',   dir='',    mlang='fr',   nav=('À propos', 'Catalogue', 'Installer', 'FAQ')),
    'ar':    dict(path='/ar/',     label='العربية',   code='AR',   dir='rtl', mlang='ar',   nav=('حول', 'المعرض', 'التثبيت', 'الأسئلة')),
    'bn':    dict(path='/bn/',     label='বাংলা',     code='BN',   dir='rtl', mlang='bn',   nav=('পরিচিতি', 'ক্যাটালগ', 'ইনস্টল', 'প্রশ্ন')),
    'pt':    dict(path='/pt/',     label='Português', code='PT',   dir='',    mlang='pt',   nav=('Sobre', 'Catálogo', 'Instalar', 'FAQ')),
    'ru':    dict(path='/ru/',     label='Русский',   code='RU',   dir='',    mlang='ru',   nav=('О проекте', 'Каталог', 'Установка', 'FAQ')),
    'ur':    dict(path='/ur/',     label='اردو',      code='UR',   dir='rtl', mlang='ur',   nav=('تعارف', 'کیٹالاگ', 'انسٹال', 'سوالات')),
}

T = {
    'zh-CN': dict(
        title='Nugget 壁纸 — iPhone 动画与动态壁纸（iOS 17–26）',
        meta_desc='Nugget 壁纸库：为 iPhone 和 iPad 精选的动画与动态壁纸，可使用 Nugget 工具在 iOS 17–26 上安装。浏览、预览并下载免费和高级动态壁纸。',
        og_title='Nugget 壁纸 — iPhone 动画与动态壁纸（iOS 17–26）',
        og_desc='为 iPhone/iPad 精选的动态与动画壁纸。使用 Nugget 工具在 iOS 17–26 上安装。免费和高级壁纸库。',
        website_desc='精选的 iPhone 和 iPad 动画与动态壁纸库，可使用 Nugget 工具在 iOS 17–26 上安装。',
        eyebrow='为 Nugget 打造动态壁纸',
        h1='Nugget 壁纸库<br />iPhone 动画壁纸',
        sub='为你的 iPhone 和 iPad 精选的动态、动画壁纸。使用 <strong>Nugget 工具</strong>即可直接安装，无需越狱——兼容 iOS 17 到 iOS 26。',
        cta_primary='浏览 Nugget 壁纸库 →',
        cta_ghost='官方安装教程',
        spec_ios='支持 <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone 与 <b>iPad</b>',
        spec_free='<b>免费</b> 与高级',
        spec_jailbreak='无需越狱',
        about_h2='什么是 Nugget 壁纸？',
        about_muted='了解如何使用 Nugget 工具在 iPhone 上安装动画壁纸的全部信息。',
        about_p1='<strong>Nugget 壁纸</strong>是一种为 iPhone 和 iPad 设计的动画动态壁纸，通过 <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> 安装——这是 LeMinLimez 开发的开源 iOS 定制工具，使用 sparserestore 和 BookRestore 方法，<em>无需完整越狱</em>即可修改 Apple 设备。',
        about_p2='Nugget 壁纸不再是你图标后面的一张静态图片，它可以在锁屏和主屏幕上移动、互动和动画化。<a href="https://mwallx.com/" rel="noopener">Nugget 壁纸项目</a>汇集了这些动态壁纸的精选库，每个页面都有实时动画 GIF 预览，让你清楚知道正在安装什么。',
        f1_h='动态壁纸库', f1_p='数百款精选动态壁纸格式，涵盖动漫、体育、音乐、3D 与生活主题。',
        f2_h='Nugget 工具', f2_p='将动画壁纸应用到设备上的开源 Windows / macOS 应用——无需越狱。',
        f3_h='分步教程', f3_p='从备份到动态锁屏的入门友好安装教程。',
        catalog_h2='Nugget 壁纸目录里有什么',
        catalog_muted='在 mwallx.com 上探索 Nugget 壁纸合集——下载前先预览动态效果。',
        cat1_b='动漫与漫画', cat1_h='EVA、鬼灭之刃、漫威', cat1_p='来自你喜爱系列的惊艳动画壁纸。',
        cat2_b='体育', cat2_h='足球与电竞', cat2_p='从阿森纳到 FIFA 2026 的球队与球员动态壁纸。',
        cat3_b='3D 与创意', cat3_h='3D 人脸与梦幻场景', cat3_p='充满生机的 3D 深度壁纸与梦幻星球壁纸。',
        cat4_b='免费', cat4_h='免费与高级', cat4_p='按免费或高级筛选，找到你想要的 Nugget 壁纸。',
        cat5_b='官方', cat5_h='Apple 格式壁纸', cat5_p='官方格式的壁纸包，以及 Nugget 社区构建。',
        cat6_b='每周上新', cat6_h='每周更新', cat6_p='Nugget 壁纸库随时都有新壁纸上架。',
        install_h2='如何安装 Nugget 壁纸',
        install_muted='从下载到动态锁屏，只需四个简单步骤。',
        step1_h='选择你的壁纸', step1_p='浏览 <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">Nugget 壁纸库</a>，观看动画 GIF 预览并下载壁纸包。',
        step2_h='备份设备', step2_p='将 iPhone 或 iPad 连接到电脑并创建完整备份。使用任何 iOS 修改工具前务必先备份。',
        step3_h='用 Nugget 应用', step3_p='运行 Nugget 应用，将壁纸载入 PosterBoard 功能，并按<a href="https://nugget.host/tutorial/nugget" rel="noopener">官方教程</a>恢复你的设备。',
        step4_h='享受动态效果', step4_p='你的 iPhone 现在运行真正的动画壁纸——平移、滑动，看着它在锁屏和主屏幕上活起来。',
        disclaimer='<strong>安全提示：</strong>Nugget 使用 sparserestore 和 BookRestore 方法，<strong>不兼容 iOS 27</strong>（Apple 已修补恢复方法，可能导致数据丢失）。只安装你信任的壁纸，遵循官方指南，并始终保留备份。',
        faq_h2='Nugget 壁纸常见问题',
        faq_muted='关于 iPhone 动态壁纸最常见问题的快速解答。',
        faq=[
            ('什么是 Nugget 壁纸？', 'Nugget 壁纸是一种通过 Nugget 工具安装到 iPhone 和 iPad 上的动画或动态壁纸，Nugget 是一款开源 iOS 定制工具。它远不止一张静态锁屏图片——可以在你的屏幕上动画、互动和移动，这是 Apple 原生没有的功能。'),
            ('Nugget 壁纸支持哪些 iOS 版本？', 'Nugget 壁纸支持 iOS 和 iPadOS 17 至 26，以及通用平台。请完全避开 iOS 27——Nugget 的恢复方法在那里已被修补，很可能导致数据丢失。'),
            ('如何在 iPhone 上安装 Nugget 壁纸？', '从壁纸库下载壁纸，在 Windows 或 macOS 上运行 Nugget 工具（Linux 也可以），并通过 PosterBoard 功能应用。完整教程在 <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a> 上。'),
            ('安装 Nugget 壁纸需要越狱吗？', '不需要。Nugget 通过 sparserestore 和 BookRestore 非越狱方法工作，因此只要系统是 iOS 17–26，就可以在原生 iPhone 上添加动画壁纸。'),
            ('有免费的 Nugget 壁纸吗？', '有。<a href="https://mwallx.com" rel="noopener">mwallx.com</a> 上的壁纸库提供免费和高级精选壁纸，每一款都有动画 GIF 预览。'),
        ],
        footer_note='Nugget 壁纸是一个社区项目。本网站介绍 Nugget 壁纸库，并链接到官方 <a href="https://mwallx.com/" rel="noopener">mwallx.com</a> 服务。与 Apple Inc. 无关。© 2026 Nugget 壁纸。',
    ),
    'hi': dict(
        title='Nugget वॉलपेपर — iPhone के लिए एनिमेटेड और मोशन वॉलपेपर (iOS 17–26)',
        meta_desc='Nugget वॉलपेपर लाइब्रेरी: iPhone और iPad के लिए चयनित एनिमेटेड और मोशन वॉलपेपर, जिन्हें Nugget टूल से iOS 17–26 पर इंस्टॉल किया जा सकता है। मुफ्त और प्रीमियम डायनामिक वॉलपेपर ब्राउज़ करें, प्रीव्यू करें और डाउनलोड करें।',
        og_title='Nugget वॉलपेपर — iPhone के लिए एनिमेटेड और मोशन वॉलपेपर (iOS 17–26)',
        og_desc='iPhone/iPad के लिए चयनित डायनामिक और मोशन वॉलपेपर। Nugget टूल से iOS 17–26 पर इंस्टॉल करें। मुफ्त और प्रीमियम वॉलपेपर लाइब्रेरी।',
        website_desc='iPhone और iPad के लिए एनिमेटेड और मोशन वॉलपेपर की चयनित लाइब्रेरी, जिन्हें Nugget टूल से iOS 17–26 पर इंस्टॉल किया जा सकता है।',
        eyebrow='Nugget के लिए मोशन वॉलपेपर',
        h1='Nugget वॉलपेपर लाइब्रेरी<br />iPhone के लिए एनिमेटेड वॉलपेपर',
        sub='आपके iPhone और iPad के लिए चयनित डायनामिक, एनिमेटेड और मोशन वॉलपेपर। इन्हें <strong>Nugget टूल</strong> से सीधे इंस्टॉल करें — जेलब्रेक की जरूरत नहीं — iOS 17 से iOS 26 तक।',
        cta_primary='Nugget वॉलपेपर लाइब्रेरी देखें →',
        cta_ghost='आधिकारिक इंस्टॉल ट्यूटोरियल',
        spec_ios='<b>iOS 17 – iOS 26</b> सपोर्ट',
        spec_device='iPhone और <b>iPad</b>',
        spec_free='<b>मुफ्त</b> और प्रीमियम',
        spec_jailbreak='जेलब्रेक की जरूरत नहीं',
        about_h2='Nugget वॉलपेपर क्या है?',
        about_muted='Nugget टूल से अपने iPhone पर एनिमेटेड वॉलपेपर लगाने के बारे में वह सब कुछ जो आपको जानना चाहिए।',
        about_p1='<strong>Nugget वॉलपेपर</strong> iPhone और iPad के लिए एक एनिमेटेड, मोशन-आधारित वॉलपेपर है जिसे आप <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> के माध्यम से इंस्टॉल करते हैं — LeMinLimez का एक ओपन-सोर्स iOS कस्टमाइज़ेशन टूल, जो sparserestore और BookRestore विधियों से Apple डिवाइस को <em>बिना पूर्ण जेलब्रेक के</em> मॉडिफाई करता है।',
        about_p2='आपके आइकन के पीछे एक स्थिर इमेज के बजाय, Nugget वॉलपेपर आपकी लॉक स्क्रीन और होम स्क्रीन पर हिल, रिएक्ट और एनिमेट हो सकता है। <a href="https://mwallx.com/" rel="noopener">Nugget वॉलपेपर प्रोजेक्ट</a> इन मोशन वॉलपेपर की एक चयनित लाइब्रेरी रखता है, हर पेज पर लाइव एनिमेटेड GIF प्रीव्यू के साथ।',
        f1_h='मोशन वॉलपेपर लाइब्रेरी', f1_p='एनीमे, स्पोर्ट्स, म्यूजिक, 3D और लाइफस्टाइल थीम में सैकड़ों चयनित डायनामिक वॉलपेपर फॉर्मेट।',
        f2_h='Nugget टूल', f2_p='ओपन-सोर्स Windows / macOS ऐप जो आपके डिवाइस पर एनिमेटेड वॉलपेपर लगाता है — जेलब्रेक की जरूरत नहीं।',
        f3_h='स्टेप-बाय-स्टेप गाइड', f3_p='बैकअप से लाइव एनिमेटेड लॉक स्क्रीन तक का शुरुआती-अनुकूल इंस्टॉल ट्यूटोरियल।',
        catalog_h2='Nugget वॉलपेपर कैटलॉग में क्या है',
        catalog_muted='mwallx.com पर Nugget वॉलपेपर कलेक्शन देखें — डाउनलोड से पहले मोशन प्रीव्यू करें।',
        cat1_b='एनीमे और मंगा', cat1_h='ईवा, डेमन स्लेयर, मार्वल', cat1_p='आपकी पसंदीदा सीरीज़ के शानदार एनिमेटेड वॉलपेपर।',
        cat2_b='स्पोर्ट्स', cat2_h='फुटबॉल और एस्पोर्ट्स', cat2_p='आर्सेनल से FIFA 2026 तक टीम और खिलाड़ियों के मोशन वॉलपेपर।',
        cat3_b='3D और क्रिएटिव', cat3_h='3D फेस और ड्रीम सीन', cat3_p='डेप्थ-आधारित 3D और सपनों जैसे ग्रहों के वॉलपेपर जो जीवंत लगते हैं।',
        cat4_b='मुफ्त', cat4_h='मुफ्त और प्रीमियम', cat4_p='मुफ्त या प्रीमियम फ़िल्टर करके वही Nugget वॉलपेपर खोजें जो आप चाहते हैं।',
        cat5_b='आधिकारिक', cat5_h='Apple-फॉर्मेट वॉलपेपर', cat5_p='आधिकारिक फॉर्मेट के वॉलपेपर पैक, साथ में Nugget कम्युनिटी बिल्ड।',
        cat6_b='ताज़ा ड्रॉप', cat6_h='हर हफ्ते नए', cat6_p='Nugget वॉलपेपर लाइब्रेरी में हर समय नए वॉलपेपर जुड़ते रहते हैं।',
        install_h2='Nugget वॉलपेपर कैसे इंस्टॉल करें',
        install_muted='डाउनलोड से मूविंग लॉक स्क्रीन तक चार आसान कदम।',
        step1_h='अपना वॉलपेपर चुनें', step1_p='<a href="https://mwallx.com/{L}/wallpapers" rel="noopener">Nugget वॉलपेपर लाइब्रेरी</a> ब्राउज़ करें, एनिमेटेड GIF प्रीव्यू देखें और पैक डाउनलोड करें।',
        step2_h='अपने डिवाइस का बैकअप लें', step2_p='अपने iPhone या iPad को PC से कनेक्ट करें और पूरा बैकअप बनाएं। किसी भी iOS मॉडिफिकेशन टूल का उपयोग करने से पहले हमेशा बैकअप लें।',
        step3_h='Nugget से लागू करें', step3_p='Nugget ऐप चलाएं, वॉलपेपर को PosterBoard फीचर में लोड करें, और <a href="https://nugget.host/tutorial/nugget" rel="noopener">आधिकारिक ट्यूटोरियल</a> के अनुसार अपने डिवाइस को रिस्टोर करें।',
        step4_h='मोशन का आनंद लें', step4_p='अब आपका iPhone असली एनिमेटेड वॉलपेपर चलाता है — पैन करें, स्वाइप करें और इसे लॉक स्क्रीन और होम स्क्रीन पर जीवंत होते देखें।',
        disclaimer='<strong>सुरक्षा नोट:</strong> Nugget sparserestore और BookRestore विधियों का उपयोग करता है और <strong>iOS 27 के साथ संगत नहीं है</strong> (Apple ने रिस्टोर विधि पैच की है, डेटा लॉस संभव है)। केवल उन्हीं वॉलपेपर को इंस्टॉल करें जिन पर आप भरोसा करते हैं, आधिकारिक गाइड का पालन करें और हमेशा बैकअप रखें।',
        faq_h2='Nugget वॉलपेपर FAQ',
        faq_muted='iPhone मोशन वॉलपेपर के बारे में लोगों के सबसे आम सवालों के त्वरित उत्तर।',
        faq=[
            ('Nugget वॉलपेपर क्या है?', 'Nugget वॉलपेपर एक एनिमेटेड या मोशन वॉलपेपर है जो Nugget टूल से इंस्टॉल होता है — एक ओपन-सोर्स iOS कस्टमाइज़ेशन यूटिलिटी। यह स्थिर लॉक-स्क्रीन इमेज से कहीं आगे है — यह आपकी स्क्रीन पर एनिमेट और मूव हो सकता है, जो Apple नेटिव रूप से नहीं देता।'),
            ('Nugget वॉलपेपर किन iOS वर्जन को सपोर्ट करता है?', 'Nugget वॉलपेपर iOS और iPadOS 17 से 26 तक, साथ ही जेनेरिक प्लेटफॉर्म को सपोर्ट करते हैं। iOS 27 से पूरी तरह बचें — वहाँ Nugget की रिस्टोर विधि पैच हो चुकी है और डेटा लॉस संभव है।'),
            ('मैं अपने iPhone पर Nugget वॉलपेपर कैसे इंस्टॉल करूं?', 'लाइब्रेरी से वॉलपेपर डाउनलोड करें, Windows या macOS पर Nugget टूल चलाएं (Linux भी काम करता है), और PosterBoard फीचर से लागू करें। पूरा ट्यूटोरियल <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a> पर है।'),
            ('क्या Nugget वॉलपेपर इंस्टॉल करने के लिए जेलब्रेक जरूरी है?', 'नहीं। Nugget sparserestore और BookRestore नॉन-जेलब्रेक विधियों से काम करता है, इसलिए आप iOS 17–26 पर स्टॉक iPhone में एनिमेटेड वॉलपेपर जोड़ सकते हैं।'),
            ('क्या मुफ्त Nugget वॉलपेपर हैं?', 'हाँ। <a href="https://mwallx.com" rel="noopener">mwallx.com</a> की लाइब्रेरी में हर वॉलपेपर के एनिमेटेड GIF प्रीव्यू के साथ मुफ्त और प्रीमियम दोनों चयनित वॉलपेपर हैं।'),
        ],
        footer_note='Nugget वॉलपेपर एक कम्युनिटी प्रोजेक्ट है। यह साइट Nugget वॉलपेपर लाइब्रेरी का परिचय देती है और आधिकारिक <a href="https://mwallx.com/" rel="noopener">mwallx.com</a> सेवा से लिंक करती है। Apple Inc. से संबद्ध नहीं। © 2026 Nugget वॉलपेपर।',
    ),
    'es': dict(
        title='Nugget Wallpaper — Fondos de pantalla animados y en movimiento para iPhone (iOS 17–26)',
        meta_desc='Biblioteca de Nugget Wallpaper: fondos de pantalla animados y en movimiento para iPhone y iPad, instalables en iOS 17–26 con la herramienta Nugget. Explora, previsualiza y descarga fondos dinámicos gratis y premium.',
        og_title='Nugget Wallpaper — Fondos animados y en movimiento para iPhone (iOS 17–26)',
        og_desc='Fondos de pantalla dinámicos y animados para iPhone/iPad. Instálalos en iOS 17–26 con la herramienta Nugget. Biblioteca gratis y premium.',
        website_desc='Biblioteca seleccionada de fondos de pantalla animados y en movimiento para iPhone y iPad, instalables en iOS 17–26 con la herramienta Nugget.',
        eyebrow='Fondos en movimiento para Nugget',
        h1='Biblioteca Nugget Wallpaper<br />Fondos animados para iPhone',
        sub='Fondos dinámicos, animados y en movimiento seleccionados para tu iPhone y iPad. Instálalos directamente con la <strong>herramienta Nugget</strong>, sin jailbreak — compatible con iOS 17 a iOS 26.',
        cta_primary='Explorar la biblioteca Nugget Wallpaper →',
        cta_ghost='Tutorial oficial de instalación',
        spec_ios='Compatible <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone y <b>iPad</b>',
        spec_free='<b>Gratis</b> y premium',
        spec_jailbreak='Sin jailbreak',
        about_h2='¿Qué es un Nugget Wallpaper?',
        about_muted='Todo lo que necesitas saber para poner fondos animados en tu iPhone con la herramienta Nugget.',
        about_p1='Un <strong>Nugget wallpaper</strong> es un fondo de pantalla animado y en movimiento para iPhone y iPad que instalas mediante <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> — una utilidad de personalización de iOS de código abierto de LeMinLimez que usa los métodos sparserestore y BookRestore para modificar dispositivos Apple <em>sin un jailbreak completo</em>.',
        about_p2='En lugar de una imagen estática detrás de tus iconos, un Nugget wallpaper puede moverse, reaccionar y animarse en tu pantalla de bloqueo y pantalla de inicio. El <a href="https://mwallx.com/" rel="noopener">proyecto Nugget Wallpaper</a> aloja una biblioteca seleccionada de estos fondos, con previsualizaciones GIF animadas en cada página.',
        f1_h='Biblioteca de fondos en movimiento', f1_p='Cientos de formatos dinámicos seleccionados en temas de anime, deportes, música, 3D y estilo de vida.',
        f2_h='Herramienta Nugget', f2_p='La app de código abierto para Windows / macOS que aplica fondos animados a tu dispositivo — sin jailbreak.',
        f3_h='Guía paso a paso', f3_p='Un tutorial de instalación para principiantes, del backup a una pantalla de bloqueo animada.',
        catalog_h2='Qué hay dentro del catálogo de Nugget wallpaper',
        catalog_muted='Explora la colección de Nugget wallpaper en mwallx.com — previsualiza el movimiento antes de descargar.',
        cat1_b='Anime y manga', cat1_h='Eva, Demon Slayer, Marvel', cat1_p='Impresionantes fondos animados de tus series favoritas.',
        cat2_b='Deportes', cat2_h='Fútbol y esports', cat2_p='Fondos en movimiento de equipos y jugadores, de Arsenal a FIFA 2026.',
        cat3_b='3D y creativo', cat3_h='Caras 3D y escenas soñadas', cat3_p='Fondos 3D con profundidad y planetas de ensueño que se sienten vivos.',
        cat4_b='Gratis', cat4_h='Gratis y premium', cat4_p='Filtra por gratis o premium y encuentra exactamente el Nugget wallpaper que quieres.',
        cat5_b='Oficial', cat5_h='Fondos en formato Apple', cat5_p='Paquetes de fondos en formato oficial, además de builds de la comunidad Nugget.',
        cat6_b='Novedades', cat6_h='Nuevos cada semana', cat6_p='Siempre se añaden nuevos Nugget wallpapers a la biblioteca.',
        install_h2='Cómo instalar un Nugget wallpaper',
        install_muted='Cuatro pasos simples de la descarga a una pantalla de bloqueo en movimiento.',
        step1_h='Elige tu fondo', step1_p='Explora la <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">biblioteca de Nugget wallpaper</a>, mira el GIF animado y descarga el paquete.',
        step2_h='Haz una copia de seguridad', step2_p='Conecta tu iPhone o iPad a un PC y crea una copia completa. Siempre haz backup antes de usar cualquier herramienta de modificación de iOS.',
        step3_h='Aplícalo con Nugget', step3_p='Ejecuta la app Nugget, carga el fondo en la función PosterBoard y restaura tu dispositivo siguiendo el <a href="https://nugget.host/tutorial/nugget" rel="noopener">tutorial oficial</a>.',
        step4_h='Disfruta del movimiento', step4_p='Tu iPhone ahora usa un verdadero fondo animado: desliza y míralo cobrar vida en la pantalla de bloqueo y de inicio.',
        disclaimer='<strong>Nota de seguridad:</strong> Nugget usa los métodos sparserestore y BookRestore y <strong>no es compatible con iOS 27</strong> (Apple parcheó el método de restauración y puede haber pérdida de datos). Instala solo fondos de confianza, sigue la guía oficial y mantén siempre un backup.',
        faq_h2='Preguntas frecuentes sobre Nugget wallpaper',
        faq_muted='Respuestas rápidas a las preguntas más comunes sobre fondos en movimiento para iPhone.',
        faq=[
            ('¿Qué es un Nugget wallpaper?', 'Un Nugget wallpaper es un fondo animado o en movimiento para iPhone y iPad que se instala con la herramienta Nugget, una utilidad de personalización de iOS de código abierto. Va mucho más allá de una imagen estática: puede animarse y moverse por tu pantalla, algo que Apple no ofrece de forma nativa.'),
            ('¿Qué versiones de iOS soporta un Nugget wallpaper?', 'Los Nugget wallpapers soportan iOS y iPadOS 17 a 26, además de plataformas genéricas. Evita iOS 27 por completo: allí el método de restauración de Nugget está parcheado y es probable la pérdida de datos.'),
            ('¿Cómo instalo un Nugget wallpaper en mi iPhone?', 'Descarga un fondo de la biblioteca, ejecuta la herramienta Nugget en Windows o macOS (Linux también funciona) y aplícalo con la función PosterBoard. El tutorial completo está en <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>.'),
            ('¿Instalar un Nugget wallpaper requiere jailbreak?', 'No. Nugget funciona con los métodos no-jailbreak sparserestore y BookRestore, así que puedes añadir fondos animados a un iPhone sin modificar mientras estés en iOS 17–26.'),
            ('¿Hay Nugget wallpapers gratis?', 'Sí. La biblioteca de <a href="https://mwallx.com" rel="noopener">mwallx.com</a> tiene fondos gratis y premium seleccionados, con previsualizaciones GIF animadas para cada uno.'),
        ],
        footer_note='Nugget wallpaper es un proyecto comunitario. Este sitio presenta la biblioteca de Nugget wallpaper y enlaza al servicio oficial <a href="https://mwallx.com/" rel="noopener">mwallx.com</a>. No afiliado con Apple Inc. © 2026 Nugget Wallpaper.',
    ),
    'fr': dict(
        title='Nugget Wallpaper — Fonds d\'écran animés et en mouvement pour iPhone (iOS 17–26)',
        meta_desc='Bibliothèque Nugget Wallpaper : fonds d\'écran animés et en mouvement pour iPhone et iPad, installables sur iOS 17–26 avec l\'outil Nugget. Parcourez, prévisualisez et téléchargez des fonds dynamiques gratuits et premium.',
        og_title='Nugget Wallpaper — Fonds animés et en mouvement pour iPhone (iOS 17–26)',
        og_desc='Fonds d\'écran dynamiques et animés pour iPhone/iPad. Installez-les sur iOS 17–26 avec l\'outil Nugget. Bibliothèque gratuite et premium.',
        website_desc='Bibliothèque sélectionnée de fonds d\'écran animés et en mouvement pour iPhone et iPad, installables sur iOS 17–26 avec l\'outil Nugget.',
        eyebrow='Fonds en mouvement pour Nugget',
        h1='Bibliothèque Nugget Wallpaper<br />Fonds animés pour iPhone',
        sub='Fonds dynamiques, animés et en mouvement sélectionnés pour votre iPhone et iPad. Installez-les directement avec <strong>l\'outil Nugget</strong>, sans jailbreak — compatible avec iOS 17 à iOS 26.',
        cta_primary='Explorer la bibliothèque Nugget Wallpaper →',
        cta_ghost='Tutoriel d\'installation officiel',
        spec_ios='Compatible <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone et <b>iPad</b>',
        spec_free='<b>Gratuit</b> et premium',
        spec_jailbreak='Sans jailbreak',
        about_h2='Qu\'est-ce qu\'un Nugget Wallpaper ?',
        about_muted='Tout ce que vous devez savoir pour mettre des fonds animés sur votre iPhone avec l\'outil Nugget.',
        about_p1='Un <strong>Nugget wallpaper</strong> est un fond d\'écran animé et en mouvement pour iPhone et iPad que vous installez avec <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> — un utilitaire de personnalisation iOS open source de LeMinLimez qui utilise les méthodes sparserestore et BookRestore pour modifier les appareils Apple <em>sans jailbreak complet</em>.',
        about_p2='Au lieu d\'une image statique derrière vos icônes, un Nugget wallpaper peut bouger, réagir et s\'animer sur votre écran de verrouillage et votre écran d\'accueil. Le <a href="https://mwallx.com/" rel="noopener">projet Nugget Wallpaper</a> héberge une bibliothèque sélectionnée de ces fonds, avec des aperçus GIF animés sur chaque page.',
        f1_h='Bibliothèque de fonds en mouvement', f1_p='Des centaines de formats dynamiques sélectionnés en thèmes anime, sport, musique, 3D et lifestyle.',
        f2_h='Outil Nugget', f2_p='L\'app open source Windows / macOS qui applique des fonds animés à votre appareil — sans jailbreak.',
        f3_h='Guide pas à pas', f3_p='Un tutoriel d\'installation pour débutants, de la sauvegarde à un écran de verrouillage animé.',
        catalog_h2='Ce qu\'il y a dans le catalogue Nugget wallpaper',
        catalog_muted='Explorez la collection Nugget wallpaper sur mwallx.com — prévisualisez le mouvement avant de télécharger.',
        cat1_b='Anime et manga', cat1_h='Eva, Demon Slayer, Marvel', cat1_p='De superbes fonds animés de vos séries préférées.',
        cat2_b='Sport', cat2_h='Football et esports', cat2_p='Fonds en mouvement d\'équipes et de joueurs, d\'Arsenal à la FIFA 2026.',
        cat3_b='3D et créatif', cat3_h='Visages 3D et scènes oniriques', cat3_p='Fonds 3D avec profondeur et planètes de rêve qui semblent vivants.',
        cat4_b='Gratuit', cat4_h='Gratuit et premium', cat4_p='Filtrez par gratuit ou premium pour trouver exactement le Nugget wallpaper que vous voulez.',
        cat5_b='Officiel', cat5_h='Fonds au format Apple', cat5_p='Des packs de fonds au format officiel, plus les builds de la communauté Nugget.',
        cat6_b='Nouveautés', cat6_h='Nouveaux chaque semaine', cat6_p='De nouveaux Nugget wallpapers sont ajoutés à la bibliothèque en permanence.',
        install_h2='Comment installer un Nugget wallpaper',
        install_muted='Quatre étapes simples, du téléchargement à un écran de verrouillage animé.',
        step1_h='Choisissez votre fond', step1_p='Parcourez la <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">bibliothèque Nugget wallpaper</a>, regardez le GIF animé et téléchargez le pack.',
        step2_h='Sauvegardez votre appareil', step2_p='Connectez votre iPhone ou iPad à un PC et créez une sauvegarde complète. Sauvegardez toujours avant d\'utiliser un outil de modification iOS.',
        step3_h='Appliquez-le avec Nugget', step3_p='Lancez l\'app Nugget, chargez le fond dans la fonction PosterBoard et restaurez votre appareil en suivant le <a href="https://nugget.host/tutorial/nugget" rel="noopener">tutoriel officiel</a>.',
        step4_h='Profitez du mouvement', step4_p='Votre iPhone utilise désormais un vrai fond animé — glissez et regardez-le prendre vie sur l\'écran de verrouillage et d\'accueil.',
        disclaimer='<strong>Note de sécurité :</strong> Nugget utilise les méthodes sparserestore et BookRestore et <strong>n\'est pas compatible avec iOS 27</strong> (Apple a patché la méthode de restauration, des pertes de données sont possibles). Installez uniquement des fonds de confiance, suivez le guide officiel et gardez toujours une sauvegarde.',
        faq_h2='FAQ Nugget wallpaper',
        faq_muted='Réponses rapides aux questions les plus posées sur les fonds en mouvement pour iPhone.',
        faq=[
            ('Qu\'est-ce qu\'un Nugget wallpaper ?', 'Un Nugget wallpaper est un fond d\'écran animé ou en mouvement pour iPhone et iPad installé avec l\'outil Nugget, un utilitaire de personnalisation iOS open source. Il va bien au-delà d\'une image statique : il peut s\'animer et se déplacer sur votre écran, ce qu\'Apple ne propose pas nativement.'),
            ('Quelles versions d\'iOS supporte un Nugget wallpaper ?', 'Les Nugget wallpapers supportent iOS et iPadOS 17 à 26, plus les plateformes génériques. Évitez totalement iOS 27 — la méthode de restauration de Nugget y est patchée et la perte de données est probable.'),
            ('Comment installer un Nugget wallpaper sur mon iPhone ?', 'Téléchargez un fond depuis la bibliothèque, lancez l\'outil Nugget sur Windows ou macOS (Linux fonctionne aussi) et appliquez-le via la fonction PosterBoard. Le tutoriel complet est sur <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>.'),
            ('Installer un Nugget wallpaper nécessite-t-il un jailbreak ?', 'Non. Nugget fonctionne via les méthodes non-jailbreak sparserestore et BookRestore, vous pouvez donc ajouter des fonds animés sur un iPhone classique tant que vous êtes en iOS 17–26.'),
            ('Y a-t-il des Nugget wallpapers gratuits ?', 'Oui. La bibliothèque de <a href="https://mwallx.com" rel="noopener">mwallx.com</a> propose des fonds sélectionnés gratuits et premium, avec un aperçu GIF animé pour chacun.'),
        ],
        footer_note='Nugget wallpaper est un projet communautaire. Ce site présente la bibliothèque Nugget wallpaper et renvoie vers le service officiel <a href="https://mwallx.com/" rel="noopener">mwallx.com</a>. Non affilié à Apple Inc. © 2026 Nugget Wallpaper.',
    ),
    'ar': dict(
        title='Nugget Wallpaper — خلفيات متحركة وحيوية لآيفون (iOS 17–26)',
        meta_desc='مكتبة Nugget Wallpaper: خلفيات متحركة وحيوية مختارة لآيفون وآيباد، قابلة للتثبيت على iOS 17–26 باستخدام أداة Nugget. تصفح وشاهد وفكّم خلفيات ديناميكية مجانية ومميزة.',
        og_title='Nugget Wallpaper — خلفيات متحركة وحيوية لآيفون (iOS 17–26)',
        og_desc='خلفيات ديناميكية ومتحركة لآيفون/آيباد. ثبّتها على iOS 17–26 باستخدام أداة Nugget. مكتبة مجانية ومميزة.',
        website_desc='مكتبة مختارة من الخلفيات المتحركة والحيوية لآيفون وآيباد، قابلة للتثبيت على iOS 17–26 باستخدام أداة Nugget.',
        eyebrow='خلفيات متحركة لـ Nugget',
        h1='مكتبة Nugget Wallpaper<br />خلفيات متحركة لآيفون',
        sub='خلفيات ديناميكية ومتحركة وحيوية مختارة لجهاز آيفون وآيباد الخاص بك. ثبّتها مباشرة باستخدام <strong>أداة Nugget</strong>، دون الحاجة إلى كسر الحماية — متوافقة مع iOS 17 حتى iOS 26.',
        cta_primary='تصفح مكتبة Nugget Wallpaper ←',
        cta_ghost='دليل التثبيت الرسمي',
        spec_ios='متوافق <b>iOS 17 – iOS 26</b>',
        spec_device='آيفون و<b>آيباد</b>',
        spec_free='<b>مجاني</b> ومميز',
        spec_jailbreak='بدون كسر حماية',
        about_h2='ما هو Nugget Wallpaper؟',
        about_muted='كل ما تحتاج معرفته لوضع خلفيات متحركة على آيفون باستخدام أداة Nugget.',
        about_p1='<strong>Nugget wallpaper</strong> هو خلفية متحركة وحيوية لآيفون وآيباد تقوم بتثبيتها باستخدام <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> — أداة تخصيص iOS مفتوحة المصدر من LeMinLimez تستخدم طريقتي sparserestore وBookRestore لتعديل أجهزة Apple <em>دون كسر حماية كامل</em>.',
        about_p2='بدلاً من صورة ثابتة خلف أيقوناتك، يمكن لخلفية Nugget أن تتحرك وتتفاعل وتتحرك عبر شاشة القفل والشاشة الرئيسية. يستضيف <a href="https://mwallx.com/" rel="noopener">مشروع Nugget Wallpaper</a> مكتبة مختارة من هذه الخلفيات المتحركة، مع معاينات GIF متحركة في كل صفحة.',
        f1_h='مكتبة الخلفيات المتحركة', f1_p='مئات من صيغ الخلفيات الديناميكية المختارة عبر مواضيع الأنمي والرياضة والموسيقى و3D وأسلوب الحياة.',
        f2_h='أداة Nugget', f2_p='تطبيق مفتوح المصدر لنظامي Windows / macOS يطبّق الخلفيات المتحركة على جهازك — دون كسر حماية.',
        f3_h='دليل خطوة بخطوة', f3_p='دليل تثبيت مناسب للمبتدئين، من النسخ الاحتياطي إلى شاشة قفل متحركة.',
        catalog_h2='ماذا يوجد داخل كتالوج Nugget wallpaper',
        catalog_muted='استكشف مجموعة Nugget wallpaper على mwallx.com — شاهد الحركة قبل التنزيل.',
        cat1_b='أنمي ومانغا', cat1_h='إيفا، ديمون سلاير، مارفل', cat1_p='خلفيات متحركة مذهلة من مسلسلاتك المفضلة.',
        cat2_b='رياضة', cat2_h='كرة القدم والرياضات الإلكترونية', cat2_p='خلفيات متحركة للفرق واللاعبين، من أرسنال إلى كأس العالم 2026.',
        cat3_b='3D وإبداعي', cat3_h='وجوه 3D ومشاهد حالمة', cat3_p='خلفيات 3D بعمق وكواكب حالمة تبدو حية.',
        cat4_b='مجاني', cat4_h='مجاني ومميز', cat4_p='قم بالتصفية حسب المجاني أو المميز للعثور على خلفية Nugget التي تريدها بالضبط.',
        cat5_b='رسمي', cat5_h='خلفيات بصيغة Apple', cat5_p='حزم خلفيات بالصيغة الرسمية، بالإضافة إلى إصدارات مجتمع Nugget.',
        cat6_b='إصدارات جديدة', cat6_h='جديد كل أسبوع', cat6_p='تُضاف خلفيات Nugget جديدة إلى المكتبة باستمرار.',
        install_h2='كيف تثبّت Nugget wallpaper',
        install_muted='أربع خطوات بسيطة من التنزيل إلى شاشة قفل متحركة.',
        step1_h='اختر خلفيتك', step1_p='تصفح <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">مكتبة Nugget wallpaper</a>، وشاهد معاينة GIF المتحركة وفكّم الحزمة.',
        step2_h='انسخ جهازك احتياطياً', step2_p='وصّل آيفون أو آيباد بجهاز كمبيوتر وأنشئ نسخة احتياطية كاملة. انسخ احتياطياً دائماً قبل استخدام أي أداة تعديل iOS.',
        step3_h='طبّقها باستخدام Nugget', step3_p='شغّل تطبيق Nugget، وحمّل الخلفية في ميزة PosterBoard، واستعد جهازك باتباع <a href="https://nugget.host/tutorial/nugget" rel="noopener">الدليل الرسمي</a>.',
        step4_h='استمتع بالحركة', step4_p='أصبح آيفونك الآن يعمل بخلفية متحركة حقيقية — مرّر وشاهدها تنبض بالحياة على شاشة القفل والشاشة الرئيسية.',
        disclaimer='<strong>ملاحظة أمان:</strong> يستخدم Nugget طريقتي sparserestore وBookRestore وهو <strong>غير متوافق مع iOS 27</strong> (قامت Apple بترقيع طريقة الاستعادة، وقد يحدث فقدان للبيانات). ثبّت فقط الخلفيات التي تثق بها، واتبع الدليل الرسمي، واحتفظ دائماً بنسخة احتياطية.',
        faq_h2='الأسئلة الشائعة حول Nugget wallpaper',
        faq_muted='إجابات سريعة على أكثر الأسئلة شيوعاً حول الخلفيات المتحركة لآيفون.',
        faq=[
            ('ما هو Nugget wallpaper؟', 'Nugget wallpaper هو خلفية متحركة أو حيوية لآيفون وآيباد يتم تثبيتها بأداة Nugget، وهي أداة تخصيص iOS مفتوحة المصدر. تتجاوز بكثير صورة شاشة قفل ثابتة — يمكنها أن تتحرك وتتفاعل عبر شاشتك، وهو ما لا تقدمه Apple أصلاً.'),
            ('ما إصدارات iOS التي يدعمها Nugget wallpaper؟', 'تدعم خلفيات Nugget نظامي iOS وiPadOS 17 حتى 26، بالإضافة إلى المنصات العامة. تجنب iOS 27 تماماً — طريقة الاستعادة في Nugget مرقّعة هناك ومن المرجح فقدان البيانات.'),
            ('كيف أثبّت Nugget wallpaper على آيفوني؟', 'حمّل خلفية من المكتبة، وشغّل أداة Nugget على Windows أو macOS (يعمل Linux أيضاً)، وطبّقها عبر ميزة PosterBoard. الشرح الكامل على <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>.'),
            ('هل يتطلب تثبيت Nugget wallpaper كسر الحماية؟', 'لا. يعمل Nugget عبر طريقتي sparserestore وBookRestore بدون كسر حماية، لذا يمكنك إضافة خلفيات متحركة إلى آيفون عادي طالما أنك على iOS 17–26.'),
            ('هل توجد خلفيات Nugget مجانية؟', 'نعم. تحتوي مكتبة <a href="https://mwallx.com" rel="noopener">mwallx.com</a> على خلفيات مجانية ومميزة مختارة، مع معاينات GIF متحركة لكل واحدة منها.'),
        ],
        footer_note='Nugget wallpaper مشروع مجتمعي. يعرّف هذا الموقع بمكتبة Nugget wallpaper ويربط بالخدمة الرسمية <a href="https://mwallx.com/" rel="noopener">mwallx.com</a>. غير تابع لشركة Apple Inc. © 2026 Nugget Wallpaper.',
    ),
    'bn': dict(
        title='Nugget ওয়ালপেপার — iPhone-এর জন্য অ্যানিমেটেড এবং মোশন ওয়ালপেপার (iOS 17–26)',
        meta_desc='Nugget ওয়ালপেপার লাইব্রেরি: iPhone এবং iPad-এর জন্য নির্বাচিত অ্যানিমেটেড ও মোশন ওয়ালপেপার, যা Nugget টুল দিয়ে iOS 17–26-এ ইনস্টল করা যায়। বিনামূল্যে ও প্রিমিয়াম ডায়নামিক ওয়ালপেপার ব্রাউজ, প্রিভিউ ও ডাউনলোড করুন।',
        og_title='Nugget ওয়ালপেপার — iPhone-এর জন্য অ্যানিমেটেড এবং মোশন ওয়ালপেপার (iOS 17–26)',
        og_desc='iPhone/iPad-এর জন্য নির্বাচিত ডায়নামিক ও মোশন ওয়ালপেপার। Nugget টুল দিয়ে iOS 17–26-এ ইনস্টল করুন। বিনামূল্যে ও প্রিমিয়াম ওয়ালপেপার লাইব্রেরি।',
        website_desc='iPhone এবং iPad-এর জন্য অ্যানিমেটেড ও মোশন ওয়ালপেপারের নির্বাচিত লাইব্রেরি, যা Nugget টুল দিয়ে iOS 17–26-এ ইনস্টল করা যায়।',
        eyebrow='Nugget-এর জন্য মোশন ওয়ালপেপার',
        h1='Nugget ওয়ালপেপার লাইব্রেরি<br />iPhone-এর জন্য অ্যানিমেটেড ওয়ালপেপার',
        sub='আপনার iPhone ও iPad-এর জন্য নির্বাচিত ডায়নামিক, অ্যানিমেটেড ও মোশন ওয়ালপেপার। এগুলো <strong>Nugget টুল</strong> দিয়ে সরাসরি ইনস্টল করুন — জেলব্রেক লাগবে না — iOS 17 থেকে iOS 26-এর সাথে সামঞ্জস্যপূর্ণ।',
        cta_primary='Nugget ওয়ালপেপার লাইব্রেরি দেখুন →',
        cta_ghost='অফিসিয়াল ইনস্টল টিউটোরিয়াল',
        spec_ios='সাপোর্ট <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone ও <b>iPad</b>',
        spec_free='<b>ফ্রি</b> ও প্রিমিয়াম',
        spec_jailbreak='জেলব্রেক লাগবে না',
        about_h2='Nugget ওয়ালপেপার কী?',
        about_muted='Nugget টুল দিয়ে আপনার iPhone-এ অ্যানিমেটেড ওয়ালপেপার বসানোর সব তথ্য।',
        about_p1='<strong>Nugget ওয়ালপেপার</strong> হলো iPhone ও iPad-এর জন্য একটি অ্যানিমেটেড, মোশন-ভিত্তিক ওয়ালপেপার যা আপনি <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> দিয়ে ইনস্টল করেন — LeMinLimez-এর একটি ওপেন-সোর্স iOS কাস্টমাইজেশন টুল, যা sparserestore ও BookRestore পদ্ধতিতে Apple ডিভাইস <em>সম্পূর্ণ জেলব্রেক ছাড়াই</em> পরিবর্তন করে।',
        about_p2='আপনার আইকনের পেছনে স্থির ছবির বদলে, একটি Nugget ওয়ালপেপার আপনার লক স্ক্রিন ও হোম স্ক্রিনে নড়াচড়া, প্রতিক্রিয়া ও অ্যানিমেশন করতে পারে। <a href="https://mwallx.com/" rel="noopener">Nugget ওয়ালপেপার প্রজেক্ট</a> এই মোশন ওয়ালপেপারগুলোর একটি নির্বাচিত লাইব্রেরি হোস্ট করে, প্রতিটি পেজে লাইভ অ্যানিমেটেড GIF প্রিভিউ সহ।',
        f1_h='মোশন ওয়ালপেপার লাইব্রেরি', f1_p='অ্যানিমে, স্পোর্টস, মিউজিক, 3D ও লাইফস্টাইল থিমে শত শত নির্বাচিত ডায়নামিক ওয়ালপেপার ফরম্যাট।',
        f2_h='Nugget টুল', f2_p='ওপেন-সোর্স Windows / macOS অ্যাপ যা আপনার ডিভাইসে অ্যানিমেটেড ওয়ালপেপার বসায় — জেলব্রেক ছাড়াই।',
        f3_h='ধাপে ধাপে গাইড', f3_p='ব্যাকআপ থেকে লাইভ অ্যানিমেটেড লক স্ক্রিন পর্যন্ত নতুনদের জন্য সহজ ইনস্টল টিউটোরিয়াল।',
        catalog_h2='Nugget ওয়ালপেপার ক্যাটালগে কী আছে',
        catalog_muted='mwallx.com-এ Nugget ওয়ালপেপার কালেকশন দেখুন — ডাউনলোডের আগে মোশন প্রিভিউ করুন।',
        cat1_b='অ্যানিমে ও মাঙ্গা', cat1_h='ইভা, ডেমন স্লেয়ার, মার্ভেল', cat1_p='আপনার প্রিয় সিরিজের চমৎকার অ্যানিমেটেড ওয়ালপেপার।',
        cat2_b='স্পোর্টস', cat2_h='ফুটবল ও এস্পোর্টস', cat2_p='আর্সেনাল থেকে FIFA 2026 পর্যন্ত দল ও খেলোয়াড়ের মোশন ওয়ালপেপার।',
        cat3_b='3D ও ক্রিয়েটিভ', cat3_h='3D ফেস ও ড্রিম সিন', cat3_p='গভীরতা-ভিত্তিক 3D ও স্বপ্নময় গ্রহের ওয়ালপেপার যা জীবন্ত মনে হয়।',
        cat4_b='ফ্রি', cat4_h='ফ্রি ও প্রিমিয়াম', cat4_p='ফ্রি বা প্রিমিয়াম ফিল্টার করে আপনার পছন্দের Nugget ওয়ালপেপার খুঁজুন।',
        cat5_b='অফিসিয়াল', cat5_h='Apple-ফরম্যাট ওয়ালপেপার', cat5_p='অফিসিয়াল ফরম্যাটে ওয়ালপেপার প্যাক, সাথে Nugget কমিউনিটি বিল্ড।',
        cat6_b='নতুন ড্রপ', cat6_h='প্রতি সপ্তাহে নতুন', cat6_p='লাইব্রেরিতে সব সময় নতুন Nugget ওয়ালপেপার যোগ হয়।',
        install_h2='Nugget ওয়ালপেপার কীভাবে ইনস্টল করবেন',
        install_muted='ডাউনলোড থেকে মোশন লক স্ক্রিন পর্যন্ত চারটি সহজ ধাপ।',
        step1_h='আপনার ওয়ালপেপার বেছে নিন', step1_p='<a href="https://mwallx.com/{L}/wallpapers" rel="noopener">Nugget ওয়ালপেপার লাইব্রেরি</a> ব্রাউজ করুন, অ্যানিমেটেড GIF প্রিভিউ দেখুন এবং প্যাক ডাউনলোড করুন।',
        step2_h='ডিভাইস ব্যাকআপ নিন', step2_p='আপনার iPhone বা iPad PC-তে সংযুক্ত করে সম্পূর্ণ ব্যাকআপ তৈরি করুন। যেকোনো iOS মডিফিকেশন টুল ব্যবহারের আগে সবসময় ব্যাকআপ নিন।',
        step3_h='Nugget দিয়ে প্রয়োগ করুন', step3_p='Nugget অ্যাপ চালান, PosterBoard ফিচারে ওয়ালপেপার লোড করুন এবং <a href="https://nugget.host/tutorial/nugget" rel="noopener">অফিসিয়াল টিউটোরিয়াল</a> অনুসরণ করে ডিভাইস রিস্টোর করুন।',
        step4_h='মোশন উপভোগ করুন', step4_p='আপনার iPhone এখন সত্যিকারের অ্যানিমেটেড ওয়ালপেপার চালায় — প্যান করুন, সোয়াইপ করুন এবং লক স্ক্রিন ও হোম স্ক্রিনে এটিকে জীবন্ত হতে দেখুন।',
        disclaimer='<strong>নিরাপত্তা নোট:</strong> Nugget sparserestore ও BookRestore পদ্ধতি ব্যবহার করে এবং <strong>iOS 27-এর সাথে সামঞ্জস্যপূর্ণ নয়</strong> (Apple রিস্টোর পদ্ধতি প্যাচ করেছে, ডেটা লস সম্ভব)। শুধু বিশ্বস্ত ওয়ালপেপার ইনস্টল করুন, অফিসিয়াল গাইড অনুসরণ করুন এবং সবসময় ব্যাকআপ রাখুন।',
        faq_h2='Nugget ওয়ালপেপার FAQ',
        faq_muted='iPhone-এর জন্য মোশন ওয়ালপেপার সম্পর্কে সবচেয়ে সাধারণ প্রশ্নের দ্রুত উত্তর।',
        faq=[
            ('Nugget ওয়ালপেপার কী?', 'Nugget ওয়ালপেপার হলো iPhone ও iPad-এর জন্য একটি অ্যানিমেটেড বা মোশন ওয়ালপেপার যা Nugget টুল দিয়ে ইনস্টল হয় — একটি ওপেন-সোর্স iOS কাস্টমাইজেশন ইউটিলিটি। এটি স্থির লক-স্ক্রিন ছবির চেয়ে অনেক বেশি — আপনার স্ক্রিনে অ্যানিমেট ও নড়তে পারে, যা Apple নেটিভভাবে দেয় না।'),
            ('Nugget ওয়ালপেপার কোন iOS ভার্সন সাপোর্ট করে?', 'Nugget ওয়ালপেপার iOS ও iPadOS 17 থেকে 26, সাথে জেনেরিক প্ল্যাটফর্ম সাপোর্ট করে। iOS 27 সম্পূর্ণ এড়িয়ে চলুন — সেখানে Nugget-এর রিস্টোর পদ্ধতি প্যাচ করা হয়েছে এবং ডেটা লস হওয়ার সম্ভাবনা রয়েছে।'),
            ('আমি কীভাবে আমার iPhone-এ Nugget ওয়ালপেপার ইনস্টল করব?', 'লাইব্রেরি থেকে ওয়ালপেপার ডাউনলোড করুন, Windows বা macOS-এ Nugget টুল চালান (Linux-ও কাজ করে), এবং PosterBoard ফিচার দিয়ে প্রয়োগ করুন। সম্পূর্ণ গাইড <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>-এ রয়েছে।'),
            ('Nugget ওয়ালপেপার ইনস্টল করতে জেলব্রেক লাগে?', 'না। Nugget sparserestore ও BookRestore নন-জেলব্রেক পদ্ধতিতে কাজ করে, তাই আপনি iOS 17–26-এ থাকলে স্টক iPhone-এ অ্যানিমেটেড ওয়ালপেপার যোগ করতে পারেন।'),
            ('ফ্রি Nugget ওয়ালপেপার আছে কি?', 'হ্যাঁ। <a href="https://mwallx.com" rel="noopener">mwallx.com</a>-এর লাইব্রেরিতে প্রতিটির অ্যানিমেটেড GIF প্রিভিউসহ ফ্রি ও প্রিমিয়াম নির্বাচিত ওয়ালপেপার আছে।'),
        ],
        footer_note='Nugget ওয়ালপেপার একটি কমিউনিটি প্রজেক্ট। এই সাইট Nugget ওয়ালপেপার লাইব্রেরি পরিচয় করিয়ে দেয় এবং অফিসিয়াল <a href="https://mwallx.com/" rel="noopener">mwallx.com</a> সার্ভিসে লিংক করে। Apple Inc.-এর সাথে সংশ্লিষ্ট নয়। © 2026 Nugget ওয়ালপেপার।',
    ),
    'pt': dict(
        title='Nugget Wallpaper — Papéis de parede animados e em movimento para iPhone (iOS 17–26)',
        meta_desc='Biblioteca Nugget Wallpaper: papéis de parede animados e em movimento selecionados para iPhone e iPad, instaláveis em iOS 17–26 com a ferramenta Nugget. Navegue, veja e baixe papéis dinâmicos gratuitos e premium.',
        og_title='Nugget Wallpaper — Papéis animados e em movimento para iPhone (iOS 17–26)',
        og_desc='Papéis de parede dinâmicos e animados para iPhone/iPad. Instale em iOS 17–26 com a ferramenta Nugget. Biblioteca gratuita e premium.',
        website_desc='Biblioteca selecionada de papéis de parede animados e em movimento para iPhone e iPad, instaláveis em iOS 17–26 com a ferramenta Nugget.',
        eyebrow='Papéis em movimento para Nugget',
        h1='Biblioteca Nugget Wallpaper<br />Papéis animados para iPhone',
        sub='Papéis dinâmicos, animados e em movimento selecionados para o seu iPhone e iPad. Instale-os diretamente com a <strong>ferramenta Nugget</strong>, sem jailbreak — compatível com iOS 17 a iOS 26.',
        cta_primary='Explorar a biblioteca Nugget Wallpaper →',
        cta_ghost='Tutorial oficial de instalação',
        spec_ios='Compatível <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone e <b>iPad</b>',
        spec_free='<b>Grátis</b> e premium',
        spec_jailbreak='Sem jailbreak',
        about_h2='O que é um Nugget Wallpaper?',
        about_muted='Tudo o que você precisa saber para colocar papéis animados no seu iPhone com a ferramenta Nugget.',
        about_p1='Um <strong>Nugget wallpaper</strong> é um papel de parede animado e em movimento para iPhone e iPad que você instala usando <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> — um utilitário de personalização de iOS de código aberto do LeMinLimez que usa os métodos sparserestore e BookRestore para modificar dispositivos Apple <em>sem um jailbreak completo</em>.',
        about_p2='Em vez de uma imagem estática atrás dos seus ícones, um Nugget wallpaper pode se mover, reagir e animar na sua Tela de Bloqueio e Tela Inicial. O <a href="https://mwallx.com/" rel="noopener">projeto Nugget Wallpaper</a> hospeda uma biblioteca selecionada desses papéis, com prévias em GIF animado em cada página.',
        f1_h='Biblioteca de papéis em movimento', f1_p='Centenas de formatos dinâmicos selecionados em temas de anime, esportes, música, 3D e estilo de vida.',
        f2_h='Ferramenta Nugget', f2_p='O app de código aberto para Windows / macOS que aplica papéis animados ao seu dispositivo — sem jailbreak.',
        f3_h='Guia passo a passo', f3_p='Um tutorial de instalação para iniciantes, do backup a uma Tela de Bloqueio animada.',
        catalog_h2='O que tem dentro do catálogo de Nugget wallpaper',
        catalog_muted='Explore a coleção Nugget wallpaper em mwallx.com — veja o movimento antes de baixar.',
        cat1_b='Anime e mangá', cat1_h='Eva, Demon Slayer, Marvel', cat1_p='Papéis animados impressionantes das suas séries favoritas.',
        cat2_b='Esportes', cat2_h='Futebol e esports', cat2_p='Papéis em movimento de times e jogadores, do Arsenal à FIFA 2026.',
        cat3_b='3D e criativo', cat3_h='Rostos 3D e cenas dos sonhos', cat3_p='Papéis 3D com profundidade e planetas de sonho que parecem vivos.',
        cat4_b='Grátis', cat4_h='Grátis e premium', cat4_p='Filtre por grátis ou premium e encontre exatamente o Nugget wallpaper que você quer.',
        cat5_b='Oficial', cat5_h='Papéis no formato Apple', cat5_p='Pacotes de papéis no formato oficial, além das builds da comunidade Nugget.',
        cat6_b='Novidades', cat6_h='Novos toda semana', cat6_p='Novos Nugget wallpapers são adicionados à biblioteca o tempo todo.',
        install_h2='Como instalar um Nugget wallpaper',
        install_muted='Quatro passos simples do download a uma Tela de Bloqueio em movimento.',
        step1_h='Escolha seu papel', step1_p='Navegue pela <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">biblioteca de Nugget wallpaper</a>, veja o GIF animado e baixe o pacote.',
        step2_h='Faça backup do dispositivo', step2_p='Conecte seu iPhone ou iPad a um PC e crie um backup completo. Sempre faça backup antes de usar qualquer ferramenta de modificação de iOS.',
        step3_h='Aplique com Nugget', step3_p='Execute o app Nugget, carregue o papel no recurso PosterBoard e restaure seu dispositivo seguindo o <a href="https://nugget.host/tutorial/nugget" rel="noopener">tutorial oficial</a>.',
        step4_h='Aproveite o movimento', step4_p='Seu iPhone agora roda um verdadeiro papel animado — deslize e veja-o ganhar vida na Tela de Bloqueio e na Tela Inicial.',
        disclaimer='<strong>Nota de segurança:</strong> Nugget usa os métodos sparserestore e BookRestore e <strong>não é compatível com iOS 27</strong> (a Apple corrigiu o método de restauração e pode haver perda de dados). Instale apenas papéis confiáveis, siga o guia oficial e mantenha sempre um backup.',
        faq_h2='Perguntas frequentes sobre Nugget wallpaper',
        faq_muted='Respostas rápidas às perguntas mais comuns sobre papéis em movimento para iPhone.',
        faq=[
            ('O que é um Nugget wallpaper?', 'Um Nugget wallpaper é um papel de parede animado ou em movimento para iPhone e iPad instalado com a ferramenta Nugget, um utilitário de personalização de iOS de código aberto. Vai muito além de uma imagem estática: pode animar e se mover pela sua tela, algo que a Apple não oferece nativamente.'),
            ('Quais versões do iOS um Nugget wallpaper suporta?', 'Nugget wallpapers suportam iOS e iPadOS 17 a 26, além de plataformas genéricas. Evite totalmente o iOS 27 — o método de restauração do Nugget foi corrigido lá e a perda de dados é provável.'),
            ('Como instalo um Nugget wallpaper no meu iPhone?', 'Baixe um papel da biblioteca, execute a ferramenta Nugget no Windows ou macOS (Linux também funciona) e aplique pelo recurso PosterBoard. O tutorial completo está em <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>.'),
            ('Instalar um Nugget wallpaper exige jailbreak?', 'Não. Nugget funciona pelos métodos sem jailbreak sparserestore e BookRestore, então você pode adicionar papéis animados a um iPhone normal desde que esteja no iOS 17–26.'),
            ('Existem Nugget wallpapers grátis?', 'Sim. A biblioteca de <a href="https://mwallx.com" rel="noopener">mwallx.com</a> tem papéis selecionados grátis e premium, com prévias em GIF animado para cada um.'),
        ],
        footer_note='Nugget wallpaper é um projeto comunitário. Este site apresenta a biblioteca Nugget wallpaper e aponta para o serviço oficial <a href="https://mwallx.com/" rel="noopener">mwallx.com</a>. Não afiliado à Apple Inc. © 2026 Nugget Wallpaper.',
    ),
    'ru': dict(
        title='Nugget Wallpaper — анимированные и живые обои для iPhone (iOS 17–26)',
        meta_desc='Библиотека Nugget Wallpaper: подборка анимированных и живых обоев для iPhone и iPad, устанавливаемых на iOS 17–26 с помощью инструмента Nugget. Смотрите, предпросматривайте и скачивайте бесплатные и премиум динамические обои.',
        og_title='Nugget Wallpaper — анимированные и живые обои для iPhone (iOS 17–26)',
        og_desc='Динамические и анимированные обои для iPhone/iPad. Установите на iOS 17–26 с помощью Nugget. Бесплатная и премиум библиотека.',
        website_desc='Подборка анимированных и живых обоев для iPhone и iPad, устанавливаемых на iOS 17–26 с помощью инструмента Nugget.',
        eyebrow='Живые обои для Nugget',
        h1='Библиотека Nugget Wallpaper<br />Анимированные обои для iPhone',
        sub='Подборка динамических, анимированных и живых обоев для вашего iPhone и iPad. Установите их напрямую с помощью <strong>инструмента Nugget</strong>, без джейлбрейка — совместимо с iOS 17 по iOS 26.',
        cta_primary='Открыть библиотеку Nugget Wallpaper →',
        cta_ghost='Официальный урок по установке',
        spec_ios='Поддержка <b>iOS 17 – iOS 26</b>',
        spec_device='iPhone и <b>iPad</b>',
        spec_free='<b>Бесплатно</b> и премиум',
        spec_jailbreak='Без джейлбрейка',
        about_h2='Что такое Nugget Wallpaper?',
        about_muted='Всё, что нужно знать об установке анимированных обоев на iPhone с помощью инструмента Nugget.',
        about_p1='<strong>Nugget wallpaper</strong> — это анимированные, живые обои для iPhone и iPad, которые вы устанавливаете с помощью <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> — утилиты кастомизации iOS с открытым исходным кодом от LeMinLimez, которая использует методы sparserestore и BookRestore для изменения устройств Apple <em>без полного джейлбрейка</em>.',
        about_p2='Вместо статичного изображения за вашими иконками, Nugget wallpaper может двигаться, реагировать и анимироваться на экране блокировки и главном экране. <a href="https://mwallx.com/" rel="noopener">Проект Nugget Wallpaper</a> размещает подборку таких живых обоев с живыми GIF-превью на каждой странице.',
        f1_h='Библиотека живых обоев', f1_p='Сотни подобранных динамических форматов обоев на темы аниме, спорта, музыки, 3D и образа жизни.',
        f2_h='Инструмент Nugget', f2_p='Приложение с открытым исходным кодом для Windows / macOS, которое применяет анимированные обои — без джейлбрейка.',
        f3_h='Пошаговое руководство', f3_p='Простой урок по установке для новичков — от резервной копии до живого экрана блокировки.',
        catalog_h2='Что внутри каталога Nugget wallpaper',
        catalog_muted='Изучите коллекцию Nugget wallpaper на mwallx.com — посмотрите движение до загрузки.',
        cat1_b='Аниме и манга', cat1_h='Ева, Клинок, Марвел', cat1_p='Потрясающие анимированные обои из ваших любимых серий.',
        cat2_b='Спорт', cat2_h='Футбол и киберспорт', cat2_p='Живые обои команд и игроков — от «Арсенала» до FIFA 2026.',
        cat3_b='3D и креатив', cat3_h='3D-лица и мечтательные сцены', cat3_p='Объёмные 3D-обои и мечтательные планеты, которые выглядят живыми.',
        cat4_b='Бесплатно', cat4_h='Бесплатно и премиум', cat4_p='Отфильтруйте по бесплатным или премиум, чтобы найти именно тот Nugget wallpaper.',
        cat5_b='Официально', cat5_h='Обои в формате Apple', cat5_p='Пакеты обоев в официальном формате плюс сборки сообщества Nugget.',
        cat6_b='Новые поступления', cat6_h='Новые каждую неделю', cat6_p='Новые Nugget wallpapers добавляются в библиотеку постоянно.',
        install_h2='Как установить Nugget wallpaper',
        install_muted='Четыре простых шага от загрузки до живого экрана блокировки.',
        step1_h='Выберите обои', step1_p='Откройте <a href="https://mwallx.com/{L}/wallpapers" rel="noopener">библиотеку Nugget wallpaper</a>, посмотрите анимированное GIF-превью и скачайте пакет.',
        step2_h='Сделайте резервную копию', step2_p='Подключите iPhone или iPad к ПК и создайте полную резервную копию. Всегда делайте бэкап перед использованием любого инструмента модификации iOS.',
        step3_h='Примените через Nugget', step3_p='Запустите приложение Nugget, загрузите обои в функцию PosterBoard и восстановите устройство по <a href="https://nugget.host/tutorial/nugget" rel="noopener">официальному уроку</a>.',
        step4_h='Наслаждайтесь движением', step4_p='Теперь на вашем iPhone настоящие анимированные обои — листайте и смотрите, как они оживают на экране блокировки и главном экране.',
        disclaimer='<strong>Примечание по безопасности:</strong> Nugget использует методы sparserestore и BookRestore и <strong>не совместим с iOS 27</strong> (Apple закрыла метод восстановления, возможна потеря данных). Устанавливайте только проверенные обои, следуйте официальному руководству и всегда храните резервную копию.',
        faq_h2='Вопросы о Nugget wallpaper',
        faq_muted='Быстрые ответы на самые частые вопросы о живых обоях для iPhone.',
        faq=[
            ('Что такое Nugget wallpaper?', 'Nugget wallpaper — это анимированные или живые обои для iPhone и iPad, которые устанавливаются с помощью инструмента Nugget — утилиты кастомизации iOS с открытым исходным кодом. Это не просто статичная картинка: обои могут анимироваться и двигаться по экрану, чего Apple не предлагает из коробки.'),
            ('Какие версии iOS поддерживает Nugget wallpaper?', 'Nugget wallpapers поддерживают iOS и iPadOS 17–26, а также обычные платформы. Полностью избегайте iOS 27 — там метод восстановления Nugget закрыт и вероятна потеря данных.'),
            ('Как установить Nugget wallpaper на iPhone?', 'Скачайте обои из библиотеки, запустите инструмент Nugget на Windows или macOS (Linux тоже работает) и примените через функцию PosterBoard. Полный гайд — на <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a>.'),
            ('Нужен ли джейлбрейк для установки Nugget wallpaper?', 'Нет. Nugget работает через методы без джейлбрейка sparserestore и BookRestore, поэтому вы можете добавить анимированные обои на обычный iPhone на iOS 17–26.'),
            ('Есть ли бесплатные Nugget wallpapers?', 'Да. В библиотеке <a href="https://mwallx.com" rel="noopener">mwallx.com</a> есть бесплатные и премиум обои с GIF-превью для каждой.'),
        ],
        footer_note='Nugget wallpaper — это общественный проект. Этот сайт знакомит с библиотекой Nugget wallpaper и ведёт на официальный сервис <a href="https://mwallx.com/" rel="noopener">mwallx.com</a>. Не аффилирован с Apple Inc. © 2026 Nugget Wallpaper.',
    ),
    'ur': dict(
        title='Nugget وال پیپر — آئی فون کے لیے اینیمیٹڈ اور موشن وال پیپر (iOS 17–26)',
        meta_desc='Nugget وال پیپر لائبریری: آئی فون اور آئی پیڈ کے لیے منتخب اینیمیٹڈ اور موشن وال پیپر، جنہیں Nugget ٹول سے iOS 17–26 پر انسٹال کیا جا سکتا ہے۔ مفت اور پریمیم ڈائنامک وال پیپرز براؤز، پیش نظارہ اور ڈاؤن لوڈ کریں۔',
        og_title='Nugget وال پیپر — آئی فون کے لیے اینیمیٹڈ اور موشن وال پیپر (iOS 17–26)',
        og_desc='آئی فون/آئی پیڈ کے لیے منتخب ڈائنامک اور موشن وال پیپرز۔ Nugget ٹول سے iOS 17–26 پر انسٹال کریں۔ مفت اور پریمیم وال پیپر لائبریری۔',
        website_desc='آئی فون اور آئی پیڈ کے لیے اینیمیٹڈ اور موشن وال پیپرز کی منتخب لائبریری، جنہیں Nugget ٹول سے iOS 17–26 پر انسٹال کیا جا سکتا ہے۔',
        eyebrow='Nugget کے لیے موشن وال پیپر',
        h1='Nugget وال پیپر لائبریری<br />آئی فون کے لیے اینیمیٹڈ وال پیپرز',
        sub='آپ کے آئی فون اور آئی پیڈ کے لیے منتخب ڈائنامک، اینیمیٹڈ اور موشن وال پیپرز۔ انہیں <strong>Nugget ٹول</strong> سے براہِ راست انسٹال کریں — جیل بریک کی ضرورت نہیں — iOS 17 سے iOS 26 تک مطابقت۔',
        cta_primary='Nugget وال پیپر لائبریری دیکھیں ←',
        cta_ghost='سرکاری انسٹال ٹیوٹوریل',
        spec_ios='سپورٹ <b>iOS 17 – iOS 26</b>',
        spec_device='آئی فون اور <b>آئی پیڈ</b>',
        spec_free='<b>مفت</b> اور پریمیم',
        spec_jailbreak='جیل بریک کی ضرورت نہیں',
        about_h2='Nugget وال پیپر کیا ہے؟',
        about_muted='Nugget ٹول سے اپنے آئی فون پر اینیمیٹڈ وال پیپر لگانے کے بارے میں سب کچھ۔',
        about_p1='<strong>Nugget وال پیپر</strong> آئی فون اور آئی پیڈ کے لیے ایک اینیمیٹڈ، موشن پر مبنی وال پیپر ہے جسے آپ <a href="https://github.com/leminlimez/Nugget" rel="noopener">Nugget</a> کے ذریعے انسٹال کرتے ہیں — LeMinLimez کی ایک اوپن سورس iOS کسٹمائزیشن یوٹیلیٹی، جو sparserestore اور BookRestore طریقوں سے Apple آلات کو <em>مکمل جیل بریک کے بغیر</em> تبدیل کرتی ہے۔',
        about_p2='آپ کے آئیکنز کے پیچھے جامد تصویر کے بجائے، Nugget وال پیپر آپ کی لاک اسکرین اور ہوم اسکرین پر حرکت، ردِ عمل اور اینیمیشن کر سکتا ہے۔ <a href="https://mwallx.com/" rel="noopener">Nugget وال پیپر پروجیکٹ</a> ان موشن وال پیپرز کی ایک منتخب لائبریری رکھتا ہے، ہر صفحے پر لائیو اینیمیٹڈ GIF پیش نظارے کے ساتھ۔',
        f1_h='موشن وال پیپر لائبریری', f1_p='اینیمی، اسپورٹس، میوزک، 3D اور لائف اسٹائل تھیمز میں سینکڑوں منتخب ڈائنامک وال پیپر فارمیٹس۔',
        f2_h='Nugget ٹول', f2_p='اوپن سورس Windows / macOS ایپ جو آپ کے ڈیوائس پر اینیمیٹڈ وال پیپر لگاتی ہے — جیل بریک کے بغیر۔',
        f3_h='مرحلہ وار گائیڈ', f3_p='بیک اپ سے لائیو اینیمیٹڈ لاک اسکرین تک ابتدائی دوستانہ انسٹال ٹیوٹوریل۔',
        catalog_h2='Nugget وال پیپر کیٹالاگ میں کیا ہے',
        catalog_muted='mwallx.com پر Nugget وال پیپر کلیکشن دیکھیں — ڈاؤن لوڈ سے پہلے موشن پیش نظارہ کریں۔',
        cat1_b='اینیمی اور مانگا', cat1_h='ایوا، ڈیمن سلیئر، مارول', cat1_p='آپ کی پسندیدہ سیریز کے شاندار اینیمیٹڈ وال پیپرز۔',
        cat2_b='اسپورٹس', cat2_h='فٹ بال اور ای اسپورٹس', cat2_p='آرسنل سے FIFA 2026 تک ٹیموں اور کھلاڑیوں کے موشن وال پیپرز۔',
        cat3_b='3D اور تخلیقی', cat3_h='3D چہرے اور خواب جیسے مناظر', cat3_p='گہرائی والے 3D اور خواب جیسے سیاروں کے وال پیپرز جو زندہ محسوس ہوتے ہیں۔',
        cat4_b='مفت', cat4_h='مفت اور پریمیم', cat4_p='مفت یا پریمیم فلٹر کریں اور وہی Nugget وال پیپر تلاش کریں جو آپ چاہتے ہیں۔',
        cat5_b='سرکاری', cat5_h='Apple فارمیٹ وال پیپرز', cat5_p='سرکاری فارمیٹ میں وال پیپر پیک، ساتھ میں Nugget کمیونٹی بلڈز۔',
        cat6_b='نئی ریلیز', cat6_h='ہر ہفتے نئے', cat6_p='لائبریری میں ہر وقت نئے Nugget وال پیپرز شامل ہوتے رہتے ہیں۔',
        install_h2='Nugget وال پیپر کیسے انسٹال کریں',
        install_muted='ڈاؤن لوڈ سے موونگ لاک اسکرین تک چار آسان مراحل۔',
        step1_h='اپنا وال پیپر منتخب کریں', step1_p='<a href="https://mwallx.com/{L}/wallpapers" rel="noopener">Nugget وال پیپر لائبریری</a> براؤز کریں، اینیمیٹڈ GIF پیش نظارہ دیکھیں اور پیک ڈاؤن لوڈ کریں۔',
        step2_h='اپنے ڈیوائس کا بیک اپ لیں', step2_p='اپنے آئی فون یا آئی پیڈ کو PC سے جوڑ کر مکمل بیک اپ بنائیں۔ کوئی بھی iOS موڈیفیکیشن ٹول استعمال کرنے سے پہلے ہمیشہ بیک اپ لیں۔',
        step3_h='Nugget سے لاگو کریں', step3_p='Nugget ایپ چلائیں، وال پیپر کو PosterBoard فیچر میں لوڈ کریں، اور <a href="https://nugget.host/tutorial/nugget" rel="noopener">سرکاری ٹیوٹوریل</a> کے مطابق اپنے ڈیوائس کو بحال کریں۔',
        step4_h='موشن سے لطف اندوز ہوں', step4_p='آپ کا آئی فون اب حقیقی اینیمیٹڈ وال پیپر چلاتا ہے — پین کریں، سوائپ کریں اور اسے لاک اسکرین اور ہوم اسکرین پر زندہ ہوتے دیکھیں۔',
        disclaimer='<strong>سیکیورٹی نوٹ:</strong> Nugget sparserestore اور BookRestore طریقے استعمال کرتا ہے اور <strong>iOS 27 کے ساتھ مطابقت نہیں رکھتا</strong> (Apple نے بحالی کا طریقہ پیچ کر دیا ہے، ڈیٹا ضائع ہو سکتا ہے)۔ صرف قابلِ اعتماد وال پیپرز انسٹال کریں، سرکاری گائیڈ پر عمل کریں اور ہمیشہ بیک اپ رکھیں۔',
        faq_h2='Nugget وال پیپر سوالات',
        faq_muted='آئی فون کے لیے موشن وال پیپرز کے بارے میں سب سے عام سوالات کے فوری جوابات۔',
        faq=[
            ('Nugget وال پیپر کیا ہے؟', 'Nugget وال پیپر آئی فون اور آئی پیڈ کے لیے ایک اینیمیٹڈ یا موشن وال پیپر ہے جو Nugget ٹول سے انسٹال ہوتا ہے — ایک اوپن سورس iOS کسٹمائزیشن یوٹیلیٹی۔ یہ جامد لاک اسکرین تصویر سے کہیں آگے ہے — یہ آپ کی اسکرین پر اینیمیٹ اور حرکت کر سکتا ہے، جو Apple قدرتی طور پر نہیں دیتا۔'),
            ('Nugget وال پیپر کون سے iOS ورژن سپورٹ کرتا ہے؟', 'Nugget وال پیپرز iOS اور iPadOS 17 سے 26 تک، ساتھ ہی عام پلیٹ فارمز سپورٹ کرتے ہیں۔ iOS 27 سے مکمل گریز کریں — وہاں Nugget کا بحالی طریقہ پیچ ہو چکا ہے اور ڈیٹا ضائع ہونے کا امکان ہے۔'),
            ('میں اپنے آئی فون پر Nugget وال پیپر کیسے انسٹال کروں؟', 'لائبریری سے وال پیپر ڈاؤن لوڈ کریں، Windows یا macOS پر Nugget ٹول چلائیں (Linux بھی کام کرتا ہے)، اور PosterBoard فیچر سے لاگو کریں۔ مکمل گائیڈ <a href="https://nugget.host/tutorial/nugget" rel="noopener">Nugget Host</a> پر ہے۔'),
            ('کیا Nugget وال پیپر انسٹال کرنے کے لیے جیل بریک ضروری ہے؟', 'نہیں۔ Nugget غیر جیل بریک طریقوں sparserestore اور BookRestore سے کام کرتا ہے، لہٰذا آپ iOS 17–26 پر عام آئی فون میں اینیمیٹڈ وال پیپرز شامل کر سکتے ہیں۔'),
            ('کیا مفت Nugget وال پیپرز موجود ہیں؟', 'جی ہاں۔ <a href="https://mwallx.com" rel="noopener">mwallx.com</a> کی لائبریری میں ہر ایک کے اینیمیٹڈ GIF پیش نظارے کے ساتھ مفت اور پریمیم منتخب وال پیپرز ہیں۔'),
        ],
        footer_note='Nugget وال پیپر ایک کمیونٹی پروجیکٹ ہے۔ یہ سائٹ Nugget وال پیپر لائبریری کا تعارف کراتی ہے اور سرکاری <a href="https://mwallx.com/" rel="noopener">mwallx.com</a> سروس سے لنک کرتی ہے۔ Apple Inc. سے منسلک نہیں۔ © 2026 Nugget وال پیپر۔',
    ),
}

TW_HEAD = '  <link rel="stylesheet" href="{SITE_BASE}/tailwind.css" />'
TEMPLATE = """<!DOCTYPE html>
<html lang="{LANG}"{DIR}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-QPS3GQ53Z9"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-QPS3GQ53Z9');
  </script>
  <script type="text/javascript">
    (function(c,l,a,r,i,t,y){{
        c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    }})(window, document, "clarity", "script", "y3mk8czwb2");
  </script>
  <title>{TITLE}</title>
  <meta name="description" content="{META_DESC}" />
  <link rel="canonical" href="{SELF_URL}" />
{HREFLANG}  <meta property="og:type" content="website" />
  <meta property="og:title" content="{OG_TITLE}" />
  <meta property="og:description" content="{OG_DESC}" />
  <meta property="og:url" content="{SELF_URL}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="robots" content="index, follow" />
  <link rel="icon" type="image/png" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='22' fill='%23111827'/><rect x='26' y='38' width='48' height='36' rx='8' fill='none' stroke='%2363e6be' stroke-width='5'/><circle cx='40' cy='82' r='3.5' fill='%2363e6be'/><circle cx='62' cy='82' r='3.5' fill='%2363e6be'/></svg>" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "Nugget Wallpaper",
    "alternateName": "Motion Wallpaper for Nugget",
    "url": "{SELF_URL}",
    "description": "{WEBSITE_DESC}",
    "inLanguage": "{LANG}",
    "datePublished": "2026-08-17T00:00:00Z",
    "dateModified": "2026-08-17T00:00:00Z",
    "publisher": {{
      "@type": "Organization",
      "name": "Nugget Wallpaper",
      "sameAs": ["https://mwallx.com/", "https://x.com/nuggetwallpaper", "https://www.tiktok.com/@nugget_wallpaper"]
    }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
{FAQ_JSON}
    ]
  }}
  </script>
{TW_HEAD}
  <script>
    document.addEventListener('click', function (e) {{
      var btn = document.querySelector('.lang-btn');
      var menu = document.getElementById('langMenu');
      if (!menu) return;
      if (btn && btn.contains(e.target)) {{ menu.classList.toggle('open'); e.stopPropagation(); }}
      else {{ menu.classList.remove('open'); }}
    }});
  </script>
</head>
<body>

<header class="site">
  <div class="wrap brand-row">
    <div class="brand">
      <svg width="30" height="30" viewBox="0 0 100 100" aria-hidden="true">
        <rect width="100" height="100" rx="22" fill="#111827"/>
        <rect x="26" y="36" width="48" height="38" rx="9" fill="none" stroke="#63e6be" stroke-width="5"/>
        <rect x="34" y="52" width="18" height="8" rx="4" fill="#63e6be"/>
        <circle cx="40" cy="82" r="3.5" fill="#63e6be"/>
        <circle cx="62" cy="82" r="3.5" fill="#63e6be"/>
      </svg>
      Nugget Wallpaper
    </div>
    <nav class="site">
      <a href="#about">{NAV0}</a>
      <a href="#catalog">{NAV1}</a>
      <a href="#install">{NAV2}</a>
      <a href="#faq">{NAV3}</a>
      <div class="lang-wrap">
        <button class="lang-btn" type="button" aria-label="Choose language">🌐 {LABEL} ▾</button>
        <div class="lang-menu" id="langMenu">
{LANG_ITEMS}
        </div>
      </div>
      <a class="cta" href="https://mwallx.com/{MLANG}/wallpapers" rel="noopener">{NAV_CTA}</a>
    </nav>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <span class="eyebrow">{EYEBROW}</span>
      <h1>{H1}</h1>
      <p class="sub">
        {SUB}
      </p>
      <div class="cta-row">
        <a class="btn btn-primary" href="https://mwallx.com/{MLANG}/wallpapers" rel="noopener">{CTA_PRIMARY}</a>
        <a class="btn btn-ghost" href="https://nugget.host/tutorial/nugget" rel="noopener">{CTA_GHOST}</a>
      </div>
      <div class="specs">
        <div class="spec">{SPEC_IOS}</div>
        <div class="spec">{SPEC_DEVICE}</div>
        <div class="spec">{SPEC_FREE}</div>
        <div class="spec">{SPEC_JAILBREAK}</div>
      </div>
      <p class="updated">🕒 {UPDATED}</p>
    </div>
  </section>

  <section id="about" class="alt">
    <div class="wrap">
      <div class="sec-head">
        <h2>{ABOUT_H2}</h2>
        <p class="muted">{ABOUT_MUTED}</p>
      </div>
      <p>
        {ABOUT_P1}
      </p>
      <p style="margin-top:14px;">
        {ABOUT_P2}
      </p>
      <div class="grid grid-3" style="margin-top:30px;">
        <div class="feature">
          <span class="ic">🎞️</span>
          <h3><a href="https://mwallx.com/{MLANG}/" rel="noopener">{F1_H}</a></h3>
          <p>{F1_P}</p>
        </div>
        <div class="feature">
          <span class="ic">🖥️</span>
          <h3><a href="https://github.com/leminlimez/Nugget" rel="noopener">{F2_H}</a></h3>
          <p>{F2_P}</p>
        </div>
        <div class="feature">
          <span class="ic">📱</span>
          <h3><a href="https://nugget.host/tutorial/nugget" rel="noopener">{F3_H}</a></h3>
          <p>{F3_P}</p>
        </div>
      </div>
    </div>
  </section>

  <section id="facts" class="alt">
    <div class="wrap">
      <div class="sec-head">
        <h2>{FACTS_H2}</h2>
        <p class="muted">{FACTS_MUTED}</p>
      </div>
      <div class="facts">
        <div class="fact"><b>{FACT1_N}</b><span>{FACT1_L}</span><cite>{FACT_SRC1}</cite></div>
        <div class="fact"><b>{FACT2_N}</b><span>{FACT2_L}</span><cite>{FACT_SRC2}</cite></div>
        <div class="fact"><b>{FACT3_N}</b><span>{FACT3_L}</span><cite>{FACT_SRC3}</cite></div>
        <div class="fact"><b>{FACT4_N}</b><span>{FACT4_L}</span><cite>{FACT_SRC4}</cite></div>
      </div>
    </div>
  </section>

  <section id="catalog">
    <div class="wrap">
      <div class="sec-head">
        <h2>{CATALOG_H2}</h2>
        <p class="muted">{CATALOG_MUTED}</p>
      </div>
      <div class="cats">
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?keyword=anime" rel="noopener">
          <span class="badge">{CAT1_B}</span>
          <h3>{CAT1_H}</h3>
          <p>{CAT1_P}</p>
        </a>
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?keyword=football" rel="noopener">
          <span class="badge">{CAT2_B}</span>
          <h3>{CAT2_H}</h3>
          <p>{CAT2_P}</p>
        </a>
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?keyword=3d" rel="noopener">
          <span class="badge">{CAT3_B}</span>
          <h3>{CAT3_H}</h3>
          <p>{CAT3_P}</p>
        </a>
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?paymentType=free" rel="noopener">
          <span class="badge">{CAT4_B}</span>
          <h3>{CAT4_H}</h3>
          <p>{CAT4_P}</p>
        </a>
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?wallpaperType=apple_official" rel="noopener">
          <span class="badge">{CAT5_B}</span>
          <h3>{CAT5_H}</h3>
          <p>{CAT5_P}</p>
        </a>
        <a class="cat" href="https://mwallx.com/{MLANG}/wallpapers?sortBy=latest" rel="noopener">
          <span class="badge">{CAT6_B}</span>
          <h3>{CAT6_H}</h3>
          <p>{CAT6_P}</p>
        </a>
      </div>
    </div>
  </section>

  <section id="install" class="alt">
    <div class="wrap">
      <div class="sec-head">
        <h2>{INSTALL_H2}</h2>
        <p class="muted">{INSTALL_MUTED}</p>
      </div>
      <div class="steps">
        <div class="step">
          <h3>{STEP1_H}</h3>
          <p>{STEP1_P}</p>
        </div>
        <div class="step">
          <h3>{STEP2_H}</h3>
          <p>{STEP2_P}</p>
        </div>
        <div class="step">
          <h3>{STEP3_H}</h3>
          <p>{STEP3_P}</p>
        </div>
        <div class="step">
          <h3>{STEP4_H}</h3>
          <p>{STEP4_P}</p>
        </div>
      </div>
      <div class="disclaimer" style="margin-top:26px;">
        {DISCLAIMER}
      </div>
    </div>
  </section>

  <section id="compare">
    <div class="wrap">
      <div class="sec-head">
        <h2>{CMP_H2}</h2>
        <p class="muted">{CMP_MUTED}</p>
      </div>
      <div class="cmp-wrap">
        <table class="cmp">
          <thead>
            <tr>
              <th>{CMP_T1}</th>
              <th>{CMP_T2}</th>
              <th class="cmp-best">{CMP_T3}</th>
              <th>{CMP_T4}</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>{CMP_R1}</td><td>{CMP_R1A}</td><td class="cmp-best">{CMP_R1B}</td><td>{CMP_R1C}</td></tr>
            <tr><td>{CMP_R2}</td><td>{CMP_R2A}</td><td class="cmp-best">{CMP_R2B}</td><td>{CMP_R2C}</td></tr>
            <tr><td>{CMP_R3}</td><td>{CMP_R3A}</td><td class="cmp-best">{CMP_R3B}</td><td>{CMP_R3C}</td></tr>
            <tr><td>{CMP_R4}</td><td>{CMP_R4A}</td><td class="cmp-best">{CMP_R4B}</td><td>{CMP_R4C}</td></tr>
            <tr><td>{CMP_R5}</td><td>{CMP_R5A}</td><td class="cmp-best">{CMP_R5B}</td><td>{CMP_R5C}</td></tr>
          </tbody>
        </table>
      </div>
      <p class="cmp-bottom">{CMP_BOTTOM}</p>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <div class="sec-head">
        <h2>{FAQ_H2}</h2>
        <p class="muted">{FAQ_MUTED}</p>
      </div>
{FAQ_HTML}
    </div>
  </section>
</main>

<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <h4>Nugget Wallpaper</h4>
        <ul>
          <li><a href="https://mwallx.com/{MLANG}/" rel="noopener">{F1_H}</a></li>
          <li><a href="https://nugget.host/tutorial/nugget" rel="noopener">{FOOTER_TUT}</a></li>
          <li><a href="https://github.com/leminlimez/Nugget" rel="noopener">{FOOTER_GITHUB}</a></li>
        </ul>
      </div>
      <div>
        <h4>{FOOTER_FOLLOW}</h4>
        <ul>
          <li><a href="https://www.tiktok.com/@nugget_wallpaper" rel="noopener">TikTok</a></li>
          <li><a href="https://t.me/nugget_wallpaper" rel="noopener">Telegram</a></li>
          <li><a href="https://x.com/nuggetwallpaper" rel="noopener">{FOOTER_X}</a></li>
        </ul>
      </div>
      <div>
        <h4>{FOOTER_PAGES}</h4>
        <ul>
          <li><a href="https://mwallx.com/{MLANG}/price" rel="noopener">{FOOTER_PRICE}</a></li>
          <li><a href="https://mwallx.com/{MLANG}/orders" rel="noopener">{FOOTER_ORDERS}</a></li>
          <li><a href="https://mwallx.com/{MLANG}/privacy-policy" rel="noopener">{FOOTER_PRIVACY}</a></li>
          <li><a href="https://mwallx.com/{MLANG}/terms-of-service" rel="noopener">{FOOTER_TERMS}</a></li>
        </ul>
      </div>
    </div>
    <p class="copy">{FOOTER_NOTE}</p>
    <p class="author-box"><b>{AUTHOR}</b> {AUTHOR_TEXT}</p>
  </div>
</footer>

</body>
</html>
"""

AI_ = {
    'en': dict(
        updated='Last updated: August 17, 2026',
        facts_h2='Nugget wallpaper key facts',
        facts_muted='Verified figures cited from the official Nugget repository and the mwallx.com gallery.',
        fact1_n='iOS 17–26', fact1_l='iOS versions supported for animated wallpapers',
        fact2_n='7,000+', fact2_l='GitHub stars for the open-source Nugget tool',
        fact3_n='10', fact3_l='Languages available on this page',
        fact4_n='Free', fact4_l='to browse and preview every wallpaper on mwallx.com',
        cmp_h2='Nugget wallpaper vs stock iOS vs jailbreak',
        cmp_muted='How animated Nugget wallpapers compare with Apple\u2019s built-in wallpaper and a full jailbreak.',
        cmp_t1='Approach', cmp_t2='Stock iOS', cmp_t3='Nugget wallpaper', cmp_t4='Jailbreak',
        cmp_r1='Jailbreak required', cmp_r1a='No', cmp_r1b='No', cmp_r1c='Yes',
        cmp_r2='iOS range', cmp_r2a='Native (all devices)', cmp_r2b='iOS 17 – 26 only', cmp_r2c='Varies, breaks on updates',
        cmp_r3='Animated wallpapers', cmp_r3a='Not natively', cmp_r3b='Yes, motion & interactive', cmp_r3c='Yes',
        cmp_r4='Data-loss risk', cmp_r4a='None', cmp_r4b='Low \u2014 back up first', cmp_r4c='High',
        cmp_r5='Ongoing maintenance', cmp_r5a='None', cmp_r5b='None, installer-based', cmp_r5c='Constant',
        cmp_bottom='Bottom line: for animated, no-jailbreak lock screen wallpapers on iOS 17\u201326, Nugget wallpaper with the Nugget tool is the practical choice \u2014 just back up your device and avoid iOS 27.',
        author='About this page',
        author_text='A community project introducing the Nugget wallpaper library and linking to the official mwallx.com service. The Nugget tool is open source by LeMinLimez, available on GitHub under the AGPL-3.0 license.',
    ),
    'zh-CN': dict(
        updated='最后更新：2026 年 8 月 17 日',
        facts_h2='Nugget 壁纸核心数据',
        facts_muted='以下数据均来自官方的 Nugget 代码仓库与 mwallx.com 壁纸库。',
        fact1_n='iOS 17–26', fact1_l='支持动画壁纸的 iOS 版本',
        fact2_n='7,000+', fact2_l='开源 Nugget 工具在 GitHub 上的 Star 数',
        fact3_n='10', fact3_l='本页提供的语言版本数量',
        fact4_n='免费', fact4_l='即可在 mwallx.com 浏览和预览每一款壁纸',
        cmp_h2='Nugget 壁纸 vs 原生 iOS vs 越狱',
        cmp_muted='对比 Nugget 动画壁纸、Apple 自带壁纸与完整越狱的区别。',
        cmp_t1='方案', cmp_t2='原生 iOS', cmp_t3='Nugget 壁纸', cmp_t4='越狱',
        cmp_r1='需要越狱', cmp_r1a='不需要', cmp_r1b='不需要', cmp_r1c='需要',
        cmp_r2='系统版本', cmp_r2a='原生（所有设备）', cmp_r2b='仅 iOS 17 – 26', cmp_r2c='视情况而定，更新后会失效',
        cmp_r3='动画壁纸', cmp_r3a='原生不支持', cmp_r3b='支持，动态与交互', cmp_r3c='支持',
        cmp_r4='数据丢失风险', cmp_r4a='无', cmp_r4b='较低 —— 请先备份', cmp_r4c='较高',
        cmp_r5='长期维护', cmp_r5a='无需', cmp_r5b='无需，基于安装工具', cmp_r5c='持续需要',
        cmp_bottom='结论：如果你想要 iOS 17–26 上无需越狱的动画锁屏壁纸，使用 Nugget 工具安装 Nugget 壁纸就是最实用的选择 —— 只需先备份设备并避开 iOS 27。',
        author='关于本页',
        author_text='本页是介绍 Nugget 壁纸库并链接到官方 mwallx.com 服务的社区项目。Nugget 工具由 LeMinLimez 开源，在 GitHub 上以 AGPL-3.0 许可发布。',
    ),
    'hi': dict(
        updated='अंतिम अपडेट: 17 अगस्त 2026',
        facts_h2='Nugget वॉलपेपर के मुख्य तथ्य',
        facts_muted='आधिकारिक Nugget रिपॉज़िटरी और mwallx.com गैलरी से लिए गए सत्यापित आंकड़े।',
        fact1_n='iOS 17–26', fact1_l='एनिमेटेड वॉलपेपर के लिए समर्थित iOS वर्शन',
        fact2_n='7,000+', fact2_l='ओपन-सोर्स Nugget टूल के GitHub स्टार्स',
        fact3_n='10', fact3_l='इस पेज पर उपलब्ध भाषाएँ',
        fact4_n='मुफ़्त', fact4_l='mwallx.com पर हर वॉलपेपर ब्राउज़ और प्रीव्यू करने के लिए',
        cmp_h2='Nugget वॉलपेपर बनाम स्टॉक iOS बनाम जेलब्रेक',
        cmp_muted='एनिमेटेड Nugget वॉलपेपर की तुलना Apple के बिल्ट-इन वॉलपेपर और पूर्ण जेलब्रेक से।',
        cmp_t1='तरीका', cmp_t2='स्टॉक iOS', cmp_t3='Nugget वॉलपेपर', cmp_t4='जेलब्रेक',
        cmp_r1='जेलब्रेक चाहिए', cmp_r1a='नहीं', cmp_r1b='नहीं', cmp_r1c='हाँ',
        cmp_r2='iOS रेंज', cmp_r2a='नेटिव (सभी डिवाइस)', cmp_r2b='केवल iOS 17 – 26', cmp_r2c='भिन्न, अपडेट पर टूट जाता है',
        cmp_r3='एनिमेटेड वॉलपेपर', cmp_r3a='नेटिव रूप से नहीं', cmp_r3b='हाँ, मोशन और इंटरैक्टिव', cmp_r3c='हाँ',
        cmp_r4='डेटा-लॉस जोखिम', cmp_r4a='कोई नहीं', cmp_r4b='कम — पहले बैकअप लें', cmp_r4c='उच्च',
        cmp_r5='निरंतर रखरखाव', cmp_r5a='कोई नहीं', cmp_r5b='कोई नहीं, इंस्टॉलर-आधारित', cmp_r5c='लगातार',
        cmp_bottom='निष्कर्ष: iOS 17–26 पर बिना जेलब्रेक एनिमेटेड लॉक स्क्रीन वॉलपेपर के लिए, Nugget टूल के साथ Nugget वॉलपेपर ही व्यावहारिक विकल्प है — बस पहले बैकअप लें और iOS 27 से बचें।',
        author='इस पेज के बारे में',
        author_text='नugget वॉलपेपर लाइब्रेरी का परिचय देने और आधिकारिक mwallx.com सेवा से जोड़ने वाला एक कम्युनिटी प्रोजेक्ट। Nugget टूल LeMinLimez द्वारा ओपन-सोर्स है, GitHub पर AGPL-3.0 लाइसेंस के तहत उपलब्ध।',
    ),
    'es': dict(
        updated='Última actualización: 17 de agosto de 2026',
        facts_h2='Datos clave de Nugget wallpaper',
        facts_muted='Cifras verificadas procedentes del repositorio oficial de Nugget y de la galería de mwallx.com.',
        fact1_n='iOS 17–26', fact1_l='versiones de iOS compatibles con fondos animados',
        fact2_n='7,000+', fact2_l='estrellas de GitHub de la herramienta open source Nugget',
        fact3_n='10', fact3_l='idiomas disponibles en esta página',
        fact4_n='Gratis', fact4_l='para explorar y previsualizar cada fondo en mwallx.com',
        cmp_h2='Nugget wallpaper frente a iOS nativo y jailbreak',
        cmp_muted='Cómo se comparan los Nugget wallpapers animados con el fondo integrado de Apple y con un jailbreak completo.',
        cmp_t1='Enfoque', cmp_t2='iOS nativo', cmp_t3='Nugget wallpaper', cmp_t4='Jailbreak',
        cmp_r1='Requiere jailbreak', cmp_r1a='No', cmp_r1b='No', cmp_r1c='Sí',
        cmp_r2='Rango de iOS', cmp_r2a='Nativo (todos los dispositivos)', cmp_r2b='Solo iOS 17 – 26', cmp_r2c='Varía, se rompe con las actualizaciones',
        cmp_r3='Fondos animados', cmp_r3a='No de forma nativa', cmp_r3b='Sí, movimiento e interactivos', cmp_r3c='Sí',
        cmp_r4='Riesgo de pérdida de datos', cmp_r4a='Ninguno', cmp_r4b='Bajo: haz copia de seguridad', cmp_r4c='Alto',
        cmp_r5='Mantenimiento continuo', cmp_r5a='Ninguno', cmp_r5b='Ninguno, basado en instalador', cmp_r5c='Constante',
        cmp_bottom='En resumen: para fondos animados en la pantalla de bloqueo sin jailbreak en iOS 17–26, Nugget wallpaper con la herramienta Nugget es la opción práctica: solo haz una copia de seguridad y evita iOS 27.',
        author='Acerca de esta página',
        author_text='Es un proyecto comunitario que presenta la biblioteca de Nugget wallpaper y enlaza al servicio oficial mwallx.com. La herramienta Nugget es de código abierto por LeMinLimez, disponible en GitHub bajo la licencia AGPL-3.0.',
    ),
    'fr': dict(
        updated='Dernière mise à jour : 17 août 2026',
        facts_h2='Faits clés sur Nugget wallpaper',
        facts_muted='Chiffres vérifiés issus du dépôt officiel Nugget et de la galerie mwallx.com.',
        fact1_n='iOS 17–26', fact1_l='versions d\u2019iOS compatibles avec les fonds animés',
        fact2_n='7,000+', fact2_l='étoiles GitHub de l\u2019outil open source Nugget',
        fact3_n='10', fact3_l='langues disponibles sur cette page',
        fact4_n='Gratuit', fact4_l='pour parcourir et prévisualiser chaque fond sur mwallx.com',
        cmp_h2='Nugget wallpaper face à iOS natif et au jailbreak',
        cmp_muted='Comparaison des fonds animés Nugget avec le fond intégré d\u2019Apple et un jailbreak complet.',
        cmp_t1='Approche', cmp_t2='iOS natif', cmp_t3='Nugget wallpaper', cmp_t4='Jailbreak',
        cmp_r1='Jailbreak requis', cmp_r1a='Non', cmp_r1b='Non', cmp_r1c='Oui',
        cmp_r2='Étendue iOS', cmp_r2a='Natif (tous les appareils)', cmp_r2b='iOS 17 – 26 uniquement', cmp_r2c='Variable, cassé par les mises à jour',
        cmp_r3='Fonds animés', cmp_r3a='Pas nativement', cmp_r3b='Oui, mouvement et interactifs', cmp_r3c='Oui',
        cmp_r4='Risque de perte de données', cmp_r4a='Aucun', cmp_r4b='Faible — sauvegardez d\u2019abord', cmp_r4c='Élevé',
        cmp_r5='Maintenance continue', cmp_r5a='Aucune', cmp_r5b='Aucune, basée sur installeur', cmp_r5c='Constante',
        cmp_bottom='En résumé : pour des fonds animés sur l\u2019écran de verrouillage sans jailbreak sous iOS 17–26, Nugget wallpaper avec l\u2019outil Nugget est le choix pratique — sauvegardez votre appareil et évitez iOS 27.',
        author='À propos de cette page',
        author_text='Un projet communautaire qui présente la bibliothèque de Nugget wallpaper et renvoie vers le service officiel mwallx.com. L\u2019outil Nugget est open source, créé par LeMinLimez, disponible sur GitHub sous licence AGPL-3.0.',
    ),
    'ar': dict(
        updated='آخر تحديث: 17 أغسطس 2026',
        facts_h2='حقائق أساسية عن Nugget wallpaper',
        facts_muted='أرقام موثّقة مأخوذة من مستودع Nugget الرسمي ومعرض mwallx.com.',
        fact1_n='iOS 17–26', fact1_l='إصدارات iOS المدعومة للخلفيات المتحركة',
        fact2_n='7,000+', fact2_l='نجمة على GitHub لأداة Nugget مفتوحة المصدر',
        fact3_n='10', fact3_l='لغة متاحة في هذه الصفحة',
        fact4_n='مجاني', fact4_l='لتصفح ومعاينة كل خلفية على mwallx.com',
        cmp_h2='Nugget wallpaper مقابل iOS الأصلي وجيلبريك',
        cmp_muted='كيف تُقارن خلفيات Nugget المتحركة بخلفية Apple المدمجة وبعملية جيلبريك كاملة.',
        cmp_t1='الطريقة', cmp_t2='iOS الأصلي', cmp_t3='Nugget wallpaper', cmp_t4='جيلبريك',
        cmp_r1='يتطلب جيلبريك', cmp_r1a='لا', cmp_r1b='لا', cmp_r1c='نعم',
        cmp_r2='نطاق iOS', cmp_r2a='أصلي (كل الأجهزة)', cmp_r2b='iOS 17 – 26 فقط', cmp_r2c='متغير، يتعطل مع التحديثات',
        cmp_r3='خلفيات متحركة', cmp_r3a='ليس أصلياً', cmp_r3b='نعم، حركة وتفاعلية', cmp_r3c='نعم',
        cmp_r4='خطر فقدان البيانات', cmp_r4a='لا يوجد', cmp_r4b='منخفض — انسخ احتياطياً أولاً', cmp_r4c='مرتفع',
        cmp_r5='صيانة مستمرة', cmp_r5a='لا توجد', cmp_r5b='لا توجد، تعتمد على المثبّت', cmp_r5c='مستمرة',
        cmp_bottom='الخلاصة: لخلفيات قفل متحركة دون جيلبريك على iOS 17–26، يُعد Nugget wallpaper مع أداة Nugget الخيار العملي — فقط انسخ جهازك احتياطياً وتجنب iOS 27.',
        author='حول هذه الصفحة',
        author_text='مشروع مجتمعي يعرّف بمكتبة Nugget wallpaper ويربط بالخدمة الرسمية mwallx.com. أداة Nugget مفتوحة المصدر من LeMinLimez، متاحة على GitHub بترخيص AGPL-3.0.',
    ),
    'bn': dict(
        updated='সর্বশেষ আপডেট: ১৭ আগস্ট ২০২৬',
        facts_h2='Nugget ওয়ালপেপারের মূল তথ্য',
        facts_muted='অফিসিয়াল Nugget রিপোজিটরি এবং mwallx.com গ্যালারি থেকে নেওয়া যাচাইকৃত তথ্য।',
        fact1_n='iOS 17–26', fact1_l='অ্যানিমেটেড ওয়ালপেপারের জন্য সমর্থিত iOS ভার্সন',
        fact2_n='7,000+', fact2_l='ওপেন-সোর্স Nugget টুলের GitHub স্টার',
        fact3_n='10', fact3_l='এই পেজে উপলব্ধ ভাষা',
        fact4_n='ফ্রি', fact4_l='mwallx.com-এ প্রতিটি ওয়ালপেপার ব্রাউজ ও প্রিভিউ করতে',
        cmp_h2='Nugget ওয়ালপেপার বনাম স্টক iOS বনাম জেলব্রেক',
        cmp_muted='Apple-এর বিল্ট-ইন ওয়ালপেপার এবং সম্পূর্ণ জেলব্রেকের সাথে অ্যানিমেটেড Nugget ওয়ালপেপারের তুলনা।',
        cmp_t1='পদ্ধতি', cmp_t2='স্টক iOS', cmp_t3='Nugget ওয়ালপেপার', cmp_t4='জেলব্রেক',
        cmp_r1='জেলব্রেক প্রয়োজন', cmp_r1a='না', cmp_r1b='না', cmp_r1c='হ্যাঁ',
        cmp_r2='iOS রেঞ্জ', cmp_r2a='নেটিভ (সব ডিভাইস)', cmp_r2b='শুধু iOS 17 – 26', cmp_r2c='ভিন্ন, আপডেটে ভেঙে যায়',
        cmp_r3='অ্যানিমেটেড ওয়ালপেপার', cmp_r3a='নেটিভভাবে না', cmp_r3b='হ্যাঁ, মোশন ও ইন্টারঅ্যাকটিভ', cmp_r3c='হ্যাঁ',
        cmp_r4='ডেটা-লস ঝুঁকি', cmp_r4a='কোনোটি নয়', cmp_r4b='কম — আগে ব্যাকআপ নিন', cmp_r4c='উচ্চ',
        cmp_r5='নিরবচ্ছিন্ন রক্ষণাবেক্ষণ', cmp_r5a='কোনোটি নয়', cmp_r5b='কোনোটি নয়, ইনস্টলার-ভিত্তিক', cmp_r5c='নিয়মিত',
        cmp_bottom='নিচের লাইন: iOS 17–26-এ জেলব্রেক ছাড়া অ্যানিমেটেড লক স্ক্রিন ওয়ালপেপারের জন্য, Nugget টুলসহ Nugget ওয়ালপেপারই কার্যকরী পছন্দ — শুধু আগে ব্যাকআপ নিন এবং iOS 27 এড়িয়ে চলুন।',
        author='এই পেজ সম্পর্কে',
        author_text='Nugget ওয়ালপেপার লাইব্রেরি পরিচয় করিয়ে দেওয়া এবং অফিসিয়াল mwallx.com সার্ভিসের সাথে সংযোগকারী একটি কমিউনিটি প্রজেক্ট। Nugget টুল LeMinLimez-এর ওপেন-সোর্স, GitHub-এ AGPL-3.0 লাইসেন্সে উপলব্ধ।',
    ),
    'pt': dict(
        updated='Última atualização: 17 de agosto de 2026',
        facts_h2='Fatos-chave sobre Nugget wallpaper',
        facts_muted='Números verificados provenientes do repositório oficial do Nugget e da galeria do mwallx.com.',
        fact1_n='iOS 17–26', fact1_l='versões do iOS compatíveis com papéis de parede animados',
        fact2_n='7,000+', fact2_l='estrelas no GitHub da ferramenta open source Nugget',
        fact3_n='10', fact3_l='idiomas disponíveis nesta página',
        fact4_n='Grátis', fact4_l='para navegar e pré-visualizar cada papel no mwallx.com',
        cmp_h2='Nugget wallpaper frente ao iOS padrão e ao jailbreak',
        cmp_muted='Como os papéis animados Nugget se comparam ao papel integrado da Apple e a um jailbreak completo.',
        cmp_t1='Abordagem', cmp_t2='iOS padrão', cmp_t3='Nugget wallpaper', cmp_t4='Jailbreak',
        cmp_r1='Exige jailbreak', cmp_r1a='Não', cmp_r1b='Não', cmp_r1c='Sim',
        cmp_r2='Intervalo de iOS', cmp_r2a='Nativo (todos os dispositivos)', cmp_r2b='Somente iOS 17 – 26', cmp_r2c='Varia, quebra com atualizações',
        cmp_r3='Papéis animados', cmp_r3a='Não nativamente', cmp_r3b='Sim, movimento e interativos', cmp_r3c='Sim',
        cmp_r4='Risco de perda de dados', cmp_r4a='Nenhum', cmp_r4b='Baixo — faça backup antes', cmp_r4c='Alto',
        cmp_r5='Manutenção contínua', cmp_r5a='Nenhuma', cmp_r5b='Nenhuma, baseada em instalador', cmp_r5c='Constante',
        cmp_bottom='Conclusão: para papéis de parede animados na tela de bloqueio sem jailbreak no iOS 17–26, Nugget wallpaper com a ferramenta Nugget é a escolha prática — basta fazer backup e evitar o iOS 27.',
        author='Sobre esta página',
        author_text='Um projeto comunitário que apresenta a biblioteca de Nugget wallpaper e aponta para o serviço oficial mwallx.com. A ferramenta Nugget é open source, criada por LeMinLimez, disponível no GitHub sob a licença AGPL-3.0.',
    ),
    'ru': dict(
        updated='Обновлено: 17 августа 2026',
        facts_h2='Ключевые факты о Nugget wallpaper',
        facts_muted='Проверенные цифры из официального репозитория Nugget и галереи mwallx.com.',
        fact1_n='iOS 17–26', fact1_l='версий iOS поддерживают анимированные обои',
        fact2_n='7,000+', fact2_l='звёзд GitHub у open source инструмента Nugget',
        fact3_n='10', fact3_l='языков доступно на этой странице',
        fact4_n='Бесплатно', fact4_l='просматривать и предпросматривать каждые обои на mwallx.com',
        cmp_h2='Nugget wallpaper против стандартного iOS и джейлбрейка',
        cmp_muted='Как анимированные Nugget обои сравниваются со встроенными обоями Apple и полным джейлбрейком.',
        cmp_t1='Подход', cmp_t2='Стандартный iOS', cmp_t3='Nugget wallpaper', cmp_t4='Джейлбрейк',
        cmp_r1='Нужен джейлбрейк', cmp_r1a='Нет', cmp_r1b='Нет', cmp_r1c='Да',
        cmp_r2='Версии iOS', cmp_r2a='Нативные (все устройства)', cmp_r2b='Только iOS 17 – 26', cmp_r2c='По-разному, ломается от обновлений',
        cmp_r3='Анимированные обои', cmp_r3a='Нет, не нативно', cmp_r3b='Да, движение и интерактив', cmp_r3c='Да',
        cmp_r4='Риск потери данных', cmp_r4a='Нет', cmp_r4b='Низкий — сделайте резервную копию', cmp_r4c='Высокий',
        cmp_r5='Постоянное обслуживание', cmp_r5a='Нет', cmp_r5b='Нет, на основе установщика', cmp_r5c='Постоянное',
        cmp_bottom='Итог: для анимированных обоев на экране блокировки без джейлбрейка на iOS 17–26 Nugget wallpaper с инструментом Nugget — практичный выбор: сделайте резервную копию и избегайте iOS 27.',
        author='Об этой странице',
        author_text='Это сообщество проект, который знакомит с библиотекой Nugget wallpaper и ведёт к официальному сервису mwallx.com. Инструмент Nugget имеет открытый исходный код, автор LeMinLimez, доступен на GitHub под лицензией AGPL-3.0.',
    ),
    'ur': dict(
        updated='آخری اپ ڈیٹ: 17 اگست 2026',
        facts_h2='Nugget وال پیپر کے اہم حقائق',
        facts_muted='یہ تصدیق شدہ اعداد سرکاری Nugget ریپوزیٹری اور mwallx.com گیلری سے لیے گئے ہیں۔',
        fact1_n='iOS 17–26', fact1_l='متحرک وال پیپرز کے لیے معاونت یافتہ iOS ورژن',
        fact2_n='7,000+', fact2_l='اوپن سورس Nugget ٹول کے GitHub ستارے',
        fact3_n='10', fact3_l='اس صفحے پر دستیاب زبانیں',
        fact4_n='مفت', fact4_l='mwallx.com پر ہر وال پیپر براؤز اور پیش نظارہ کرنے کے لیے',
        cmp_h2='Nugget وال پیپر بمقابلہ عام iOS بمقابلہ جیل بریک',
        cmp_muted='Apple کے بلٹ ان وال پیپر اور مکمل جیل بریک کے ساتھ متحرک Nugget وال پیپرز کا موازنہ۔',
        cmp_t1='طریقہ', cmp_t2='عام iOS', cmp_t3='Nugget وال پیپر', cmp_t4='جیل بریک',
        cmp_r1='جیل بریک درکار', cmp_r1a='نہیں', cmp_r1b='نہیں', cmp_r1c='ہاں',
        cmp_r2='iOS رینج', cmp_r2a='عام (تمام آلات)', cmp_r2b='صرف iOS 17 – 26', cmp_r2c='مختلف، اپ ڈیٹس سے ٹوٹ جاتا ہے',
        cmp_r3='متحرک وال پیپرز', cmp_r3a='عام طور پر نہیں', cmp_r3b='ہاں، موشن اور انٹرایکٹو', cmp_r3c='ہاں',
        cmp_r4='ڈیٹا نقصان کا خطرہ', cmp_r4a='کوئی نہیں', cmp_r4b='کم — پہلے بیک اپ لیں', cmp_r4c='زیادہ',
        cmp_r5='مسلسل دیکھ بھال', cmp_r5a='کوئی نہیں', cmp_r5b='کوئی نہیں، انسٹالر پر مبنی', cmp_r5c='مستقل',
        cmp_bottom='خلاصہ: iOS 17–26 پر بغیر جیل بریک متحرک لاک اسکرین وال پیپرز کے لیے، Nugget ٹول کے ساتھ Nugget وال پیپر ہی عملی انتخاب ہے — بس پہلے بیک اپ لیں اور iOS 27 سے گریز کریں۔',
        author='اس صفحے کے بارے میں',
        author_text='یہ ایک کمیونٹی پروجیکٹ ہے جو Nugget وال پیپر لائبریری کا تعارف کراتا ہے اور سرکاری mwallx.com سروس سے لنک کرتا ہے۔ Nugget ٹول LeMinLimez کا اوپن سورس ہے، GitHub پر AGPL-3.0 لائسنس کے تحت دستیاب ہے۔',
    ),
}

FOOTER_SHARED = {
    'en':    dict(tut='Install Tutorial', github='Nugget on GitHub', follow='Follow', x='X (Twitter)', pages='Pages', price='Pricing', orders='Orders', privacy='Privacy', terms='Terms', cta='Browse Wallpapers'),
    'zh-CN': dict(tut='安装教程', github='GitHub 上的 Nugget', follow='关注', x='X（推特）', pages='页面', price='价格', orders='订单', privacy='隐私', terms='条款', cta='浏览壁纸'),
    'hi':    dict(tut='इंस्टॉल ट्यूटोरियल', github='GitHub पर Nugget', follow='फॉलो करें', x='X (ट्विटर)', pages='पेज', price='कीमत', orders='ऑर्डर', privacy='गोपनीयता', terms='शर्तें', cta='वॉलपेपर देखें'),
    'es':    dict(tut='Tutorial de instalación', github='Nugget en GitHub', follow='Síguenos', x='X (Twitter)', pages='Páginas', price='Precios', orders='Pedidos', privacy='Privacidad', terms='Términos', cta='Ver fondos'),
    'fr':    dict(tut='Tutoriel d\'installation', github='Nugget sur GitHub', follow='Suivre', x='X (Twitter)', pages='Pages', price='Tarifs', orders='Commandes', privacy='Confidentialité', terms='Conditions', cta='Voir les fonds'),
    'ar':    dict(tut='دليل التثبيت', github='Nugget على GitHub', follow='تابعنا', x='X (تويتر)', pages='الصفحات', price='الأسعار', orders='الطلبات', privacy='الخصوصية', terms='الشروط', cta='تصفح الخلفيات'),
    'bn':    dict(tut='ইনস্টল টিউটোরিয়াল', github='GitHub-এ Nugget', follow='ফলো করুন', x='X (টুইটার)', pages='পেজ', price='মূল্য', orders='অর্ডার', privacy='গোপনীয়তা', terms='শর্তাবলি', cta='ওয়ালপেপার দেখুন'),
    'pt':    dict(tut='Tutorial de instalação', github='Nugget no GitHub', follow='Siga', x='X (Twitter)', pages='Páginas', price='Preços', orders='Pedidos', privacy='Privacidade', terms='Termos', cta='Ver papéis'),
    'ru':    dict(tut='Урок по установке', github='Nugget на GitHub', follow='Подписаться', x='X (Twitter)', pages='Страницы', price='Цены', orders='Заказы', privacy='Конфиденциальность', terms='Условия', cta='Смотреть обои'),
    'ur':    dict(tut='انسٹال ٹیوٹوریل', github='GitHub پر Nugget', follow='فالو کریں', x='X (ٹویٹر)', pages='صفحات', price='قیمتیں', orders='آرڈرز', privacy='پرائیویسی', terms='شرائط', cta='وال پیپر دیکھیں'),
}


def render(lang):
    cfg = LANGS[lang]
    t = T[lang]
    fs = FOOTER_SHARED[lang]
    ai = AI_[lang]
    src_gh = ai.get('fact_src_gh') or 'GitHub'
    src_mw = ai.get('fact_src_mw') or 'mwallx.com'
    src_here = ai.get('fact_src_here') or 'This page'
    src_word = {
        'zh-CN': '来源', 'hi': 'स्रोत', 'es': 'Fuente', 'fr': 'Source',
        'ar': 'المصدر', 'bn': 'উৎস', 'pt': 'Fonte', 'ru': 'Источник', 'ur': 'ماخذ',
    }.get(lang, 'Source')
    FACT1_SRC = '%s: %s' % (src_word, src_here)
    FACT2_SRC = '%s: <a href="https://github.com/leminlimez/Nugget" rel="noopener">%s</a>' % (src_word, src_gh)
    FACT3_SRC = '%s: %s' % (src_word, src_here)
    FACT4_SRC = '%s: <a href="https://mwallx.com/" rel="noopener">%s</a>' % (src_word, src_mw)
    self_url = BASE + cfg['path']
    hreflang = ''.join('  <link rel="alternate" hreflang="%s" href="%s" />\n' % (l, BASE + LANGS[l]['path'])
                       for l in LANGS)
    hreflang += '  <link rel="alternate" hreflang="x-default" href="%s" />\n' % self_url

    lang_items = ''
    for l in LANGS:
        active = ' class="active"' if l == lang else ''
        lang_items += '          <a href="%s"%s>%s <span class="code">%s</span></a>\n' % (
            BASE + LANGS[l]['path'], active, LANGS[l]['label'], LANGS[l]['code'])

    faq_json = ',\n'.join(
        '      {\n        "@type": "Question",\n        "name": "%s",\n        "acceptedAnswer": {\n          "@type": "Answer",\n          "text": "%s"\n        }\n      }' % (q.replace('"', '\\"').replace('\n', ' '), a.replace('"', '\\"').replace('\n', ' '))
        for q, a in t['faq'])

    faq_html = ''.join(
        ('      <details%s>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>\n' % (' open' if i == 0 else '', q, a))
        for i, (q, a) in enumerate(t['faq']))

    p = dict(
        LANG=lang, DIR=' dir="rtl"' if cfg['dir'] else '', LABEL=cfg['label'], CODE=cfg['code'],
        MLANG=cfg['mlang'], NAV0=cfg['nav'][0], NAV1=cfg['nav'][1], NAV2=cfg['nav'][2], NAV3=cfg['nav'][3],
        NAV_CTA=fs['cta'], SELF_URL=self_url, HREFLANG=hreflang,
        TITLE=t['title'], META_DESC=t['meta_desc'], OG_TITLE=t['og_title'], OG_DESC=t['og_desc'],
        WEBSITE_DESC=t['website_desc'], FAQ_JSON=faq_json, LANG_ITEMS=lang_items,
        EYEBROW=t['eyebrow'], H1=t['h1'], SUB=t['sub'], CTA_PRIMARY=t['cta_primary'], CTA_GHOST=t['cta_ghost'],
        SPEC_IOS=t['spec_ios'], SPEC_DEVICE=t['spec_device'], SPEC_FREE=t['spec_free'], SPEC_JAILBREAK=t['spec_jailbreak'],
        ABOUT_H2=t['about_h2'], ABOUT_MUTED=t['about_muted'], ABOUT_P1=t['about_p1'], ABOUT_P2=t['about_p2'],
        F1_H=t['f1_h'], F1_P=t['f1_p'], F2_H=t['f2_h'], F2_P=t['f2_p'], F3_H=t['f3_h'], F3_P=t['f3_p'],
        CATALOG_H2=t['catalog_h2'], CATALOG_MUTED=t['catalog_muted'],
        CAT1_B=t['cat1_b'], CAT1_H=t['cat1_h'], CAT1_P=t['cat1_p'],
        CAT2_B=t['cat2_b'], CAT2_H=t['cat2_h'], CAT2_P=t['cat2_p'],
        CAT3_B=t['cat3_b'], CAT3_H=t['cat3_h'], CAT3_P=t['cat3_p'],
        CAT4_B=t['cat4_b'], CAT4_H=t['cat4_h'], CAT4_P=t['cat4_p'],
        CAT5_B=t['cat5_b'], CAT5_H=t['cat5_h'], CAT5_P=t['cat5_p'],
        CAT6_B=t['cat6_b'], CAT6_H=t['cat6_h'], CAT6_P=t['cat6_p'],
        INSTALL_H2=t['install_h2'], INSTALL_MUTED=t['install_muted'],
        STEP1_H=t['step1_h'], STEP1_P=t['step1_p'].format(L=cfg['mlang']),
        STEP2_H=t['step2_h'], STEP2_P=t['step2_p'],
        STEP3_H=t['step3_h'], STEP3_P=t['step3_p'].format(L=cfg['mlang']),
        STEP4_H=t['step4_h'], STEP4_P=t['step4_p'],
        DISCLAIMER=t['disclaimer'], FAQ_H2=t['faq_h2'], FAQ_MUTED=t['faq_muted'], FAQ_HTML=faq_html,
        FOOTER_NOTE=t['footer_note'],
        FOOTER_TUT=fs['tut'], FOOTER_GITHUB=fs['github'], FOOTER_FOLLOW=fs['follow'], FOOTER_X=fs['x'],
        FOOTER_PAGES=fs['pages'], FOOTER_PRICE=fs['price'], FOOTER_ORDERS=fs['orders'],
        FOOTER_PRIVACY=fs['privacy'], FOOTER_TERMS=fs['terms'],
        TW_HEAD=TW_HEAD.format(SITE_BASE=BASE),
        UPDATED=ai['updated'],
        FACTS_H2=ai['facts_h2'], FACTS_MUTED=ai['facts_muted'],
        FACT1_N=ai['fact1_n'], FACT1_L=ai['fact1_l'], FACT_SRC1=FACT1_SRC,
        FACT2_N=ai['fact2_n'], FACT2_L=ai['fact2_l'], FACT_SRC2=FACT2_SRC,
        FACT3_N=ai['fact3_n'], FACT3_L=ai['fact3_l'], FACT_SRC3=FACT3_SRC,
        FACT4_N=ai['fact4_n'], FACT4_L=ai['fact4_l'], FACT_SRC4=FACT4_SRC,
        CMP_H2=ai['cmp_h2'], CMP_MUTED=ai['cmp_muted'],
        CMP_T1=ai['cmp_t1'], CMP_T2=ai['cmp_t2'], CMP_T3=ai['cmp_t3'], CMP_T4=ai['cmp_t4'],
        CMP_R1=ai['cmp_r1'], CMP_R1A=ai['cmp_r1a'], CMP_R1B=ai['cmp_r1b'], CMP_R1C=ai['cmp_r1c'],
        CMP_R2=ai['cmp_r2'], CMP_R2A=ai['cmp_r2a'], CMP_R2B=ai['cmp_r2b'], CMP_R2C=ai['cmp_r2c'],
        CMP_R3=ai['cmp_r3'], CMP_R3A=ai['cmp_r3a'], CMP_R3B=ai['cmp_r3b'], CMP_R3C=ai['cmp_r3c'],
        CMP_R4=ai['cmp_r4'], CMP_R4A=ai['cmp_r4a'], CMP_R4B=ai['cmp_r4b'], CMP_R4C=ai['cmp_r4c'],
        CMP_R5=ai['cmp_r5'], CMP_R5A=ai['cmp_r5a'], CMP_R5B=ai['cmp_r5b'], CMP_R5C=ai['cmp_r5c'],
        CMP_BOTTOM=ai['cmp_bottom'], AUTHOR=ai['author'], AUTHOR_TEXT=ai['author_text'],
    )
    return TEMPLATE.format(**p)


if __name__ == '__main__':
    for lang in ['zh-CN', 'hi', 'es', 'fr', 'ar', 'bn', 'pt', 'ru', 'ur']:
        out = render(lang)
        path = os.path.join('docs', lang, 'index.html')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        print('wrote', path, len(out), 'bytes')
