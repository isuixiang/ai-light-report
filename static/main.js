// 当前页码和总页数
let currentPage = 1;
let totalPages = 1;

// 当前数据源和模板ID
let currentDsId = null;
let currentTemplateId = null;

// 当前模板定义，初始化一个JSON空数组
let templateContent = [];

// 加载和隐藏动画
function showLoading() {
	document.getElementById('loading').style.display = 'block';
}

function hideLoading() {
	document.getElementById('loading').style.display = 'none';
}

// 加载和隐藏动画（聊天窗口）
function showChatLoading() {
	document.getElementById('chat-loading').style.display = 'block';
}

function hideChatLoading() {
	document.getElementById('chat-loading').style.display = 'none';
}

// 初始化聊天区
function initMessage() {
	// 清空输入框
	document.getElementById('messageInput').value = "";

	// 初始化聊天区
	document.getElementById('chatContainer').innerHTML = `
		<div class="ai-message assistant">
			<div class="ai-message-content">
				您好！我是AI报表助手，很高兴为您服务。
			</div>
		</div>
	`;
}

// New Chat
document.getElementById('newChatBtn').addEventListener('click', () => {
	newChat();
})

// 新聊天
function newChat() {
	// 初始化聊天区
	initMessage();
}

// 初始化模板编辑区
function initExcelTemplate() {
	document.getElementById('tableContainer').innerHTML = `
		<div class="mt-3 text-center">
			<img width="48px" src="static/images/excel.png">
			<div class="mt-1 text-muted">请选择模板</div>
		</div>
	`;
}

// 页面加载事件
document.addEventListener('DOMContentLoaded', () => {
	// 初始化聊天区
	initMessage();

	// 查找所有数据源
	const ds_length = document.querySelectorAll('.datasource-item').length;
	if (ds_length == 0) return false;

	// 取当前激活的数据源
	currentDsId = document.querySelector('.datasource-item.active').getAttribute('data-id');
	if (!currentDsId) return false;

	// 取模板列表
	getExcelTemplate(currentPage);

	// 使用事件委托处理分页按钮点击
	document.getElementById('pagination').addEventListener('click', function(e) {
		if (e.target.tagName === 'A') {
			e.preventDefault();
			
			// 获取目标页码
			const targetPage = e.target.getAttribute('data-page');
			if (targetPage) {
				getExcelTemplate(parseInt(targetPage));
			}
		}
	})
})

// 取报表模板
function getExcelTemplate(page) {
	// 发起请求
	$.ajax({
		url: "/exceltemplate/list",
		data: JSON.stringify({'page':page, 'ds_id': currentDsId}),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error)
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				const results = result.data.results;

				// 更新当前页码和总页数
				currentPage = result.data.current_page;
				totalPages = result.data.total_pages;

				// 更新报表模板
				updateExcelTemplate(results);

				// 更新分页控件
                updatePagination();
			} else {
				// 其它错误
				console.log(result.message);
			}
		}
	})
}

// 更新报表模板
function updateExcelTemplate(items) {
	const historyList = document.getElementById('historyList');
	historyList.innerHTML = '';
	
	if (items.length === 0) {
		historyList.innerHTML = '<div class="text-center text-muted mt-3">暂无数据</div>';
		return;
	}

	items.forEach(item => {
		const content = document.createElement('div');
		content.className = 'history-item';
		content.setAttribute('data-id', `${item.id}`);
		content.addEventListener('click', function() {
			selectExcelTemplate(this);
		});
		content.innerHTML = `
			<div class="d-flex justify-content-between align-items-center">
				<span class="text-truncate small">${item.title}</span>
				<button class="btn btn-sm btn-link" onclick="toggleExcelTemplateMenu(event, this, ${item.id}, '${item.title}', '${item.desc}')">
					<i class="bi bi-three-dots-vertical"></i>
				</button>
			</div>
		`;
		historyList.appendChild(content);
	});
}

