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
    const resultField = root.querySelector("#resultField");
    let hints = root.querySelector("#hints").innerHTML.split(',');
    let honeypot_hint = root.querySelector('#honeypot').innerHTML;
    let hintShowase = root.querySelector("#hintShowcase");
    this.messagediv = root.querySelector("#messages");
    this.order = [];
    

    console.log(hints);
    console.log(hintShowase);
    console.log(honeypot_hint)
    console.log(resultField);

    this.input = root.querySelectorAll('input');
    const button = root.querySelector('button');

    function updateValue(e) {
        if (this.hasAttribute("highlighted")) {
            this.removeAttribute("highlighted")
        } else {
            this.setAttribute("highlighted", "highlighted")
        }
    }

    this.input.forEach((inp) => {
        inp.addEventListener('click', updateValue);
    });



    hintShowase.innerHTML = "<br> <b>Hint: </b>" + hints[0];
    // let order = [];
    this.index = 1;
    this.highlight_count = 0;
    this.button_count = 23;
    this.honeypot_index = 3
    this.honeypot_asked = false

    function buttonEvent(e) {
      var imgs = [];
      let highlighted = []

      // Check if the right amount of images have been selected
      this.input.forEach((item) => {
        if (item.hasAttribute("highlighted")) {
          highlighted.push(item);
        }
      });
      
      if (highlighted.length + this.highlight_count > this.button_count) {
        this.messagediv.innerHTML = "You can not select all images, please leave atleast one"
        const task = this.getTask();
        const task_id = task.id;
        return
      } else {
        this.messagediv.innerHTML = ""
      }

      console.log(resultField);
      if (this.index < hints.length) {
        if(this.index == this.honeypot_index && !this.honeypot_asked) {
          hintShowase.innerHTML = "<br> <b>Hint: </b>" + honeypot_hint;
          this.honeypot_asked = true;
        } else {
          hintShowase.innerHTML = "<br> <b>Hint: </b>" + hints[this.index];
          this.index += 1 ;
          console.log(this.index)
        }
        highlighted.forEach((item) => {
          item.removeAttribute("highlighted");
          item.setAttribute("selected", "selected");
          imgs.push(item.getAttribute("idx"));
          item.disabled = true;
          this.highlight_count += 1;
        });
        this.order.push(imgs);
        resultField.value = this.order;
        resultField.innerHTML = this.order.join();
        const sol = this.getSolution();
        let r = {result: this.order};
        sol.output_values = r;
        console.log(this.getSolution());
      } else {
          this.out_of_hints = true;
          hintShowase.innerHTML = "We are out of hints, please submit the assignment :)"
      }

    }

    button.addEventListener('click', buttonEvent.bind(this));

    console.log("test");
  },
  onDestroy: function() {
    // Task is completed. Global resources can be released (if used)
  },
  validate: function() {
    var imgs = [];
    let highlighted = [];

    // Check if at least 3 hints have been seen
    if(this.index < 3){
      this.messagediv.innerHTML = "Please use atleast 4 hints"
      const task = this.getTask();
      const task_id = task.id;
      return {"task_id": task_id, "errors": {"result": {"code:": 1, "message": "Please use atleast 3 hints"}}};
    }
  else {
    this.messagediv.innerHTML = "";
    }


    // Check if the right amount of images have been selected
    this.input.forEach((item) => {
      if (item.hasAttribute("highlighted")) {
        highlighted.push(item);
      }
    });

  if (highlighted.length + this.highlight_count > this.button_count) {
      this.messagediv.innerHTML = "You can not select all images, please leave atleast one"
      const task = this.getTask();
      const task_id = task.id;
      return {"task_id": task_id, "errors": {"result": {"code:": 1, "message": "Please do not select all images"}}};
    }
  else if(this.highlight_count + highlighted.length < this.button_count) {
    this.messagediv.innerHTML = "Only one image should remain, use another hint or guess"
      const task = this.getTask();
      const task_id = task.id;
      return {"task_id": task_id, "errors": {"result": {"code:": 1, "message": "Please select more images"}}};
  }
  else {
    this.messagediv.innerHTML = "";
    }
  
  // If all is well, we can select the remaining highlighted images and submit
  // Remove highlighted items
  highlighted.forEach((item) => {
    item.removeAttribute("highlighted");
    item.setAttribute("selected", "selected");
    imgs.push(item.getAttribute("idx"));
    item.disabled = true;
    this.highlight_count += 1;
    console.log(this.highlight_count)
  });

  this.order.push(imgs);

  const sol = this.getSolution();
  let r = {result: this.order};
  sol.output_values = r;
  console.log(this.getSolution());
    if (this.highlight_count == this.button_count && (this.out_of_hints || this.index > 3)) {
          console.log("Submission is alright")


        } else {
            const task = this.getTask();
            const task_id = task.id;
            return {"task_id": task_id, "errors": {"result": {"code:": 1, "message": "Please finish the game"}}};
        }
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
