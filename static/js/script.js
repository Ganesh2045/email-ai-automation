document.addEventListener("DOMContentLoaded", () => {
    // State management
    let tasks = [];
    let activeFilter = "all";
    let searchQuery = "";

    // DOM Elements
    const tasksList = document.getElementById("tasks-list");
    const loadingSpinner = document.getElementById("loading-spinner");
    const emptyState = document.getElementById("empty-state");
    const searchInput = document.getElementById("search-input");
    const filterButtons = document.querySelectorAll(".filter-btn");
    
    // Stats elements
    const statTotalVal = document.querySelector("#stat-total .stat-value");
    const statPendingVal = document.querySelector("#stat-pending .stat-value");
    const statCompletedVal = document.querySelector("#stat-completed .stat-value");
    
    // Modal elements
    const taskModal = document.getElementById("task-modal");
    const openModalBtn = document.getElementById("open-modal-btn");
    const closeModalBtn = document.getElementById("close-modal-btn");
    const cancelModalBtn = document.getElementById("cancel-modal-btn");
    const addTaskForm = document.getElementById("add-task-form");

    // Fetch all tasks
    async function fetchTasks() {
        showLoading(true);
        try {
            const response = await fetch("/api/tasks");
            const data = await response.json();
            if (data.success) {
                tasks = data.tasks;
                updateStats();
                renderTasks();
            } else {
                showToast("Failed to load tasks: " + data.error, "error");
            }
        } catch (error) {
            console.error("Error fetching tasks:", error);
            showToast("Failed to connect to backend", "error");
        } finally {
            showLoading(false);
        }
    }

    // Toggle Task Status (Pending / Completed)
    async function toggleTaskStatus(id, taskRaw, checkboxElement) {
        const originalChecked = checkboxElement.checked;
        try {
            const response = await fetch("/api/tasks/toggle", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, task_raw: taskRaw })
            });
            const data = await response.json();
            if (data.success) {
                // Update local state
                const task = tasks.find(t => t.id === id);
                if (task) {
                    task.status = data.new_status;
                    
                    // Card opacity animation helper
                    const card = document.querySelector(`[data-id="${id}"]`);
                    if (card) {
                        if (task.status === "Completed") {
                            card.classList.add("completed");
                        } else {
                            card.classList.remove("completed");
                        }
                    }
                    
                    updateStats();
                    showToast(`Task marked as ${task.status.toLowerCase()}`, "success");
                    
                    // Re-render after a tiny delay if we are in a status-specific filter
                    if (activeFilter === "completed" || activeFilter === "pending") {
                        setTimeout(renderTasks, 400);
                    }
                }
            } else {
                checkboxElement.checked = !originalChecked;
                showToast("Failed to update task: " + data.error, "error");
            }
        } catch (error) {
            checkboxElement.checked = !originalChecked;
            console.error("Error toggling task status:", error);
            showToast("Connection error occurred", "error");
        }
    }

    // Delete Task
    async function deleteTask(id, taskRaw, cardElement) {
        if (!confirm("Are you sure you want to delete this task?")) return;
        
        try {
            const response = await fetch("/api/tasks/delete", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id, task_raw: taskRaw })
            });
            const data = await response.json();
            if (data.success) {
                // Remove card with scale-down animation
                cardElement.style.animation = "fadeOut 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards";
                
                setTimeout(() => {
                    tasks = tasks.filter(t => t.id !== id);
                    updateStats();
                    renderTasks();
                    showToast("Task deleted successfully", "success");
                }, 300);
            } else {
                showToast("Failed to delete task: " + data.error, "error");
            }
        } catch (error) {
            console.error("Error deleting task:", error);
            showToast("Connection error occurred", "error");
        }
    }

    // Add Task
    addTaskForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const titleInput = document.getElementById("task-title");
        const priorityInput = document.querySelector('input[name="priority"]:checked');
        
        const title = titleInput.value.trim();
        const priority = priorityInput ? priorityInput.value : "MEDIUM";
        
        if (!title) return;
        
        try {
            const response = await fetch("/api/tasks/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, priority })
            });
            const data = await response.json();
            
            if (data.success) {
                showToast("Task added successfully", "success");
                toggleModal(false);
                titleInput.value = "";
                // Refresh list
                await fetchTasks();
            } else {
                showToast(data.error, "error");
            }
        } catch (error) {
            console.error("Error adding task:", error);
            showToast("Connection error occurred", "error");
        }
    });

    // Compute Stats
    function updateStats() {
        const total = tasks.length;
        const pending = tasks.filter(t => t.status !== "Completed").length;
        const completed = total - pending;
        
        statTotalVal.innerText = total;
        statPendingVal.innerText = pending;
        statCompletedVal.innerText = completed;
    }

    // Render task cards in DOM
    function renderTasks() {
        tasksList.innerHTML = "";
        
        // Filter tasks
        const filteredTasks = tasks.filter(task => {
            // Priority/Status Filters
            const matchesFilter = 
                activeFilter === "all" ||
                (activeFilter === "high" && task.priority === "HIGH") ||
                (activeFilter === "medium" && task.priority === "MEDIUM") ||
                (activeFilter === "low" && task.priority === "LOW") ||
                (activeFilter === "completed" && task.status === "Completed") ||
                (activeFilter === "pending" && task.status !== "Completed");
                
            // Search Query Filter
            const matchesSearch = 
                task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                task.task_raw.toLowerCase().includes(searchQuery.toLowerCase());
                
            return matchesFilter && matchesSearch;
        });

        if (filteredTasks.length === 0) {
            emptyState.classList.remove("hidden");
            tasksList.classList.add("hidden");
            return;
        }

        emptyState.classList.add("hidden");
        tasksList.classList.remove("hidden");

        filteredTasks.forEach(task => {
            const isCompleted = task.status === "Completed";
            
            const card = document.createElement("div");
            card.className = `task-card ${isCompleted ? "completed" : ""}`;
            card.setAttribute("data-id", task.id);
            
            // Generate Priority Badge
            let priorityBadgeHtml = "";
            if (task.priority) {
                const priorityClass = task.priority.toLowerCase();
                let emoji = "⚪";
                if (task.priority === "HIGH") emoji = "🔴";
                if (task.priority === "MEDIUM") emoji = "🟡";
                if (task.priority === "LOW") emoji = "🟢";
                
                priorityBadgeHtml = `
                    <span class="priority-badge ${priorityClass}">
                        ${emoji} ${task.priority}
                    </span>
                `;
            }

            card.innerHTML = `
                <div class="task-left">
                    <label class="custom-checkbox">
                        <input type="checkbox" ${isCompleted ? "checked" : ""}>
                        <span class="checkmark"></span>
                    </label>
                    <div class="task-details">
                        <div class="task-title">${escapeHTML(task.title)}</div>
                        <div class="badge-row">
                            ${priorityBadgeHtml}
                            <span class="status-badge">${task.status}</span>
                        </div>
                    </div>
                </div>
                <div class="task-actions">
                    <button class="delete-btn" title="Delete Task">🗑️</button>
                </div>
            `;

            // Bind Checkbox Toggling
            const checkbox = card.querySelector("input[type='checkbox']");
            checkbox.addEventListener("change", () => {
                toggleTaskStatus(task.id, task.task_raw, checkbox);
            });

            // Bind Delete Button
            const deleteBtn = card.querySelector(".delete-btn");
            deleteBtn.addEventListener("click", () => {
                deleteTask(task.id, task.task_raw, card);
            });

            tasksList.appendChild(card);
        });
    }

    // Show/Hide Loading Indicator
    function showLoading(show) {
        if (show) {
            loadingSpinner.classList.remove("hidden");
            tasksList.classList.add("hidden");
            emptyState.classList.add("hidden");
        } else {
            loadingSpinner.classList.add("hidden");
        }
    }

    // Modal Operations
    function toggleModal(open) {
        if (open) {
            taskModal.classList.remove("hidden");
            document.getElementById("task-title").focus();
        } else {
            taskModal.classList.add("hidden");
        }
    }

    openModalBtn.addEventListener("click", () => toggleModal(true));
    closeModalBtn.addEventListener("click", () => toggleModal(false));
    cancelModalBtn.addEventListener("click", () => toggleModal(false));
    
    // Close modal when clicking outside card
    taskModal.addEventListener("click", (e) => {
        if (e.target === taskModal) toggleModal(false);
    });

    // Search input typing handler
    searchInput.addEventListener("input", (e) => {
        searchQuery = e.target.value;
        renderTasks();
    });

    // Filter selector handler
    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            filterButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            activeFilter = btn.getAttribute("data-filter");
            renderTasks();
        });
    });

    // Toast System
    function showToast(message, type = "success") {
        const container = document.getElementById("toast-container");
        const toast = document.createElement("div");
        toast.className = `toast ${type}`;
        
        let emoji = "ℹ️";
        if (type === "success") emoji = "✨";
        if (type === "error") emoji = "⚠️";
        
        toast.innerHTML = `
            <span class="toast-icon">${emoji}</span>
            <span class="toast-text">${escapeHTML(message)}</span>
        `;
        
        container.appendChild(toast);
        
        // Auto remove toast after 3 seconds
        setTimeout(() => {
            toast.style.animation = "fadeOut 0.3s forwards";
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    // Safe HTML Escaping
    function escapeHTML(str) {
        return str
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Initial load
    fetchTasks();
});
