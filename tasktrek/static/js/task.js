const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

document.querySelectorAll('.edit-btn').forEach(editButton => {
    let task_id = editButton.getAttribute('data-taskid')
    let admin_id = editButton.getAttribute('data-adminid')
    editButton.addEventListener('click', function () {
        const taskItem = editButton.closest('li'); // Target the <li> containing the task
        const taskTitle = taskItem.querySelector('.task-title'); // Get task title
        const taskDescription = taskItem.querySelector('.task-description'); // Get task description
        const actionButtons = taskItem.querySelector('.action-buttons');

        // Check if there are existing input fields
        if (!taskItem.querySelector('input') && !taskItem.querySelector('textarea')) {
            // Create input field for title editing
            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.value = taskTitle.textContent.trim(); // Populate with existing title
            titleInput.className = 'edit-title-input';

            // Create textarea for description editing
            const descriptionTextarea = document.createElement('textarea');
            descriptionTextarea.value = taskDescription.textContent.trim(); // Populate with existing description
            descriptionTextarea.className = 'edit-description-textarea';

            // Create "Save" button
            const saveButton = document.createElement('button');
            saveButton.textContent = 'Save';
            saveButton.className = 'save-btn';

            // Create "Cancel" button
            const cancelButton = document.createElement('button');
            cancelButton.textContent = 'Cancel';
            cancelButton.className = 'cancel-btn';

            // Insert title input above actions
            taskItem.insertBefore(titleInput, actionButtons);
            
            // Insert description textarea right after the title input
            taskItem.insertBefore(descriptionTextarea, actionButtons);

            // Append Save and Cancel buttons
            taskItem.insertBefore(saveButton, actionButtons);
            taskItem.insertBefore(cancelButton, actionButtons);

            // Handle Save Button
            saveButton.addEventListener('click', function () {
                // Update title and description
                taskTitle.textContent = titleInput.value;
                taskDescription.textContent = descriptionTextarea.value;
                let new_title = titleInput.value;
                let new_description = descriptionTextarea.value;
                //Store these values and make a post request...
                console.log(new_title)
                console.log(new_description)
                fetch('/handleedit/', {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify({
                        'data': "hi",
                        'title' : new_title,
                        'desc' : new_description,
                        'admin_id' : admin_id,
                        'task_id': task_id

                    })
                })
                // Remove editing elements
                taskItem.removeChild(titleInput);
                taskItem.removeChild(descriptionTextarea);
                taskItem.removeChild(saveButton);
                taskItem.removeChild(cancelButton);
            });

            // Handle Cancel Button
            cancelButton.addEventListener('click', function () {
                // Remove editing elements without saving
                taskItem.removeChild(titleInput);
                taskItem.removeChild(descriptionTextarea);
                taskItem.removeChild(saveButton);
                taskItem.removeChild(cancelButton);
            });
        }
    });
});
// Add functionality to toggle task completion
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
        const taskCard = checkbox.closest('.task-card'); // Get the parent task card
        const taskTitle = taskCard.querySelector('h3'); // Get the task's title

        if (checkbox.checked) {
            // Mark the task as completed
            taskCard.classList.add('completed');
        } else {
            // Unmark the task as completed
            taskCard.classList.remove('completed');
        }
    });
});

function edithandler(){

}