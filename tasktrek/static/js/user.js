const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//for all checkboxes
//get their task id attributes
//make a fetch call to the views and update db
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
    console.log("Hello checkbox")
    checkbox.addEventListener('change', function () {
        const taskCard = checkbox.closest('.task-card'); // Get the parent task card
        const taskTitle = taskCard.querySelector('h3'); // Get the task's title
        const task_id = checkbox.getAttribute("data-taskid");
        if (checkbox.checked) {
            // Mark the task as completed
            taskCard.classList.add('completed');
            fetch('/handlecomplete/', {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify({
                        'completion': "True",
                        'task_id': task_id

                    })
            })
        } else {
            // Unmark the task as completed
            taskCard.classList.remove('completed');
            fetch('/handlecomplete/', {
                    method: "POST",
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json' 
                    },
                    body: JSON.stringify({
                        'completion': "False",
                        'task_id': task_id

                    })
            })
        }

        

        
        
    });
});