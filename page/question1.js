let cv_tags = [];
let task_id = 0;
exports.Task = extend(TolokaHandlebarsTask, function (options) {
  TolokaHandlebarsTask.call(this, options);
}, {
  onRender: function() {
        var $el = $(this.getDOMElement());

        this._getFile = this.file.getFile;
        this.file.getFile = function() {
        this.focus();
            return this._getFile.apply(this.file, arguments);
        }.bind(this);

        const root = this.getDOMElement();

        const task = this.getTask();

        const solution = this.getSolution();

        console.log(task);
        console.log(solution);

        cv_tags = task.input_values.cv_tags;
        task_id = task.id;
        console.log(cv_tags);
        console.log(task_id);
  },
  onDestroy: function() {
    // Task is completed. Global resources can be released (if used)
  },
  validate: function(solution) {
      console.log("Validating");
      function check_tags(output_values, index) {
          if (output_values[index]) {
              const res = output_values[index].toLowerCase();
              let test = false;
              cv_tags.forEach(cv_tag => {
                  if (res.includes(",")) {
                      test = true;
                  }
                  if (cv_tag.toLowerCase().includes(res)) {
                      console.log("equal?");
                      test = true;
                  }
              });
              return test;
          }
          return false;
      }
      const output_values = solution.output_values;
      if (check_tags(output_values, "result0")) {
          return {"task_id": task_id, "errors": {"result0": {"code:": 1, "message": "The first field contains a disallowed word"}}};
      }
      if (check_tags(output_values, "result1")) {
          return {"task_id": task_id, "errors": {"result1": {"code:": 1, "message": "The second field contains a disallowed word"}}};
      }
      if (check_tags(output_values, "result2")) {
          return {"task_id": task_id, "errors": {"result2": {"code:": 1, "message": "The third field contains a disallowed word"}}};
      }
      if (check_tags(output_values, "result3")) {
          return {"task_id": task_id, "errors": {"result3": {"code:": 1, "message": "The fourth field contains a disallowed word"}}};
      }
      if (check_tags(output_values, "result4")) {
          return {"task_id": task_id, "errors": {"result4": {"code:": 1, "message": "The fifth field contains a disallowed word"}}};
      }
      return null;
  },
  onValidationFail: function(errors) {
      console.log(errors);
  }
});

function extend(ParentClass, constructorFunction, prototypeHash) {
  constructorFunction = constructorFunction || function () {};
  prototypeHash = prototypeHash || {};
  if (ParentClass) {
    constructorFunction.prototype = Object.create(ParentClass.prototype);
  }
  for (var i in prototypeHash) {
    constructorFunction.prototype[i] = prototypeHash[i];
  }
  return constructorFunction;
}
