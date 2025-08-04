console.log("To-Do App loaded successfully!");

// Add confirmation for delete actions
document.addEventListener('DOMContentLoaded', function() {
    // Confirm before clearing all tasks
    const clearButton = document.querySelector('.btn-clear');
    if (clearButton) {
        clearButton.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to clear all tasks? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    }

    // Confirm before deleting individual tasks
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
            }
        });
    });

    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });

    // Focus on task input when page loads
    const taskInput = document.querySelector('input[name="title"]');
    if (taskInput) {
        taskInput.focus();
    }
});