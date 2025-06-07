/**
 * Admin Dashboard JavaScript
 * Handles all admin dashboard functionality including user management,
 * scan logs, reported content moderation, and analytics
 */

// Admin Dashboard JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminDashboard();
});

function initializeAdminDashboard() {
    // Initialize charts
    initializeCharts();
    
    // Setup real-time updates
    setInterval(updateLiveStats, 30000); // Update every 30 seconds
    
    // Setup tip category switching
    setupTipCategories();
    
    // Setup search functionality
    setupSearchFilters();
}

function initializeCharts() {
    // Charts disabled to prevent script errors - visual placeholders shown instead
    console.log('Chart initialization skipped - using visual placeholders');
}

function setupTipCategories() {
    document.querySelectorAll('#tipCategories .list-group-item').forEach(button => {
        button.addEventListener('click', function() {
            // Update active state
            document.querySelectorAll('#tipCategories .list-group-item').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show corresponding tips
            const category = this.dataset.category;
            document.querySelectorAll('.tip-category').forEach(div => {
                div.style.display = div.dataset.category === category ? 'block' : 'none';
            });
        });
    });
}

// User management bulk operations
function selectAllUsers() {
    const selectAllCheckbox = document.getElementById('selectAllUsers');
    const userCheckboxes = document.querySelectorAll('.user-checkbox');
    
    userCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
    });
    
    updateBulkActionButtons();
}

function updateBulkActionButtons() {
    const checkedBoxes = document.querySelectorAll('.user-checkbox:checked');
    const bulkActions = document.getElementById('bulkActions');
    const selectedCount = document.getElementById('selectedCount');
    const selectAllCheckbox = document.getElementById('selectAllUsers');
    
    if (checkedBoxes.length > 0) {
        bulkActions.style.display = 'block';
        selectedCount.textContent = checkedBoxes.length;
    } else {
        bulkActions.style.display = 'none';
    }
    
    // Update select all checkbox state
    const allCheckboxes = document.querySelectorAll('.user-checkbox');
    if (checkedBoxes.length === allCheckboxes.length) {
        selectAllCheckbox.checked = true;
        selectAllCheckbox.indeterminate = false;
    } else if (checkedBoxes.length > 0) {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = true;
    } else {
        selectAllCheckbox.checked = false;
        selectAllCheckbox.indeterminate = false;
    }
}

function bulkDeleteUsers() {
    const checkedBoxes = document.querySelectorAll('.user-checkbox:checked');
    const userIds = Array.from(checkedBoxes).map(cb => cb.value);
    
    if (userIds.length === 0) {
        showNotification('No users selected for deletion', 'warning');
        return;
    }
    
    if (confirm(`Are you sure you want to delete ${userIds.length} selected users? This action cannot be undone.`)) {
        fetch('/admin/bulk-delete-users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_ids: userIds })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                if (data.errors && data.errors.length > 0) {
                    showNotification('Some users could not be deleted: ' + data.errors.join(', '), 'warning');
                }
                // Refresh the page to update the user list
                setTimeout(() => window.location.reload(), 1500);
            } else {
                showNotification('Error: ' + data.error, 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Failed to delete users', 'error');
        });
    }
}

