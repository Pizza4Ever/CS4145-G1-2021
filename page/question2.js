
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
    let hintShowase = root.querySelector("#hintShowcase");
    console.log(hints);
    console.log(hintShowase);
    console.log(resultField);

    const input = root.querySelectorAll('input');
    const button = root.querySelector('button');

    function updateValue(e) {
        if (this.hasAttribute("highlighted")) {
            this.removeAttribute("highlighted")
        } else {
            this.setAttribute("highlighted", "highlighted")
        }
    }

    input.forEach((inp) => {
        inp.addEventListener('click', updateValue);
    });
    let order = [];



    hintShowase.innerHTML = "<br> <b>Hint: </b>" + hints[0];
    // let order = [];
    let index = 1;
    this.highlight_count = 0;
    this.button_count = 23;
    function buttonEvent(e) {
        var imgs = [];
        input.forEach((item) => {
            if (item.hasAttribute("highlighted")) {
                item.removeAttribute("highlighted");
                item.setAttribute("selected", "selected");
                imgs.push(item.getAttribute("idx"));
                item.disabled = true;
                this.highlight_count += 1;
            }
        });
        order.push(imgs);
        resultField.value = order;
        resultField.innerHTML = order.join();

        console.log(resultField);
        if (index < hints.length) {
            hintShowase.innerHTML = "<br> <b>Hint: </b>" + hints[index];
            index += 1;
        } else {
            this.out_of_hints = true;
            hintShowase.innerHTML = "We are out of hints, please submit the assignment :)"
        }
        const sol = this.getSolution();
        let r = {result: order};
        sol.output_values = r;
        console.log(this.getSolution());
    }

    button.addEventListener('click', buttonEvent.bind(this));

    console.log("test");
  },
  onDestroy: function() {
    // Task is completed. Global resources can be released (if used)
  },
  validate: function() {
        if (this.out_of_hints || this.highlight_count >= this.button_count) {

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
