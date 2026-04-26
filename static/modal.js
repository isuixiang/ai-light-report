// 获取DOM元素
const datasourceModal = document.getElementById('datasourceModal');
const dbtype = document.getElementById('dbtype');
const dbport = document.getElementById('dbport');

// 数据源模态窗口显示时的事件
datasourceModal.addEventListener('show.bs.modal', function() {
    // 检查下拉框是否有选项（除了第一个空选项）
    if (dbtype.options.length >= 1) {
        // 获取第一个非空选项的值
        const firstOptionValue = $('#dbtype option:first').data('port');
        // 设置输入框的值
        dbport.value = firstOptionValue;
    }
})

// 数据源模态窗口下拉框选择变化事件
dbtype.addEventListener('change', function() {
    // 修改历史记录标题模态窗口显示时的事件
    // 更新输入框的值为当前选择的值
    dbport.value = $(this).find('option:selected').data('port');
})

// 数据源更新模态窗口事件
datasourceEditModal.addEventListener('show.bs.modal', function() {
    const name = $('#temp-datasource-name').val();
    $('#new-dsname').val(name);
	
	// 隐藏弹出框
	document.getElementById('datasourceMenu').style.display = 'none';
})

// 原密码显示/隐藏
$('#toggleOldPassword').on('click', function() {
    const passwordInput = $('#old-password');
    const passwordIcon = $('#oldPasswordIcon');
    
    if (passwordInput.attr('type') === 'password') {
        passwordInput.attr('type', 'text');
        passwordIcon.removeClass('bi-eye-slash').addClass('bi-eye');
    } else {
        passwordInput.attr('type', 'password');
        passwordIcon.removeClass('bi-eye').addClass('bi-eye-slash');
    }
})

// 新密码显示/隐藏
$('#toggleNewPassword').on('click', function() {
    const passwordInput = $('#new-password');
    const passwordIcon = $('#newPasswordIcon');
    
    if (passwordInput.attr('type') === 'password') {
        passwordInput.attr('type', 'text');
        passwordIcon.removeClass('bi-eye-slash').addClass('bi-eye');
    } else {
        passwordInput.attr('type', 'password');
        passwordIcon.removeClass('bi-eye').addClass('bi-eye-slash');
    }
})

// 下拉标题功能
/*
const titleDropdown = document.getElementById('titleDropdown');
const navbarTitle = titleDropdown.querySelector('.navbar-title');
const menuItems = titleDropdown.querySelectorAll('.dropdown-title-item');
const menuRadioIcons = titleDropdown.querySelectorAll('.menu-radio');

// 初始化选中状态
updateRadioSelection(navbarTitle.textContent);

// 点击标题区域切换下拉菜单
titleDropdown.addEventListener('click', function(e) {
    e.stopPropagation();
    this.classList.toggle('open');
})

// 点击菜单项
menuItems.forEach(item => {
    item.addEventListener('click', function(e) {
        e.stopPropagation();
        const newTitle = this.getAttribute('data-value');
        navbarTitle.textContent = newTitle;
        updateRadioSelection(newTitle);
        titleDropdown.classList.remove('open');
    })
})

// 更新单选按钮状态
function updateRadioSelection(selectedValue) {
    menuRadioIcons.forEach(icon => {
        icon.style.visibility = 'hidden';
    });
    
    menuItems.forEach(item => {
        if (item.getAttribute('data-value') === selectedValue) {
            item.querySelector('.menu-radio').style.visibility = 'visible';
        }
    })
}

// 点击页面其他地方关闭下拉菜单
document.addEventListener('click', function() {
    titleDropdown.classList.remove('open');
})*/

// AI侧边栏
// 获取DOM元素
const aiFloatIcon = document.getElementById('aiFloatIcon');
const aiSidebar = document.getElementById('aiSidebar');
const closeSidebarBtn = document.getElementById('closeSidebar');
const sidebarOverlay = document.getElementById('sidebarOverlay');

// 打开侧边栏
aiFloatIcon.addEventListener('click', function() {
    aiSidebar.classList.add('active');
    aiFloatIcon.classList.add('hidden');
    sidebarOverlay.classList.add('active');

    // 清空输入框
	document.getElementById('messageInput').value = "";
    
    // 自动滚动到底部
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
})

// 关闭侧边栏
function closeSidebar() {
    aiSidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    // 延迟显示浮动图标以获得更好的视觉效果
    setTimeout(() => {
        aiFloatIcon.classList.remove('hidden');
    }, 300);
}

// 点击关闭按钮关闭侧边栏
closeSidebarBtn.addEventListener('click', closeSidebar);

// 点击遮罩关闭侧边栏
sidebarOverlay.addEventListener('click', closeSidebar);