function bulkExportUsers() {
    const checkedBoxes = document.querySelectorAll('.user-checkbox:checked');
    const userIds = Array.from(checkedBoxes).map(cb => cb.value);
    
    if (userIds.length === 0) {
        showNotification('No users selected for export', 'warning');
        return;
    }
    
    showNotification(`Exporting ${userIds.length} selected users...`, 'info');
    
    fetch('/admin/bulk-export-users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_ids: userIds })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        } else {
            return response.json().then(data => {
                throw new Error(data.error || 'Export failed');
            });
        }
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `selected_users_export_${new Date().toISOString().slice(0,10)}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showNotification('Users exported successfully', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Export failed: ' + error.message, 'error');
    });
}

function clearSelection() {
    document.querySelectorAll('.user-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    document.getElementById('selectAllUsers').checked = false;
    document.getElementById('selectAllUsers').indeterminate = false;
    updateBulkActionButtons();
}

function setupSearchFilters() {
    // User search
    const userSearch = document.getElementById('userSearch');
    if (userSearch) {
        userSearch.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const rows = document.querySelectorAll('#usersTableBody tr');
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }
    
    // Scan filters
    const scanFilter = document.getElementById('scanFilter');
    const scanDateFilter = document.getElementById('scanDateFilter');
    
    if (scanFilter) scanFilter.addEventListener('change', filterScanLogs);
    if (scanDateFilter) scanDateFilter.addEventListener('change', filterScanLogs);
}

// Toggle password field visibility in edit user modal
function togglePasswordField() {
    const checkbox = document.getElementById('changePasswordCheck');
    const passwordField = document.getElementById('passwordField');
    
    if (checkbox && passwordField) {
        passwordField.style.display = checkbox.checked ? 'block' : 'none';
        
        // Clear password field when hiding it
        if (!checkbox.checked) {
            const passwordInput = passwordField.querySelector('input[name="new_password"]');
            if (passwordInput) {
                passwordInput.value = '';
            }
        }
    }
}

function updateLiveStats() {
    fetch('/admin/live-stats')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const stats = data.stats;
                updateElementIfExists('totalUsers', stats.total_users);
                updateElementIfExists('totalScans', stats.total_scans);
                updateElementIfExists('threatsDetected', stats.threats_detected);
                updateElementIfExists('activeSessions', stats.active_sessions);
            }
        })
        .catch(error => console.error('Error updating live stats:', error));
}

function updateElementIfExists(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value || 0;
    }
}

function refreshDashboard() {
    location.reload();
}

function togglePasswordField() {
    const checkbox = document.getElementById('changePasswordCheck');
    const passwordField = document.getElementById('passwordField');
    const passwordInput = passwordField.querySelector('input[name="new_password"]');
    
    if (checkbox.checked) {
        passwordField.style.display = 'block';
        passwordInput.required = true;
    } else {
        passwordField.style.display = 'none';
        passwordInput.required = false;
        passwordInput.value = '';
    }
}

// User Management Functions
function createUser() {
    showModal('Create New User', `
        <form id="createUserForm">
            <div class="mb-3">
                <label class="form-label">Username</label>
                <input type="text" class="form-control" name="username" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" name="email" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Role</label>
                <select class="form-select" name="role" required>
                    <option value="user">User</option>
                    <option value="admin">Admin</option>
                </select>
            </div>
            <div class="mb-3">
                <label class="form-label">Temporary Password</label>
                <input type="password" class="form-control" name="password" required>
            </div>
        </form>
    `, 'handleCreateUser()');
}

function viewUser(userId) {
    if (!userId || userId === 'None') {
        showAlert('Invalid user ID provided', 'danger');
        return;
    }
    
    fetch(`/admin/get-user/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const user = data.user;
                showModal('User Details', `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Basic Information</h6>
                            <p><strong>Username:</strong> ${user.username || 'N/A'}</p>
                            <p><strong>Email:</strong> ${user.email || 'N/A'}</p>
                            <p><strong>Role:</strong> ${user.role || 'N/A'}</p>
                            <p><strong>Status:</strong> ${user.is_active ? 'Active' : 'Inactive'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Activity</h6>
                            <p><strong>Created:</strong> ${user.created_at || 'N/A'}</p>
                            <p><strong>Last Login:</strong> ${user.last_login || 'Never'}</p>
                            <p><strong>Total Scans:</strong> ${user.scan_count || 0}</p>
                            <p><strong>Login Attempts:</strong> ${user.login_attempts || 0}</p>
                        </div>
                    </div>
                `);
            } else {
                showAlert('Error loading user details: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error fetching user details:', error);
            showAlert('Error loading user details', 'danger');
        });
}