// 更新分页控件
function updatePagination() {
	const pagination = document.getElementById('pagination');
	pagination.innerHTML = '';
	
	const maxVisiblePages = 5; // 最多显示5个页码按钮
	let startPage, endPage;
	
	// 计算显示的页码范围
	if (totalPages <= maxVisiblePages) {
		// 总页数少于等于5页，显示所有页码
		startPage = 1;
		endPage = totalPages;
	} else {
		// 总页数多于5页，计算显示范围
		const halfVisible = Math.floor(maxVisiblePages / 2);
		
		if (currentPage <= halfVisible + 1) {
			// 当前页在开头部分
			startPage = 1;
			endPage = maxVisiblePages;
		} else if (currentPage >= totalPages - halfVisible) {
			// 当前页在结尾部分
			startPage = totalPages - maxVisiblePages + 1;
			endPage = totalPages;
		} else {
			// 当前页在中间部分
			startPage = currentPage - halfVisible;
			endPage = currentPage + halfVisible;
		}
	}
	
	if (totalPages > 0) {
		// 添加上一页按钮
		const prevLi = document.createElement('li');
		prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
		prevLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage - 1}">&laquo;</a>`;
		pagination.appendChild(prevLi);
		
		// 添加第一页和前面的省略号（如果需要）
		if (startPage > 1) {
			if (startPage > 1) {
				const ellipsisLi = document.createElement('li');
				ellipsisLi.className = 'page-item disabled';
				ellipsisLi.innerHTML = `<span class="page-link">...</span>`;
				pagination.appendChild(ellipsisLi);
			}
		}
		
		// 添加页码按钮
		for (let i = startPage; i <= endPage; i++) {
			const pageLi = document.createElement('li');
			pageLi.className = `page-item ${i === currentPage ? 'active' : ''}`;
			pageLi.innerHTML = `<a class="page-link" href="#" data-page="${i}">${i}</a>`;
			pagination.appendChild(pageLi);
		}
		
		// 添加最后一页和后面的省略号（如果需要）
		if (endPage < totalPages) {
			if (endPage < totalPages) {
				const ellipsisLi = document.createElement('li');
				ellipsisLi.className = 'page-item disabled';
				ellipsisLi.innerHTML = `<span class="page-link">...</span>`;
				pagination.appendChild(ellipsisLi);
			}
		}
		
		// 添加下一页按钮
		const nextLi = document.createElement('li');
		nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
		nextLi.innerHTML = `<a class="page-link" href="#" data-page="${currentPage + 1}">&raquo;</a>`;
		pagination.appendChild(nextLi);
	}
}

// DataSource Menu
function toggleDataSourceMenu(event, btn, id, name) {
	event.stopPropagation();	// 阻止事件冒泡，避免触发父元素的事件
	const menu = document.getElementById('datasourceMenu');
	const rect = btn.getBoundingClientRect();
	menu.style.top = rect.bottom + 'px';
	menu.style.left = (rect.left - 50) + 'px';
	menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
	
	// 当前选中的记录id、name
	$('#temp-datasource-id').val(id);
	$('#temp-datasource-name').val(name);
}

// Click outside to close datasource menu
document.addEventListener('click', (e) => {
	if (!e.target.closest('#datasourceMenu') && !e.target.closest('.bi-three-dots-vertical')) {
		document.getElementById('datasourceMenu').style.display = 'none';
	}
})

// ExcelTemplate Menu
function toggleExcelTemplateMenu(event, btn, id, title, desc) {
	event.stopPropagation();	// 阻止事件冒泡，避免触发父元素的事件
	const menu = document.getElementById('excelTemplateMenu');
	const rect = btn.getBoundingClientRect();
	menu.style.top = rect.bottom + 'px';
	menu.style.left = (rect.left - 120) + 'px';
	menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
	
	// 当前选中的模板ID、标题和描述
	$('#temp-exceltemplate-id').val(id);
	$('#temp-exceltemplate-title').val(title);
	$('#temp-exceltemplate-desc').val(desc);
}

// Click outside to close exceltemplate menu
document.addEventListener('click', (e) => {
	if (!e.target.closest('#excelTemplateMenu') && !e.target.closest('.bi-three-dots-vertical')) {
		document.getElementById('excelTemplateMenu').style.display = 'none';
	}
})

// Datasource selection
function selectDatasource(element) {
	document.querySelectorAll('.datasource-item').forEach(item => {
		item.classList.remove('active');
	});
	element.classList.add('active');

	// 全局数据源ID
	currentDsId = element.getAttribute('data-id');
	if (!currentDsId) return false;

	// 初始化模板区
	initExcelTemplate();

	// 更新报表模板
	getExcelTemplate(currentPage);
	
	// 初始化聊天区
	initMessage();
}

// 点击报表模板
function selectExcelTemplate(element) {
	document.querySelectorAll('.history-item').forEach(item => {
		item.classList.remove('active');
	});
	element.classList.add('active');

	// 取当前模板ID
	const template_id = element.getAttribute('data-id');
	if (!template_id) return false;
	//console.log(template_id);

	// Update status
	document.getElementById('statusText').textContent = '正在获取报表模板...';

	// 发起请求
	$.ajax({
		url: "/exceltemplate/detail",
		data: JSON.stringify({'id': template_id}),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				//console.log(result.data)

				// 更新当前的模板ID
				currentTemplateId = result.data.id;
				//console.log(currentTemplateId);

				// 更新当前的模板定义
				templateContent = [];
				if (result.data.content) {
					templateContent = JSON.parse(result.data.content);
					//console.log(templateContent);
				}

				// 渲染历史对话过程
				setTimeout(() => {
					showExcelTemplate(result.data);
					document.getElementById('statusText').textContent = '就绪';
				}, 1000);
			} else {
				// 其它错误
				//console.log(result.message);
				document.getElementById('statusText').textContent = result.message;
			}
		}
	})
}

// 工具函数：将列索引转为 Excel 风格字母（1→A, 2→B, ..., 27→AA）
function columnIndexToLetter(colIndex) {
	let letters = '';
	while (colIndex > 0) {
		colIndex -= 1;
		letters = String.fromCharCode(65 + (colIndex % 26)) + letters;
		colIndex = Math.floor(colIndex / 26);
	}
	return letters || 'A';
}

