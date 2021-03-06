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

        const cv_tags = task.input_values.cv_tags;
        const task_id = task.id;
        console.log(cv_tags);
        console.log(task_id);
  },
  onDestroy: function() {
    // Task is completed. Global resources can be released (if used)
  },
  validate: function(solution) {
      const root = this.getDOMElement();
      const task = this.getTask();
      const cv_tags = task.input_values.cv_tags;
      const task_id = task.id;

      console.log(task);
      console.log(cv_tags);
      console.log(task_id);

      root.querySelectorAll(".footer").forEach(value => value.style.background = "#FFFFFF");

      console.log("Validating");
      function check_tags(output_values, index) {
          if (output_values[index]) {
              const res = output_values[index].toLowerCase();
              let test = false; 
              if (res.includes(",")) {
                test = true;
              }
              cv_tags.forEach(cv_tag => {
                  if (res.includes(cv_tag.toLowerCase())) {
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
          root.querySelector("#a").style.background = "#A52A2A";
          return {"task_id": task_id, "errors": {"result0": {"code:": 1, "message": "The first field contains a disallowed word or comma"}}};
      }
      if (check_tags(output_values, "result1")) {
          root.querySelector("#b").style.background = "#A52A2A";
          return {"task_id": task_id, "errors": {"result1": {"code:": 1, "message": "The second field contains a disallowed word or comma"}}};
      }
      if (check_tags(output_values, "result2")) {
          root.querySelector("#c").style.background = "#A52A2A";
          return {"task_id": task_id, "errors": {"result2": {"code:": 1, "message": "The third field contains a disallowed word or comma"}}};
      }
      if (check_tags(output_values, "result3")) {
          root.querySelector("#d").style.background = "#A52A2A";
          return {"task_id": task_id, "errors": {"result3": {"code:": 1, "message": "The fourth field contains a disallowed word or comma"}}};
      }
      if (check_tags(output_values, "result4")) {
          root.querySelector("#e").style.background = "#A52A2A";
          return {"task_id": task_id, "errors": {"result4": {"code:": 1, "message": "The fifth field contains a disallowed word or comma"}}};
      }
      return null;
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