function editUser(userId) {
    if (!userId || userId === 'None') {
        showAlert('Invalid user ID provided', 'danger');
        return;
    }
    
    fetch(`/admin/get-user/${userId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const user = data.user;
                showModal('Edit User', `
                    <form id="editUserForm">
                        <input type="hidden" name="user_id" value="${userId}">
                        <div class="mb-3">
                            <label class="form-label">Username</label>
                            <input type="text" class="form-control" name="username" value="${user.username}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" name="email" value="${user.email}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Role</label>
                            <select class="form-select" name="role" required>
                                <option value="user" ${user.role === 'user' ? 'selected' : ''}>User</option>
                                <option value="sub_admin" ${user.role === 'sub_admin' ? 'selected' : ''}>Sub Admin</option>
                                <option value="super_admin" ${user.role === 'super_admin' ? 'selected' : ''}>Super Admin</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" name="is_active" ${(user.is_active || user.active || user.status === 'active') ? 'checked' : ''}>
                                <label class="form-check-label">Active</label>
                            </div>
                        </div>
                        <div class="mb-3">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="changePasswordCheck" onchange="togglePasswordField()">
                                <label class="form-check-label">Change Password</label>
                            </div>
                        </div>
                        <div class="mb-3" id="passwordField" style="display: none;">
                            <label class="form-label">New Password</label>
                            <input type="password" class="form-control" name="new_password" placeholder="Enter new password">
                            <div class="form-text">Leave empty to keep current password</div>
                        </div>
                    </form>
                `, 'handleEditUser()');
            } else {
                showAlert('Error loading user details: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error fetching user details:', error);
            showAlert('Error loading user details', 'danger');
        });
}

function toggleUserStatus(userId) {
    if (confirm('Are you sure you want to change this user\'s status?')) {
        fetch(`/admin/user/${userId}/toggle-status`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('User status updated successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error toggling user status:', error);
            showAlert('Error updating user status', 'danger');
        });
    }
}

function deleteUser(userId) {
    if (!userId || userId === 'None') {
        showAlert('Invalid user ID provided', 'danger');
        return;
    }
    
    if (confirm('Are you sure you want to delete this user? This action cannot be undone and will permanently remove all user data.')) {
        fetch(`/admin/delete-user/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('User deleted successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Error deleting user: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            showAlert('Error deleting user', 'danger');
        });
    }
}

// Safety Tips Functions
function createTip() {
    showModal('Create Safety Tip', `
        <form id="createTipForm">
            <div class="mb-3">
                <label class="form-label">Title</label>
                <input type="text" class="form-control" name="title" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Content</label>
                <textarea class="form-control" name="content" rows="3" required></textarea>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <label class="form-label">Category</label>
                    <select class="form-select" name="category" required>
                        <option value="email">Email</option>
                        <option value="url">URL</option>
                        <option value="general">General</option>
                    </select>
                </div>
                <div class="col-md-6">
                    <label class="form-label">Priority</label>
                    <select class="form-select" name="priority">
                        <option value="1">High</option>
                        <option value="2">Medium</option>
                        <option value="3">Low</option>
                    </select>
                </div>
            </div>
        </form>
    `, 'handleCreateTip()');
}