// 渲染报表模板
function showExcelTemplate(data) {
	// 报表模板定义
	const pattern = JSON.parse(data.pattern);
	//console.log(pattern);

	// 模板容器
	const container = document.getElementById('tableContainer');
	container.innerHTML = "";

	const table = document.createElement('table');
	table.setAttribute('contenteditable', 'false'); // 防止整表可编辑

	// 初始化选中的行和列
	let row_index = 1;
	pattern.forEach(row => {
		const tr = document.createElement('tr');
		let col_index = 1;
		row.forEach(cellValue => {
			const td = document.createElement('td');
			td.textContent = cellValue || '';
			// 空值的单元格允许编辑
			if (cellValue == "") {
				td.setAttribute('contenteditable', 'true'); // 关键：允许编辑

				// 填充报表定义
				const item = templateContent.find(item => item.row === row_index && item.col === col_index);
				const itemValue = item ? item.value : '';
				if (itemValue) {
					td.textContent = itemValue;
					td.className = "cell-truncate cell-setting";	// 截取字符长度并添加背景色
				}
			}

			// 可选：按 Enter 跳到下一行或保存
			td.addEventListener('keydown', function(e) {
				if (e.key === 'Enter') {
					e.preventDefault();
					this.blur(); // 失去焦点即“保存”
				}
			})

			tr.appendChild(td);
			//console.log(row_index, col_index);
			col_index = col_index + 1;		// 列递增
		})

		row_index = row_index + 1;	// 行递增
		table.appendChild(tr);
	})

	container.appendChild(table);

	// 初始化选中的行和列
	let rowIndex = 0;
	let colIndex = 0;

	// 单元格获取焦点时
	table.addEventListener('focusin', function(e) {
		if (e.target.matches('td[contenteditable="true"]')) {
			e.target.style.backgroundColor = '#e3f2fd';

			// 显示行列
			const td = e.target;
			const row = td.parentElement; // <tr>
			const tb = row.closest('table');

			// 计算行号：从 1 开始
			rowIndex = Array.from(tb.querySelectorAll('tr')).indexOf(row) + 1;

			// 计算列号：从 1 开始
			colIndex = Array.from(row.querySelectorAll('td')).indexOf(td) + 1;
			
			// 单元格行和列
			$('#row-index').val(rowIndex);
			$('#col-index').val(colIndex);

			// 单元格的值
			const item = templateContent.find(item => item.row === rowIndex && item.col === colIndex);
			const itemValue = item ? item.value : '';
			$('#cell-value').val(itemValue);

			// 打开编辑窗口
			const modal = new bootstrap.Modal(document.getElementById('cellEditorModal'));
			modal.show();
		}
	})

	// 单元格失去焦点时保存
	table.addEventListener('focusout', function(e) {
		if (e.target.matches('td[contenteditable="true"]')) {
			e.target.style.backgroundColor = '';
			//console.log('单元格值已更新:', e.target.textContent.trim());
			//console.log('行：', rowIndex, '列：', colIndex);
		}
	})
}

// 保存报表定义
$('#btnExcelSetting').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	const rowIndex = parseInt($("#row-index").val());
	const colIndex = parseInt($("#col-index").val());
	const cellValue = $("#cell-value").val().trim();
	//console.log("row:", rowIndex, "col:", colIndex, "value:", cellValue);

	// 修改报表定义JSON数组
	if (cellValue.length > 0) {
		let cellType = "text";
		if (cellValue.toLowerCase().startsWith("select")) {
			cellType = "sql";
		}
		//console.log(rowIndex, colIndex, cellType, cellValue);

		// 更新单元格逻辑
		const item = templateContent.find(item => item.row === rowIndex && item.col === colIndex);
		if (item) {
			item.type = cellType;
			item.value = cellValue;
		} else {
			const newItem = {
				"row": rowIndex,
				"col": colIndex,
				"type": cellType,
				"value": cellValue
			}
			templateContent.push(newItem);
		}
	} else {
		// 从原定义中删除单元格逻辑
		const index = templateContent.findIndex(item => item.row === rowIndex && item.col === colIndex);
		if (index != -1) {
			templateContent.splice(index, 1);	// 删除索引处的元素
		}
	}
	//console.log(templateContent);

	// 更新报表定义
	excelTemplateSetting();

	// 关闭模态窗口
	$("#cellEditorModal").modal('hide');
})

// 清除报表定义
function excelTemplateClear() {
	// 当前模板ID
	if (!currentTemplateId) return false;

	// 请求数据
	const data = {
		"id": currentTemplateId,
		"content": []
	}

	// Update status
	document.getElementById('statusText').textContent = '正在清除报表逻辑...';

	// 发起请求
	$.ajax({
		url: "/exceltemplate/setting",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				// 更新当前的模板定义
				templateContent = [];
				if (result.data.content) {
					templateContent = JSON.parse(result.data.content);
					//console.log(templateContent);
				}

				// 渲染报表过程
				showExcelTemplate(result.data);

				document.getElementById('statusText').textContent = '就绪';
			} else {
				// 其它错误
				//console.log(result.message);
				//alert(result.message);
				document.getElementById('statusText').textContent = result.message;
			}
		}
	})
}

