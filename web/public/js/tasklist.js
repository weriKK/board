function Task(data)
{
    this.isDone = ko.observable(data.isDone);
    this.title  = ko.observable(data.title);
    this.uri    = data.uri;
}

function TaskListViewModel()
{
    // Data
    var self = this;

    self.tasks = ko.observableArray([]);
    self.newTaskTitle = ko.observable();
    self.incompleteTasks = ko.computed(function() {
        return ko.utils.arrayFilter(self.tasks(), function(task) { return !task.isDone() });
    });

    // Operations
    self.addTask = function() {

        $.ajax("http://localhost:5000/api/v1.0/tasks", {
            data: ko.toJSON({ title: this.newTaskTitle() }),
            type: "POST",
            contentType: "application/json",
            success: function(response) {
                self.tasks.push(new Task( response.task));
                self.newTaskTitle("");
            }
        });
    };

    self.getTask = function(task) {
        $.getJSON(task.uri, function(data) {
            var newTask = new Task(data.task);
            self.tasks.replace(task, newTask);
        });
    };

    self.saveTask = function(task) {

        $.ajax(task.uri, {
            data: ko.toJSON(task),
            type: "PUT",
            contentType: "application/json",
            error: function(response) {
                self.getTask(task);
            }
        });
    };

    self.removeTask = function(task) {

        $.ajax(task.uri, {
            type: "DELETE",
            contentType: "application/json",
            success: function(response) {
                self.tasks.remove(task)
            }
        });
    };


    // self.replaceTask = function(taskUri, newTask) {
    //     for (var i = 0; i < self.tasks().length; ++i)
    //     {
    //         if (self.tasks()[i].uri ===  taskUri)
    //         {
    //             // Because the object itself is not observed only some properties of it
    //             // we have to manually tell knockout that a value has changed
    //             self.tasks()[i] = newTask;
    //             self.tasks.valueHasMutated();
    //         }
    //     }
    // };



    // Load initial state from server
    $.getJSON("http://localhost:5000/api/v1.0/tasks", function(allData) {
        var mappedTasks = $.map(allData.tasks, function(item) { return new Task(item) } );
        self.tasks(mappedTasks);
    });
}

ko.applyBindings(new TaskListViewModel());