function editTip(tipId) {
    fetch(`/admin/tip/${tipId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const tip = data.tip;
                showModal('Edit Safety Tip', `
                    <form id="editTipForm">
                        <input type="hidden" name="tip_id" value="${tipId}">
                        <div class="mb-3">
                            <label class="form-label">Title</label>
                            <input type="text" class="form-control" name="title" value="${tip.title}" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Content</label>
                            <textarea class="form-control" name="content" rows="3" required>${tip.content}</textarea>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <label class="form-label">Category</label>
                                <select class="form-select" name="category" required>
                                    <option value="email" ${tip.category === 'email' ? 'selected' : ''}>Email</option>
                                    <option value="url" ${tip.category === 'url' ? 'selected' : ''}>URL</option>
                                    <option value="general" ${tip.category === 'general' ? 'selected' : ''}>General</option>
                                </select>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label">Priority</label>
                                <select class="form-select" name="priority">
                                    <option value="1" ${tip.priority == 1 ? 'selected' : ''}>High</option>
                                    <option value="2" ${tip.priority == 2 ? 'selected' : ''}>Medium</option>
                                    <option value="3" ${tip.priority == 3 ? 'selected' : ''}>Low</option>
                                </select>
                            </div>
                        </div>
                    </form>
                `, 'handleEditTip()');
            }
        });
}

function deleteTip(tipId) {
    if (confirm('Are you sure you want to delete this tip?')) {
        fetch(`/admin/tip/${tipId}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Tip deleted successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error deleting tip:', error);
            showAlert('Error deleting tip', 'danger');
        });
    }
}

// Scan Logs Functions
function filterScanLogs() {
    const filter = document.getElementById('scanFilter')?.value || 'all';
    const dateFilter = document.getElementById('scanDateFilter')?.value;
    
    const rows = document.querySelectorAll('#scanLogsTableBody tr');
    rows.forEach(row => {
        let showRow = true;
        
        // Filter by result type
        if (filter !== 'all') {
            const resultBadge = row.querySelector('.badge');
            const resultText = resultBadge ? resultBadge.textContent.toLowerCase() : '';
            showRow = showRow && resultText.includes(filter);
        }
        
        // Filter by date
        if (dateFilter && showRow) {
            const dateCell = row.querySelector('td:first-child small');
            const rowDate = dateCell ? dateCell.textContent.trim().split(' ')[0] : '';
            showRow = showRow && rowDate === dateFilter;
        }
        
        row.style.display = showRow ? '' : 'none';
    });
}

function exportScanLogs() {
    window.open('/admin/export/scan-logs', '_blank');
}

function viewScanDetails(scanId) {
    fetch(`/detection-details/${scanId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const scan = data.detection;
                showModal('Scan Details', `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Scan Information</h6>
                            <p><strong>Type:</strong> ${scan.input_type || 'Unknown'}</p>
                            <p><strong>Result:</strong> <span class="badge bg-${scan.result === 'safe' ? 'success' : (scan.result === 'suspicious' ? 'warning' : 'danger')}">${scan.result || 'Unknown'}</span></p>
                            <p><strong>Confidence:</strong> ${((scan.confidence_score || scan.confidence || 0) * 100).toFixed(1)}%</p>
                            <p><strong>Date:</strong> ${scan.created_at || scan.timestamp || 'Unknown'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Content</h6>
                            <div class="bg-light p-3 rounded" style="max-height: 200px; overflow-y: auto;">
                                <code style="font-size: 0.9em;">${scan.input_content || scan.content || 'No content available'}</code>
                            </div>
                        </div>
                    </div>
                    ${scan.threat_indicators && scan.threat_indicators.length > 0 ? `
                        <hr>
                        <h6>Threat Indicators</h6>
                        <ul class="list-unstyled">
                            ${scan.threat_indicators.map(indicator => `<li><i class="fas fa-exclamation-triangle text-warning me-2"></i>${indicator}</li>`).join('')}
                        </ul>
                    ` : ''}
                `);
            }
        });
}

// Reported Content Functions
function approveReport(reportId) {
    if (confirm('Are you sure you want to approve this report?')) {
        fetch(`/admin/report/${reportId}/approve`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Report approved successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
            }
        });
    }
}

function rejectReport(reportId) {
    if (confirm('Are you sure you want to reject this report?')) {
        fetch(`/admin/report/${reportId}/reject`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('Report rejected successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
            }
        });
    }
}

function viewReportDetails(reportId) {
    fetch(`/admin/report/${reportId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const report = data.report;
                showModal('Report Details', `
                    <div class="row">
                        <div class="col-md-6">
                            <h6>Report Information</h6>
                            <p><strong>Type:</strong> ${report.type || 'Unknown'}</p>
                            <p><strong>Status:</strong> <span class="badge bg-${report.status === 'pending' ? 'warning' : 'success'}">${report.status || 'Unknown'}</span></p>
                            <p><strong>Reporter:</strong> ${report.reporter_username || 'Anonymous'}</p>
                            <p><strong>Reason:</strong> ${report.reason || 'Not specified'}</p>
                            <p><strong>Date:</strong> ${report.created_at || 'Unknown'}</p>
                        </div>
                        <div class="col-md-6">
                            <h6>Reported Content</h6>
                            <div class="bg-light p-3 rounded" style="max-height: 200px; overflow-y: auto;">
                                ${report.content || 'No content available'}
                            </div>
                        </div>
                    </div>
                `);
            }
        });
}