// 更新报表定义
function excelTemplateSetting() {
	// 当前模板ID
	if (!currentTemplateId) return false;

	// 请求数据
	const data = {
		"id": currentTemplateId,
		"content": templateContent
	}

	// Update status
	document.getElementById('statusText').textContent = '正在保存报表逻辑...';

	// 发起请求
	$.ajax({
		url: "/exceltemplate/setting",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				// 更新当前的模板定义
				templateContent = [];
				if (result.data.content) {
					templateContent = JSON.parse(result.data.content);
					//console.log(templateContent);
				}

				// 渲染报表过程
				showExcelTemplate(result.data);

				document.getElementById('statusText').textContent = '就绪';
			} else {
				// 其它错误
				//console.log(result.message);
				//alert(result.message);
				document.getElementById('statusText').textContent = result.message;
			}
		}
	})
}

// 生成输出报表
function excelTemplateExecute() {
	// 当前模板ID
	if (!currentTemplateId) return false;

	// 请求数据
	const data = {
		"id": currentTemplateId
	}

	// Update status
	document.getElementById('statusText').textContent = '正在生成输出报表...';

	showLoading();		// 加载动画

	// 发起请求
	$.ajax({
		url: "/exceltemplate/execute",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				//console.log(result.message);

				// 显示报表输出模态窗口
				showOutputExcelModal();

				document.getElementById('statusText').textContent = '就绪';
			} else {
				// 其它错误
				//console.log(result.message);
				//alert(result.message);
				document.getElementById('statusText').textContent = result.message;
			}
		},
		complete: function() {
			hideLoading();		// 隐藏动画
		}
	})
}

// 一键生成报表逻辑
function excelTemplateFullSetting() {
	// 数据源ID
	if (!currentDsId) return false;

	// 当前模板ID
	if (!currentTemplateId) return false;

	// 取当前大模型名称
	const llmname = document.getElementById('llm').value;
	if (!llmname) return false;

	// 请求数据
	const data = {
		"ds_id": currentDsId,
		"template_id": currentTemplateId,
		"llmname": llmname
	}

	// Update status
	document.getElementById('statusText').textContent = '正在生成报表逻辑...';

	showLoading();		// 加载动画

	// 发起请求
	$.ajax({
		url: "/chat/fullsetting",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		timeout: 90000,		// 超时时间90s
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				// 更新当前的模板定义
				templateContent = [];
				if (result.data.content) {
					templateContent = JSON.parse(result.data.content);
					//console.log(templateContent);
				}

				// 渲染报表过程
				showExcelTemplate(result.data);

				document.getElementById('statusText').textContent = '就绪';
			} else {
				// 其它错误
				//console.log(result.message);
				//alert(result.message);
				document.getElementById('statusText').textContent = result.message;
			}
		},
		complete: function() {
			hideLoading();		// 隐藏动画
		}
	})
}

// Send message
document.getElementById('sendButton').addEventListener('click', sendMessage);
document.getElementById('messageInput').addEventListener('keypress', (e) => {
	if (e.key === 'Enter') sendMessage();
})

// 提交聊天消息
function sendMessage() {
	const input = document.getElementById('messageInput');
	const message = input.value.trim();
	if (!message) return false;

	// 未选中数据源时
	if (!currentDsId) return false;

	// 未选择模板时
	//if (!currentTemplateId) return false;

	// 取当前大模型名称
	const llmname = document.getElementById('llm').value;
	if (!llmname) return false;

	// Add user message
	addMessage(message, 'user');
	input.value = '';
	
	// 请求数据
	const data = {
		"ds_id": currentDsId,			// 全局数据源ID
		"llmname": llmname,			// 大模型名称
		"message": message
	}

	showChatLoading();		// 加载动画

	// 发起请求
	$.ajax({
		url: "/chat/sendmessage",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		timeout: 90000,		// 超时时间90s
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				console.log(result.data)

				// 添加SQL语句
				setTimeout(() => {
					addSQLBlock(result.data);
				}, 1000);
			} else {
				// 其它错误
				//console.log(result.message);
				addMessage(result.message, 'assistant');
			}
		},
		complete: function() {
			hideChatLoading();		// 隐藏动画
		}
	})
}

