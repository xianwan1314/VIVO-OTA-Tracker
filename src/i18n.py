APP_VERSION = "V1.3.0_Release_mytiantian"
BASE_DPI = 96.0

TR = {
    'window_title':       {'zh': f'Vivo Ota Tracker By mytiantian {APP_VERSION}', 'en': f'Vivo Ota Tracker By mytiantian {APP_VERSION}'},
    'device_model_select': {'zh': '设备型号选择', 'en': 'Device Model'},
    'config_params':      {'zh': '配置参数', 'en': 'Configuration'},
    'series':       {'zh': '系列', 'en': 'Series'},
    'model':        {'zh': '型号', 'en': 'Model'},
    'select_device': {'zh': '请选择设备', 'en': 'Please select a device'},
    'model_sw_ver_label': {'zh': '项目代号', 'en': 'Project Code'},
    'device_model_label': {'zh': '入网型号', 'en': 'Network Model'},
    'sw_version_label':   {'zh': '系统软件版本', 'en': 'System Version'},
    'android_ver_label':  {'zh': '底层安卓版本', 'en': 'Android Version'},
    'model_sw_ver_ph':  {'zh': '软件型号，例如 PD2408', 'en': 'Software model, e.g. PD2408'},
    'device_model_ph':  {'zh': '设备型号，例如 V2408A', 'en': 'Device model, e.g. V2408A'},
    'sw_version_ph':    {'zh': '系统版本号，例如 16.1.16.5.W10', 'en': 'System version, e.g. 16.1.16.5.W10'},
    'android_ver_ph':   {'zh': '安卓版本，例如 16', 'en': 'Android version, e.g. 16'},
    'model_sw_ver_tip': {'zh': '软件型号，例如 PD2408', 'en': 'Software model, e.g. PD2408'},
    'device_model_tip': {'zh': '设备型号，例如 V2408A', 'en': 'Device model, e.g. V2408A'},
    'sw_version_tip':   {'zh': '系统版本号，例如 16.1.16.5.W10', 'en': 'System version, e.g. 16.1.16.5.W10'},
    'android_ver_tip':  {'zh': '安卓版本，例如 16（13=OriginOS3, 14=OriginOS4, 15=OriginOS5, 16=OriginOS6）',
                          'en': 'Android version, e.g. 16 (13=OriginOS3, 14=OriginOS4, 15=OriginOS5, 16=OriginOS6)'},
    'snp_label':        {'zh': '序列号 (SN)', 'en': 'Serial Number'},
    'snp_tip':          {'zh': '设备序列号，留空使用默认值', 'en': 'Device serial number, leave empty for default'},
    'snp_ph':           {'zh': '例如 A0000000000000A', 'en': 'e.g. A0000000000000A'},
    'is_full_label':    {'zh': '全量包', 'en': 'Full Package'},
    'is_full_tip':      {'zh': '勾选请求全量升级包，否则请求增量包', 'en': 'Check for full OTA package, uncheck for incremental'},
    'start_get_link':  {'zh': '开始获取链接', 'en': 'Get Download Link'},
    'verbose_mode':    {'zh': '详细日志模式', 'en': 'Verbose Log'},
    'verbose_tip':     {'zh': '勾选后显示完整日志输出，不勾选仅显示简洁结果',
                         'en': 'Show full log output when checked, concise result otherwise'},
    'copy_clipboard':  {'zh': '一键复制到剪贴板', 'en': 'Copy to Clipboard'},
    'theme_toggle':    {'zh': '切换深色模式', 'en': 'Toggle Light Mode'},
    'lang_toggle':     {'zh': 'EN', 'en': '中'},
    'lang_tip':        {'zh': '切换为英文', 'en': 'Switch to Chinese'},
    'changelog_btn':   {'zh': '更新日志', 'en': 'Changelog'},
    'about_btn':       {'zh': '关于', 'en': 'About'},
    'ok_btn':          {'zh': '好的', 'en': 'OK'},
    'about_title':     {'zh': '关于', 'en': 'About'},
    'about_text': {
        'zh': '<h2>Vivo OTA Tracker</h2>'
              '<p><b>版本:</b> {ver}</p>'
              '<p><b>构建日期:</b> 2026-07-24</p>'
              '<hr>'
              '<p><b>GUI 作者:</b> 酷安 @mytiantian_是天天吖</p>'
              '<p><b>原项目作者:</b> 酷安 @桜酱没有未来</p>'
              '<p><b>原项目地址:</b> '
              '<a href="https://github.com/JerryTse-OSS/VIVO-OTA-Tracker">'
              'JerryTse-OSS/VIVO-OTA-Tracker</a></p>'
              '<hr>'
              '<p>GUI 基于 <b>PyQt-Fluent-Widgets</b> 构建</p>'
              '<p>采用 Liquid Glass 液态玻璃界面风格</p>'.format(ver=APP_VERSION),
        'en': '<h2>Vivo OTA Tracker</h2>'
              '<p><b>Version:</b> {ver}</p>'
              '<p><b>Built:</b> 2026-07-24</p>'
              '<hr>'
              '<p><b>GUI Author:</b> CoolAPK @mytiantian</p>'
              '<p><b>Original Author:</b> CoolAPK @桜酱没有未来</p>'
              '<p><b>Original Project:</b> '
              '<a href="https://github.com/JerryTse-OSS/VIVO-OTA-Tracker">'
              'JerryTse-OSS/VIVO-OTA-Tracker</a></p>'
              '<hr>'
              '<p>GUI built with <b>PyQt-Fluent-Widgets</b></p>'
              '<p>Liquid Glass UI design</p>'.format(ver=APP_VERSION),
    },
    'changelog_title': {'zh': '更新日志', 'en': 'Changelog'},
    'changelog_text': {
        'zh': '<h3>V1.3.0</h3>'
              '<ul>'
              '<li>全面重构 GUI，采用 PyQt-Fluent-Widgets 液态玻璃界面风格</li>'
              '<li>Acrylic 亚克力模糊背景，全透明卡片和控件</li>'
              '<li>白色字体 + 微软雅黑，统一 7pt 字号</li>'
              '<li>系统软件版本拆分为 5 段独立输入框，标签左对齐</li>'
              '<li>新增序列号 (SNP) 输入和全量包 (IS_FULL) 选项</li>'
              '<li>新增更新日志自动获取和展示功能</li>'
              '<li>新增「关于」页面</li>'
              '<li>下拉菜单半透明玻璃风格，向下展开动画</li>'
              '<li>弹窗（警告、关于、更新日志）均采用 acrylic 模糊背景</li>'
              '<li>重新编译 JAR，内置最新 Java 源码（支持 IS_FULL、SNP 参数）</li>'
              '<li>移除 Updater.apk 依赖，使用硬编码证书</li>'
              '<li>新增 JSON 结构化输出，提升解析可靠性</li>'
              '<li>修复 SSL 握手问题（强制 TLS 1.2）</li>'
              '<li>强制 IPv4 连接，修复 Vivo 服务器超时</li>'
              '<li>修复设备系列→型号级联选择（userData 参数修正）</li>'
              '</ul>'
              '<h3>V1.2.0</h3>'
              '<ul>'
              '<li>基于 PyQt5 的图形化界面</li>'
              '<li>支持设备型号自动选择</li>'
              '<li>支持中英文切换</li>'
              '</ul>',
        'en': '<h3>V1.3.0</h3>'
              '<ul>'
              '<li>Full GUI rewrite with PyQt-Fluent-Widgets liquid glass design</li>'
              '<li>Acrylic blur background, fully transparent cards and controls</li>'
              '<li>White text + Microsoft YaHei font, unified 7pt size</li>'
              '<li>System version split into 5 separate input fields, left-aligned labels</li>'
              '<li>Added Serial Number (SNP) input and Full Package (IS_FULL) option</li>'
              '<li>Added automatic update log fetching and display</li>'
              '<li>Added About page</li>'
              '<li>Dropdown menus with glass styling, drop-down animation</li>'
              '<li>All dialogs (warning, about, update log) with acrylic blur</li>'
              '<li>Recompiled JAR with latest Java source (IS_FULL, SNP support)</li>'
              '<li>Removed Updater.apk dependency, using hardcoded certificate</li>'
              '<li>Added structured JSON output for reliable parsing</li>'
              '<li>Fixed SSL handshake (enforce TLS 1.2)</li>'
              '<li>Force IPv4 connection, fixed Vivo server timeout</li>'
              '<li>Fixed series-to-model cascade selection (userData fix)</li>'
              '</ul>'
              '<h3>V1.2.0</h3>'
              '<ul>'
              '<li>PyQt5-based graphical interface</li>'
              '<li>Auto device model selection</li>'
              '<li>Chinese/English language toggle</li>'
              '</ul>',
    },
    'update_log_title': {'zh': '更新日志', 'en': 'Update Log'},
    'update_log_empty': {'zh': '本次响应中未找到可展示的更新日志。', 'en': 'No displayable update log was found in this response.'},
    'update_log_loading': {'zh': '正在加载更新日志页面...', 'en': 'Loading update log page...'},
    'update_log_load_failed': {'zh': '更新日志页面加载失败。', 'en': 'Failed to load the update log page.'},
    'update_log_link': {'zh': '更新日志', 'en': 'Update Log'},
    'update_log_expand': {'zh': '更\n新\n日\n志\n◀', 'en': 'L\no\ng\n◀'},
    'update_log_collapse': {'zh': '更\n新\n日\n志\n▶', 'en': 'L\no\ng\n▶'},
    'warn_fill_all':   {'zh': '请填写所有参数后再开始获取链接！\n\n- 项目代号\n- 入网型号\n- 系统软件版本\n- 底层安卓版本（需为数字）',
                         'en': 'Please fill in all parameters before getting the link!\n\n- Project Code\n- Network Model\n- System Version\n- Android Version (digits only)'},
    'no_result_to_copy': {'zh': '没有可复制的结果，请先运行查询。', 'en': 'No result to copy. Please run a query first.'},
    'copied':       {'zh': '已复制到剪贴板！', 'en': 'Copied to clipboard!'},
    'error_title':  {'zh': '错误', 'en': 'Error'},
    'warn_title':   {'zh': '警告', 'en': 'Warning'},
    'success_title': {'zh': '成功', 'en': 'Success'},
    'info_title':   {'zh': '提示', 'en': 'Info'},
    'please_wait':  {'zh': '正在执行中，请稍等……', 'en': 'Running, please wait...'},
    'step_running': {'zh': '[Step 1/1] 正在运行 VivoOtaTracker...', 'en': '[Step 1/1] Running VivoOtaTracker...'},
    'exec_cmd':     {'zh': '执行命令', 'en': 'Command'},
    'error_exec_fail': {'zh': '执行失败！错误码', 'en': 'Execution failed! Exit code'},
    'error_no_java': {'zh': '未找到 Java 运行时环境', 'en': 'Java runtime not found'},
    'done':         {'zh': '任务执行完毕', 'en': 'Task completed'},
    'ota_banner':   {'zh': 'OTA 更新信息', 'en': 'OTA Update Info'},
    'device_type_field': {'zh': '设备类型', 'en': 'Device Type'},
    'device_model_field': {'zh': '设备型号', 'en': 'Device Model'},
    'android_ver_field':  {'zh': 'Android版本', 'en': 'Android Ver'},
    'sw_ver_field':       {'zh': '软件版本', 'en': 'SW Version'},
    'file_size_field':    {'zh': '软件包大小', 'en': 'Package Size'},
    'download_url_field': {'zh': '下载链接', 'en': 'Download URL'},
    'phone_cn':  {'zh': '手机', 'en': 'Phone'},
    'tablet_cn': {'zh': '平板', 'en': 'Tablet'},
    'credit_text': {
        'zh': '图形化制作基于 <b>PyQt5</b> | GUI作者: <b>酷安@mytiantian_是天天吖</b> | 原项目作者: <b>酷安@桜酱没有未来</b><br>'
              '原项目: ',
        'en': 'GUI built with <b>PyQt5</b> | GUI Author: <b>CoolAPK@mytiantian</b> | Original Author: <b>CoolAPK@桜酱没有未来</b><br>'
              'Original: ',
    },
}


def t(key, lang='zh'):
    entry = TR.get(key, {})
    return entry.get(lang, key)