function bulkModeration() {
    showAlert('Bulk moderation functionality would be implemented here', 'info');
}

// System Functions
function exportSystemReport() {
    window.open('/admin/export/system-report', '_blank');
}

function clearSystemLogs() {
    if (confirm('Are you sure you want to clear old system logs? This action cannot be undone.')) {
        fetch('/admin/clear-logs', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showAlert('System logs cleared successfully', 'success');
            } else {
                showAlert('Error clearing logs: ' + (data.error || 'Unknown error'), 'danger');
            }
        })
        .catch(error => {
            console.error('Error clearing logs:', error);
            showAlert('Error clearing logs', 'danger');
        });
    }
}

function systemMaintenance() {
    showAlert('System maintenance functionality would be implemented here', 'info');
}

// Form Handlers
function handleCreateUser() {
    const form = document.getElementById('createUserForm');
    const formData = new FormData(form);
    
    fetch('/admin/users', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('User created successfully', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error creating user:', error);
        showAlert('Error creating user', 'danger');
    });
}

function handleEditUser() {
    const form = document.getElementById('editUserForm');
    const formData = new FormData(form);
    const userId = formData.get('user_id');
    
    const userData = {
        username: formData.get('username'),
        email: formData.get('email'),
        role: formData.get('role'),
        is_active: formData.get('is_active') === 'on',
        new_password: formData.get('new_password') || ''
    };
    
    fetch(`/admin/edit-user/${userId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('User updated successfully', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error updating user:', error);
        showAlert('Error updating user', 'danger');
    });
}

function handleCreateTip() {
    const form = document.getElementById('createTipForm');
    const formData = new FormData(form);
    
    fetch('/admin/tips', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Tip created successfully', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
        }
    })
    .catch(error => {
        console.error('Error creating tip:', error);
        showAlert('Error creating tip', 'danger');
    });
}

function handleEditTip() {
    const form = document.getElementById('editTipForm');
    const formData = new FormData(form);
    const tipId = formData.get('tip_id');
    
    fetch(`/admin/tip/${tipId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAlert('Tip updated successfully', 'success');
            setTimeout(() => location.reload(), 1500);
        } else {
            showAlert('Error: ' + (data.error || 'Unknown error'), 'danger');
        }
    });
}

// Utility Functions
function showModal(title, content, submitAction = null) {
    const modalId = 'adminModal' + Date.now();
    const modalHtml = `
        <div class="modal fade" id="${modalId}" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${submitAction ? `
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" onclick="${submitAction}">Save</button>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('adminModals').innerHTML = modalHtml;
    const modal = new bootstrap.Modal(document.getElementById(modalId));
    modal.show();
    
    // Clean up modal after it's hidden
    document.getElementById(modalId).addEventListener('hidden.bs.modal', function() {
        document.getElementById('adminModals').innerHTML = '';
    });
}

function showAlert(message, type = 'info') {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const alertContainer = document.createElement('div');
    alertContainer.innerHTML = alertHtml;
    document.body.appendChild(alertContainer);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
        alertContainer.remove();
    }, 5000);
}