// 添加消息到聊天区
function addMessage(content, sender) {
	const messagesContainer = document.getElementById('chatContainer');
	const messageDiv = document.createElement('div');
	messageDiv.className = `ai-message ${sender}`;
	
	const contentDiv = document.createElement('div');
	contentDiv.className = 'ai-message-content';
	contentDiv.textContent = content;
	
	/*if (sender === 'user') {
		contentDiv.textContent = content;
	} else {
		contentDiv.innerHTML = `
			<div class="d-flex align-items-center mb-2">
				<i class="bi bi-robot text-primary me-2"></i>
				<strong>AI助手</strong>
			</div>
			<p>${content}</p>
		`;
	}*/
	
	messageDiv.appendChild(contentDiv);
	messagesContainer.appendChild(messageDiv);
	messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 添加SQL语句
function addSQLBlock(data) {
	// 格式化与HTML转义
	const id = data.id;
	const sql = data.sql;
	const formatted = sqlFormatter.format(sql, { language: 'sql' });
    const escaped = formatted
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
	
	// 元素ID
	const element_id = "sql-" + id;

	const messagesContainer = document.getElementById('chatContainer');
	const messageDiv = document.createElement('div');
	messageDiv.className = 'ai-message assistant';

	const contentDiv = document.createElement('div');
	contentDiv.className = 'ai-message-content';
	contentDiv.innerHTML = `
		<div class="sql-block">
			<pre><code class="language-sql" id="${element_id}">${escaped}</code></pre>
		</div>
		<div class="d-flex justify-content-end gap-2 mt-2">
			<button class="btn btn-sm btn-outline-secondary" data-sql="${escaped}" onclick="copySQL(event, '${element_id}')">
			<i class="bi bi-files"></i> 复制
			</button>
			<button class="btn btn-sm btn-outline-secondary" onclick="executeSQL(event, ${id})">
			<i class="bi bi-play-circle"></i> 执行
			</button>
		</div>
	`;

	messageDiv.appendChild(contentDiv);
	messagesContainer.appendChild(messageDiv);

	// SQL语法高亮
	const codeEl = document.getElementById(element_id);
	if (codeEl) {
		Prism.highlightElement(codeEl);
	}

	messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 复制SQL
async function copySQL(event, id) {
	// 防止重复提交
	event.preventDefault();

	// SQL元素
	const codeElement = document.getElementById(id);

	try {
		// 使用现代Clipboard API
		await navigator.clipboard.writeText(codeElement.textContent);

		// 显示成功提示
		button = event.target;
        //button.textContent = '✓ 已复制';
		button.innerHTML = `<i class="bi bi-check-lg"></i> 已复制`;

		// 恢复提示
		setTimeout(() => {
			button.innerHTML = `<i class="bi bi-files"></i> 复制`;
		}, 2000);
	} catch (err) {
        console.error('复制失败:', err);
	}
}

// 执行SQL
function executeSQL(event, id) {
	//console.log(id);
	if (!id) return false;

	// 未选中数据源时
	if (!currentDsId) return false;

	// 防止重复操作
	const button = event.target;
	button.disabled = true;

	// 请求数据
	const data = {
		'ds_id': currentDsId,
		'sql_id': id
	}

	showChatLoading();		// 加载动画

	// 发起请求
	$.ajax({
		url: "/chat/executesql",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		timeout: 90000,		// 超时时间90s
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				//console.log(result.data)

				setTimeout(() => {
					generateTable(result.data);
				}, 1000);
			} else {
				// 其它错误
				//console.log(result.message);
				addMessage(result.message, 'assistant');
			}
		},
		complete: function() {
			button.disabled = false;
			hideChatLoading();		// 隐藏动画
		}
	})
}

// 生成表格数据
function generateTable(data) {
	const id = data.id;
	const columns = data.content.columns;
	const records = data.content.records;
	const row_count = data.content.row_count;

	// 替换JSON对象中的双引号(必须要转义处理)
	//const json_data = JSON.stringify(data).replace(/"/g, '&quot;');

	// 检查数据行数是否超过限制
	const maxRows = 10;
    const displayData = records.slice(0, maxRows);
    const hasMore = row_count > maxRows;

	const messagesContainer = document.getElementById('chatContainer');
	const messageDiv = document.createElement('div');
	messageDiv.className = 'ai-message assistant';

	const contentDiv = document.createElement('div');
	contentDiv.className = 'ai-message-content';
	contentDiv.innerHTML = `
		<div class="data-block">
			<table class="table table-sm table-striped mb-0">
			  <thead>
				<tr>${columns.map(col => `<th>${col}</th>`).join('')}</tr>
			  </thead>
			  <tbody>
				${displayData.map(row => 
                    `<tr>${row.map(cell => `<td>${cell || ''}</td>`).join('')}</tr>`
                ).join('')}
				${hasMore ? `<tr><td colspan="${columns.length}">还有 ${row_count - maxRows} 行数据未显示</td></tr>` : ''}
			  </tbody>
			</table>
		</div>
	`;

	messageDiv.appendChild(contentDiv);
	messagesContainer.appendChild(messageDiv);
	messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// 数据源测试链接
$('#btnDsTest').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();
	
	//const dsname = $("#dsname").val();
	//if (dsname == "") return false;
	const dbtype = $("#dbtype").val();
	if (dbtype == "") return false;
	const dbport = $("#dbport").val();
	if (dbport == "") return false;
	const dbhost = $("#dbhost").val();
	if (dbhost == "") return false;
	const dbname = $("#dbname").val();
	if (dbname == "") return false;
	const dbuser = $("#dbuser").val();
	if (dbuser == "") return false;
	const dbpassword = $("#dbpassword").val();
	if (dbpassword == "") return false;

	// 请求数据
	const data = {
		//"name": dsname,
		"dbtype": dbtype,
		"dbport": dbport,
		"dbhost": dbhost,
		"dbname": dbname,
		"dbuser": dbuser,
		"dbpassword": dbpassword
	}
	
	// 禁用提交按钮
	const btn = document.getElementById('btnDsTest');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/datasource/test",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error)
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('连接成功')
				btn.disabled = false;
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 数据源参数保存
$('#btnDsSave').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	const dsname = $("#dsname").val();
	if (dsname == "") return false;
	const dbtype = $("#dbtype").val();
	if (dbtype == "") return false;
	const dbport = $("#dbport").val();
	if (dbport == "") return false;
	const dbhost = $("#dbhost").val();
	if (dbhost == "") return false;
	const dbname = $("#dbname").val();
	if (dbname == "") return false;
	const dbuser = $("#dbuser").val();
	if (dbuser == "") return false;
	const dbpassword = $("#dbpassword").val();
	if (dbpassword == "") return false;

	// 请求数据
	const data = {
		"name": dsname,
		"dbtype": dbtype,
		"dbport": dbport,
		"dbhost": dbhost,
		"dbname": dbname,
		"dbuser": dbuser,
		"dbpassword": dbpassword
	}
	
	// 禁用提交按钮
	const btn = document.getElementById('btnDsSave');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/datasource/save",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('保存成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#datasourceModal").modal('hide');
				location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 数据源更新名称
$('#btnDsEdit').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 数据源ID
	const ds_id = $('#temp-datasource-id').val();
	if (!ds_id) return false;
	
	// 数据源名称
	const dsname = $("#new-dsname").val();
	if (!dsname) return false;

	// 请求数据
	const data = {
		"ds_id": ds_id,
		"name": dsname,
	}
	
	// 禁用提交按钮
	const btn = document.getElementById('btnDsEdit');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/datasource/edit",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('保存成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#datasourceEditModal").modal('hide');
				location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 删除数据源
$('#deleteDataSource').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 隐藏弹出框
	document.getElementById('datasourceMenu').style.display = 'none';

	// 数据源ID
	const id = $('#temp-datasource-id').val();
	if (!id) return false;

	if (confirm('同时删除归属该数据源的所有历史记录，确定要删除该数据源吗？')) {
		// 发起请求
		$.ajax({
			url: "/datasource/delete",
			data: JSON.stringify({'id': id}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('删除成功')
					location.reload(true);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
})

// 添加大模型模态窗口
function addModel() {
	const modal = new bootstrap.Modal(document.getElementById('modelAddModal'));
	modal.show();
}

// 添加大模型配置
$('#btnLlmSave').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();
	
	const llmname = $("#llmname").val();
	if (llmname == "") return false;
	const apikey = $("#apikey").val();
	if (apikey == "") return false;

	// 请求数据
	const data = {
		"name": llmname,
		"apikey": apikey
	}
	
	// 禁用提交按钮
	const btn = document.getElementById('btnLlmSave');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/llm/save",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('添加成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#modelAddModal").modal('hide');
				location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 删除模型配置
function delModel(id) {
	if (confirm('确定要删除该模型配置吗？')) {
		// 发起请求
		$.ajax({
			url: "/llm/delete",
			data: JSON.stringify({'id': id}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('删除成功')
					// 关闭模态窗口并重新加载页面
					$("#modelManageModal").modal('hide');
					location.reload(true);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
}

// 设置默认模型
function setModel(id) {
	if (confirm('确定要将该模型设置为默认吗？')) {
		// 发起请求
		$.ajax({
			url: "/llm/setting",
			data: JSON.stringify({'id': id}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('设置成功')
					// 关闭模态窗口并重新加载页面
					$("#modelManageModal").modal('hide');
					location.reload(true);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
}

// 修改密码
$('#btnSettingPassword').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 原密码
	const old_password = $('#old-password').val().trim();
	if (!old_password) return false;

	// 新密码
	const new_password = $('#new-password').val().trim();
	if (new_password.length < 6) {
		alert("新密码长度不能少于6位");
		return false;
	}

	// 请求数据
	const data = {
		"old_password": old_password,
		"new_password": new_password
	}

	// 禁用提交按钮
	const btn = document.getElementById('btnSettingPassword');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/user/settingpassword",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('修改成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#settingPasswordModal").modal('hide');
				//location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

/********************** Skills 功能 Start ***************************************/
// 弹出技能管理窗口
skillsManageModal.addEventListener('show.bs.modal', function() {
	// 数据源ID
	const ds_id = $('#temp-datasource-id').val();
	if (!ds_id) return false;

	// 发起请求
	$.ajax({
		url: "/skills/list",
		data: JSON.stringify({'ds_id': ds_id}),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				//console.log(result.data);
				
				// 显示技能
				showSkills(result.data);
			} else {
				// 其它错误
				console.log(result.message);
			}
		}
	})
})

// 显示技能
function showSkills(data) {
	// 定义技能类型映射表
	const TYPE_LABELS = {
		'1': '主技能',
		'2': '子技能',
		'3': '通用技能'
	}

	// 使用模板字符串循环生成 HTML
	const html = data.map(item => `
		<tr>
			<td width="100">${TYPE_LABELS[item.type]}</td>
			<td>${item.name}</td>
			<td>${item.desc}</td>
			<td width="120">
				<div class="d-flex gap-1">
					<a href="${item.filename}" target="_blank">
						<button class="btn btn-sm text-primary" title="下载">
							<i class="bi bi-file-earmark-arrow-down"></i>
						</button>
					</a>
					<button class="btn btn-sm text-danger" title="删除" onclick="delSkill(${item.id})">
						<i class="bi bi-trash"></i>
					</button>
				</div>
			</td>
		</tr>
	`).join('');
	
	document.getElementById('skills-result').innerHTML = html;
}

// 添加技能模态窗口
function addSkill() {
	const modal = new bootstrap.Modal(document.getElementById('skillAddModal'));
	modal.show();
}

// 添加Skill文件
const uploadFile = document.getElementById('uploadFile');
let skill_filename = "";	// Skill文件名
uploadFile.addEventListener('click', function() {
	const fileInput = document.getElementById('fileInput');
	const file = fileInput.files[0];
	
	if (!file) {
		alert('请选择要上传的文件');
		return false;
	}

	// 上传md文件时需要通过扩展名判断文件类型
	const fileName = file.name.toLowerCase();
  	if (!fileName.endsWith('.md')) {
		alert('只支持上传Markdown文件');
		return false;
	}
	
	// 检查文件大小 (2MB)
	if (file.size > 2 * 1024 * 1024) {
		alert('文件大小不能超过2MB');
		return false;
	}
	
	// 创建FormData对象
	const formData = new FormData();
	formData.append('file', file);

	uploadFile.disabled = true;
	uploadFile.innerHTML = '上传中...';
	
	// 发送AJAX请求
	fetch('/upload/skillfile', {
		method: 'POST',
		//timeout: 60000,		// 60s超时
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			alert('上传成功');
			console.log('文件URL: ', data.url);
			skill_filename = data.filename;
		} else {
			alert('上传失败: ' + data.error);
		}
	})
	.catch(error => {
		alert('上传过程中发生错误: ' + error.message);
	})
	.finally(() => {
		uploadFile.disabled = false;
		uploadFile.innerHTML = '上传';
	})
})

// Skill文档保存
$('#btnSkillSave').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 判断文件是否已上传
	if (skill_filename == "") {
		alert("请上传技能文件");
		return false;
	}

	// 数据源ID
	const ds_id = $('#temp-datasource-id').val();
	if (!ds_id) return false;

	const skill_type = $("#skill-type").val();
	if (skill_type == "") return false;
	const skill_name = $("#skill-name").val();
	if (skill_name == "") return false;
	const skill_desc = $("#skill-desc").val();
	if (skill_desc == "") return false;

	// 请求数据
	const data = {
		"ds_id": ds_id,
		"type": skill_type,
		"name": skill_name,
		"desc": skill_desc,
		"filename": skill_filename
	}
	
	// 禁用提交按钮
	const btn = document.getElementById('btnSkillSave');
	btn.disabled = true;
	
	// 发起请求
	$.ajax({
		url: "/skills/save",
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('保存成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#skillAddModal").modal('hide');
				location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 删除技能文档
function delSkill(skillid) {
	console.log(skillid);
	if (!skillid) return false;

	if (confirm('删除技能可能影响推理结果，确定要删除吗？')) {
		// 发起请求
		$.ajax({
			url: "/skills/delete",
			data: JSON.stringify({'id': skillid}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('删除成功');
					// 关闭模态窗口并重新加载页面
					$("#skillsManageModal").modal('hide');
					location.reload(true);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
}
/********************** Skills 功能 End ******************************************/

// 添加Excel模板模态窗口
function addExcelTemplate() {
	// 初始化参数
	excel_filename = "";
	$('#excel-headtitle').text("添加模板");
    $('#exceltemplate-id').val("");
    $('#excel-title').val("");
    $('#excel-desc').val("");

	const modal = new bootstrap.Modal(document.getElementById('excelAddModal'));
	modal.show();
}

// 编辑Excel模板模态窗口
$('#editExcelTemplate').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 设置报表参数
	$('#excel-headtitle').text("更新模板");
	const template_id = $('#temp-exceltemplate-id').val();
    $('#exceltemplate-id').val(template_id);
	const title = $('#temp-exceltemplate-title').val();
    $('#excel-title').val(title);
	const desc = $('#temp-exceltemplate-desc').val();
    $('#excel-desc').val(desc);
	
	// 隐藏弹出框
	document.getElementById('excelTemplateMenu').style.display = 'none';

	// 弹出框
	const modal = new bootstrap.Modal(document.getElementById('excelAddModal'));
	modal.show();
})

// 添加Excel文件
const uploadExcelFile = document.getElementById('uploadExcelFile');
let excel_filename = "";	// Excel文件名
uploadExcelFile.addEventListener('click', function() {
	const fileInput = document.getElementById('excelFileInput');
	const file = fileInput.files[0];
	
	if (!file) {
		alert('请选择要上传的文件');
		return false;
	}

	// 上传文件时需要通过扩展名判断文件类型
	const fileName = file.name.toLowerCase();
  	if (!fileName.endsWith('.xlsx')) {
		alert('只支持上传Excel文件');
		return false;
	}
	
	// 检查文件大小 (1MB)
	if (file.size > 1 * 1024 * 1024) {
		alert('文件大小不能超过1MB');
		return false;
	}
	
	// 创建FormData对象
	const formData = new FormData();
	formData.append('file', file);

	uploadExcelFile.disabled = true;
	uploadExcelFile.innerHTML = '上传中...';
	
	// 发送AJAX请求
	fetch('/upload/excelfile', {
		method: 'POST',
		//timeout: 60000,		// 60s超时
		body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.success) {
			alert('上传成功');
			console.log('文件URL: ', data.url);
			excel_filename = data.filename;
		} else {
			alert('上传失败: ' + data.error);
		}
	})
	.catch(error => {
		alert('上传过程中发生错误: ' + error.message);
	})
	.finally(() => {
		uploadExcelFile.disabled = false;
		uploadExcelFile.innerHTML = '上传';
	})
})

// 保存Excel模板
$('#btnExcelSave').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 模板ID
	const template_id = $("#exceltemplate-id").val();

	// 判断文件是否已上传
	if (!template_id && excel_filename == "") {
		alert("请上传模板文件");
		return false;
	}

	// 数据源ID
	if (!currentDsId) return false;
	//console.log(currentDsId);

	// 模板标题和描述
	const excel_title = $("#excel-title").val();
	if (excel_title == "") return false;
	const excel_desc = $("#excel-desc").val();
	if (excel_desc == "") return false;

	// 请求数据
	const data = {
		"ds_id": currentDsId,
		"id": template_id,
		"title": excel_title,
		"desc": excel_desc,
		"filename": excel_filename
	}
	console.log(data);
	
	// 禁用提交按钮
	const btn = document.getElementById('btnExcelSave');
	btn.disabled = true;

	// 判断是添加还是修改
	const url = !template_id ? "/exceltemplate/save" : "/exceltemplate/edit";
	
	// 发起请求
	$.ajax({
		url: url,
		data: JSON.stringify(data),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
			btn.disabled = false;
		},
		success: function(result){
			if (result.code == 200) {
				// 成功
				alert('保存成功')
				btn.disabled = false;
				// 关闭模态窗口并重新加载页面
				$("#skillAddModal").modal('hide');
				location.reload(true);
			} else {
				// 其它错误
				//console.log(result.message);
				alert(result.message);
				btn.disabled = false;
			}
		}
	})
})

// 删除报表模板
$('#deleteExcelTemplate').on('click', function(event) {
	// 防止重复提交
	event.preventDefault();

	// 隐藏弹出框
	document.getElementById('excelTemplateMenu').style.display = 'none';

	const template_id = $('#temp-exceltemplate-id').val();
	if (template_id == "") return false;

	if (confirm('确定要删除该报表模板吗？')) {
		// 发起请求
		$.ajax({
			url: "/exceltemplate/delete",
			data: JSON.stringify({'template_id': template_id}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('删除成功');

					// 初始化模板编辑区
					initExcelTemplate();
					
					// 更新报表模板
					getExcelTemplate(currentPage);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
})

// 报表输出模态窗口
function showOutputExcelModal() {
	// 模板ID
	if (!currentTemplateId) return false;

	// 发起请求
	$.ajax({
		url: "/exceloutput/list",
		data: JSON.stringify({'template_id': currentTemplateId}),
		async: true,		//异步模式
		method: "POST",
		headers: {"Authorization": token},
		contentType: "application/json;charset=utf-8",
		error: function() {
			console.log('调用接口报错:', error);
		},
		success: function(result){
			if (result.code == 200) {
				//console.log(result.data);
				
				// 显示输出报表
				if (result.data) {
					showOutputExcelFiles(result.data);

					// 显示模态窗口
					const modal = new bootstrap.Modal(document.getElementById('outputExcelModal'));
					modal.show();
				}
			} else {
				// 其它错误
				console.log(result.message);
			}
		}
	})
}

// 显示输出报表清单
function showOutputExcelFiles(data) {
	// 使用模板字符串循环生成 HTML
	const html = data.map(item => `
		<tr>
			<td>${item.title}</td>
			<td>${item.create_time}</td>
			<td width="120">
				<div class="d-flex gap-1">
					<a href="${item.filename}" download="download.xlsx">
						<button class="btn btn-sm text-primary" title="下载">
							<i class="bi bi-file-earmark-arrow-down"></i>
						</button>
					</a>
					<button class="btn btn-sm text-danger" title="删除" onclick="delExcelFile(${item.id})">
						<i class="bi bi-trash"></i>
					</button>
				</div>
			</td>
		</tr>
	`).join('');
	
	document.getElementById('output-result').innerHTML = html;
}

// 删除报表输出文件
function delExcelFile(excelid) {
	if (!excelid) return false;

	if (confirm('确定要删除这个报表输出文件吗？')) {
		// 发起请求
		$.ajax({
			url: "/exceloutput/delete",
			data: JSON.stringify({'id': excelid}),
			async: true,		//异步模式
			method: "POST",
			headers: {"Authorization": token},
			contentType: "application/json;charset=utf-8",
			error: function() {
				console.log('调用接口报错:', error);
			},
			success: function(result){
				if (result.code == 200) {
					// 成功
					alert('删除成功');
					// 关闭模态窗口
					$("#outputExcelModal").modal('hide');
					//location.reload(true);
				} else {
					// 其它错误
					//console.log(result.message);
					alert(result.message);
				}
			}
		})
	}
}
